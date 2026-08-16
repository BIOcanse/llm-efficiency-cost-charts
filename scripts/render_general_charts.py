from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter, MaxNLocator, MultipleLocator
from matplotlib.transforms import Bbox


BACKGROUND = "#FBFBFA"
TEXT = "#172033"
MUTED = "#5D687A"
GRID = "#DCE2EA"
PALETTE = (
    "#1D4ED8",
    "#D97706",
    "#708238",
    "#7C3AED",
    "#DB2777",
    "#B91C1C",
    "#0F766E",
    "#475569",
    "#2563EB",
    "#A855F7",
    "#0891B2",
    "#BE123C",
)
COUNTRY_COLORS = {
    "US": "#64748B",
    "CN": "#9A3412",
    "FR": "#78716C",
    "ES": "#A16207",
    "CA": "#0369A1",
    "KR": "#0E7490",
    "AE": "#6D28D9",
    "CH": "#7C2D12",
    "IN": "#15803D",
}
EFFORT_MARKERS = {
    "instant": "v",
    "non-reasoning": "X",
    "low": "o",
    "medium": "s",
    "default": "h",
    "high": "D",
    "xhigh": "^",
    "max": "P",
}
EFFORT_LABELS = {
    "en": {
        "instant": "Instant",
        "non-reasoning": "Non-reasoning",
        "low": "Low",
        "medium": "Medium",
        "default": "Default",
        "high": "High",
        "xhigh": "Xhigh",
        "max": "Max",
    },
    "zh-CN": {
        "instant": "Instant",
        "non-reasoning": "非推理",
        "low": "低",
        "medium": "中",
        "default": "默认",
        "high": "高",
        "xhigh": "超高",
        "max": "Max",
    },
}


@dataclass(frozen=True)
class Point:
    model: str
    effort: str
    effort_order: int
    country_code: str
    developer: str
    historical: bool
    scope: str
    score: float
    x: float


@dataclass(frozen=True)
class Chart:
    metric: str
    filename: str
    rows: tuple[Point, ...]
    title_en: str
    title_zh: str
    subtitle_en: str
    subtitle_zh: str
    xlabel_en: str
    xlabel_zh: str
    tick_kind: str


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Render the bilingual general-model chart suite.")
    parser.add_argument("--snapshot", default="2026-08-15")
    parser.add_argument("--repository-root", type=Path, default=root)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def configure_fonts() -> None:
    candidates = (
        Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
    )
    regular = next(path for path in candidates if path.exists())
    bold = Path(r"C:\Windows\Fonts\msyhbd.ttc")
    for path in (regular, bold):
        if path.exists():
            font_manager.fontManager.addfont(str(path))
    family = font_manager.FontProperties(fname=str(regular)).get_name()
    plt.rcParams.update(
        {
            "font.family": family,
            "axes.unicode_minus": False,
            "svg.fonttype": "path",
            "figure.facecolor": BACKGROUND,
            "axes.facecolor": BACKGROUND,
        }
    )


def model_points(rows: list[dict[str, str]], field: str) -> tuple[Point, ...]:
    result = []
    for row in rows:
        if not row[field]:
            continue
        result.append(
            Point(
                model=row["model"],
                effort=row["effort"],
                effort_order=int(row["effort_order"]),
                country_code=row["country_code"],
                developer=row["developer"],
                historical=row["is_historical"] == "true",
                scope=row["data_scope"],
                score=float(row["intelligence_score_raw"]),
                x=float(row[field]),
            )
        )
    return tuple(result)


def access_points(rows: list[dict[str, str]]) -> tuple[Point, ...]:
    return tuple(
        Point(
            model=row["model"],
            effort=row["effort"],
            effort_order=int(row["effort_order"]),
            country_code=row["country_code"],
            developer=row["developer"],
            historical=row["is_historical"] == "true",
            scope=(
                "subscription"
                if row["access_mode"].startswith("subscription_")
                else "api_only"
            ),
            score=float(row["intelligence_score_raw"]),
            x=float(row["effective_cost_per_task_usd"]),
        )
        for row in rows
    )


