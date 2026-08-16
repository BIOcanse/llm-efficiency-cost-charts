from __future__ import annotations

import argparse
import csv
import json
import math
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


AA_ROOT = "https://artificialanalysis.ai/models"
MODEL_FILE = "model_efficiency.csv"
ACCESS_FILE = "subscription_first_task_cost.csv"
EVIDENCE_FILE = "access_evidence.csv"
FRONTIER_FILE = "frontier_model_positions.csv"
USER_AGENT = "Mozilla/5.0 (compatible; llm-efficiency-cost-charts snapshotter/1.0)"


@dataclass(frozen=True)
class ObservationSpec:
    model: str
    effort: str
    effort_order: int
    country_code: str
    country_name: str
    developer: str
    is_historical: bool
    source_url: str
    access_template: str | None = None

    @property
    def key(self) -> tuple[str, str]:
        return self.model, self.effort

    @property
    def slug(self) -> str:
        return urlparse(self.source_url).path.rstrip("/").split("/")[-1]


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Create a current AA general-model snapshot from direct model pages."
    )
    parser.add_argument(
        "--selection",
        type=Path,
        default=root / "data" / "general_snapshot_selection_2026-08-15.json",
    )
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fetch(url: str, timeout: float) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8"), response.geturl()
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def decode_escaped_object(source: str, start: int) -> tuple[dict[str, Any], int]:
    depth = 0
    end = -1
    for index in range(start, len(source)):
        char = source[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    if end < 0:
        raise ValueError("Unbalanced escaped JSON object")
    escaped = source[start:end]
    decoded = json.loads(f'"{escaped}"')
    return json.loads(decoded), end


def extract_current_model(html: str) -> dict[str, Any]:
    marker = '\\"currentModel\\":'
    marker_index = html.find(marker)
    if marker_index < 0:
        raise ValueError("currentModel payload not found")
    start = html.find("{", marker_index + len(marker))
    model, _ = decode_escaped_object(html, start)
    required = (
        "slug",
        "releaseDate",
        "intelligenceIndex",
        "canonicalIntelligenceIndexTokenCount",
    )
    missing = [key for key in required if key not in model]
    if missing:
        raise ValueError(f"currentModel is missing {missing}")
    return model


def extract_provider_records(html: str, model_slug: str) -> list[dict[str, Any]]:
    marker = f'\\"model\\":{{\\"slug\\":\\"{model_slug}\\"}}'
    records_by_id: dict[str, dict[str, Any]] = {}
    simplified_by_id: dict[str, dict[str, Any]] = {}
    cursor = 0
    while True:
        marker_index = html.find(marker, cursor)
        if marker_index < 0:
            break
        start = html.rfind('{\\"id\\":', max(0, marker_index - 20_000), marker_index)
        cursor = marker_index + len(marker)
        if start < 0:
            continue
        try:
            record, _ = decode_escaped_object(html, start)
        except (ValueError, json.JSONDecodeError):
            continue
        record_id = str(record.get("id", ""))
        if not record_id or record.get("model", {}).get("slug") != model_slug:
            continue
        if "slug" in record and "host" in record and "pricing" in record:
            records_by_id[record_id] = record
        elif "hostApiId" in record and "pricing" in record:
            simplified_by_id[record_id] = record

    for record_id, record in records_by_id.items():
        simplified = simplified_by_id.get(record_id)
        if simplified:
            record["_hostApiId"] = simplified.get("hostApiId")
            record["_cacheWritePrice"] = simplified.get("pricing", {}).get(
                "cacheWritePrice"
            )
    return list(records_by_id.values())


def load_selection(
    config: dict[str, Any], base_rows: list[dict[str, str]]
) -> list[ObservationSpec]:
    excluded = set(config["exclude_models"])
    renames = config.get("renames", {})
    specs: list[ObservationSpec] = []
    for row in base_rows:
        if row["model"] in excluded:
            continue
        specs.append(
            ObservationSpec(
                model=renames.get(row["model"], row["model"]),
                effort=row["effort"],
                effort_order=int(row["effort_order"]),
                country_code=row["country_code"],
                country_name=row["country_name"],
                developer=row["developer"],
                is_historical=row["is_historical"].lower() == "true",
                source_url=row["source_url"],
            )
        )
    for item in config["additions"]:
        specs.append(
            ObservationSpec(
                model=item["model"],
                effort=item["effort"],
                effort_order=int(item["effort_order"]),
                country_code=item["country_code"],
                country_name=item["country_name"],
                developer=item["developer"],
                is_historical=bool(item.get("is_historical", False)),
                source_url=f"{AA_ROOT}/{item['source_slug']}",
                access_template=item.get("access_template"),
            )
        )
    seen: set[tuple[str, str]] = set()
    for spec in specs:
        if spec.key in seen:
            raise ValueError(f"Duplicate selected configuration: {spec.key}")
        seen.add(spec.key)
    return specs


def fetch_observation(spec: ObservationSpec, timeout: float) -> dict[str, Any]:
    html, final_url = fetch(spec.source_url, timeout)
    model = extract_current_model(html)
    provider_html, provider_url = fetch(f"{spec.source_url}/providers", timeout)
    providers = extract_provider_records(provider_html, model["slug"])
    return {
        "spec": spec,
        "final_url": final_url,
        "provider_url": provider_url,
        "model": model,
        "providers": providers,
    }


def positive_provider_cost(record: dict[str, Any]) -> float | None:
    total = record.get("performance", {}).get("intelligenceIndexCostPerTask", {}).get(
        "total"
    )
    if total is None:
        return None
    value = float(total)
    return value if math.isfinite(value) and value > 0 else None


def is_explicitly_quantized_provider(record: dict[str, Any]) -> bool:
    label = str(record.get("host", {}).get("label") or "").upper()
    markers = ("BF16", "FP8", "FP4", "NVFP", "MXFP", "INT8", "INT4", "AWQ", "GPTQ")
    return any(marker in label for marker in markers)


def synthetic_default_provider(
    current_model: dict[str, Any], provider_name: str
) -> dict[str, Any] | None:
    cost = current_model.get("intelligenceIndexCostPerTask", {}).get("cost")
    input_price = current_model.get("price1mInputTokens")
    output_price = current_model.get("price1mOutputTokens")
    if (
        not cost
        or cost.get("total") is None
        or float(cost["total"]) <= 0
        or input_price is None
        or output_price is None
        or float(output_price) <= 0
    ):
        return None
    return {
        "id": f"aa-default-{current_model['slug']}",
        "slug": f"aa_default_{current_model['slug']}",
        "host": {
            "name": provider_name,
            "label": provider_name,
            "slug": "__aa_default__",
        },
        "model": {"slug": current_model["slug"]},
        "pricing": {
            "price1mInputTokens": input_price,
            "price1mOutputTokens": output_price,
            "cacheHitPrice": current_model.get("cacheHitPrice"),
        },
        "performance": {"intelligenceIndexCostPerTask": cost},
        "_cacheWritePrice": current_model.get("cacheWritePrice"),
        "_hostApiId": current_model["slug"],
        "_isAaDefault": True,
    }


def select_common_providers(
    observations: list[dict[str, Any]],
) -> dict[str, str | None]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for observation in observations:
        grouped[observation["spec"].model].append(observation)
    selected: dict[str, str | None] = {}
    for model_name, group in grouped.items():
        host_sets = []
        has_positive_provider_records = False
        for observation in group:
            has_positive_provider_records = has_positive_provider_records or any(
                positive_provider_cost(record) is not None
                for record in observation["providers"]
            )
            hosts = {
                record["host"]["slug"]
                for record in observation["providers"]
                if positive_provider_cost(record) is not None
                and not is_explicitly_quantized_provider(record)
            }
            host_sets.append(hosts)
        common = set.intersection(*host_sets) if host_sets else set()
        if not common:
            default_is_complete = not has_positive_provider_records and all(
                synthetic_default_provider(
                    observation["model"], observation["spec"].developer
                )
                is not None
                for observation in group
            )
            selected[model_name] = "__aa_default__" if default_is_complete else None
            continue
        totals: dict[str, float] = defaultdict(float)
        for host in common:
            for observation in group:
                record = next(
                    record
                    for record in observation["providers"]
                    if record["host"]["slug"] == host
                )
                totals[host] += float(positive_provider_cost(record))
        selected[model_name] = min(common, key=lambda host: (totals[host], host))
    return selected


def fmt(value: float | int | None, places: int = 12) -> str:
    if value is None:
        return ""
    return f"{float(value):.{places}f}"


def derive_task_tokens(
    record: dict[str, Any], current_model: dict[str, Any]
) -> dict[str, float]:
    pricing = record["pricing"]
    cost = record["performance"]["intelligenceIndexCostPerTask"]
    input_price = float(pricing["price1mInputTokens"])
    output_price = float(pricing["price1mOutputTokens"])
    cache_price_raw = pricing.get("cacheHitPrice")
    cache_price = float(cache_price_raw) if cache_price_raw is not None else input_price
    cache_write_raw = record.get("_cacheWritePrice")
    if cache_write_raw is None:
        same_default_prices = (
            current_model.get("price1mInputTokens") == pricing.get("price1mInputTokens")
            and current_model.get("price1mOutputTokens")
            == pricing.get("price1mOutputTokens")
            and current_model.get("cacheHitPrice") == pricing.get("cacheHitPrice")
        )
        cache_write_raw = (
            current_model.get("cacheWritePrice") if same_default_prices else input_price
        )
    cache_write_price = float(
        input_price if cache_write_raw is None else cache_write_raw
    )

    def tokens(component: str, price: float) -> float:
        amount = float(cost.get(component) or 0.0)
        if amount == 0:
            return 0.0
        if price <= 0:
            raise ValueError(f"Positive {component} cost has non-positive price")
        return amount / price * 1_000_000

    reasoning = tokens("reasoning", output_price)
    answer = tokens("answer", output_price)
    result = {
        "noncache": tokens("nonCacheInput", input_price),
        "cache_read": tokens("cacheRead", cache_price),
        "cache_write": tokens("cacheWrite", cache_write_price),
        "reasoning": reasoning,
        "answer": answer,
        "output": reasoning + answer,
        "cache_write_price": cache_write_price,
    }
    result["total"] = (
        result["noncache"]
        + result["cache_read"]
        + result["cache_write"]
        + result["output"]
    )
    return result


def build_model_rows(
    observations: list[dict[str, Any]], selected_hosts: dict[str, str | None]
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    rows: list[dict[str, str]] = []
    evidence: list[dict[str, Any]] = []
    for observation in observations:
        spec: ObservationSpec = observation["spec"]
        model = observation["model"]
        tokens = model["canonicalIntelligenceIndexTokenCount"]
        raw_cost = model.get("intelligenceIndexCostPerTask", {}).get("cost", {})
        host_slug = selected_hosts[spec.model]
        provider = None
        if host_slug == "__aa_default__":
            provider = synthetic_default_provider(model, spec.developer)
        elif host_slug is not None:
            provider = next(
                record
                for record in observation["providers"]
                if record["host"]["slug"] == host_slug
            )

        row = {
            "model": spec.model,
            "effort": spec.effort,
            "effort_order": str(spec.effort_order),
            "country_code": spec.country_code,
            "country_name": spec.country_name,
            "developer": spec.developer,
            "release_date": str(model["releaseDate"] or ""),
            "is_historical": str(spec.is_historical).lower(),
            "data_scope": "token_and_cost" if provider else "token_only",
            "intelligence_score": str(round(float(model["intelligenceIndex"]))),
            "intelligence_score_raw": fmt(model["intelligenceIndex"]),
            "output_tokens_million": fmt(float(tokens["output"]) / 1_000_000, 6),
            "canonical_input_tokens": str(int(tokens["input"])),
            "canonical_answer_tokens": str(int(tokens["answer"])),
            "canonical_reasoning_tokens": str(int(tokens["reasoning"])),
            "canonical_output_tokens": str(int(tokens["output"])),
            "total_tokens_million": fmt(
                (float(tokens["input"]) + float(tokens["output"])) / 1_000_000,
                6,
            ),
            "aa_raw_blended_usd_per_million_tokens": fmt(
                model.get("price1mBlended7To2To1")
            ),
            "aa_raw_cost_per_index_task_usd": fmt(raw_cost.get("total")),
            "blended_usd_per_million_tokens": "",
            "cost_per_index_task_usd": "",
            "task_noncache_input_tokens": "",
            "task_cache_read_tokens": "",
            "task_cache_write_tokens": "",
            "task_answer_tokens": "",
            "task_reasoning_tokens": "",
            "task_output_tokens": "",
            "total_tokens_per_index_task": "",
            "api_provider": "",
            "api_provider_model_id": "",
            "api_precision": "",
            "api_original_match": "",
            "api_input_usd_per_million": "",
            "api_cache_read_usd_per_million": "",
            "api_cache_write_usd_per_million": "",
            "api_output_usd_per_million": "",
            "api_price_scenario": "current",
            "api_price_valid_until": "",
            "api_price_source_url": "",
            "api_precision_source_url": "",
            "api_price_confidence": "",
            "api_selection_basis": "",
            "api_price_note": "",
            "source_url": spec.source_url,
        }
        if provider:
            pricing = provider["pricing"]
            task_tokens = derive_task_tokens(provider, model)
            input_price = float(pricing["price1mInputTokens"])
            output_price = float(pricing["price1mOutputTokens"])
            cache_price = float(
                pricing["cacheHitPrice"]
                if pricing.get("cacheHitPrice") is not None
                else input_price
            )
            selected_cost = float(
                provider["performance"]["intelligenceIndexCostPerTask"]["total"]
            )
            row.update(
                {
                    "blended_usd_per_million_tokens": fmt(
                        0.2 * input_price + 0.7 * cache_price + 0.1 * output_price
                    ),
                    "cost_per_index_task_usd": fmt(selected_cost),
                    "task_noncache_input_tokens": fmt(task_tokens["noncache"], 6),
                    "task_cache_read_tokens": fmt(task_tokens["cache_read"], 6),
                    "task_cache_write_tokens": fmt(task_tokens["cache_write"], 6),
                    "task_answer_tokens": fmt(task_tokens["answer"], 6),
                    "task_reasoning_tokens": fmt(task_tokens["reasoning"], 6),
                    "task_output_tokens": fmt(task_tokens["output"], 6),
                    "total_tokens_per_index_task": fmt(task_tokens["total"], 6),
                    "api_provider": provider["host"].get("label")
                    or provider["host"]["name"],
                    "api_provider_model_id": str(
                        provider.get("_hostApiId") or provider["slug"]
                    ),
                    "api_precision": "AA provider benchmark endpoint",
                    "api_original_match": "aa_provider_endpoint_exact_model",
                    "api_input_usd_per_million": fmt(input_price),
                    "api_cache_read_usd_per_million": fmt(cache_price),
                    "api_cache_write_usd_per_million": fmt(
                        task_tokens["cache_write_price"]
                    ),
                    "api_output_usd_per_million": fmt(output_price),
                    "api_price_source_url": (
                        spec.source_url
                        if provider.get("_isAaDefault")
                        else observation["provider_url"]
                    ),
                    "api_precision_source_url": (
                        spec.source_url
                        if provider.get("_isAaDefault")
                        else observation["provider_url"]
                    ),
                    "api_price_confidence": "high",
                    "api_selection_basis": (
                        "AA model-page default; no comparable provider table"
                        if provider.get("_isAaDefault")
                        else "lowest positive AA weighted task cost among providers "
                        "common to all reasoning levels of this model"
                    ),
                    "api_price_note": (
                        "AA provider-specific cost; zero-price routes excluded"
                    ),
                }
            )
        rows.append(row)
        evidence.append(
            {
                "model": spec.model,
                "effort": spec.effort,
                "source_url": spec.source_url,
                "resolved_url": observation["final_url"],
                "aa_slug": model["slug"],
                "aa_name": model["name"],
                "benchmark": "Artificial Analysis Intelligence Index v4.1.1",
                "selected_provider_slug": host_slug,
                "selected_provider": row["api_provider"] or None,
                "provider_source_url": observation["provider_url"],
            }
        )
    rows.sort(key=lambda row: (row["model"], int(row["effort_order"])))
    return rows, evidence


def build_access_rows(
    specs: list[ObservationSpec],
    model_rows: list[dict[str, str]],
    base_access: list[dict[str, str]],
    renames: dict[str, str],
    observations: list[dict[str, Any]],
) -> list[dict[str, str]]:
    model_index = {(row["model"], row["effort"]): row for row in model_rows}
    base_index = {(row["model"], row["effort"]): row for row in base_access}
    observation_index = {
        observation["spec"].key: observation for observation in observations
    }
    reverse_renames = {new: old for old, new in renames.items()}
    rows: list[dict[str, str]] = []
    for spec in specs:
        model_row = model_index[spec.key]
        if not model_row["cost_per_index_task_usd"]:
            continue
        template_key: tuple[str, str] | None = None
        if spec.access_template:
            template_key = tuple(spec.access_template.split("|", maxsplit=1))  # type: ignore[assignment]
        else:
            base_model = reverse_renames.get(spec.model, spec.model)
            if (base_model, spec.effort) in base_index:
                template_key = (base_model, spec.effort)
        if template_key is None or template_key not in base_index:
            continue
        template = base_index[template_key]
        row = dict(template)
        access_mode = row["access_mode"]
        observation = observation_index[spec.key]
        default_provider = synthetic_default_provider(
            observation["model"], spec.developer
        )
        default_tokens = (
            derive_task_tokens(default_provider, observation["model"])
            if default_provider
            else None
        )
        is_subscription = access_mode.startswith("subscription_")
        row.update(
            {
                "provider": (
                    template["provider"] if is_subscription else model_row["api_provider"]
                ),
                "model": spec.model,
                "effort": spec.effort,
                "effort_order": str(spec.effort_order),
                "country_code": spec.country_code,
                "country_name": spec.country_name,
                "developer": spec.developer,
                "is_historical": str(spec.is_historical).lower(),
                "intelligence_score": model_row["intelligence_score"],
                "intelligence_score_raw": model_row["intelligence_score_raw"],
                "api_cost_per_task_usd": (
                    fmt(
                        default_provider["performance"][
                            "intelligenceIndexCostPerTask"
                        ]["total"]
                    )
                    if is_subscription and default_provider
                    else model_row["cost_per_index_task_usd"]
                ),
                "total_tokens_per_index_task": (
                    fmt(default_tokens["total"], 6)
                    if is_subscription and default_tokens
                    else model_row["total_tokens_per_index_task"]
                ),
                "api_price_provider": (
                    template["api_price_provider"]
                    if is_subscription
                    else model_row["api_provider"]
                ),
                "api_provider_model_id": (
                    template["api_provider_model_id"]
                    if is_subscription
                    else model_row["api_provider_model_id"]
                ),
                "api_precision": (
                    template["api_precision"]
                    if is_subscription
                    else model_row["api_precision"]
                ),
                "api_price_source_url": (
                    template["api_price_source_url"]
                    if is_subscription
                    else model_row["api_price_source_url"]
                ),
                "benchmark_source_url": model_row["source_url"],
            }
        )
        api_cost = float(row["api_cost_per_task_usd"])
        task_tokens = float(row["total_tokens_per_index_task"])
        ratio_text = row["api_value_ratio"]
        if access_mode == "subscription_api_equivalent_estimate":
            if not default_provider or not default_tokens:
                raise ValueError(f"Missing first-party task composition for {spec.key}")
            ratio = float(ratio_text)
            weekly_api_equivalent = float(row["weekly_api_equivalent_usd"])
            tasks_per_week = weekly_api_equivalent / api_cost
            effective_cost = float(row["weekly_cost_usd"]) / tasks_per_week
            row["tasks_per_week"] = fmt(tasks_per_week)
            row["normalized_weekly_quota"] = fmt(
                tasks_per_week * task_tokens, 6
            )
        elif access_mode == "subscription_reconstructed":
            weekly_quota = float(template["normalized_weekly_quota"])
            tasks_per_week = weekly_quota / task_tokens
            effective_cost = float(template["weekly_cost_usd"]) / tasks_per_week
            row["normalized_weekly_quota"] = fmt(weekly_quota, 6)
            row["tasks_per_week"] = fmt(tasks_per_week)
        elif access_mode == "subscription_official":
            if not default_tokens:
                raise ValueError(f"Missing official task composition for {spec.key}")
            weekly_credits = float(template["normalized_weekly_quota"])
            credits_per_task = (
                default_tokens["cache_read"] * 2.5
                + (default_tokens["noncache"] + default_tokens["cache_write"])
                * 300
                + default_tokens["output"] * 600
            )
            tasks_per_week = weekly_credits / credits_per_task
            effective_cost = float(template["weekly_cost_usd"]) / tasks_per_week
            row["normalized_weekly_quota"] = fmt(weekly_credits, 6)
            row["tasks_per_week"] = fmt(tasks_per_week)
        else:
            effective_cost = api_cost
            row["tasks_per_week"] = ""
            row["normalized_weekly_quota"] = ""
        row["effective_cost_per_task_usd"] = fmt(effective_cost)
        row["effective_usd_per_million_task_tokens"] = fmt(
            effective_cost / task_tokens * 1_000_000
        )
        rows.append(row)
    rows.sort(key=lambda row: (row["model"], int(row["effort_order"])))
    return rows


def apply_api_price_candidates(
    model_rows: list[dict[str, str]], candidates: list[dict[str, Any]]
) -> None:
    """Apply a current original-model price only when it beats the AA route.

    AA provider benchmark pages are the default source. A dated snapshot may
    add a newer official candidate when the provider changed price before AA's
    provider table caught up. Selection remains fixed for every level of the
    model and never substitutes a quantized endpoint.
    """

    rows_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in model_rows:
        rows_by_model[row["model"]].append(row)
    candidates_by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for candidate in candidates:
        candidates_by_model[str(candidate["model"])].append(candidate)

    for model, rows in rows_by_model.items():
        model_candidates = candidates_by_model.get(model, [])
        if not model_candidates:
            continue

        current_costs = [
            float(row["cost_per_index_task_usd"])
            for row in rows
            if row["cost_per_index_task_usd"]
        ]
        current_mean = (
            sum(current_costs) / len(current_costs) if len(current_costs) == len(rows) else math.inf
        )
        scored: list[tuple[float, dict[str, Any], list[float]]] = []
        for candidate in model_candidates:
            costs: list[float] = []
            for row in rows:
                cost = (
                    float(row["task_noncache_input_tokens"])
                    * float(candidate["input_usd_per_million"])
                    + float(row["task_cache_read_tokens"])
                    * float(candidate["cache_read_usd_per_million"])
                    + float(row["task_cache_write_tokens"])
                    * float(candidate["cache_write_usd_per_million"])
                    + float(row["task_output_tokens"])
                    * float(candidate["output_usd_per_million"])
                ) / 1_000_000
                costs.append(cost)
            scored.append((sum(costs) / len(costs), candidate, costs))
        candidate_mean, candidate, candidate_costs = min(scored, key=lambda item: item[0])
        if candidate_mean >= current_mean - 1e-15:
            continue

        for row, cost in zip(rows, candidate_costs, strict=True):
            task_tokens = float(row["total_tokens_per_index_task"])
            row.update(
                {
                    "blended_usd_per_million_tokens": fmt(
                        cost / task_tokens * 1_000_000
                    ),
                    "cost_per_index_task_usd": fmt(cost),
                    "api_provider": str(candidate["provider"]),
                    "api_provider_model_id": str(candidate["provider_model_id"]),
                    "api_precision": str(candidate["precision"]),
                    "api_original_match": "official_original_endpoint_exact_model",
                    "api_input_usd_per_million": fmt(
                        float(candidate["input_usd_per_million"])
                    ),
                    "api_cache_read_usd_per_million": fmt(
                        float(candidate["cache_read_usd_per_million"])
                    ),
                    "api_cache_write_usd_per_million": fmt(
                        float(candidate["cache_write_usd_per_million"])
                    ),
                    "api_output_usd_per_million": fmt(
                        float(candidate["output_usd_per_million"])
                    ),
                    "api_price_scenario": "current",
                    "api_price_valid_until": "",
                    "api_price_source_url": str(candidate["source_url"]),
                    "api_precision_source_url": str(candidate["source_url"]),
                    "api_price_confidence": "high",
                    "api_selection_basis": (
                        "lowest current positive unquantized route fixed across "
                        "all reasoning levels of this model"
                    ),
                    "api_price_note": str(candidate["note"]),
                }
            )


def build_access_evidence(
    model_rows: list[dict[str, str]],
    base_evidence: list[dict[str, str]],
    snapshot: str,
) -> list[dict[str, str]]:
    base = {row["provider"]: row for row in base_evidence}
    by_developer: dict[str, set[str]] = defaultdict(set)
    for row in model_rows:
        by_developer[row["developer"]].add(row["model"])

    policies: dict[str, tuple[str, str, dict[str, str]]] = {
        "OpenAI": ("OpenAI", "OpenAI", {}),
        "Anthropic": ("Anthropic", "Anthropic", {}),
        "Xiaomi": ("Xiaomi MiMo", "Xiaomi MiMo", {}),
        "Z AI": ("Zhipu AI", "Zhipu AI", {}),
        "DeepSeek": (
            "DeepSeek",
            "DeepSeek",
            {
                "reason": "No first-party capped model subscription is published; use the lowest current original-model API route, including current official pricing when it is cheaper than AA's provider table",
                "quota_source_url": "https://artificialanalysis.ai/models",
            },
        ),
        "Meta": (
            "Meta",
            "Meta",
            {
                "reason": "No quantifiable paid model subscription is published; use the current AA original-model API task cost",
                "quota_source_url": "https://artificialanalysis.ai/models/muse-spark-1-2/providers",
            },
        ),
        "NVIDIA": (
            "NVIDIA",
            "NVIDIA",
            {
                "decision": "include_api_partial",
                "reason": "Nemotron Ultra has a comparable original-model API route; Lightning remains Token-only because no positive comparable task price is published",
                "quota_source_url": "https://artificialanalysis.ai/models/nvidia-nemotron-3-ultra-550b-a55b/providers",
            },
        ),
        "Multiverse Computing": (
            "Multiverse Computing",
            "Multiverse Computing",
            {
                "decision": "exclude_api_cost_unavailable",
                "access_basis": "",
                "reason": "Open weights are available, but the current AA observation has no positive comparable hosted task price",
                "quota_source_url": "https://artificialanalysis.ai/models/hypernova-60b/providers",
            },
        ),
        "SpaceXAI": ("xAI", "xAI", {}),
        "Google": ("Google", "Google", {}),
        "Kimi": ("Kimi", "Kimi", {}),
        "Alibaba": ("Alibaba", "Alibaba", {}),
        "MiniMax": ("MiniMax", "MiniMax", {}),
        "Mistral": ("Mistral", "Mistral", {}),
        "InclusionAI": ("InclusionAI", "InclusionAI", {}),
        "Cohere": (
            "Cohere",
            "",
            {
                "candidate_best_value_plan": "Free rate-limited API / Model Vault",
                "quota_period": "monthly",
                "published_quota": "Rate-limited free access; production deployment by agreement",
                "decision": "exclude_api_cost_unavailable",
                "access_basis": "",
                "confidence": "high",
                "reason": "No stable positive public per-Token task price is available for a comparable cost calculation",
                "plan_source_url": "https://docs.cohere.com/docs/command-a-plus",
                "quota_source_url": "https://docs.cohere.com/v2/docs/rate-limits",
            },
        ),
        "LG AI Research": (
            "LG AI Research",
            "",
            {
                "candidate_best_value_plan": "None",
                "quota_period": "none",
                "published_quota": "None",
                "token_conversion": "None",
                "decision": "exclude_api_cost_unavailable",
                "access_basis": "",
                "confidence": "high",
                "reason": "Current benchmark Token data exists, but no positive comparable hosted task price is published",
                "plan_source_url": "https://www.lgresearch.ai/data/cdn/upload/K-EXAONE_Technical_Report.pdf",
                "quota_source_url": "https://artificialanalysis.ai/models/k-exaone-2-0-0803/providers",
            },
        ),
        "Upstage": (
            "Upstage",
            "",
            {
                "candidate_best_value_plan": "Optional API commitment tiers",
                "quota_period": "monthly_or_yearly_prepaid",
                "published_quota": "Metered prepaid credits with 10%-40% bonus",
                "token_conversion": "Credits retain metered API billing; no capped model quota",
                "decision": "include_api",
                "access_basis": "api_metered_no_model_subscription",
                "confidence": "high",
                "reason": "Commitment tiers are prepaid metered API credits, not a capped model subscription; use the fixed current AA original-model route",
                "plan_source_url": "https://www.upstage.ai/pricing/api",
                "quota_source_url": "https://artificialanalysis.ai/models/solar-pro4/providers",
            },
        ),
    }

    rows: list[dict[str, str]] = []
    fieldnames = list(base_evidence[0])
    for developer, models in sorted(by_developer.items()):
        if developer not in policies:
            raise ValueError(f"Missing access-evidence policy for {developer}")
        display, template_name, overrides = policies[developer]
        template = dict(base.get(template_name, {field: "" for field in fieldnames}))
        template.update(overrides)
        template.update(
            {
                "provider": display,
                "models_in_chart": "; ".join(sorted(models)),
                "as_of_date": snapshot,
            }
        )
        rows.append({field: template.get(field, "") for field in fieldnames})
    return rows


def build_frontier_rows(model_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    positions: dict[str, dict[str, str]] = {
        "GPT-5.6 Sol": {"developer": "OpenAI", "position": "sol"},
        "GPT-5.6 Terra": {"developer": "OpenAI", "position": "terra"},
        "GPT-5.6 Luna": {"developer": "OpenAI", "position": "luna"},
        "GPT-5.5 Pro": {"developer": "OpenAI", "position": "pro"},
        "Claude Opus 5": {"developer": "Anthropic", "position": "opus"},
        "Claude Sonnet 5": {"developer": "Anthropic", "position": "sonnet"},
        "Claude Fable 5 (with fallback)": {
            "developer": "Anthropic",
            "position": "fable",
        },
        "Grok 4.6": {"developer": "SpaceXAI", "position": "flagship"},
        "Gemini 3.7 Flash": {"developer": "Google", "position": "flash"},
        "Gemini 3.5 Flash-Lite": {
            "developer": "Google",
            "position": "flash-lite",
        },
        "Gemini 3.1 Pro Preview": {"developer": "Google", "position": "pro"},
        "Muse Spark 1.2": {"developer": "Meta", "position": "spark"},
        "Kimi K3": {"developer": "Kimi", "position": "flagship"},
        "DeepSeek V4 Pro 0813": {"developer": "DeepSeek", "position": "pro"},
        "DeepSeek V4 Flash 0731": {
            "developer": "DeepSeek",
            "position": "flash",
        },
        "Qwen3.8 Max": {"developer": "Alibaba", "position": "max"},
        "Qwen3.8 2.4T A95B": {
            "developer": "Alibaba",
            "position": "open-weights-flagship",
        },
        "K2-V2": {
            "developer": "MBZUAI Institute of Foundation Models",
            "position": "reasoning",
        },
        "Solar Pro 4": {"developer": "Upstage", "position": "pro"},
        "K-EXAONE 2.0 0803": {
            "developer": "LG AI Research",
            "position": "flagship",
        },
        "Nemotron 3.5 Lightning": {
            "developer": "NVIDIA",
            "position": "lightning",
        },
        "Nemotron 3 Ultra 550B A55B": {
            "developer": "NVIDIA",
            "position": "ultra",
        },
        "GLM-5.2": {"developer": "Z AI", "position": "flagship"},
        "MiniMax-M3": {"developer": "MiniMax", "position": "flagship"},
    }
    models = {row["model"] for row in model_rows}
    rows = [
        {"developer": value["developer"], "position": value["position"], "model": model}
        for model, value in sorted(positions.items(), key=lambda item: (item[1]["developer"], item[1]["position"]))
        if model in models
    ]
    covered_developers = {row["developer"] for row in rows}
    by_developer: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in model_rows:
        by_developer[row["developer"]].append(row)
    for developer, candidates in sorted(by_developer.items()):
        if developer in covered_developers:
            continue
        best = max(candidates, key=lambda row: float(row["intelligence_score_raw"]))
        rows.append(
            {"developer": developer, "position": "frontier", "model": best["model"]}
        )
    return sorted(rows, key=lambda row: (row["developer"], row["position"]))


def validate(
    specs: list[ObservationSpec],
    model_rows: list[dict[str, str]],
    access_rows: list[dict[str, str]],
    observations: list[dict[str, Any]],
) -> None:
    if len(model_rows) != len(specs):
        raise ValueError("Selection and model-row counts differ")
    match_ratio = len(observations) / len(specs)
    if match_ratio < 0.95:
        raise ValueError(f"AA observation match ratio below 95%: {match_ratio:.1%}")
    if any("Preview" in row["model"] and "DeepSeek" in row["model"] for row in model_rows):
        raise ValueError("Preview DeepSeek row leaked into current snapshot")
    for row in model_rows:
        total = (
            int(row["canonical_input_tokens"]) + int(row["canonical_output_tokens"])
        ) / 1_000_000
        if abs(total - float(row["total_tokens_million"])) > 1e-6:
            raise ValueError(f"Canonical Token total mismatch: {row['model']} {row['effort']}")
        if row["cost_per_index_task_usd"] and float(row["cost_per_index_task_usd"]) <= 0:
            raise ValueError(f"Non-positive selected task cost: {row['model']}")
    access_keys = {(row["model"], row["effort"]) for row in access_rows}
    if len(access_keys) != len(access_rows):
        raise ValueError("Duplicate subscription-first configuration")


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    config = json.loads(args.selection.read_text(encoding="utf-8"))
    base_dir = root / "data" / config["base_snapshot"]
    output_dir = root / "data" / config["snapshot"]
    if output_dir.exists() and not args.dry_run and not args.overwrite:
        raise FileExistsError(f"Snapshot already exists: {output_dir}")
    base_models = read_csv(base_dir / MODEL_FILE)
    specs = load_selection(config, base_models)

    observations: list[dict[str, Any]] = []
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(fetch_observation, spec, args.timeout): spec for spec in specs
        }
        for future in as_completed(futures):
            spec = futures[future]
            try:
                observations.append(future.result())
            except Exception as exc:  # noqa: BLE001 - aggregate the full audit
                errors.append(f"{spec.model}|{spec.effort}|{spec.source_url}|{exc}")
    observations.sort(
        key=lambda item: (item["spec"].model, item["spec"].effort_order)
    )
    if errors:
        print("fetch errors:")
        for error in errors:
            print(f"  {error}")
    if len(observations) / len(specs) < 0.95:
        raise RuntimeError(
            f"Fetched {len(observations)}/{len(specs)} observations; below 95% gate"
        )
    failed_keys = {
        tuple(error.split("|", maxsplit=2)[:2]) for error in errors
    }
    specs = [spec for spec in specs if spec.key not in failed_keys]
    selected_hosts = select_common_providers(observations)
    model_rows, aa_evidence = build_model_rows(observations, selected_hosts)
    apply_api_price_candidates(model_rows, config.get("api_price_candidates", []))
    base_evidence = read_csv(base_dir / EVIDENCE_FILE)
    access_rows = build_access_rows(
        specs,
        model_rows,
        read_csv(base_dir / ACCESS_FILE),
        config.get("renames", {}),
        observations,
    )
    validate(specs, model_rows, access_rows, observations)

    api_count = sum(bool(row["cost_per_index_task_usd"]) for row in model_rows)
    print(
        f"snapshot={config['snapshot']} benchmark={config['benchmark']} "
        f"token={len(model_rows)} api={api_count} subscription={len(access_rows)} "
        f"fetch_errors={len(errors)}"
    )
    for model_name, host in sorted(selected_hosts.items()):
        print(f"provider\t{model_name}\t{host or 'none'}")
    if args.dry_run:
        return

    write_csv(output_dir / MODEL_FILE, model_rows, list(base_models[0]))
    base_access = read_csv(base_dir / ACCESS_FILE)
    write_csv(output_dir / ACCESS_FILE, access_rows, list(base_access[0]))
    write_csv(
        output_dir / EVIDENCE_FILE,
        build_access_evidence(model_rows, base_evidence, config["snapshot"]),
        list(base_evidence[0]),
    )
    frontier_rows = build_frontier_rows(model_rows)
    write_csv(
        output_dir / FRONTIER_FILE,
        frontier_rows,
        ["developer", "position", "model"],
    )
    (output_dir / "aa_observations.json").write_text(
        json.dumps(
            {
                "snapshot": config["snapshot"],
                "benchmark": config["benchmark"],
                "selection_source": args.selection.name,
                "observations": aa_evidence,
                "fetch_errors": errors,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
