from __future__ import annotations

import argparse
import csv
import json
import math
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

from PIL import Image


EXPECTED = {"token": 70, "api": 66, "subscription": 40}
BENCHMARK = "Artificial Analysis Intelligence Index v4.1.1"
LANGUAGES = ("en", "zh-CN")
ANALYSIS_STEMS = (
    "01_total_token_consumption_vs_score",
    "02_api_task_cost_vs_score",
    "03_subscription_first_task_cost_vs_score",
)
RANKING_STEMS = (
    "04_token_efficiency_ranking",
    "05_api_cost_ranking",
    "05_api_cost_ranking_full",
    "06_subscription_cost_ranking",
    "06_subscription_cost_ranking_full",
)
QUANTIZED_ROUTE = re.compile(r"(?:^|[^A-Z0-9])(BF16|FP8|FP4|NVFP|MXFP|INT8|INT4|AWQ|GPTQ)(?:[^A-Z0-9]|$)", re.I)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def close(actual: float, expected: float, *, absolute: float = 1e-8) -> bool:
    return math.isclose(actual, expected, rel_tol=2e-8, abs_tol=absolute)


def validate_models(root: Path, snapshot: str) -> list[dict[str, str]]:
    rows = read_csv(root / "data" / snapshot / "model_efficiency.csv")
    assert len(rows) == EXPECTED["token"], len(rows)
    assert len({(row["model"], row["effort"]) for row in rows}) == len(rows)
    assert not any(
        "DeepSeek" in row["model"] and "Preview" in row["model"] for row in rows
    )
    assert sum(bool(row["cost_per_index_task_usd"]) for row in rows) == EXPECTED["api"]

    api_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        canonical_total = (
            int(row["canonical_input_tokens"]) + int(row["canonical_output_tokens"])
        ) / 1_000_000
        assert close(canonical_total, float(row["total_tokens_million"]), absolute=1e-6)
        assert row["source_url"].startswith("https://artificialanalysis.ai/models/")
        if not row["cost_per_index_task_usd"]:
            assert row["data_scope"] == "token_only"
            continue

        api_by_model[row["model"]].append(row)
        route_text = " ".join(
            (row["api_provider"], row["api_provider_model_id"], row["api_precision"])
        )
        assert not QUANTIZED_ROUTE.search(route_text), (row["model"], route_text)
        task_total = sum(
            float(row[name])
            for name in (
                "task_noncache_input_tokens",
                "task_cache_read_tokens",
                "task_cache_write_tokens",
                "task_output_tokens",
            )
        )
        assert close(task_total, float(row["total_tokens_per_index_task"]), absolute=1e-5)
        computed_cost = (
            float(row["task_noncache_input_tokens"])
            * float(row["api_input_usd_per_million"])
            + float(row["task_cache_read_tokens"])
            * float(row["api_cache_read_usd_per_million"])
            + float(row["task_cache_write_tokens"])
            * float(row["api_cache_write_usd_per_million"])
            + float(row["task_output_tokens"])
            * float(row["api_output_usd_per_million"])
        ) / 1_000_000
        assert close(computed_cost, float(row["cost_per_index_task_usd"]), absolute=2e-9), (
            row["model"],
            row["effort"],
            computed_cost,
            row["cost_per_index_task_usd"],
        )

    fixed_fields = (
        "api_provider",
        "api_input_usd_per_million",
        "api_cache_read_usd_per_million",
        "api_cache_write_usd_per_million",
        "api_output_usd_per_million",
    )
    for model, model_rows in api_by_model.items():
        for field in fixed_fields:
            assert len({row[field] for row in model_rows}) == 1, (model, field)

    expected_deepseek = {
        "DeepSeek V4 Pro 0813": {
            "score": 53.1976849297815,
            "tokens": 1014.847808,
            "provider": "DeepSeek",
            "cost": 0.056094160219,
            "source": "https://api-docs.deepseek.com/quick_start/pricing/",
        },
        "DeepSeek V4 Flash 0731": {
            "score": 51.7665776089032,
            "tokens": 1486.993592,
            "provider": "DeepInfra",
            "cost": 0.056678692934,
            "source": "https://artificialanalysis.ai/models/deepseek-v4-flash/providers",
        },
    }
    for model, expected in expected_deepseek.items():
        row = next(item for item in rows if item["model"] == model)
        assert close(float(row["intelligence_score_raw"]), expected["score"], absolute=1e-10)
        assert close(float(row["total_tokens_million"]), expected["tokens"], absolute=1e-6)
        assert row["api_provider"] == expected["provider"]
        assert close(float(row["cost_per_index_task_usd"]), expected["cost"], absolute=2e-9)
        assert row["api_price_source_url"] == expected["source"]
    return rows