def chart_suite(root: Path, snapshot: str) -> tuple[Chart, ...]:
    model_rows = read_csv(root / "data" / snapshot / "model_efficiency.csv")
    access_rows = read_csv(
        root / "data" / snapshot / "subscription_first_task_cost.csv"
    )
    token = model_points(model_rows, "total_tokens_million")
    api = model_points(model_rows, "cost_per_index_task_usd")
    subscription = access_points(access_rows)
    return (
        Chart(
            metric="token",
            filename="01_total_token_consumption_vs_score",
            rows=token,
            title_en=f"Model + reasoning-level Token efficiency: {len(token)} configurations",
            title_zh=f"模型＋思考档位 Token 效率：{len(token)} 个配置",
            subtitle_en=(
                "Each point is one model and reasoning level · same-color lines join levels of one model · upper left is better"
            ),
            subtitle_zh="每个点代表一个模型与思考档位 · 同色线连接同一模型的不同档位 · 越靠左上越好",
            xlabel_en="Complete-suite Token consumption (millions, lower is better)",
            xlabel_zh="整套评测 Token 消耗（百万，越低越好）",
            tick_kind="tokens",
        ),
        Chart(
            metric="api",
            filename="02_api_task_cost_vs_score",
            rows=api,
            title_en=f"API cost per task versus score: {len(api)} configurations",
            title_zh=f"API 单位任务成本与分数：{len(api)} 个配置",
            subtitle_en=(
                "Lowest positive AA-tested provider shared by all levels of one model · explicit quantized routes excluded · upper left is better"
            ),
            subtitle_zh="同一模型各档位使用共同可用且成本最低的 AA 实测正价供应商 · 排除显式量化端点 · 越靠左上越好",
            xlabel_en="API cost per Intelligence Index task (USD, lower is better)",
            xlabel_zh="每个 Intelligence Index 任务的 API 成本（美元，越低越好）",
            tick_kind="currency",
        ),
        Chart(
            metric="subscription",
            filename="03_subscription_first_task_cost_vs_score",
            rows=subscription,
            title_en=f"Subscription-first cost per task versus score: {len(subscription)} configurations",
            title_zh=f"套餐优先单位任务成本与分数：{len(subscription)} 个配置",
            subtitle_en=(
                "Use a plan only with a usable allowance estimate · otherwise API only when no applicable plan exists · upper left is better"
            ),
            subtitle_zh="套餐有可用额度估算才纳入 · 只有不存在适用套餐时才使用 API · 越靠左上越好",
            xlabel_en="Subscription-first effective cost per task (USD, lower is better)",
            xlabel_zh="套餐优先的有效单位任务成本（美元，越低越好）",
            tick_kind="currency",
        ),
    )


def pareto(rows: tuple[Point, ...]) -> list[Point]:
    ordered = sorted(rows, key=lambda row: (row.x, -row.score))
    result = []
    best = -math.inf
    for row in ordered:
        if row.score > best:
            result.append(row)
            best = row.score
    return result


def label_candidates() -> list[tuple[int, int, str]]:
    vertical = (9, -13, 22, -26, 36, -40, 52, -56, 70, -74, 90, -94, 112, -116)
    horizontal = (8, 20, 38, 62, 92, 128, 172, 226, 290, 360, 440, 530)
    values = []
    for dy in vertical:
        for dx in horizontal:
            values.append((dx, dy, "left"))
            values.append((-dx, dy, "right"))
    values.sort(key=lambda item: (item[0] ** 2 + item[1] ** 2, abs(item[0]), abs(item[1])))
    return values


LABEL_CANDIDATES = label_candidates()


def series_palette(rows: tuple[Point, ...]) -> tuple[dict[str, int], dict[str, str]]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[row.model] += 1
    series = sorted(model for model, count in counts.items() if count > 1)
    colors = {model: PALETTE[index % len(PALETTE)] for index, model in enumerate(series)}
    return dict(counts), colors


def color(row: Point, counts: dict[str, int], colors: dict[str, str]) -> str:
    if counts[row.model] > 1:
        return colors[row.model]
    return COUNTRY_COLORS.get(row.country_code, "#64748B")


def label(row: Point, locale: str, counts: dict[str, int]) -> str:
    history = "†" if row.historical else ""
    effort = EFFORT_LABELS[locale].get(row.effort, row.effort)
    if counts[row.model] > 1:
        return f"{row.model}{history} · {effort} · {row.score:.0f}"
    scope = ""
    if row.scope == "token_only":
        scope = ", Token only" if locale == "en" else "，仅 Token"
    return f"{row.model}{history} [{row.country_code}{scope}] · {row.score:.0f}"


