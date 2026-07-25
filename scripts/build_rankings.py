from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable


SNAPSHOT = "2026-07-24"
SCORE_THRESHOLDS = (40, 45, 50, 55, 58, 60)
CORE_MIN_LEVELS = 4
CORE_MIN_SCORE_SPAN = 8.0
INTEGRATION_STEPS = 2000


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def interpolate(curve: list[tuple[float, float]], score: float) -> float:
    if score <= curve[0][0]:
        return curve[0][1]
    if score >= curve[-1][0]:
        return curve[-1][1]
    index = 1
    while index < len(curve) and score > curve[index][0]:
        index += 1
    left_score, left_value = curve[index - 1]
    right_score, right_value = curve[index]
    fraction = (score - left_score) / (right_score - left_score)
    return left_value + fraction * (right_value - left_value)


def unique_score_curve(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    best_by_score: dict[float, float] = {}
    for score, log_tokens in points:
        if score not in best_by_score or log_tokens < best_by_score[score]:
            best_by_score[score] = log_tokens
    return sorted(best_by_score.items())


def observed_frontier(
    rows: list[dict[str, str]],
) -> list[tuple[float, float]]:
    ordered = sorted(
        (
            (
                float(row["total_tokens_million"]),
                float(row["intelligence_score_raw"]),
            )
            for row in rows
        ),
        key=lambda point: (point[0], -point[1]),
    )
    frontier: list[tuple[float, float]] = []
    best_score = float("-inf")
    for tokens, score in ordered:
        if score <= best_score:
            continue
        frontier.append((score, math.log(tokens)))
        best_score = score
    return sorted(frontier)


def aggregate_token_efficiency(
    model_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    frontier = observed_frontier(model_rows)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in model_rows:
        grouped[row["model"]].append(row)

    ranked: list[dict[str, object]] = []
    for model, rows in grouped.items():
        if len(rows) < 2:
            continue
        curve = unique_score_curve(
            [
                (
                    float(row["intelligence_score_raw"]),
                    math.log(float(row["total_tokens_million"])),
                )
                for row in rows
            ]
        )
        if len(curve) < 2:
            continue
        score_min = curve[0][0]
        score_max = curve[-1][0]
        score_span = score_max - score_min
        if score_span <= 0:
            continue

        log_overheads: list[float] = []
        index = 0
        while index <= INTEGRATION_STEPS:
            score = score_min + score_span * index / INTEGRATION_STEPS
            model_log_tokens = interpolate(curve, score)
            frontier_log_tokens = interpolate(frontier, score)
            # A model segment can fall below the straight interpolation of the
            # observed point frontier.  In that interval the model itself is
            # part of the lower envelope, so its overhead is exactly 1.
            log_overheads.append(max(0.0, model_log_tokens - frontier_log_tokens))
            index += 1

        mean_log_overhead = (
            sum(log_overheads)
            - 0.5 * log_overheads[0]
            - 0.5 * log_overheads[-1]
        ) / INTEGRATION_STEPS
        token_overhead = math.exp(mean_log_overhead)
        efficiency_index = 100.0 / token_overhead
        category = (
            "core"
            if len(curve) >= CORE_MIN_LEVELS and score_span >= CORE_MIN_SCORE_SPAN
            else "limited"
        )
        ranked.append(
            {
                "rank": 0,
                "category": category,
                "model": model,
                "levels": len(curve),
                "score_min": round(score_min, 4),
                "score_max": round(score_max, 4),
                "score_span": round(score_span, 4),
                "efficiency_index": round(efficiency_index, 2),
                "token_overhead_vs_frontier": round(token_overhead, 4),
            }
        )

    core = sorted(
        (row for row in ranked if row["category"] == "core"),
        key=lambda row: (-float(row["efficiency_index"]), str(row["model"])),
    )
    limited = sorted(
        (row for row in ranked if row["category"] == "limited"),
        key=lambda row: (-float(row["efficiency_index"]), str(row["model"])),
    )
    for category_rows in (core, limited):
        for rank, row in enumerate(category_rows, start=1):
            row["rank"] = rank
    return core, limited


def api_cost_ranking(model_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    eligible = [row for row in model_rows if row["cost_per_index_task_usd"]]
    eligible.sort(
        key=lambda row: (
            float(row["cost_per_index_task_usd"]),
            -float(row["intelligence_score_raw"]),
            row["model"],
            row["effort"],
        )
    )
    result: list[dict[str, object]] = []
    for rank, row in enumerate(eligible, start=1):
        result.append(
            {
                "rank": rank,
                "model": row["model"],
                "effort": row["effort"],
                "score": round(float(row["intelligence_score_raw"]), 4),
                "cost_usd_per_task": round(float(row["cost_per_index_task_usd"]), 9),
                "total_tokens_million": round(float(row["total_tokens_million"]), 6),
                "provider": row["api_provider"],
                "provider_model_id": row["api_provider_model_id"],
                "precision": row["api_precision"],
            }
        )
    return result


def subscription_cost_ranking(
    access_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    ordered = sorted(
        access_rows,
        key=lambda row: (
            float(row["effective_cost_per_task_usd"]),
            -float(row["intelligence_score_raw"]),
            row["model"],
            row["effort"],
        ),
    )
    result: list[dict[str, object]] = []
    for rank, row in enumerate(ordered, start=1):
        plan_price = (
            round(float(row["plan_price_usd_per_month"]), 4)
            if row["plan_price_usd_per_month"]
            else None
        )
        result.append(
            {
                "rank": rank,
                "model": row["model"],
                "effort": row["effort"],
                "score": round(float(row["intelligence_score_raw"]), 4),
                "cost_usd_per_task": round(float(row["effective_cost_per_task_usd"]), 9),
                "api_cost_usd_per_task": round(float(row["api_cost_per_task_usd"]), 9),
                "access_mode": row["access_mode"],
                "quota_scenario": row["quota_scenario"],
                "plan_name": row["plan_name"],
                "plan_price_usd_per_month": plan_price,
                "provider": row["provider"],
                "confidence": row["confidence"],
            }
        )
    return result


def token_chart_rows(model_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for row in model_rows:
        result.append(
            {
                "model": row["model"],
                "effort": row["effort"],
                "effort_order": int(row["effort_order"]),
                "score": round(float(row["intelligence_score_raw"]), 4),
                "total_tokens_million": round(
                    float(row["total_tokens_million"]), 6
                ),
                "developer": row["developer"],
                "country_code": row["country_code"],
                "data_scope": row["data_scope"],
                "is_historical": row["is_historical"].lower() == "true",
            }
        )
    return result


def api_chart_rows(model_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for row in model_rows:
        if not row["cost_per_index_task_usd"]:
            continue
        result.append(
            {
                "model": row["model"],
                "effort": row["effort"],
                "effort_order": int(row["effort_order"]),
                "score": round(float(row["intelligence_score_raw"]), 4),
                "cost_usd_per_task": round(
                    float(row["cost_per_index_task_usd"]), 9
                ),
                "total_tokens_million": round(
                    float(row["total_tokens_million"]), 6
                ),
                "developer": row["developer"],
                "country_code": row["country_code"],
                "provider": row["api_provider"],
                "precision": row["api_precision"],
                "is_historical": row["is_historical"].lower() == "true",
            }
        )
    return result


def subscription_chart_rows(
    access_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for row in access_rows:
        result.append(
            {
                "model": row["model"],
                "effort": row["effort"],
                "effort_order": int(row["effort_order"]),
                "score": round(float(row["intelligence_score_raw"]), 4),
                "cost_usd_per_task": round(
                    float(row["effective_cost_per_task_usd"]), 9
                ),
                "developer": row["developer"],
                "country_code": row["country_code"],
                "access_mode": row["access_mode"],
                "plan_name": row["plan_name"],
                "provider": row["provider"],
                "confidence": row["confidence"],
                "is_historical": row["is_historical"].lower() == "true",
            }
        )
    return result


def threshold_leaders(
    rows: list[dict[str, object]],
    metric: str,
) -> list[dict[str, object]]:
    leaders: list[dict[str, object]] = []
    for threshold in SCORE_THRESHOLDS:
        eligible = [row for row in rows if float(row["score"]) >= threshold]
        if not eligible:
            continue
        best = min(
            eligible,
            key=lambda row: (
                float(row["cost_usd_per_task"]),
                -float(row["score"]),
            ),
        )
        leaders.append(
            {
                "metric": metric,
                "score_threshold": threshold,
                "model": best["model"],
                "effort": best["effort"],
                "score": best["score"],
                "cost_usd_per_task": best["cost_usd_per_task"],
                "provider": best["provider"],
                "access_mode": best.get("access_mode", "api"),
                "plan_name": best.get("plan_name", ""),
                "confidence": best.get("confidence", ""),
            }
        )
    return leaders


def parse_args() -> argparse.Namespace:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Build numerical rankings from one dated chart-data snapshot."
    )
    parser.add_argument(
        "--snapshot",
        default=SNAPSHOT,
        help="Snapshot directory and output version in YYYY-MM-DD form.",
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=repository_root,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = args.repository_root / "data" / args.snapshot
    model_rows = read_csv(data_dir / "model_efficiency.csv")
    access_rows = read_csv(data_dir / "subscription_first_task_cost.csv")
    if len(model_rows) != 73:
        raise ValueError(f"Expected 73 model configurations, found {len(model_rows)}")
    if len(access_rows) != 46:
        raise ValueError(
            f"Expected 46 subscription-first configurations, found {len(access_rows)}"
        )

    token_core, token_limited = aggregate_token_efficiency(model_rows)
    api_ranking = api_cost_ranking(model_rows)
    subscription_ranking = subscription_cost_ranking(access_rows)
    api_thresholds = threshold_leaders(api_ranking, "api")
    subscription_thresholds = threshold_leaders(
        subscription_ranking, "subscription_first"
    )
    token_chart = token_chart_rows(model_rows)
    api_chart = api_chart_rows(model_rows)
    subscription_chart = subscription_chart_rows(access_rows)
    if len(token_chart) != 73:
        raise ValueError(f"Expected 73 Token chart points, found {len(token_chart)}")
    if len(api_chart) != 68:
        raise ValueError(f"Expected 68 API chart points, found {len(api_chart)}")
    if len(subscription_chart) != 46:
        raise ValueError(
            "Expected 46 subscription chart points, "
            f"found {len(subscription_chart)}"
        )

    rankings_dir = args.repository_root / "rankings" / args.snapshot
    token_rows = token_core + token_limited
    write_csv(
        rankings_dir / "token_efficiency_ranking.csv",
        token_rows,
        (
            "rank",
            "category",
            "model",
            "levels",
            "score_min",
            "score_max",
            "score_span",
            "efficiency_index",
            "token_overhead_vs_frontier",
        ),
    )
    write_csv(
        rankings_dir / "api_cost_ranking.csv",
        api_ranking,
        (
            "rank",
            "model",
            "effort",
            "score",
            "cost_usd_per_task",
            "total_tokens_million",
            "provider",
            "provider_model_id",
            "precision",
        ),
    )
    write_csv(
        rankings_dir / "subscription_cost_ranking.csv",
        subscription_ranking,
        (
            "rank",
            "model",
            "effort",
            "score",
            "cost_usd_per_task",
            "api_cost_usd_per_task",
            "access_mode",
            "quota_scenario",
            "plan_name",
            "plan_price_usd_per_month",
            "provider",
            "confidence",
        ),
    )
    threshold_rows = api_thresholds + subscription_thresholds
    write_csv(
        rankings_dir / "score_threshold_leaders.csv",
        threshold_rows,
        (
            "metric",
            "score_threshold",
            "model",
            "effort",
            "score",
            "cost_usd_per_task",
            "provider",
            "access_mode",
            "plan_name",
            "confidence",
        ),
    )

    payload = {
        "snapshot": args.snapshot,
        "counts": {
            "token_configurations": len(model_rows),
            "api_cost_configurations": len(api_ranking),
            "subscription_first_configurations": len(subscription_ranking),
            "token_core_models": len(token_core),
            "token_limited_models": len(token_limited),
        },
        "method": {
            "token_efficiency_index": (
                "100 divided by the score-range-weighted geometric mean Token "
                "overhead versus the observed global Token frontier"
            ),
            "core_min_levels": CORE_MIN_LEVELS,
            "core_min_score_span": CORE_MIN_SCORE_SPAN,
            "score_thresholds": list(SCORE_THRESHOLDS),
        },
        "token_efficiency": {
            "core": token_core,
            "limited": token_limited,
        },
        "api_cost": api_ranking,
        "subscription_cost": subscription_ranking,
        "charts": {
            "token": token_chart,
            "api": api_chart,
            "subscription": subscription_chart,
        },
        "thresholds": {
            "api": api_thresholds,
            "subscription_first": subscription_thresholds,
        },
    }
    atomic_text(
        args.repository_root / "site" / "data" / "rankings.json",
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
    )
    print(
        "built rankings: "
        f"token={len(token_core)} core/{len(token_limited)} limited, "
        f"api={len(api_ranking)}, subscription={len(subscription_ranking)}, "
        f"thresholds={len(threshold_rows)}"
    )


if __name__ == "__main__":
    main()
