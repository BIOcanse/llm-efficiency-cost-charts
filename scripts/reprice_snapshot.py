from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


WEEKS_PER_MONTH = 4.345
MODEL_FILE = "model_efficiency.csv"
ACCESS_FILE = "subscription_first_task_cost.csv"
EVIDENCE_FILE = "access_evidence.csv"
UNCHANGED_FILES = ("frontier_model_positions.csv",)
PRICE_FIELDS = (
    "api_input_usd_per_million",
    "api_cache_read_usd_per_million",
    "api_cache_write_usd_per_million",
    "api_output_usd_per_million",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write an empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_updates(path: Path) -> dict[str, dict[str, str]]:
    rows = read_csv(path)
    updates = {row["model"]: row for row in rows}
    if len(updates) != len(rows):
        raise ValueError("Duplicate model in API price update manifest")
    for model, row in updates.items():
        if not model:
            raise ValueError("Empty model in API price update manifest")
        for field in PRICE_FIELDS:
            if float(row[field]) < 0:
                raise ValueError(f"Negative {field} for {model}")
        if not row["api_price_source_url"].startswith("https://"):
            raise ValueError(f"Missing direct price source for {model}")
    return updates


def normalized_cost(row: dict[str, str]) -> tuple[float, float]:
    input_price = float(row["api_input_usd_per_million"])
    cache_read_price = float(row["api_cache_read_usd_per_million"])
    cache_write_price = float(row["api_cache_write_usd_per_million"])
    output_price = float(row["api_output_usd_per_million"])
    blended = 0.2 * input_price + 0.7 * cache_read_price + 0.1 * output_price
    task_cost = (
        float(row["task_noncache_input_tokens"]) * input_price
        + float(row["task_cache_read_tokens"]) * cache_read_price
        + float(row["task_cache_write_tokens"]) * cache_write_price
        + float(row["task_output_tokens"]) * output_price
    ) / 1_000_000
    return blended, task_cost


def update_model_rows(
    rows: list[dict[str, str]], updates: dict[str, dict[str, str]]
) -> tuple[list[dict[str, str]], dict[tuple[str, str], dict[str, str]]]:
    found: set[str] = set()
    indexed: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        update = updates.get(row["model"])
        if update:
            found.add(row["model"])
            for field in PRICE_FIELDS:
                row[field] = f"{float(update[field]):.12f}"
            row["api_price_source_url"] = update["api_price_source_url"]
            row["api_price_note"] = update["api_price_note"]
            blended, task_cost = normalized_cost(row)
            row["blended_usd_per_million_tokens"] = f"{blended:.12f}"
            row["cost_per_index_task_usd"] = f"{task_cost:.12f}"
        key = (row["model"], row["effort"])
        if key in indexed:
            raise ValueError(f"Duplicate model configuration: {key}")
        indexed[key] = row
    missing = set(updates) - found
    if missing:
        raise ValueError(f"Price-update models absent from base snapshot: {sorted(missing)}")
    return rows, indexed


def update_access_rows(
    rows: list[dict[str, str]],
    model_index: dict[tuple[str, str], dict[str, str]],
    updated_models: set[str],
) -> list[dict[str, str]]:
    for row in rows:
        if row["model"] not in updated_models:
            continue
        key = (row["model"], row["effort"])
        model_row = model_index[key]
        api_cost = float(model_row["cost_per_index_task_usd"])
        task_tokens = float(row["total_tokens_per_index_task"])
        row["api_cost_per_task_usd"] = f"{api_cost:.12f}"
        for target, source in (
            ("api_price_provider", "api_provider"),
            ("api_provider_model_id", "api_provider_model_id"),
            ("api_precision", "api_precision"),
            ("api_price_source_url", "api_price_source_url"),
        ):
            row[target] = model_row[source]

        if row["access_mode"] == "subscription_api_equivalent_estimate":
            ratio = float(row["api_value_ratio"])
            weekly_api_equivalent = float(row["weekly_api_equivalent_usd"])
            tasks_per_week = weekly_api_equivalent / api_cost
            effective_cost = api_cost / ratio
            row["tasks_per_week"] = f"{tasks_per_week:.12f}"
            row["normalized_weekly_quota"] = f"{tasks_per_week * task_tokens:.6f}"
            row["effective_cost_per_task_usd"] = f"{effective_cost:.12f}"
        elif row["access_mode"].startswith("api_"):
            row["effective_cost_per_task_usd"] = f"{api_cost:.12f}"
        else:
            raise ValueError(
                f"Unsupported access mode for repriced model {row['model']}: "
                f"{row['access_mode']}"
            )
        effective_cost = float(row["effective_cost_per_task_usd"])
        row["effective_usd_per_million_task_tokens"] = (
            f"{effective_cost / task_tokens * 1_000_000:.12f}"
        )
    return rows


def update_evidence_rows(rows: list[dict[str, str]], snapshot: str) -> list[dict[str, str]]:
    matches = [row for row in rows if row["provider"] == "OpenAI"]
    if len(matches) != 1:
        raise ValueError(f"Expected one OpenAI access evidence row, found {len(matches)}")
    row = matches[0]
    row["as_of_date"] = snapshot
    row["published_quota"] = (
        "Best available full-limit test: about $14,000/month API-equivalent; "
        "official 2026-07-30 Codex credit rates remain proportional to standard API prices"
    )
    row["reason"] = (
        "Highest-confidence current allowance estimate; official credit pricing confirms "
        "the repricing basis, but OpenAI does not promise a fixed Token quota"
    )
    return rows


def verify(
    base_models: list[dict[str, str]],
    new_models: list[dict[str, str]],
    base_access: list[dict[str, str]],
    new_access: list[dict[str, str]],
    updates: dict[str, dict[str, str]],
) -> None:
    if len(base_models) != 73 or len(new_models) != 73:
        raise ValueError("Expected 73 model configurations")
    if len(base_access) != 46 or len(new_access) != 46:
        raise ValueError("Expected 46 subscription-first configurations")
    base_index = {(row["model"], row["effort"]): row for row in base_models}
    new_index = {(row["model"], row["effort"]): row for row in new_models}
    expected_factors = {"GPT-5.6 Terra": 0.8, "GPT-5.6 Luna": 0.2}
    for key, new_row in new_index.items():
        old_row = base_index[key]
        for field in (
            "intelligence_score_raw",
            "total_tokens_million",
            "total_tokens_per_index_task",
        ):
            if new_row[field] != old_row[field]:
                raise ValueError(f"Benchmark field changed during repricing: {key} {field}")
        if new_row["model"] in updates:
            factor = expected_factors[new_row["model"]]
            actual = float(new_row["cost_per_index_task_usd"]) / float(
                old_row["cost_per_index_task_usd"]
            )
            if abs(actual - factor) > 1e-9:
                raise ValueError(f"Unexpected task-cost factor for {key}: {actual}")
        elif new_row["cost_per_index_task_usd"] != old_row["cost_per_index_task_usd"]:
            raise ValueError(f"Unaffected model cost changed: {key}")

    old_access = {(row["model"], row["effort"]): row for row in base_access}
    for row in new_access:
        key = (row["model"], row["effort"])
        old_row = old_access[key]
        if row["model"] in updates:
            factor = expected_factors[row["model"]]
            actual = float(row["effective_cost_per_task_usd"]) / float(
                old_row["effective_cost_per_task_usd"]
            )
            if abs(actual - factor) > 1e-8:
                raise ValueError(f"Unexpected subscription-cost factor for {key}: {actual}")
            if abs(float(row["api_value_ratio"]) - 70.0) > 1e-12:
                raise ValueError(f"OpenAI API-value ratio changed for {key}")
        elif row["effective_cost_per_task_usd"] != old_row["effective_cost_per_task_usd"]:
            raise ValueError(f"Unaffected access cost changed: {key}")


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Create a dated pricing-only snapshot from an existing benchmark snapshot."
    )
    parser.add_argument("--base-snapshot", default="2026-07-24")
    parser.add_argument("--snapshot", default="2026-07-31")
    parser.add_argument(
        "--updates",
        type=Path,
        default=project_root / "data" / "api_price_updates_2026-07-31.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    base_dir = project_root / "data" / args.base_snapshot
    output_dir = project_root / "data" / args.snapshot
    if output_dir.exists():
        raise FileExistsError(f"Output snapshot already exists: {output_dir}")

    updates = load_updates(args.updates)
    base_models = read_csv(base_dir / MODEL_FILE)
    base_access = read_csv(base_dir / ACCESS_FILE)
    new_models, model_index = update_model_rows(
        [dict(row) for row in base_models], updates
    )
    new_access = update_access_rows(
        [dict(row) for row in base_access], model_index, set(updates)
    )
    new_evidence = update_evidence_rows(
        read_csv(base_dir / EVIDENCE_FILE), args.snapshot
    )
    verify(base_models, new_models, base_access, new_access, updates)

    write_csv(output_dir / MODEL_FILE, new_models)
    write_csv(output_dir / ACCESS_FILE, new_access)
    write_csv(output_dir / EVIDENCE_FILE, new_evidence)
    for name in UNCHANGED_FILES:
        shutil.copy2(base_dir / name, output_dir / name)
    print(
        f"snapshot={args.snapshot}; models={len(new_models)}; "
        f"api={sum(bool(row['cost_per_index_task_usd']) for row in new_models)}; "
        f"subscription={len(new_access)}"
    )


if __name__ == "__main__":
    main()