def overlap_area(first: Bbox, second: Bbox) -> float:
    if not Bbox.overlaps(first, second):
        return 0.0
    return max(0.0, min(first.x1, second.x1) - max(first.x0, second.x0)) * max(
        0.0, min(first.y1, second.y1) - max(first.y0, second.y0)
    )


def sampled_line_boxes(ax, grouped: dict[str, list[Point]]) -> list[Bbox]:
    boxes: list[Bbox] = []
    for rows in grouped.values():
        if len(rows) < 2:
            continue
        ordered = sorted(rows, key=lambda row: row.effort_order)
        for first, second in zip(ordered, ordered[1:]):
            x1, y1 = ax.transData.transform((first.x, first.score))
            x2, y2 = ax.transData.transform((second.x, second.score))
            samples = max(2, int(math.hypot(x2 - x1, y2 - y1) / 18))
            for index in range(1, samples):
                ratio = index / samples
                x = x1 + (x2 - x1) * ratio
                y = y1 + (y2 - y1) * ratio
                boxes.append(Bbox.from_bounds(x - 2.5, y - 2.5, 5, 5))
    return boxes


def place_labels(ax, rows: tuple[Point, ...], counts: dict[str, int], colors: dict[str, str], locale: str):
    ax.figure.canvas.draw()
    renderer = ax.figure.canvas.get_renderer()
    grouped: dict[str, list[Point]] = defaultdict(list)
    for row in rows:
        grouped[row.model].append(row)
    point_boxes = []
    for row in rows:
        x, y = ax.transData.transform((row.x, row.score))
        point_boxes.append(Bbox.from_bounds(x - 8, y - 8, 16, 16))
    obstacles = point_boxes + sampled_line_boxes(ax, grouped)
    label_boxes: list[Bbox] = []
    annotations = []
    axes_box = ax.get_window_extent().expanded(0.995, 0.98)
    frontier_keys = {(row.model, row.effort) for row in pareto(rows)}
    ordered = sorted(
        rows,
        key=lambda row: (
            (row.model, row.effort) not in frontier_keys,
            -row.score,
            row.model,
            row.effort_order,
        ),
    )
    fontsize = 6.15
    for row in ordered:
        text = label(row, locale, counts)
        probe = ax.text(0, 0, text, fontsize=fontsize, fontweight="semibold", alpha=0)
        measured = probe.get_window_extent(renderer=renderer)
        probe.remove()
        width = measured.width + 8
        height = measured.height + 5
        x, y = ax.transData.transform((row.x, row.score))
        best = None
        for dx, dy, alignment in LABEL_CANDIDATES:
            anchor_x = x + dx * ax.figure.dpi / 72
            anchor_y = y + dy * ax.figure.dpi / 72
            left = anchor_x if alignment == "left" else anchor_x - width
            box = Bbox.from_bounds(left, anchor_y - height * 0.42, width, height)
            outside = (
                max(0, axes_box.x0 - box.x0)
                + max(0, box.x1 - axes_box.x1)
                + max(0, axes_box.y0 - box.y0)
                + max(0, box.y1 - axes_box.y1)
            )
            label_overlap = sum(overlap_area(box, other) for other in label_boxes)
            obstacle_overlap = sum(overlap_area(box, other) for other in obstacles)
            distance = math.hypot(dx, dy)
            penalty = outside * 100_000 + label_overlap * 20 + obstacle_overlap * 3 + distance * 0.02
            if best is None or penalty < best[-1]:
                best = (dx, dy, alignment, box, penalty)
            if outside == 0 and label_overlap == 0 and obstacle_overlap == 0:
                break
        if best is None:
            raise RuntimeError("No label position evaluated")
        dx, dy, alignment, box, _penalty = best
        label_boxes.append(box)
        leader = None
        if abs(dx) >= 30 or abs(dy) >= 28:
            leader = {"arrowstyle": "-", "color": color(row, counts, colors), "lw": 0.45, "alpha": 0.38}
        annotations.append(
            ax.annotate(
                text,
                (row.x, row.score),
                xytext=(dx, dy),
                textcoords="offset points",
                ha=alignment,
                va="center",
                fontsize=fontsize,
                fontweight="semibold",
                color=color(row, counts, colors),
                zorder=8,
                bbox={"boxstyle": "round,pad=0.12", "fc": BACKGROUND, "ec": "none", "alpha": 0.94},
                arrowprops=leader,
            )
        )
    return annotations


