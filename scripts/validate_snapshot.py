from __future__ import annotations

import argparse
import csv
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image


EXPECTED_COUNTS = {"models": 73, "api": 68, "subscription": 46}
EXPECTED_CODING_COUNTS = {
    "token": 52,
    "api": 52,
    "subscription": 49,
    "complete": 51,
    "partial": 1,
}
ASSET_REVISION = "20260731-coding-agent-suite"
EXPECTED_FACTORS = {"GPT-5.6 Terra": 0.8, "GPT-5.6 Luna": 0.2}
EXPECTED_PRICES = {
    "GPT-5.6 Terra": (2.0, 0.2, 2.5, 12.0),
    "GPT-5.6 Luna": (0.2, 0.02, 0.25, 1.2),
}
EXPECTED_DEEPSEEK_V4_PREVIEW_MODELS = {
    "DeepSeek V4 Pro (Preview)",
    "DeepSeek V4 Flash (Preview)",
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
CODING_CHART_STEMS = (
    "07_coding_agent_total_tokens_vs_index",
    "08_coding_agent_subscription_cost_vs_index",
    "09_coding_agent_api_cost_vs_index",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def index(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    result = {(row["model"], row["effort"]): row for row in rows}
    if len(result) != len(rows):
        raise AssertionError("Duplicate model + reasoning-level configurations")
    return result


def assert_preview_suffix(rows: list[dict[str, object]]) -> None:
    for row in rows:
        model = str(row.get("model", ""))
        if model.startswith("DeepSeek V4 "):
            assert model.endswith(" (Preview)"), model


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
    for rows in (old_models, new_models, old_access, new_access):
        assert_preview_suffix(rows)
    assert {
        row["model"] for row in new_models if row["developer"] == "DeepSeek"
    } == EXPECTED_DEEPSEEK_V4_PREVIEW_MODELS

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
        rows = read_csv(ranking_dir / name)
        assert len(rows) == count, name
        assert_preview_suffix(rows)

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
    payload_rows = (
        payload["token_efficiency"]["core"]
        + payload["token_efficiency"]["limited"]
        + payload["api_cost"]
        + payload["subscription_cost"]
        + payload["charts"]["token"]
        + payload["charts"]["api"]
        + payload["charts"]["subscription"]
        + payload["thresholds"]["api"]
        + payload["thresholds"]["subscription_first"]
    )
    assert_preview_suffix(payload_rows)
    assert {
        row["model"]
        for row in payload["charts"]["token"]
        if row["developer"] == "DeepSeek"
    } == EXPECTED_DEEPSEEK_V4_PREVIEW_MODELS
    if current:
        alias = json.loads(
            (root / "site" / "data" / "rankings.json").read_text("utf-8")
        )
        assert alias == payload


def validate_chart_tree(chart_root: Path, stems: tuple[str, ...]) -> None:
    for locale in ("en", "zh-CN"):
        chart_dir = chart_root / locale
        for stem in stems:
            png = chart_dir / f"{stem}.png"
            svg = chart_dir / f"{stem}.svg"
            expected_size = (4800, 3600) if stem.endswith("_full") else (4800, 2700)
            with Image.open(png) as image:
                assert image.size == expected_size, png
                assert image.mode in {"RGB", "RGBA"}, png
            assert png.stat().st_size > 100_000, png
            ET.parse(svg)
            minimum_svg_bytes = 50_000 if stem in CODING_CHART_STEMS else 80_000
            assert svg.stat().st_size > minimum_svg_bytes, svg


def validate_charts(root: Path) -> None:
    validate_chart_tree(root / "charts", CHART_STEMS + CODING_CHART_STEMS)
    validate_chart_tree(root / "charts" / "archive" / "2026-07-24", CHART_STEMS)


def validate_coding_agents(root: Path, snapshot: str) -> None:
    data_dir = root / "data" / "coding-agents" / snapshot
    results = read_csv(data_dir / "coding_agent_results.csv")
    subscription = read_csv(data_dir / "subscription_first_task_cost.csv")
    exclusions = read_csv(data_dir / "subscription_exclusions.csv")
    policies = read_csv(data_dir / "subscription_access_policy.csv")
    assert len(results) == EXPECTED_CODING_COUNTS["token"]
    assert len(subscription) == EXPECTED_CODING_COUNTS["subscription"]
    assert len(exclusions) == 3
    assert len(policies) == 8
    assert len({row["result_id"] for row in results}) == len(results)
    assert len({row["source_display_label"] for row in results}) == len(results)
    scopes = {scope: sum(row["data_scope"] == scope for row in results) for scope in ("complete", "partial")}
    assert scopes == {
        "complete": EXPECTED_CODING_COUNTS["complete"],
        "partial": EXPECTED_CODING_COUNTS["partial"],
    }
    partial = [row for row in results if row["data_scope"] == "partial"]
    assert [row["source_display_label"] for row in partial] == [
        "Claude Code - Opus 4.6 (medium)"
    ]
    assert partial[0]["eval_count"] == "2"
    assert {
        row["model"] for row in results if row["host_model_slug"].endswith("_fp8")
    } == {"GLM-5.2 (FP8)"}
    assert {
        row["model"] for row in results if row["model"].startswith("DeepSeek V4 Pro")
    } == {"DeepSeek V4 Pro (Preview)"}

    numeric_fields = (
        "coding_agent_score",
        "cost_usd_per_task",
        "agent_wall_time_sec",
        "steps_per_task",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "total_tokens_million",
    )
    for row in results:
        for field in numeric_fields:
            value = float(row[field])
            assert math.isfinite(value) and value >= 0, (row["result_id"], field)
        assert math.isclose(float(row["score_delta"]), 0.0, abs_tol=1e-9)

    all_decision_ids = {
        row["result_id"] for row in subscription + exclusions
    }
    assert all_decision_ids == {row["result_id"] for row in results}
    assert {row["agent"] for row in exclusions} == {
        "Gemini CLI",
        "Grok Build",
        "Kimi Code CLI",
    }
    for row in subscription:
        ratio = float(row["api_value_ratio"])
        assert ratio > 0
        assert math.isclose(
            float(row["api_cost_per_task_usd"])
            / float(row["effective_cost_per_task_usd"]),
            ratio,
            rel_tol=1e-9,
        )
    cursor_rows = [row for row in subscription if row["agent"] == "Cursor CLI"]
    assert len(cursor_rows) == 6
    assert all(row["plan_name"] == "Cursor Ultra" for row in cursor_rows)
    assert all(math.isclose(float(row["api_value_ratio"]), 2.0) for row in cursor_rows)
    assert all(row["confidence"] == "high" for row in cursor_rows)

    metadata = json.loads((data_dir / "source_metadata.json").read_text("utf-8"))
    assert metadata["benchmark"] == "Coding Agent Index v1.3"
    assert metadata["counts"] == {
        "source_rows": 52,
        "complete_rows": 51,
        "partial_rows": 1,
    }
    assert len(metadata["source_sha256"]) == 64

    payload = json.loads(
        (root / "site" / "data" / "coding-agents" / f"{snapshot}.json").read_text(
            "utf-8"
        )
    )
    assert payload["snapshot"] == snapshot
    assert payload["benchmark"] == "Coding Agent Index v1.3"
    assert len(payload["charts"]["token"]) == EXPECTED_CODING_COUNTS["token"]
    assert len(payload["charts"]["api"]) == EXPECTED_CODING_COUNTS["api"]
    assert len(payload["charts"]["subscription"]) == EXPECTED_CODING_COUNTS["subscription"]
    assert sum(
        row["data_scope"] == "partial" for row in payload["charts"]["token"]
    ) == 1
    assert all(
        row["agent"] in row["model"] for row in payload["charts"]["token"]
    )

    manifest = json.loads(
        (root / "site" / "data" / "coding-agents.json").read_text("utf-8")
    )
    assert manifest["current"] == snapshot
    assert [entry["id"] for entry in manifest["snapshots"]] == [snapshot]
    assert manifest["snapshots"][0]["benchmark"] == "Coding Agent Index v1.3"

    chart_metrics = json.loads(
        (data_dir / "static_chart_metrics.json").read_text("utf-8")
    )
    assert len(chart_metrics) == 6
    assert all(metric["label_collisions"] == 0 for metric in chart_metrics)
    assert all(metric["out_of_bounds_labels"] == 0 for metric in chart_metrics)
    assert {(metric["metric"], metric["locale"]) for metric in chart_metrics} == {
        (metric, locale)
        for metric in ("token", "subscription", "api")
        for locale in ("en", "zh-CN")
    }


def validate_site_links(root: Path, snapshot: str) -> None:
    readme = (root / "README.md").read_text("utf-8")
    index_html = (root / "site" / "index.html").read_text("utf-8")
    app_js = (root / "site" / "assets" / "app.js").read_text("utf-8")
    interactive_js = (root / "site" / "assets" / "interactive-scatter.js").read_text(
        "utf-8"
    )
    deploy_workflow = (
        root / ".github" / "workflows" / "deploy-pages.yml"
    ).read_text("utf-8")
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
    assert "data/snapshots.json?v=${ASSET_REVISION}" in app_js
    assert "data/coding-agents.json?v=${ASSET_REVISION}" in app_js
    assert "metricChanged || dataChanged || !this.view" in interactive_js
    assert ASSET_REVISION in index_html
    assert ASSET_REVISION in app_js
    assert ASSET_REVISION in interactive_js
    assert 'searchParams.get("lang")' in app_js
    assert 'searchParams.get("snapshot")' in app_js
    assert 'searchParams.get("view")' in app_js
    assert '"coding-snapshot"' in app_js
    assert "window.history.replaceState" in app_js
    assert 'data-scenario="general"' in index_html
    assert 'data-scenario="coding"' in index_html
    assert 'id="coding-chart1-interactive"' in index_html
    assert 'id="coding-chart2-interactive"' in index_html
    assert 'id="coding-chart3-interactive"' in index_html
    assert "loadCodingSnapshotManifest" in app_js
    assert 'scopeMode: isCoding ? "field" : "frontier"' in app_js
    assert 'scopeField: isCoding ? "agent" : ""' in app_js
    assert "cp -R data/coding-agents/. _site/data/coding-agents/" in deploy_workflow

    assert "?lang=zh-CN" in readme
    assert "?lang=en" in readme
    assert "releases/latest" in readme
    assert "<details" not in readme
    assert "charts/en/" not in readme
    assert not (root / "site" / "assets" / "open-interactive-charts-button.svg").exists()

    sota_models = ("GPT-5.6 Sol", "Claude Opus 5", "Kimi K3")
    value_models = ("GPT-5.6 Luna", "DeepSeek V4 Pro (Preview)")
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
    validate_coding_agents(root, args.snapshot)
    validate_site_links(root, args.snapshot)
    print(
        "validated snapshot: "
        f"{args.snapshot}; 73 Token / 68 API / 46 subscription; "
        "64 bilingual current/archive chart assets; two dated payloads; "
        "UTC version metadata, recommendations, two scenario pages, and "
        "52 / 52 / 49 coding-agent charts"
    )


if __name__ == "__main__":
    main()
