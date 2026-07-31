from __future__ import annotations

import argparse
import csv
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


EXPECTED_COUNTS = {"models": 73, "api": 68, "subscription": 46}
EXPECTED_FACTORS = {"GPT-5.6 Terra": 0.8, "GPT-5.6 Luna": 0.2}
EXPECTED_PRICES = {
    "GPT-5.6 Terra": (2.0, 0.2, 2.5, 12.0),
    "GPT-5.6 Luna": (0.2, 0.02, 0.25, 1.2),
}
EXPECTED_SNAPSHOTS = {
    "2026-07-31": "2026-07-31T05:55:55Z",
    "2026-07-24": "2026-07-25T03:06:13Z",
}
PRICE_FIELDS = (
    "api_input_usd_per_million",
    "api_cache_read_usd_per_million",
    "api_cache_write_usd_per_million",
    "api_output_usd_per_million",
)
CHART_STEMS = (
    "01_total_token_consumption_vs_score",
    "02_api_task_cost_vs_score",
    "03_subscription_first_task_cost_vs_score",
    "04_token_efficiency_ranking",
    "05_api_cost_ranking",
    "05_api_cost_ranking_full",
    "06_subscription_cost_ranking",
    "06_subscription_cost_ranking_full",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    result = {(row["model"], row["effort"]): row for row in rows}
    if len(result) != len(rows):
        raise AssertionError("Duplicate model + reasoning-level configurations")
    return result


def validate_data(root: Path, base_snapshot: str, snapshot: str) -> None:
    base_dir = root / "data" / base_snapshot
    data_dir = root / "data" / snapshot
    old_models = read_csv(base_dir / "model_efficiency.csv")
    new_models = read_csv(data_dir / "model_efficiency.csv")
    old_access = read_csv(base_dir / "subscription_first_task_cost.csv")
    new_access = read_csv(data_dir / "subscription_first_task_cost.csv")
    assert len(new_models) == EXPECTED_COUNTS["models"]
    assert sum(bool(row["cost_per_index_task_usd"]) for row in new_models) == EXPECTED_COUNTS["api"]
    assert len(new_access) == EXPECTED_COUNTS["subscription"]

    old_model_index = index(old_models)
    new_model_index = index(new_models)
    for key, new_row in new_model_index.items():
        old_row = old_model_index[key]
        for field in (
            "intelligence_score_raw",
            "total_tokens_million",
            "total_tokens_per_index_task",
        ):
            assert new_row[field] == old_row[field], (key, field)
        model = new_row["model"]
        if model in EXPECTED_FACTORS:
            prices = tuple(float(new_row[field]) for field in PRICE_FIELDS)
            assert prices == EXPECTED_PRICES[model]
            assert new_row["api_price_source_url"] == (
                "https://developers.openai.com/api/docs/pricing"
            )
            ratio = float(new_row["cost_per_index_task_usd"]) / float(
                old_row["cost_per_index_task_usd"]
            )
            assert math.isclose(ratio, EXPECTED_FACTORS[model], rel_tol=1e-9)
        else:
            assert new_row["cost_per_index_task_usd"] == old_row["cost_per_index_task_usd"]

    old_access_index = index(old_access)
    new_access_index = index(new_access)
    for key, new_row in new_access_index.items():
        old_row = old_access_index[key]
        model = new_row["model"]
        if model in EXPECTED_FACTORS:
            api_ratio = float(new_row["api_cost_per_task_usd"]) / float(
                old_row["api_cost_per_task_usd"]
            )
            plan_ratio = float(new_row["effective_cost_per_task_usd"]) / float(
                old_row["effective_cost_per_task_usd"]
            )
            assert math.isclose(api_ratio, EXPECTED_FACTORS[model], rel_tol=1e-9)
            assert math.isclose(plan_ratio, EXPECTED_FACTORS[model], rel_tol=1e-8)
            assert math.isclose(float(new_row["api_value_ratio"]), 70.0, rel_tol=1e-12)
            assert math.isclose(
                float(new_row["api_cost_per_task_usd"])
                / float(new_row["effective_cost_per_task_usd"]),
                70.0,
                rel_tol=1e-8,
            )
        else:
            assert (
                new_row["effective_cost_per_task_usd"]
                == old_row["effective_cost_per_task_usd"]
            )


def validate_rankings(root: Path, snapshot: str, *, current: bool) -> None:
    ranking_dir = root / "rankings" / snapshot
    expected = {
        "token_efficiency_ranking.csv": 9,
        "api_cost_ranking.csv": 68,
        "subscription_cost_ranking.csv": 46,
        "score_threshold_leaders.csv": 12,
    }
    for name, count in expected.items():
        assert len(read_csv(ranking_dir / name)) == count, name

    payload = json.loads(
        (root / "site" / "data" / "snapshots" / f"{snapshot}.json").read_text(
            "utf-8"
        )
    )
    assert payload["snapshot"] == snapshot
    assert payload["counts"]["token_configurations"] == EXPECTED_COUNTS["models"]
    assert payload["counts"]["api_cost_configurations"] == EXPECTED_COUNTS["api"]
    assert payload["counts"]["subscription_first_configurations"] == EXPECTED_COUNTS["subscription"]
    assert len(payload["charts"]["token"]) == EXPECTED_COUNTS["models"]
    assert len(payload["charts"]["api"]) == EXPECTED_COUNTS["api"]
    assert len(payload["charts"]["subscription"]) == EXPECTED_COUNTS["subscription"]
    if current:
        alias = json.loads(
            (root / "site" / "data" / "rankings.json").read_text("utf-8")
        )
        assert alias == payload


def validate_chart_tree(chart_root: Path) -> None:
    for locale in ("en", "zh-CN"):
        chart_dir = chart_root / locale
        for stem in CHART_STEMS:
            png = chart_dir / f"{stem}.png"
            svg = chart_dir / f"{stem}.svg"
            expected_size = (4800, 3600) if stem.endswith("_full") else (4800, 2700)
            with Image.open(png) as image:
                assert image.size == expected_size, png
                assert image.mode in {"RGB", "RGBA"}, png
            assert png.stat().st_size > 100_000, png
            ET.parse(svg)
            assert svg.stat().st_size > 80_000, svg


def validate_charts(root: Path) -> None:
    validate_chart_tree(root / "charts")
    validate_chart_tree(root / "charts" / "archive" / "2026-07-24")


def validate_site_links(root: Path, snapshot: str) -> None:
    index_html = (root / "site" / "index.html").read_text("utf-8")
    app_js = (root / "site" / "assets" / "app.js").read_text("utf-8")
    interactive_js = (root / "site" / "assets" / "interactive-scatter.js").read_text(
        "utf-8"
    )
    manifest = json.loads(
        (root / "site" / "data" / "snapshots.json").read_text("utf-8")
    )
    assert manifest["current"] == snapshot
    assert {entry["id"] for entry in manifest["snapshots"]} == set(
        EXPECTED_SNAPSHOTS
    )
    for entry in manifest["snapshots"]:
        assert entry["published_at_utc"] == EXPECTED_SNAPSHOTS[entry["id"]]
        assert entry["payload_url"] == f"data/snapshots/{entry['id']}.json"
        assert entry["ranking_base"] == f"rankings/{entry['id']}"
        assert entry["data_url"] == f"data/{entry['id']}/model_efficiency.csv"
    historical = next(
        entry for entry in manifest["snapshots"] if entry["id"] == "2026-07-24"
    )
    assert historical["chart_base"] == "charts/archive/2026-07-24"

    assert 'id="snapshot-select"' in index_html
    assert 'id="sota-recommendations"' in index_html
    assert 'id="value-recommendations"' in index_html
    assert f"rankings/{snapshot}/subscription_cost_ranking.csv" in index_html
    assert f"data/{snapshot}/model_efficiency.csv" in index_html
    assert "loadSnapshotManifest" in app_js
    assert "renderRecommendations" in app_js
    assert "data/snapshots.json?v=20260731-snapshot-recommendations" in app_js
    assert "dataRevision: state.snapshot?.id" in app_js
    assert "metricChanged || dataChanged || !this.view" in interactive_js
    assert "20260731-snapshot-recommendations" in index_html
    assert "20260731-snapshot-recommendations" in app_js

    sota_models = ("GPT-5.6 Sol", "Claude Opus 5", "Kimi K3")
    value_models = ("GPT-5.6 Luna", "DeepSeek V4 Pro")
    sota_positions = [app_js.index(f'model: "{model}"') for model in sota_models]
    value_positions = [app_js.index(f'model: "{model}"') for model in value_models]
    assert sota_positions == sorted(sota_positions)
    assert value_positions == sorted(value_positions)
    assert "个人观点" in app_js
    assert "Personal opinion" in app_js


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Validate one published snapshot and chart set.")
    parser.add_argument("--repository-root", type=Path, default=root)
    parser.add_argument("--base-snapshot", default="2026-07-24")
    parser.add_argument("--snapshot", default="2026-07-31")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.repository_root.resolve()
    validate_data(root, args.base_snapshot, args.snapshot)
    for known_snapshot in EXPECTED_SNAPSHOTS:
        validate_rankings(
            root,
            known_snapshot,
            current=known_snapshot == args.snapshot,
        )
    validate_charts(root)
    validate_site_links(root, args.snapshot)
    print(
        "validated snapshot: "
        f"{args.snapshot}; 73 Token / 68 API / 46 subscription; "
        "64 bilingual current/archive chart assets; two dated payloads; "
        "UTC version metadata, recommendations, and switchable links"
    )


if __name__ == "__main__":
    main()