def chart_metrics(ax, annotations) -> tuple[int, int]:
    ax.figure.canvas.draw()
    renderer = ax.figure.canvas.get_renderer()
    boxes = [
        annotation.get_bbox_patch().get_window_extent(renderer=renderer)
        for annotation in annotations
    ]
    collisions = sum(
        Bbox.overlaps(boxes[first], boxes[second])
        for first in range(len(boxes))
        for second in range(first + 1, len(boxes))
    )
    axes_box = ax.get_window_extent()
    out_of_bounds = sum(
        box.x0 < axes_box.x0
        or box.x1 > axes_box.x1
        or box.y0 < axes_box.y0
        or box.y1 > axes_box.y1
        for box in boxes
    )
    return int(collisions), int(out_of_bounds)


def draw_sidebar(sidebar, chart: Chart, locale: str, rows: tuple[Point, ...]) -> None:
    sidebar.axis("off")
    if locale == "en":
        lines = (
            "How to read",
            "↑ Higher score",
            "← Lower Token use / cost",
            "Same-color line: levels of one model",
            "Black outline: Pareto frontier",
            "† Superseded historical reference",
        )
    else:
        lines = (
            "怎么读",
            "↑ 分数更高",
            "← Token 消耗 / 成本更低",
            "同色线：同一模型的不同档位",
            "黑色外圈：Pareto 前沿",
            "† 已被替代的历史参考",
        )
    sidebar.text(0, 0.98, lines[0], fontsize=14, fontweight="bold", color=TEXT, va="top")
    y = 0.92
    for line in lines[1:]:
        sidebar.text(0, y, line, fontsize=9.2, color=MUTED, va="top")
        y -= 0.065
    if chart.metric == "subscription":
        plan_count = sum(row.scope == "subscription" for row in rows)
        api_count = len(rows) - plan_count
        note = (
            f"Plans: {plan_count}\nAPI fallback: {api_count}"
            if locale == "en"
            else f"套餐：{plan_count}\nAPI 回退：{api_count}"
        )
        sidebar.text(0, 0.48, note, fontsize=9.5, color=TEXT, va="top", linespacing=1.5)
    sidebar.text(
        0,
        0.20,
        (
            "Country/region is the developer location."
            if locale == "en"
            else "国家/地区按开发机构所在地标注。"
        ),
        fontsize=8.5,
        color=MUTED,
        va="top",
        wrap=True,
    )


def nice_limit(maximum: float, metric: str) -> float:
    target = maximum * 1.08
    if metric == "token":
        return math.ceil(target / 500) * 500
    step = 0.05 if target < 0.5 else 0.5
    return math.ceil(target / step) * step