def validate_access(root: Path, snapshot: str, model_rows: list[dict[str, str]]) -> None:
    rows = read_csv(root / "data" / snapshot / "subscription_first_task_cost.csv")
    assert len(rows) == EXPECTED["subscription"], len(rows)
    assert len({(row["model"], row["effort"]) for row in rows}) == len(rows)
    model_keys = {(row["model"], row["effort"]) for row in model_rows}
    assert all((row["model"], row["effort"]) in model_keys for row in rows)
    for row in rows:
        api_cost = float(row["api_cost_per_task_usd"])
        effective = float(row["effective_cost_per_task_usd"])
        mode = row["access_mode"]
        if mode.startswith("subscription_"):
            tasks = float(row["tasks_per_week"])
            weekly_cost = float(row["weekly_cost_usd"])
            assert close(weekly_cost / tasks, effective, absolute=2e-9)
            if mode == "subscription_api_equivalent_estimate":
                assert close(api_cost / float(row["api_value_ratio"]), effective, absolute=2e-9)
        else:
            assert close(api_cost, effective, absolute=2e-9)

    evidence = read_csv(root / "data" / snapshot / "access_evidence.csv")
    listed_models: set[str] = set()
    for row in evidence:
        assert row["as_of_date"] == snapshot
        assert "Preview" not in row["models_in_chart"] or "Gemini" in row["models_in_chart"]
        listed_models.update(
            model.strip() for model in row["models_in_chart"].split(";") if model.strip()
        )
    assert listed_models == {row["model"] for row in model_rows}


def validate_observations(root: Path, snapshot: str) -> None:
    payload = json.loads(
        (root / "data" / snapshot / "aa_observations.json").read_text("utf-8")
    )
    assert payload["snapshot"] == snapshot
    assert payload["benchmark"] == BENCHMARK
    assert not payload["fetch_errors"]
    assert len(payload["observations"]) == EXPECTED["token"]
    assert all(item["benchmark"] == BENCHMARK for item in payload["observations"])


def validate_rankings_and_site(root: Path, snapshot: str) -> None:
    ranking_dir = root / "rankings" / snapshot
    token = read_csv(ranking_dir / "token_efficiency_ranking.csv")
    api = read_csv(ranking_dir / "api_cost_ranking.csv")
    subscription = read_csv(ranking_dir / "subscription_cost_ranking.csv")
    thresholds = read_csv(ranking_dir / "score_threshold_leaders.csv")
    assert len(token) == 8
    assert len(api) == EXPECTED["api"]
    assert len(subscription) == EXPECTED["subscription"]
    assert len(thresholds) == 12

    payload = json.loads(
        (root / "site" / "data" / "snapshots" / f"{snapshot}.json").read_text(
            "utf-8"
        )
    )
    assert payload["snapshot"] == snapshot
    assert payload["benchmark"] == BENCHMARK
    assert payload["counts"]["token_configurations"] == EXPECTED["token"]
    assert payload["counts"]["api_cost_configurations"] == EXPECTED["api"]
    assert payload["counts"]["subscription_first_configurations"] == EXPECTED["subscription"]
    assert len(payload["charts"]["token"]) == EXPECTED["token"]
    assert len(payload["charts"]["api"]) == EXPECTED["api"]
    assert len(payload["charts"]["subscription"]) == EXPECTED["subscription"]

    manifest = json.loads((root / "site" / "data" / "snapshots.json").read_text("utf-8"))
    assert manifest["current"] == snapshot
    assert [entry["id"] for entry in manifest["snapshots"]] == [
        "2026-08-15",
        "2026-07-31",
        "2026-07-24",
    ]
    archived = next(entry for entry in manifest["snapshots"] if entry["id"] == "2026-07-31")
    assert archived["chart_base"] == "charts/archive/2026-07-31"
    historical_counts = {
        item: json.loads(
            (root / "site" / "data" / "snapshots" / f"{item}.json").read_text("utf-8")
        )["counts"]
        for item in ("2026-07-31", "2026-07-24")
    }
    for counts in historical_counts.values():
        assert counts["token_configurations"] == 73
        assert counts["api_cost_configurations"] == 68
        assert counts["subscription_first_configurations"] == 46


def validate_artifacts(root: Path, snapshot: str) -> None:
    metrics = json.loads(
        (root / "data" / snapshot / "static_chart_metrics.json").read_text("utf-8")
    )
    assert len(metrics) == 6
    expected_rows = {"token": 70, "api": 66, "subscription": 40}
    for item in metrics:
        assert item["locale"] in LANGUAGES
        assert item["rows"] == expected_rows[item["metric"]]
        assert item["label_collisions"] == 0
        assert item["out_of_bounds_labels"] == 0

    for language in LANGUAGES:
        for stem in (*ANALYSIS_STEMS, *RANKING_STEMS):
            png = root / "charts" / language / f"{stem}.png"
            svg = root / "charts" / language / f"{stem}.svg"
            assert png.is_file() and svg.is_file(), (png, svg)
            with Image.open(png) as image:
                assert image.size[0] >= 2400 and image.size[1] >= 1350, (png, image.size)
            ET.parse(svg)
        for stem in ANALYSIS_STEMS:
            assert "DeepSeek V4 Pro (Preview)" not in (
                root / "charts" / language / f"{stem}.svg"
            ).read_text("utf-8")


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Validate the current general-model snapshot.")
    parser.add_argument("--repository-root", type=Path, default=root)
    parser.add_argument("--snapshot", default="2026-08-15")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.repository_root.resolve()
    rows = validate_models(root, args.snapshot)
    validate_access(root, args.snapshot, rows)
    validate_observations(root, args.snapshot)
    validate_rankings_and_site(root, args.snapshot)
    validate_artifacts(root, args.snapshot)
    print(
        f"validated {args.snapshot}: {EXPECTED['token']} Token / "
        f"{EXPECTED['api']} API / {EXPECTED['subscription']} subscription; "
        "six analysis charts and ten ranking assets"
    )


if __name__ == "__main__":
    main()
