from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SOURCE_URL = "https://artificialanalysis.ai/agents/coding-agents"
METHODOLOGY_URL = (
    "https://artificialanalysis.ai/methodology/coding-agents-benchmarking"
)
BENCHMARK_VERSION = "Coding Agent Index v1.3"
EXPECTED_COUNT = 52
KNOWN_SETTINGS = ("none", "low", "medium", "high", "xhigh", "max", "thinking")
EFFORT_ORDER = {
    "non-reasoning": 0,
    "fast": 10,
    "default": 20,
    "low": 30,
    "medium": 50,
    "thinking": 60,
    "high": 70,
    "xhigh": 90,
    "max": 100,
}
COMPONENT_COLUMNS = {
    "deep-swe": "deep_swe_score",
    "terminal-bench-v2": "terminal_bench_v2_score",
    "swe-atlas-qna": "swe_atlas_qna_score",
}


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def write_csv(path: Path, rows: list[dict[str, object]], fields: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def download_page(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/140 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        raw = response.read()
        final_url = response.geturl()
    return raw, final_url


def extract_rsc_payload(page: str) -> str:
    pattern = re.compile(
        r'self\.__next_f\.push\(\[1,("(?:\\.|[^"\\])*")\]\)'
    )
    chunks: list[str] = []
    for match in pattern.finditer(page):
        chunks.append(json.loads(match.group(1)))
    if not chunks:
        raise ValueError("No Next.js RSC payload chunks were found")
    return "\n".join(chunks)


def balanced_json_end(payload: str, start: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    index = start
    while index < len(payload):
        character = payload[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        else:
            if character == '"':
                in_string = True
            elif character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth == 0:
                    return index + 1
        index += 1
    raise ValueError(f"Unterminated JSON object at payload offset {start}")


def extract_result_objects(payload: str) -> list[dict[str, object]]:
    row_start = re.compile(r'\{"id":"[^"]+","agentName":')
    rows: list[dict[str, object]] = []
    position = 0
    while position < len(payload):
        match = row_start.search(payload, position)
        if match is None:
            break
        start = match.start()
        end = balanced_json_end(payload, start)
        candidate = json.loads(payload[start:end])
        if "mean" in candidate and "indexScore" in candidate:
            rows.append(candidate)
        position = end
    if not rows:
        raise ValueError("No coding-agent result objects were extracted")
    return rows


def normalized_model_and_effort(
    display_model: str,
    host_model_slug: str,
    variant_of: object,
) -> tuple[str, str, str]:
    model = display_model.strip()
    source_effort = "default"
    setting_pattern = re.compile(
        r"\s+\((" + "|".join(KNOWN_SETTINGS) + r")\)(?=\s*(?:\(with fallback\))?$)",
        flags=re.IGNORECASE,
    )
    match = setting_pattern.search(model)
    if match is not None:
        source_effort = match.group(1).lower()
        model = (model[: match.start()] + model[match.end() :]).strip()
    elif variant_of and model.endswith(" Fast"):
        model = model[: -len(" Fast")].strip()
        source_effort = "fast"

    effort = "non-reasoning" if source_effort == "none" else source_effort
    if model == "DeepSeek V4 Pro":
        model = "DeepSeek V4 Pro (Preview)"
    if host_model_slug.endswith("_fp8") and "(FP8)" not in model:
        model = f"{model} (FP8)"
    return model, effort, source_effort


def require_number(value: object, field: str, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label}: {field} is not numeric")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label}: {field} is negative or non-finite")
    return number


def optional_number(value: object, field: str, label: str) -> float | str:
    if value is None:
        return ""
    return require_number(value, field, label)


def normalize_row(
    source: dict[str, object],
    source_rank: int,
    observed_at: str,
    source_sha256: str,
) -> dict[str, object]:
    display = source.get("display")
    mean = source.get("mean")
    if not isinstance(display, dict) or not isinstance(mean, dict):
        raise ValueError(f"Source row {source_rank} is missing display or mean")
    creator = display.get("creator")
    if not isinstance(creator, dict):
        raise ValueError(f"Source row {source_rank} is missing creator metadata")

    result_id = str(source.get("id", "")).strip()
    agent = str(display.get("agent", source.get("agentName", ""))).strip()
    display_model = str(display.get("model", "")).strip()
    label = str(source.get("displayLabel", f"{agent} - {display_model}"))
    route_provider = str(source.get("provider", "")).strip()
    host_model_slug = str(source.get("hostModelSlug", "")).strip()
    variant_of = source.get("variantOf")
    if not result_id or not agent or not display_model or not route_provider:
        raise ValueError(f"Source row {source_rank} has incomplete identity fields")

    model, effort, source_effort = normalized_model_and_effort(
        display_model,
        host_model_slug,
        variant_of,
    )
    component_count = int(source.get("indexComponentCount", 0))
    eval_count = int(source.get("evalCount", 0))
    if component_count != 3:
        raise ValueError(
            f"{label}: expected indexComponentCount=3, found {component_count}"
        )

    index_score_raw = require_number(source.get("indexScore"), "indexScore", label)
    if index_score_raw > 1:
        raise ValueError(f"{label}: indexScore exceeds 1")
    component_values: dict[str, float | str] = {
        column: "" for column in COMPONENT_COLUMNS.values()
    }
    evals = source.get("evals")
    if not isinstance(evals, list):
        raise ValueError(f"{label}: evals is not a list")
    materialized_scores: list[float] = []
    for evaluation in evals:
        if not isinstance(evaluation, dict):
            continue
        component_name = str(evaluation.get("datasetIndexName", ""))
        column = COMPONENT_COLUMNS.get(component_name)
        evaluation_mean = evaluation.get("mean")
        if column is None or not isinstance(evaluation_mean, dict):
            continue
        component_score = require_number(
            evaluation_mean.get("reward"),
            f"{component_name}.reward",
            label,
        )
        component_values[column] = component_score * 100
        materialized_scores.append(component_score)

    if eval_count != len(materialized_scores):
        raise ValueError(
            f"{label}: evalCount={eval_count}, materialized={len(materialized_scores)}"
        )
    if eval_count not in (2, 3):
        raise ValueError(f"{label}: unsupported evalCount={eval_count}")
    recomputed_score = sum(materialized_scores) / len(materialized_scores)
    score_delta = abs(index_score_raw - recomputed_score)
    if score_delta > 1e-10:
        raise ValueError(
            f"{label}: index score differs from materialized component mean by {score_delta}"
        )

    return {
        "source_rank": source_rank,
        "result_id": result_id,
        "agent": agent,
        "agent_creator": str(creator.get("agent", "")).strip(),
        "model": model,
        "model_creator": str(creator.get("model", "")).strip(),
        "series": f"{agent} · {model}",
        "effort": effort,
        "source_effort": source_effort,
        "effort_order": EFFORT_ORDER[effort],
        "source_display_model": display_model,
        "source_display_label": label,
        "route_provider": route_provider,
        "host_model_slug": host_model_slug,
        "variant_of_result_id": "" if variant_of is None else str(variant_of),
        "benchmark_version": BENCHMARK_VERSION,
        "index_component_count": component_count,
        "eval_count": eval_count,
        "data_scope": "complete" if eval_count == 3 else "partial",
        "coding_agent_score": index_score_raw * 100,
        "recomputed_component_mean": recomputed_score * 100,
        "score_delta": score_delta * 100,
        **component_values,
        "cost_usd_per_task": require_number(mean.get("costUsd"), "costUsd", label),
        "agent_wall_time_sec": require_number(
            mean.get("agentWallTimeSec"), "agentWallTimeSec", label
        ),
        "steps_per_task": require_number(mean.get("steps"), "steps", label),
        "input_tokens": require_number(mean.get("inputTokens"), "inputTokens", label),
        "cache_write_tokens": optional_number(
            mean.get("cacheWriteTokens"), "cacheWriteTokens", label
        ),
        "cache_read_tokens": optional_number(
            mean.get("cacheTokens"), "cacheTokens", label
        ),
        "cache_hit_rate": optional_number(
            mean.get("cacheHitRate"), "cacheHitRate", label
        ),
        "output_tokens": require_number(
            mean.get("outputTokens"), "outputTokens", label
        ),
        "total_tokens": require_number(mean.get("totalTokens"), "totalTokens", label),
        "total_tokens_million": require_number(
            mean.get("totalTokens"), "totalTokens", label
        )
        / 1_000_000,
        "source_url": SOURCE_URL,
        "methodology_url": METHODOLOGY_URL,
        "observed_at_utc": observed_at,
        "source_sha256": source_sha256,
    }


def validate_rows(rows: list[dict[str, object]], expected_count: int) -> None:
    if len(rows) != expected_count:
        raise ValueError(f"Expected {expected_count} rows, found {len(rows)}")
    ids = [str(row["result_id"]) for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate Artificial Analysis result ids were extracted")
    labels = [str(row["source_display_label"]) for row in rows]
    if len(set(labels)) != len(labels):
        raise ValueError("Duplicate source display labels were extracted")
    complete_count = sum(row["data_scope"] == "complete" for row in rows)
    partial_count = sum(row["data_scope"] == "partial" for row in rows)
    if (complete_count, partial_count) != (51, 1):
        raise ValueError(
            "Expected 51 complete and 1 partial row; found "
            f"{complete_count} complete and {partial_count} partial"
        )
    partial_labels = [
        str(row["source_display_label"])
        for row in rows
        if row["data_scope"] == "partial"
    ]
    if partial_labels != ["Claude Code - Opus 4.6 (medium)"]:
        raise ValueError(f"Unexpected partial source rows: {partial_labels}")


def parse_args() -> argparse.Namespace:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Snapshot the Artificial Analysis coding-agent table."
    )
    parser.add_argument("--snapshot", default="2026-07-31")
    parser.add_argument("--source-url", default=SOURCE_URL)
    parser.add_argument("--expected-count", type=int, default=EXPECTED_COUNT)
    parser.add_argument("--repository-root", type=Path, default=repository_root)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_page, final_url = download_page(args.source_url)
    page = raw_page.decode("utf-8")
    if "v1.3" not in page or "Coding Agent Index" not in page:
        raise ValueError("The downloaded page does not identify Coding Agent Index v1.3")
    source_sha256 = hashlib.sha256(raw_page).hexdigest()
    observed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    payload = extract_rsc_payload(page)
    source_rows = extract_result_objects(payload)
    normalized = [
        normalize_row(row, source_rank, observed_at, source_sha256)
        for source_rank, row in enumerate(source_rows, start=1)
    ]
    normalized.sort(key=lambda row: int(row["source_rank"]))
    validate_rows(normalized, args.expected_count)

    output_dir = args.repository_root / "data" / "coding-agents" / args.snapshot
    fields = list(normalized[0].keys())
    write_csv(output_dir / "coding_agent_results.csv", normalized, fields)
    metadata = {
        "snapshot": args.snapshot,
        "benchmark": BENCHMARK_VERSION,
        "source_url": final_url,
        "methodology_url": METHODOLOGY_URL,
        "observed_at_utc": observed_at,
        "source_sha256": source_sha256,
        "source_bytes": len(raw_page),
        "rsc_chunks": len(
            re.findall(r"self\.__next_f\.push\(\[1,", page)
        ),
        "counts": {
            "source_rows": len(normalized),
            "complete_rows": sum(
                row["data_scope"] == "complete" for row in normalized
            ),
            "partial_rows": sum(
                row["data_scope"] == "partial" for row in normalized
            ),
        },
        "partial_rows": [
            {
                "result_id": row["result_id"],
                "display_label": row["source_display_label"],
                "eval_count": row["eval_count"],
            }
            for row in normalized
            if row["data_scope"] == "partial"
        ],
    }
    atomic_text(
        output_dir / "source_metadata.json",
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
    )
    print(
        json.dumps(
            {
                "output": str(output_dir / "coding_agent_results.csv"),
                **metadata["counts"],
                "source_sha256": source_sha256,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