def render_chart(chart: Chart, locale: str, snapshot: str, benchmark: str, output_dir: Path) -> dict[str, object]:
    rows = chart.rows
    counts, colors = series_palette(rows)
    grouped: dict[str, list[Point]] = defaultdict(list)
    for row in rows:
        grouped[row.model].append(row)

    figure = plt.figure(figsize=(24, 13.5), dpi=200, facecolor=BACKGROUND)
    ax = figure.add_axes([0.055, 0.155, 0.79, 0.735])
    sidebar = figure.add_axes([0.865, 0.155, 0.12, 0.735])
    title = chart.title_en if locale == "en" else chart.title_zh
    subtitle = chart.subtitle_en if locale == "en" else chart.subtitle_zh
    xlabel = chart.xlabel_en if locale == "en" else chart.xlabel_zh
    figure.text(0.055, 0.956, title, fontsize=25, fontweight="bold", color=TEXT)
    figure.text(0.055, 0.918, subtitle, fontsize=11.6, color=MUTED)

    ax.set_xlim(0, nice_limit(max(row.x for row in rows), chart.metric))
    ax.set_ylim(0, 65)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=9, min_n_ticks=6))
    if chart.tick_kind == "tokens":
        ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}M"))
    else:
        ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:g}"))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.9)
    ax.grid(axis="x", color=GRID, linewidth=0.7, alpha=0.65)
    ax.tick_params(axis="both", colors=MUTED, labelsize=10.5, length=0)
    for name in ("top", "right"):
        ax.spines[name].set_visible(False)
    ax.spines["left"].set_color("#9CA3AF")
    ax.spines["bottom"].set_color("#9CA3AF")
    ax.set_xlabel(xlabel, fontsize=12.5, color=TEXT, labelpad=13)
    ax.set_ylabel(
        f"{benchmark} score" if locale == "en" else f"{benchmark} 分数",
        fontsize=12.5,
        color=TEXT,
        labelpad=13,
    )

    frontier = pareto(rows)
    ax.plot(
        [row.x for row in frontier],
        [row.score for row in frontier],
        color="#111827",
        linewidth=1.25,
        linestyle=(0, (3, 3)),
        alpha=0.45,
        zorder=1,
    )
    for model, model_rows in grouped.items():
        if len(model_rows) < 2:
            continue
        ordered = sorted(model_rows, key=lambda row: row.effort_order)
        ax.plot(
            [row.x for row in ordered],
            [row.score for row in ordered],
            color=colors[model],
            linewidth=2.0,
            alpha=0.82,
            zorder=3,
        )
    for row in rows:
        point_color = color(row, counts, colors)
        face = BACKGROUND if row.historical or counts[row.model] == 1 else point_color
        ax.scatter(
            row.x,
            row.score,
            s=82,
            marker=EFFORT_MARKERS.get(row.effort, "o"),
            facecolor=face,
            edgecolor=point_color if face == BACKGROUND else "#FFFFFF",
            linewidth=1.5 if face == BACKGROUND else 1.0,
            zorder=5,
        )
    ax.scatter(
        [row.x for row in frontier],
        [row.score for row in frontier],
        s=136,
        facecolors="none",
        edgecolors="#111827",
        linewidths=0.95,
        zorder=6,
    )
    annotations = place_labels(ax, rows, counts, colors, locale)
    draw_sidebar(sidebar, chart, locale, rows)
    figure.text(
        0.055,
        0.066,
        (
            "Sources: Artificial Analysis model and provider pages; provider plan and pricing evidence in data files."
            if locale == "en"
            else "来源：Artificial Analysis 模型与供应商页面；套餐和价格证据见数据文件。"
        ),
        fontsize=9.2,
        color=MUTED,
    )
    figure.text(
        0.055,
        0.039,
        (
            f"Snapshot {snapshot} UTC · {benchmark} · linear axes start at zero"
            if locale == "en"
            else f"{snapshot} UTC 快照 · {benchmark} · 线性坐标从 0 开始"
        ),
        fontsize=9.0,
        color=MUTED,
    )
    collisions, out_of_bounds = chart_metrics(ax, annotations)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_dir / f"{chart.filename}.png", dpi=200, facecolor=BACKGROUND)
    figure.savefig(output_dir / f"{chart.filename}.svg", facecolor=BACKGROUND)
    plt.close(figure)
    print(
        f"rendered {locale}/{chart.filename}: rows={len(rows)} "
        f"collisions={collisions} out_of_bounds={out_of_bounds}"
    )
    return {
        "locale": locale,
        "metric": chart.metric,
        "rows": len(rows),
        "label_collisions": collisions,
        "out_of_bounds_labels": out_of_bounds,
    }


def main() -> None:
    args = parse_args()
    root = args.repository_root.resolve()
    configure_fonts()
    charts = chart_suite(root, args.snapshot)
    benchmark = "Artificial Analysis Intelligence Index v4.1.1"
    metrics = []
    for locale in ("en", "zh-CN"):
        for chart in charts:
            metrics.append(
                render_chart(
                    chart,
                    locale,
                    args.snapshot,
                    benchmark,
                    root / "charts" / locale,
                )
            )
    metrics_path = root / "data" / args.snapshot / "static_chart_metrics.json"
    metrics_path.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if any(
        metric["label_collisions"] or metric["out_of_bounds_labels"]
        for metric in metrics
    ):
        raise RuntimeError("Static chart label validation failed")


if __name__ == "__main__":
    main()
