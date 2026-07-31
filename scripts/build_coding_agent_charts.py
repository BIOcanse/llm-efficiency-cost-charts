from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.text import Text
from matplotlib.transforms import Bbox


EXPECTED_SOURCE_ROWS = 52
EXPECTED_SUBSCRIPTION_ROWS = 49
EXPECTED_COMPLETE_ROWS = 51
EXPECTED_PARTIAL_ROWS = 1
BENCHMARK = "Coding Agent Index v1.3"
PALETTE = (
    "#2563eb",
    "#dc2626",
    "#7c3aed",
    "#059669",
    "#d97706",
    "#db2777",
    "#0891b2",
    "#4f46e5",
    "#65a30d",
    "#ea580c",
    "#0f766e",
    "#9333ea",
    "#0284c7",
    "#be123c",
    "#15803d",
    "#b45309",
    "#0369a1",
    "#6d28d9",
    "#c2410c",
    "#047857",
    "#1d4ed8",
    "#9f1239",
    "#5b21b6",
    "#0e7490",
    "#3f6212",
    "#a21caf",
    "#b91c1c",
    "#166534",
    "#4338ca",
    "#a16207",
    "#0f766e",
    "#9d174d",
)
AGENT_MARKERS = {
    "Codex": "o",
    "Claude Code": "^",
    "Cursor CLI": "s",
    "Gemini CLI": "D",
    "Grok Build": "P",
    "Kimi Code CLI": "X",
    "Opencode": "h",
}
EFFORT_LABELS = {
    "en": {
        "non-reasoning": "none",
        "default": "default",
        "fast": "fast",
        "low": "low",
        "medium": "medium",
        "thinking": "thinking",
        "high": "high",
        "xhigh": "xhigh",
        "max": "max",
    },
    "zh-CN": {
        "non-reasoning": "非推理",
        "default": "默认",
        "fast": "快速",
        "low": "低",
        "medium": "中",
        "thinking": "思考",
        "high": "高",
        "xhigh": "超高",
        "max": "Max",
    },
}


@dataclass(frozen=True)
class MetricSpec:
    key: str
    x_key: str
    stem: str
    title_en: str
    title_zh: str
    x_label_en: str
    x_label_zh: str
    source_rows: str


METRICS = (
    MetricSpec(
        key="token",
        x_key="total_tokens_million",
        stem="07_coding_agent_total_tokens_vs_index",
        title_en="Coding agents: Token consumption vs. task success — upper left is better",
        title_zh="实际编码 Agent：Token 消耗与任务通过表现（左上更好）",
        x_label_en="Average total Tokens per coding task (millions, lower is better)",
        x_label_zh="平均每个编码任务的总 Token 消耗（百万，越低越好）",
        source_rows="results",
    ),
    MetricSpec(
        key="subscription",
        x_key="cost_usd_per_task",
        stem="08_coding_agent_subscription_cost_vs_index",
        title_en="Coding agents: subscription-first task cost vs. task success — upper left is better",
        title_zh="实际编码 Agent：套餐优先单任务成本与任务通过表现（左上更好）",
        x_label_en="Subscription-first effective cost per coding task (USD, lower is better)",
        x_label_zh="套餐优先折算单任务成本（美元，越低越好）",
        source_rows="subscription",
    ),
    MetricSpec(
        key="api",
        x_key="cost_usd_per_task",
        stem="09_coding_agent_api_cost_vs_index",
        title_en="Coding agents: API task cost vs. task success — upper left is better",
        title_zh="实际编码 Agent：API 单任务成本与任务通过表现（左上更好）",
        x_label_en="Observed pay-per-token API cost per coding task (USD, lower is better)",
        x_label_zh="按量 API 单任务成本（美元，越低越好）",
        source_rows="results",
    ),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def match_rule(row: dict[str, str], rule: dict[str, str]) -> bool:
    return (
        fnmatch.fnmatchcase(row["agent"], rule["agent"])
        and fnmatch.fnmatchcase(row["model_creator"], rule["model_creator"])
        and fnmatch.fnmatchcase(row["model"], rule["model_pattern"])
    )


def decimal_text(value: Decimal, places: int = 12) -> str:
    text = f"{value:.{places}f}".rstrip("0").rstrip(".")
    return text if text else "0"


def build_subscription_rows(
    results: list[dict[str, str]],
    policies: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    ordered_policies = sorted(policies, key=lambda row: int(row["rule_order"]))
    included: list[dict[str, object]] = []
    excluded: list[dict[str, object]] = []
    for result in results:
        matches = [rule for rule in ordered_policies if match_rule(result, rule)]
        if not matches:
            raise ValueError(f"No subscription policy matches {result['source_display_label']}")
        selected = matches[0]
        same_priority = [
            rule
            for rule in matches
            if int(rule["rule_order"]) == int(selected["rule_order"])
        ]
        if len(same_priority) != 1:
            raise ValueError(
                f"Ambiguous subscription policy for {result['source_display_label']}"
            )
        decision = selected["decision"]
        shared = {
            "result_id": result["result_id"],
            "series": result["series"],
            "agent": result["agent"],
            "model": result["model"],
            "effort": result["effort"],
            "effort_order": result["effort_order"],
            "developer": result["model_creator"],
            "coding_agent_score": result["coding_agent_score"],
            "data_scope": result["data_scope"],
            "api_cost_per_task_usd": result["cost_usd_per_task"],
            "route_provider": result["route_provider"],
            "host_model_slug": result["host_model_slug"],
            "policy_rule_order": selected["rule_order"],
            "decision": decision,
            "confidence": selected["confidence"],
            "plan_source_url": selected["plan_source_url"],
            "quota_source_url": selected["quota_source_url"],
            "reason": selected["reason"],
        }
        if decision.startswith("exclude_"):
            excluded.append(shared)
            continue
        ratio_text = selected["api_value_ratio"].strip()
        if not ratio_text:
            raise ValueError(
                f"Included policy has no API-value ratio: {selected['rule_order']}"
            )
        ratio = Decimal(ratio_text)
        if ratio <= 0:
            raise ValueError(f"Invalid API-value ratio: {ratio}")
        api_cost = Decimal(result["cost_usd_per_task"])
        effective_cost = api_cost / ratio
        access_provider = selected["access_provider"]
        if access_provider == "source_route":
            access_provider = result["route_provider"]
        included.append(
            {
                **shared,
                "effective_cost_per_task_usd": decimal_text(effective_cost),
                "access_mode": selected["access_mode"],
                "plan_name": selected["plan_name"],
                "plan_price_usd_per_month": selected[
                    "plan_price_usd_per_month"
                ],
                "quota_period": selected["quota_period"],
                "api_value_ratio": decimal_text(ratio),
                "access_provider": access_provider,
            }
        )
    return included, excluded


def pareto_ids(rows: list[dict[str, object]], x_key: str) -> set[str]:
    ordered = sorted(
        (
            row
            for row in rows
            if row.get("data_scope") != "partial"
        ),
        key=lambda row: (float(row[x_key]), -float(row["score"])),
    )
    frontier: set[str] = set()
    best_score = float("-inf")
    for row in ordered:
        score = float(row["score"])
        if score <= best_score:
            continue
        frontier.add(str(row["id"]))
        best_score = score
    return frontier


def result_chart_rows(results: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in results:
        rows.append(
            {
                "id": row["result_id"],
                "model": row["series"],
                "base_model": row["model"],
                "agent": row["agent"],
                "effort": row["effort"],
                "effort_order": int(row["effort_order"]),
                "score": round(float(row["coding_agent_score"]), 6),
                "total_tokens_million": round(
                    float(row["total_tokens_million"]), 6
                ),
                "cost_usd_per_task": round(
                    float(row["cost_usd_per_task"]), 12
                ),
                "agent_wall_time_sec": round(
                    float(row["agent_wall_time_sec"]), 6
                ),
                "steps_per_task": round(float(row["steps_per_task"]), 6),
                "developer": row["model_creator"],
                "agent_creator": row["agent_creator"],
                "provider": row["route_provider"],
                "host_model_slug": row["host_model_slug"],
                "data_scope": row["data_scope"],
                "eval_count": int(row["eval_count"]),
            }
        )
    return rows


def subscription_chart_rows(
    subscription_rows: list[dict[str, object]],
    result_by_id: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in subscription_rows:
        source = result_by_id[str(row["result_id"])]
        rows.append(
            {
                "id": row["result_id"],
                "model": row["series"],
                "base_model": row["model"],
                "agent": row["agent"],
                "effort": row["effort"],
                "effort_order": int(str(row["effort_order"])),
                "score": round(float(str(row["coding_agent_score"])), 6),
                "cost_usd_per_task": round(
                    float(str(row["effective_cost_per_task_usd"])), 12
                ),
                "api_cost_usd_per_task": round(
                    float(str(row["api_cost_per_task_usd"])), 12
                ),
                "total_tokens_million": round(
                    float(source["total_tokens_million"]), 6
                ),
                "agent_wall_time_sec": round(
                    float(source["agent_wall_time_sec"]), 6
                ),
                "steps_per_task": round(float(source["steps_per_task"]), 6),
                "developer": row["developer"],
                "agent_creator": source["agent_creator"],
                "provider": row["access_provider"],
                "route_provider": row["route_provider"],
                "host_model_slug": row["host_model_slug"],
                "access_mode": row["access_mode"],
                "plan_name": row["plan_name"],
                "api_value_ratio": float(str(row["api_value_ratio"])),
                "confidence": row["confidence"],
                "data_scope": row["data_scope"],
                "eval_count": int(source["eval_count"]),
            }
        )
    return rows


def assign_series_colors(rows: list[dict[str, object]]) -> dict[str, str]:
    series = sorted({str(row["model"]) for row in rows})
    return {
        name: PALETTE[index % len(PALETTE)]
        for index, name in enumerate(series)
    }


def darker(color: str, factor: float = 0.78) -> tuple[float, float, float]:
    red, green, blue = mcolors.to_rgb(color)
    return red * factor, green * factor, blue * factor


def padded(box: Bbox, amount: float) -> Bbox:
    return Bbox.from_extents(
        box.x0 - amount,
        box.y0 - amount,
        box.x1 + amount,
        box.y1 + amount,
    )


def text_box(
    anchor_x: float,
    anchor_y: float,
    width: float,
    height: float,
    horizontal: str,
    vertical: str,
) -> Bbox:
    if horizontal == "left":
        x0, x1 = anchor_x, anchor_x + width
    elif horizontal == "right":
        x0, x1 = anchor_x - width, anchor_x
    else:
        x0, x1 = anchor_x - width / 2, anchor_x + width / 2
    if vertical == "bottom":
        y0, y1 = anchor_y, anchor_y + height
    elif vertical == "top":
        y0, y1 = anchor_y - height, anchor_y
    else:
        y0, y1 = anchor_y - height / 2, anchor_y + height / 2
    return Bbox.from_extents(x0, y0, x1, y1)


def candidate_offsets() -> list[tuple[float, float]]:
    candidates = [
        (7, 7),
        (7, -7),
        (-7, 7),
        (-7, -7),
        (10, 0),
        (-10, 0),
        (0, 10),
        (0, -10),
    ]
    for radius in (15, 22, 31, 43, 58, 76, 98):
        candidates.extend(
            [
                (radius, 0),
                (-radius, 0),
                (radius, radius * 0.55),
                (radius, -radius * 0.55),
                (-radius, radius * 0.55),
                (-radius, -radius * 0.55),
                (radius * 0.35, radius),
                (-radius * 0.35, radius),
                (radius * 0.35, -radius),
                (-radius * 0.35, -radius),
            ]
        )
    return candidates


def offset_alignment(dx_points: float, dy_points: float) -> tuple[str, str]:
    horizontal = (
        "left" if dx_points > 1 else "right" if dx_points < -1 else "center"
    )
    vertical = (
        "bottom" if dy_points > 1 else "top" if dy_points < -1 else "center"
    )
    return horizontal, vertical


def place_labels(
    ax: plt.Axes,
    rows: list[dict[str, object]],
    metric: MetricSpec,
    colors: dict[str, str],
    language: str,
    font_properties: FontProperties,
) -> tuple[list[plt.Annotation], dict[str, int]]:
    figure = ax.figure
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    axes_box = padded(ax.get_window_extent(renderer), -5)
    point_pixels = {
        str(row["id"]): ax.transData.transform(
            (float(row[metric.x_key]), float(row["score"]))
        )
        for row in rows
    }
    point_boxes = {
        result_id: Bbox.from_extents(x - 9, y - 9, x + 9, y + 9)
        for result_id, (x, y) in point_pixels.items()
    }
    density: dict[str, int] = {}
    for result_id, (point_x, point_y) in point_pixels.items():
        density[result_id] = sum(
            1
            for other_id, (other_x, other_y) in point_pixels.items()
            if other_id != result_id
            and (point_x - other_x) ** 2 + (point_y - other_y) ** 2 < 170**2
        )
    ordered = sorted(
        rows,
        key=lambda row: (
            -density[str(row["id"])],
            -float(row["score"]),
            str(row["model"]),
        ),
    )
    placed_boxes: list[Bbox] = []
    annotations: list[plt.Annotation] = []
    forced = 0
    points_per_unit = figure.dpi / 72
    offsets = candidate_offsets()

    for row in ordered:
        result_id = str(row["id"])
        partial = "†" if row.get("data_scope") == "partial" else ""
        effort = EFFORT_LABELS[language].get(
            str(row["effort"]), str(row["effort"])
        )
        label = (
            f"{partial}{row['model']} · {effort} · {float(row['score']):.0f}"
        )
        width, height, descent = renderer.get_text_width_height_descent(
            label,
            font_properties,
            ismath=False,
        )
        # Matplotlib's raster and SVG text extents differ slightly on Windows.
        # Reserve a small deterministic margin so the exported formats keep the
        # same non-overlapping placement.
        width *= 1.15
        height = (height + descent) * 1.12
        point_x, point_y = point_pixels[result_id]
        best: tuple[float, float, str, str, Bbox, float] | None = None
        for dx_points, dy_points in offsets:
            dx = dx_points * points_per_unit
            dy = dy_points * points_per_unit
            horizontal, vertical = offset_alignment(dx_points, dy_points)
            box = text_box(
                point_x + dx,
                point_y + dy,
                width,
                height,
                horizontal,
                vertical,
            )
            out_of_bounds = (
                max(0.0, axes_box.x0 - box.x0)
                + max(0.0, box.x1 - axes_box.x1)
                + max(0.0, axes_box.y0 - box.y0)
                + max(0.0, box.y1 - axes_box.y1)
            )
            label_overlaps = sum(
                padded(box, 2).overlaps(existing) for existing in placed_boxes
            )
            point_overlaps = sum(
                padded(box, 1).overlaps(other_box)
                for other_id, other_box in point_boxes.items()
                if other_id != result_id
            )
            distance = math.hypot(dx_points, dy_points)
            penalty = (
                out_of_bounds * 5_000
                + label_overlaps * 1_000_000
                + point_overlaps * 250_000
                + distance
            )
            candidate = (
                dx_points,
                dy_points,
                horizontal,
                vertical,
                box,
                penalty,
            )
            if best is None or penalty < best[5]:
                best = candidate
            if out_of_bounds == 0 and label_overlaps == 0 and point_overlaps == 0:
                best = candidate
                break
        if best is None:
            raise RuntimeError(f"No label candidate generated for {label}")
        dx_points, dy_points, horizontal, vertical, box, penalty = best
        if penalty >= 250_000:
            forced += 1
        annotation = ax.annotate(
            label,
            xy=(float(row[metric.x_key]), float(row["score"])),
            xytext=(dx_points, dy_points),
            textcoords="offset points",
            ha=horizontal,
            va=vertical,
            color=darker(colors[str(row["model"])]),
            fontproperties=font_properties,
            zorder=8,
            arrowprops=(
                {
                    "arrowstyle": "-",
                    "color": mcolors.to_rgba(colors[str(row["model"])], 0.45),
                    "linewidth": 0.6,
                    "shrinkA": 2,
                    "shrinkB": 5,
                }
                if math.hypot(dx_points, dy_points) >= 28
                else None
            ),
        )
        annotations.append(annotation)
        placed_boxes.append(padded(box, 2))

    figure.canvas.draw()

    def annotation_boxes() -> list[Bbox]:
        # Annotation.get_window_extent includes its optional leader line.
        # Collision metrics must measure the glyph box itself.
        return [
            Text.get_window_extent(annotation, renderer=renderer)
            for annotation in annotations
        ]

    actual_boxes = annotation_boxes()
    repairs = 0
    repair_round = 0
    while repair_round < 20:
        collision: tuple[int, int] | None = None
        left_index = 0
        while left_index < len(actual_boxes) and collision is None:
            right_index = left_index + 1
            while right_index < len(actual_boxes):
                if padded(actual_boxes[left_index], 1).overlaps(
                    padded(actual_boxes[right_index], 1)
                ):
                    collision = (left_index, right_index)
                    break
                right_index += 1
            left_index += 1
        if collision is None:
            break

        moved = False
        for target_index in (collision[1], collision[0]):
            annotation = annotations[target_index]
            own_id = str(ordered[target_index]["id"])
            old_dx, old_dy = annotation.get_position()
            horizontal = annotation.get_ha()
            vertical = annotation.get_va()
            current_box = actual_boxes[target_index]
            for next_dx, next_dy in offsets:
                if (next_dx, next_dy) == (old_dx, old_dy):
                    continue
                if offset_alignment(next_dx, next_dy) != (horizontal, vertical):
                    continue
                translated = Bbox.from_extents(
                    current_box.x0 + (next_dx - old_dx) * points_per_unit,
                    current_box.y0 + (next_dy - old_dy) * points_per_unit,
                    current_box.x1 + (next_dx - old_dx) * points_per_unit,
                    current_box.y1 + (next_dy - old_dy) * points_per_unit,
                )
                if (
                    translated.x0 < axes_box.x0
                    or translated.x1 > axes_box.x1
                    or translated.y0 < axes_box.y0
                    or translated.y1 > axes_box.y1
                ):
                    continue
                if any(
                    padded(translated, 2).overlaps(other_box)
                    for index, other_box in enumerate(actual_boxes)
                    if index != target_index
                ):
                    continue
                if any(
                    padded(translated, 1).overlaps(point_box)
                    for other_id, point_box in point_boxes.items()
                    if other_id != own_id
                ):
                    continue
                annotation.set_position((next_dx, next_dy))
                moved = True
                repairs += 1
                break
            if moved:
                break
        if not moved:
            break
        figure.canvas.draw()
        actual_boxes = annotation_boxes()
        repair_round += 1

    label_collisions = 0
    collision_pairs: list[list[str]] = []
    left_index = 0
    while left_index < len(actual_boxes):
        right_index = left_index + 1
        while right_index < len(actual_boxes):
            if padded(actual_boxes[left_index], 1).overlaps(
                padded(actual_boxes[right_index], 1)
            ):
                label_collisions += 1
                collision_pairs.append(
                    [
                        annotations[left_index].get_text(),
                        annotations[right_index].get_text(),
                    ]
                )
            right_index += 1
        left_index += 1
    out_of_bounds = sum(
        box.x0 < axes_box.x0
        or box.x1 > axes_box.x1
        or box.y0 < axes_box.y0
        or box.y1 > axes_box.y1
        for box in actual_boxes
    )
    return annotations, {
        "label_collisions": int(label_collisions),
        "out_of_bounds_labels": int(out_of_bounds),
        "forced_placements": int(forced),
        "repair_moves": repairs,
        "collision_pairs": collision_pairs,
    }


def render_static_chart(
    rows: list[dict[str, object]],
    metric: MetricSpec,
    language: str,
    snapshot: str,
    output_dir: Path,
) -> dict[str, object]:
    if not rows:
        raise ValueError(f"No rows for {metric.key}")
    matplotlib.rcParams.update(
        {
            "font.family": ["Microsoft YaHei", "Segoe UI", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "svg.fonttype": "none",
        }
    )
    figure = plt.figure(figsize=(24, 13.5), dpi=200, facecolor="#fbfbfa")
    ax = figure.add_axes((0.055, 0.14, 0.79, 0.75), facecolor="#fbfbfa")
    ax.grid(True, color="#d8dee9", linewidth=0.65, alpha=0.72)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9aa7b8")
    ax.tick_params(colors="#586579", labelsize=10)

    colors = assign_series_colors(rows)
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["model"])].append(row)
    for series, series_rows in grouped.items():
        ordered = sorted(series_rows, key=lambda row: int(row["effort_order"]))
        if len(ordered) > 1:
            ax.plot(
                [float(row[metric.x_key]) for row in ordered],
                [float(row["score"]) for row in ordered],
                color=colors[series],
                linewidth=1.45,
                alpha=0.78,
                zorder=2,
            )

    frontier = pareto_ids(rows, metric.x_key)
    for row in rows:
        result_id = str(row["id"])
        partial = row.get("data_scope") == "partial"
        ax.scatter(
            [float(row[metric.x_key])],
            [float(row["score"])],
            s=56 if not partial else 66,
            marker=AGENT_MARKERS.get(str(row["agent"]), "o"),
            facecolor="#fbfbfa" if partial else colors[str(row["model"])],
            edgecolor="#172033" if result_id in frontier else colors[str(row["model"])],
            linewidth=1.8 if result_id in frontier else 1.2,
            alpha=0.96,
            zorder=6,
        )

    x_values = [float(row[metric.x_key]) for row in rows]
    y_values = [float(row["score"]) for row in rows]
    ax.set_xlim(0, max(x_values) * 1.055)
    ax.set_ylim(max(0, min(y_values) - 3), min(100, max(y_values) + 3))
    ax.set_xlabel(
        metric.x_label_zh if language == "zh-CN" else metric.x_label_en,
        fontsize=12,
        color="#172033",
        labelpad=16,
        weight="bold",
    )
    ax.set_ylabel(
        "Coding Agent Index v1.3（越高越好）"
        if language == "zh-CN"
        else "Coding Agent Index v1.3 (higher is better)",
        fontsize=12,
        color="#172033",
        labelpad=14,
        weight="bold",
    )

    title = metric.title_zh if language == "zh-CN" else metric.title_en
    figure.text(0.055, 0.95, title, fontsize=23, weight="bold", color="#111827")
    subtitle = (
        f"Artificial Analysis Coding Agent Index v1.3｜每个点 = Agent 工具链 × 模型 × 档位｜{len(rows)} 个配置"
        if language == "zh-CN"
        else f"Artificial Analysis Coding Agent Index v1.3 | Point = agent harness × model × setting | {len(rows)} configurations"
    )
    figure.text(0.055, 0.915, subtitle, fontsize=10.5, color="#586579")

    font_name = font_manager.findfont(
        FontProperties(family=["Microsoft YaHei", "Segoe UI", "DejaVu Sans"])
    )
    label_font = FontProperties(fname=font_name, size=6.15, weight="bold")
    _annotations, metrics = place_labels(
        ax,
        rows,
        metric,
        colors,
        language,
        label_font,
    )

    side_x = 0.865
    figure.text(
        side_x,
        0.86,
        "怎么看" if language == "zh-CN" else "How to read",
        fontsize=12,
        weight="bold",
        color="#172033",
    )
    read_lines = (
        [
            "↑ 分数更高",
            "← 消耗或成本更低",
            "",
            "同色线：",
            "同一 Agent＋模型的不同档位",
            "",
            "黑色描边：Pareto 前沿",
            "†：仅有 2/3 项子评测",
        ]
        if language == "zh-CN"
        else [
            "↑ Higher score",
            "← Lower consumption or cost",
            "",
            "Same-color line:",
            "settings of one agent + model",
            "",
            "Black outline: Pareto frontier",
            "†: only 2/3 components available",
        ]
    )
    figure.text(
        side_x,
        0.825,
        "\n".join(read_lines),
        fontsize=9.2,
        linespacing=1.55,
        color="#344054",
        va="top",
    )

    figure.text(
        side_x,
        0.55,
        "Agent 标记" if language == "zh-CN" else "Agent markers",
        fontsize=11,
        weight="bold",
        color="#172033",
    )
    marker_y = 0.515
    for agent in sorted({str(row["agent"]) for row in rows}):
        figure.text(side_x, marker_y, AGENT_MARKERS.get(agent, "o"), fontsize=10, color="#344054")
        figure.text(side_x + 0.018, marker_y, agent, fontsize=8.5, color="#586579")
        marker_y -= 0.032

    source_text = (
        "来源：[1] artificialanalysis.ai/agents/coding-agents  [2] artificialanalysis.ai/methodology/coding-agents-benchmarking"
        if language == "zh-CN"
        else "Sources: [1] artificialanalysis.ai/agents/coding-agents  [2] artificialanalysis.ai/methodology/coding-agents-benchmarking"
    )
    figure.text(0.055, 0.055, source_text, fontsize=8.4, color="#667085")
    caveat = (
        f"快照：{snapshot}｜线性坐标从 0 开始｜结果属于 Agent 工具链＋模型＋档位，不是纯模型能力｜† Opus 4.6 medium 为两项子评测"
        if language == "zh-CN"
        else f"Snapshot: {snapshot} | Linear X axis starts at zero | Agent + model + setting result, not model-only ability | † Opus 4.6 medium has two components"
    )
    figure.text(0.055, 0.027, caveat, fontsize=8.2, color="#667085")

    output_dir.mkdir(parents=True, exist_ok=True)
    png_path = output_dir / f"{metric.stem}.png"
    svg_path = output_dir / f"{metric.stem}.svg"
    figure.savefig(png_path, dpi=200, facecolor=figure.get_facecolor())
    figure.savefig(svg_path, facecolor=figure.get_facecolor())
    plt.close(figure)
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        re.sub(r"[ \t]+(?=\r?$)", "", svg_text, flags=re.MULTILINE),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "metric": metric.key,
        "locale": language,
        "points": len(rows),
        "series": len(grouped),
        "frontier_points": len(frontier),
        **metrics,
        "png": str(png_path),
        "svg": str(svg_path),
    }


def parse_args() -> argparse.Namespace:
    repository_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Build Coding Agent Index static charts and site payload."
    )
    parser.add_argument("--snapshot", default="2026-07-31")
    parser.add_argument("--repository-root", type=Path, default=repository_root)
    parser.add_argument(
        "--skip-static",
        action="store_true",
        help="Build data outputs without rendering PNG/SVG files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = args.repository_root / "data" / "coding-agents" / args.snapshot
    results = read_csv(data_dir / "coding_agent_results.csv")
    policies = read_csv(data_dir / "subscription_access_policy.csv")
    metadata = json.loads((data_dir / "source_metadata.json").read_text("utf-8"))
    if len(results) != EXPECTED_SOURCE_ROWS:
        raise ValueError(f"Expected 52 source rows, found {len(results)}")
    scopes = Counter(row["data_scope"] for row in results)
    if scopes != Counter(
        {"complete": EXPECTED_COMPLETE_ROWS, "partial": EXPECTED_PARTIAL_ROWS}
    ):
        raise ValueError(f"Unexpected source scopes: {dict(scopes)}")

    subscription_rows, exclusions = build_subscription_rows(results, policies)
    if len(subscription_rows) != EXPECTED_SUBSCRIPTION_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_SUBSCRIPTION_ROWS} subscription rows, "
            f"found {len(subscription_rows)}"
        )
    if len(exclusions) != EXPECTED_SOURCE_ROWS - EXPECTED_SUBSCRIPTION_ROWS:
        raise ValueError(f"Unexpected exclusion count: {len(exclusions)}")

    subscription_fields = list(subscription_rows[0].keys())
    exclusion_fields = list(exclusions[0].keys())
    write_csv(
        data_dir / "subscription_first_task_cost.csv",
        subscription_rows,
        subscription_fields,
    )
    write_csv(
        data_dir / "subscription_exclusions.csv",
        exclusions,
        exclusion_fields,
    )

    result_by_id = {row["result_id"]: row for row in results}
    base_chart_rows = result_chart_rows(results)
    subscription_chart = subscription_chart_rows(subscription_rows, result_by_id)
    charts = {
        "token": [dict(row) for row in base_chart_rows],
        "subscription": subscription_chart,
        "api": [dict(row) for row in base_chart_rows],
    }
    for metric in METRICS:
        metric_rows = charts[metric.key]
        frontier = pareto_ids(metric_rows, metric.x_key)
        for row in metric_rows:
            row["is_pareto"] = str(row["id"]) in frontier

    payload = {
        "snapshot": args.snapshot,
        "benchmark": BENCHMARK,
        "published_at_utc": metadata["observed_at_utc"],
        "source_sha256": metadata["source_sha256"],
        "counts": {
            "token_configurations": len(charts["token"]),
            "api_cost_configurations": len(charts["api"]),
            "subscription_first_configurations": len(charts["subscription"]),
            "complete_configurations": scopes["complete"],
            "partial_configurations": scopes["partial"],
            "agent_harnesses": len({row["agent"] for row in base_chart_rows}),
            "model_developers": len(
                {row["developer"] for row in base_chart_rows}
            ),
        },
        "method": {
            "observation_grain": "agent harness + model + setting",
            "score": "Artificial Analysis Coding Agent Index v1.3 × 100",
            "token": "pooled average total Tokens per coding task attempt",
            "api": "pooled average pay-per-token API cost per coding task",
            "subscription": (
                "applicable quantifiable subscription first; exclude unknown "
                "plan allowance; API only when no applicable plan exists"
            ),
            "partial_observation": (
                "Claude Code · Opus 4.6 (medium) has two materialized components"
            ),
        },
        "charts": charts,
        "subscription_exclusions": exclusions,
        "sources": {
            "results": metadata["source_url"],
            "methodology": metadata["methodology_url"],
            "access_policy": (
                f"data/coding-agents/{args.snapshot}/subscription_access_policy.csv"
            ),
        },
    }
    site_data_dir = args.repository_root / "site" / "data" / "coding-agents"
    atomic_json(site_data_dir / f"{args.snapshot}.json", payload)
    manifest = {
        "current": args.snapshot,
        "snapshots": [
            {
                "id": args.snapshot,
                "benchmark": BENCHMARK,
                "published_at_utc": metadata["observed_at_utc"],
                "payload_url": f"data/coding-agents/{args.snapshot}.json",
                "chart_base": "charts",
                "data_url": (
                    f"data/coding-agents/{args.snapshot}/coding_agent_results.csv"
                ),
                "access_data_url": (
                    "data/coding-agents/"
                    f"{args.snapshot}/subscription_first_task_cost.csv"
                ),
                "release_url": (
                    "https://github.com/BIOcanse/llm-efficiency-cost-charts/"
                    f"releases/tag/coding-agents-{args.snapshot}"
                ),
                "label": {
                    "en": f"{args.snapshot} · Coding Agent Index v1.3",
                    "zh-CN": f"{args.snapshot} · Coding Agent Index v1.3",
                },
            }
        ],
    }
    atomic_json(args.repository_root / "site" / "data" / "coding-agents.json", manifest)

    static_metrics: list[dict[str, object]] = []
    if not args.skip_static:
        for language in ("en", "zh-CN"):
            chart_dir = args.repository_root / "charts" / language
            for metric in METRICS:
                static_metrics.append(
                    render_static_chart(
                        charts[metric.key],
                        metric,
                        language,
                        args.snapshot,
                        chart_dir,
                    )
                )
        atomic_json(data_dir / "static_chart_metrics.json", static_metrics)

    output = {
        "snapshot": args.snapshot,
        "counts": payload["counts"],
        "subscription_decisions": dict(Counter(row["decision"] for row in subscription_rows + exclusions)),
        "static_metrics": static_metrics,
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
