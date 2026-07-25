from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Rectangle


BACKGROUND = "#F6F8FB"
SURFACE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#5D687A"
BORDER = "#DCE2EA"
GRID = "#E7EBF1"
BLUE = "#315EFB"
BLUE_DARK = "#2346C5"
BLUE_SOFT = "#EAF0FF"
ORANGE = "#E96B3C"
ORANGE_SOFT = "#FFF0E9"
LIMITED = "#8E99AA"
LIMITED_SOFT = "#EEF1F5"
GREEN = "#14866D"

FONT_REGULAR_PATH = Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf")
FONT_BOLD_PATH = Path(r"C:\Windows\Fonts\msyhbd.ttc")

mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["svg.fonttype"] = "path"
mpl.rcParams["savefig.facecolor"] = BACKGROUND


@dataclass(frozen=True)
class LocaleText:
    language: str
    token_title: str
    token_subtitle: str
    token_axis: str
    core_heading: str
    limited_heading: str
    limited_note: str
    score_range: str
    levels: str
    index_label: str
    overhead_label: str
    api_title: str
    plan_title: str
    cost_subtitle: str
    raw_top: str
    threshold_heading: str
    threshold_note: str
    minimum_score: str
    rank: str
    model_level: str
    score: str
    usd_task: str
    cost_percent: str
    provider_access: str
    cost_reference: str
    per_task: str
    api_full_title: str
    plan_full_title: str
    full_subtitle: str
    snapshot_note: str


LOCALES = {
    "en": LocaleText(
        language="en",
        token_title="Aggregate Token Efficiency Ranking",
        token_subtitle=(
            "Full reasoning-level curves compared at matched scores · "
            "highest observed core model = 100%"
        ),
        token_axis="Relative aggregate Token efficiency (%)",
        core_heading="Core ranking",
        limited_heading="Limited-evidence models",
        limited_note=(
            "Limited-evidence models have only 2–3 levels or cover less than "
            "8 score points; they are shown separately."
        ),
        score_range="score range",
        levels="levels",
        index_label="index",
        overhead_label="frontier Token multiplier",
        api_title="API Cost per Task Ranking",
        plan_title="Subscription-first Cost per Task Ranking",
        cost_subtitle=(
            "Exact USD per Intelligence Index task · most expensive included "
            "configuration = 100% cost"
        ),
        raw_top="15 lowest raw task costs",
        threshold_heading="Lowest cost reaching each score threshold",
        threshold_note=(
            "Threshold leaders prevent a very cheap low-score configuration "
            "from being presented as the best overall value."
        ),
        minimum_score="Minimum score",
        rank="Rank",
        model_level="Model · reasoning level",
        score="Score",
        usd_task="USD / task",
        cost_percent="Cost vs. max",
        provider_access="Provider / access",
        cost_reference="100% cost reference",
        per_task="per task",
        api_full_title="Complete API Cost per Task Ranking",
        plan_full_title="Complete Subscription-first Cost per Task Ranking",
        full_subtitle=(
            "Every included configuration · exact USD per task and "
            "Intelligence Index score"
        ),
        snapshot_note=(
            "Snapshot 2026-07-24 · Artificial Analysis Intelligence Index "
            "v4.1 · lower cost and higher score are better"
        ),
    ),
    "zh-CN": LocaleText(
        language="zh-CN",
        token_title="综合全档位 Token 效率排名",
        token_subtitle="按相同分数比较完整档位曲线 · 当前核心榜第一名 = 100%",
        token_axis="相对综合 Token 效率（%）",
        core_heading="核心排名",
        limited_heading="有限样本模型",
        limited_note="有限样本模型只有 2–3 个档位，或覆盖不到 8 个分数点，因此单独列出。",
        score_range="覆盖分数",
        levels="档位",
        index_label="原始指数",
        overhead_label="前沿 Token 倍率",
        api_title="API 单位任务成本排名",
        plan_title="套餐优先单位任务成本排名",
        cost_subtitle="标出每项任务的完整美元成本 · 同一榜单最贵配置 = 100% 成本",
        raw_top="原始单位任务成本最低的前 15 项",
        threshold_heading="达到不同分数门槛的最低成本",
        threshold_note="门槛对比可以避免把极低价但低分的配置直接称为整体性价比最高。",
        minimum_score="最低分数",
        rank="排名",
        model_level="模型 · 思考档位",
        score="分数",
        usd_task="美元 / 任务",
        cost_percent="相对最贵",
        provider_access="供应商 / 获取方式",
        cost_reference="100% 成本参照",
        per_task="/ 任务",
        api_full_title="API 单位任务成本完整排名",
        plan_full_title="套餐优先单位任务成本完整排名",
        full_subtitle="列出全部纳入配置 · 标出单位任务美元成本与 Intelligence Index 分数",
        snapshot_note=(
            "数据快照 2026-07-24 · Artificial Analysis Intelligence Index "
            "v4.1 · 成本越低、分数越高越好"
        ),
    ),
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render bilingual ranking images from dated ranking CSV files."
    )
    parser.add_argument("--snapshot", default="2026-07-24")
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        choices=sorted(LOCALES),
        default=["en", "zh-CN"],
    )
    return parser.parse_args()


def font(size: float, bold: bool = False) -> FontProperties:
    path = FONT_BOLD_PATH if bold else FONT_REGULAR_PATH
    return FontProperties(fname=str(path), size=size)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def effort_label(locale: str, effort: str) -> str:
    return EFFORT_LABELS[locale].get(effort, effort)


def model_level(locale: str, row: dict[str, str]) -> str:
    return f"{row['model']} · {effort_label(locale, row['effort'])}"


def format_score(value: str | float) -> str:
    return f"{float(value):.2f}"


def format_usd(value: str | float) -> str:
    number = float(value)
    if number < 0.01:
        return f"${number:.6f}"
    if number < 1:
        return f"${number:.4f}"
    return f"${number:.3f}"


def format_cost_percent(value: str | float, maximum: float) -> str:
    percentage = float(value) / maximum * 100.0
    if percentage < 0.1:
        return f"{percentage:.3f}%"
    if percentage < 10:
        return f"{percentage:.2f}%"
    return f"{percentage:.1f}%"


def add_title(
    figure: plt.Figure,
    title: str,
    subtitle: str,
    *,
    title_y: float = 0.952,
) -> None:
    figure.text(
        0.045,
        title_y,
        title,
        color=TEXT,
        fontproperties=font(34, bold=True),
        va="top",
    )
    figure.text(
        0.045,
        title_y - 0.062,
        subtitle,
        color=MUTED,
        fontproperties=font(17),
        va="top",
    )
    figure.add_artist(
        Rectangle(
            (0.045, title_y - 0.096),
            0.91,
            0.004,
            transform=figure.transFigure,
            facecolor=BLUE,
            edgecolor="none",
        )
    )


def save_figure(
    figure: plt.Figure,
    output_dir: Path,
    stem: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_dir / f"{stem}.png",
        dpi=100,
        facecolor=BACKGROUND,
        bbox_inches=None,
    )
    figure.savefig(
        output_dir / f"{stem}.svg",
        facecolor=BACKGROUND,
        bbox_inches=None,
    )
    plt.close(figure)


def render_token_ranking(
    rows: list[dict[str, str]],
    locale: str,
    output_dir: Path,
) -> None:
    text = LOCALES[locale]
    core = [row for row in rows if row["category"] == "core"]
    limited = [row for row in rows if row["category"] == "limited"]
    core_max = max(float(row["efficiency_index"]) for row in core)

    display_rows: list[tuple[dict[str, str], float, bool]] = []
    for row in core:
        display_rows.append(
            (row, float(row["efficiency_index"]) / core_max * 100.0, False)
        )
    for row in limited:
        display_rows.append(
            (row, float(row["efficiency_index"]) / core_max * 100.0, True)
        )

    figure = plt.figure(figsize=(48, 27), dpi=100, facecolor=BACKGROUND)
    add_title(figure, text.token_title, text.token_subtitle)
    axis = figure.add_axes((0.28, 0.16, 0.66, 0.67), facecolor=BACKGROUND)

    positions = [9.0, 8.0, 7.0, 6.0, 5.0, 3.45, 2.45, 1.45, 0.45]
    axis.set_xlim(0, 108)
    axis.set_ylim(-0.2, 9.8)
    axis.set_yticks([])
    axis.set_xticks([0, 20, 40, 60, 80, 100])
    axis.set_xticklabels(
        ["0", "20", "40", "60", "80", "100"],
        color=MUTED,
        fontproperties=font(13),
    )
    axis.set_xlabel(text.token_axis, color=TEXT, fontproperties=font(15))
    axis.grid(axis="x", color=GRID, linewidth=1.3)
    axis.set_axisbelow(True)
    for spine in axis.spines.values():
        spine.set_visible(False)

    for index, ((row, percentage, is_limited), position) in enumerate(
        zip(display_rows, positions, strict=True)
    ):
        bar_color = LIMITED if is_limited else BLUE
        axis.barh(
            position,
            percentage,
            height=0.56,
            color=bar_color,
            edgecolor=bar_color,
            alpha=0.95,
            zorder=3,
        )
        axis.text(
            percentage + 1.2,
            position,
            f"{percentage:.1f}%",
            va="center",
            ha="left",
            color=TEXT,
            fontproperties=font(15, bold=True),
        )
        model_y = position + 0.16
        meta_y = position - 0.19
        axis.text(
            -2.8,
            model_y,
            row["model"],
            va="center",
            ha="right",
            color=TEXT,
            fontproperties=font(14, bold=True),
            clip_on=False,
        )
        meta = (
            f"{row['levels']} {text.levels} · {text.score_range} "
            f"{format_score(row['score_min'])}–{format_score(row['score_max'])}"
        )
        axis.text(
            -2.8,
            meta_y,
            meta,
            va="center",
            ha="right",
            color=MUTED,
            fontproperties=font(10.5),
            clip_on=False,
        )
        detail = (
            f"{text.index_label} {float(row['efficiency_index']):.2f} · "
            f"{text.overhead_label} "
            f"{float(row['token_overhead_vs_frontier']):.2f}×"
        )
        axis.text(
            min(percentage - 1.0, 95.0),
            position,
            detail,
            va="center",
            ha="right",
            color=SURFACE if not is_limited and percentage > 45 else TEXT,
            fontproperties=font(10.5),
            zorder=4,
        )

    figure.text(
        0.045,
        0.795,
        text.core_heading,
        color=BLUE_DARK,
        fontproperties=font(16, bold=True),
    )
    figure.text(
        0.045,
        0.40,
        text.limited_heading,
        color=MUTED,
        fontproperties=font(16, bold=True),
    )
    figure.text(
        0.045,
        0.105,
        text.limited_note,
        color=MUTED,
        fontproperties=font(12),
    )
    figure.text(
        0.955,
        0.055,
        text.snapshot_note,
        ha="right",
        color=MUTED,
        fontproperties=font(10.5),
    )
    save_figure(figure, output_dir, "04_token_efficiency_ranking")


def panel(
    figure: plt.Figure,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    figure.add_artist(
        FancyBboxPatch(
            (x, y),
            width,
            height,
            transform=figure.transFigure,
            boxstyle="round,pad=0.008,rounding_size=0.014",
            facecolor=SURFACE,
            edgecolor=BORDER,
            linewidth=1.2,
        )
    )


def access_text(row: dict[str, str], mode: str) -> str:
    if mode == "api":
        return row.get("provider", "")
    return row.get("plan_name") or row.get("provider", "")


def draw_table_header(
    figure: plt.Figure,
    *,
    x: float,
    y: float,
    width: float,
    text: LocaleText,
    threshold: bool = False,
) -> None:
    columns = (
        [
            (0.025, text.minimum_score, "left"),
            (0.19, text.model_level, "left"),
            (0.65, text.score, "right"),
            (0.835, text.usd_task, "right"),
            (0.975, text.cost_percent, "right"),
        ]
        if threshold
        else [
            (0.025, text.rank, "left"),
            (0.11, text.model_level, "left"),
            (0.66, text.score, "right"),
            (0.84, text.usd_task, "right"),
            (0.975, text.cost_percent, "right"),
        ]
    )
    for relative_x, label, alignment in columns:
        figure.text(
            x + relative_x * width,
            y,
            label,
            ha=alignment,
            va="center",
            color=MUTED,
            fontproperties=font(11.5, bold=True),
        )


def draw_cost_rows(
    figure: plt.Figure,
    rows: list[dict[str, str]],
    *,
    locale: str,
    mode: str,
    x: float,
    y_top: float,
    width: float,
    row_height: float,
    maximum_cost: float,
    threshold: bool = False,
    rank_offset: int = 0,
) -> None:
    text = LOCALES[locale]
    for index, row in enumerate(rows):
        y = y_top - index * row_height
        if index % 2 == 0:
            figure.add_artist(
                Rectangle(
                    (x + 0.012 * width, y - row_height * 0.45),
                    width * 0.976,
                    row_height * 0.90,
                    transform=figure.transFigure,
                    facecolor=BLUE_SOFT if threshold else "#F8FAFD",
                    edgecolor="none",
                )
            )
        rank_value = (
            f"≥ {int(float(row['score_threshold']))}"
            if threshold
            else str(rank_offset + index + 1)
        )
        rank_x = 0.025 if threshold else 0.025
        model_x = 0.19 if threshold else 0.11
        figure.text(
            x + rank_x * width,
            y,
            rank_value,
            ha="left",
            va="center",
            color=BLUE_DARK if threshold else TEXT,
            fontproperties=font(12, bold=threshold),
        )
        figure.text(
            x + model_x * width,
            y + row_height * 0.12,
            model_level(locale, row),
            ha="left",
            va="center",
            color=TEXT,
            fontproperties=font(12, bold=True),
        )
        figure.text(
            x + model_x * width,
            y - row_height * 0.18,
            access_text(row, mode),
            ha="left",
            va="center",
            color=MUTED,
            fontproperties=font(8.8),
        )
        figure.text(
            x + 0.66 * width,
            y,
            format_score(row["score"]),
            ha="right",
            va="center",
            color=TEXT,
            fontproperties=font(11.5),
        )
        figure.text(
            x + 0.84 * width,
            y,
            format_usd(row["cost_usd_per_task"]),
            ha="right",
            va="center",
            color=ORANGE if threshold else GREEN,
            fontproperties=font(12.5, bold=True),
        )
        figure.text(
            x + 0.975 * width,
            y,
            format_cost_percent(row["cost_usd_per_task"], maximum_cost),
            ha="right",
            va="center",
            color=ORANGE if threshold else TEXT,
            fontproperties=font(11.5, bold=threshold),
        )


def render_cost_overview(
    rows: list[dict[str, str]],
    thresholds: list[dict[str, str]],
    locale: str,
    mode: str,
    output_dir: Path,
) -> None:
    text = LOCALES[locale]
    figure = plt.figure(figsize=(48, 27), dpi=100, facecolor=BACKGROUND)
    title = text.api_title if mode == "api" else text.plan_title
    stem = (
        "05_api_cost_ranking"
        if mode == "api"
        else "06_subscription_cost_ranking"
    )
    maximum_row = max(rows, key=lambda row: float(row["cost_usd_per_task"]))
    maximum_cost = float(maximum_row["cost_usd_per_task"])
    add_title(figure, title, text.cost_subtitle)

    left = (0.045, 0.12, 0.55, 0.69)
    right = (0.62, 0.12, 0.335, 0.69)
    panel(figure, *left)
    panel(figure, *right)

    figure.text(
        left[0] + 0.02,
        0.775,
        text.raw_top,
        color=TEXT,
        fontproperties=font(16, bold=True),
    )
    draw_table_header(
        figure,
        x=left[0] + 0.01,
        y=0.725,
        width=left[2] - 0.02,
        text=text,
    )
    draw_cost_rows(
        figure,
        rows[:15],
        locale=locale,
        mode=mode,
        x=left[0] + 0.01,
        y_top=0.685,
        width=left[2] - 0.02,
        row_height=0.037,
        maximum_cost=maximum_cost,
    )

    figure.text(
        right[0] + 0.02,
        0.775,
        text.threshold_heading,
        color=TEXT,
        fontproperties=font(15, bold=True),
    )
    draw_table_header(
        figure,
        x=right[0] + 0.01,
        y=0.715,
        width=right[2] - 0.02,
        text=text,
        threshold=True,
    )
    draw_cost_rows(
        figure,
        thresholds,
        locale=locale,
        mode=mode,
        x=right[0] + 0.01,
        y_top=0.655,
        width=right[2] - 0.02,
        row_height=0.078,
        threshold=True,
        maximum_cost=maximum_cost,
    )
    figure.text(
        right[0] + 0.02,
        0.155,
        text.threshold_note,
        color=MUTED,
        fontproperties=font(10.5),
        wrap=True,
    )
    figure.text(
        0.045,
        0.055,
        (
            f"{text.cost_reference}: "
            f"{model_level(locale, maximum_row)} · "
            f"{format_usd(maximum_cost)} {text.per_task}"
        ),
        ha="left",
        color=TEXT,
        fontproperties=font(10.5, bold=True),
    )
    figure.text(
        0.955,
        0.055,
        text.snapshot_note,
        ha="right",
        color=MUTED,
        fontproperties=font(10.5),
    )
    save_figure(figure, output_dir, stem)


def split_rows(
    rows: list[dict[str, str]],
    column_count: int,
) -> list[list[dict[str, str]]]:
    rows_per_column = math.ceil(len(rows) / column_count)
    return [
        rows[index : index + rows_per_column]
        for index in range(0, len(rows), rows_per_column)
    ]


def render_complete_cost_ranking(
    rows: list[dict[str, str]],
    locale: str,
    mode: str,
    output_dir: Path,
) -> None:
    text = LOCALES[locale]
    is_api = mode == "api"
    column_count = 4 if is_api else 3
    columns = split_rows(rows, column_count)
    figure = plt.figure(figsize=(48, 36), dpi=100, facecolor=BACKGROUND)
    title = text.api_full_title if is_api else text.plan_full_title
    stem = (
        "05_api_cost_ranking_full"
        if is_api
        else "06_subscription_cost_ranking_full"
    )
    maximum_row = max(rows, key=lambda row: float(row["cost_usd_per_task"]))
    maximum_cost = float(maximum_row["cost_usd_per_task"])
    add_title(figure, title, text.full_subtitle, title_y=0.965)

    outer_left = 0.035
    outer_right = 0.035
    gap = 0.012
    panel_width = (
        1.0 - outer_left - outer_right - gap * (column_count - 1)
    ) / column_count
    panel_y = 0.085
    panel_height = 0.785
    header_y = 0.835
    first_row_y = 0.797
    max_rows = max(len(column) for column in columns)
    row_height = 0.69 / max_rows

    for column_index, column_rows in enumerate(columns):
        x = outer_left + column_index * (panel_width + gap)
        panel(figure, x, panel_y, panel_width, panel_height)
        start_rank = int(column_rows[0]["rank"])
        end_rank = int(column_rows[-1]["rank"])
        figure.text(
            x + 0.014,
            0.852,
            f"{start_rank}–{end_rank}",
            color=BLUE_DARK,
            fontproperties=font(13.5, bold=True),
        )
        draw_table_header(
            figure,
            x=x + 0.005,
            y=header_y,
            width=panel_width - 0.01,
            text=text,
        )
        draw_cost_rows(
            figure,
            column_rows,
            locale=locale,
            mode=mode,
            x=x + 0.005,
            y_top=first_row_y,
            width=panel_width - 0.01,
            row_height=row_height,
            rank_offset=start_rank - 1,
            maximum_cost=maximum_cost,
        )

    figure.text(
        0.035,
        0.035,
        (
            f"{text.cost_reference}: "
            f"{model_level(locale, maximum_row)} · "
            f"{format_usd(maximum_cost)} {text.per_task}"
        ),
        ha="left",
        color=TEXT,
        fontproperties=font(10.5, bold=True),
    )
    figure.text(
        0.965,
        0.035,
        text.snapshot_note,
        ha="right",
        color=MUTED,
        fontproperties=font(10.5),
    )
    save_figure(figure, output_dir, stem)


def filter_thresholds(
    rows: Iterable[dict[str, str]],
    metric: str,
) -> list[dict[str, str]]:
    selected = [row for row in rows if row["metric"] == metric]
    return sorted(selected, key=lambda row: float(row["score_threshold"]))


def main() -> None:
    args = parse_args()
    repository_root = args.repository_root.resolve()
    ranking_dir = repository_root / "rankings" / args.snapshot
    token_rows = load_csv(ranking_dir / "token_efficiency_ranking.csv")
    api_rows = load_csv(ranking_dir / "api_cost_ranking.csv")
    subscription_rows = load_csv(ranking_dir / "subscription_cost_ranking.csv")
    threshold_rows = load_csv(ranking_dir / "score_threshold_leaders.csv")

    if len(token_rows) != 9:
        raise ValueError(f"Expected 9 Token ranking rows, found {len(token_rows)}")
    if len(api_rows) != 68:
        raise ValueError(f"Expected 68 API ranking rows, found {len(api_rows)}")
    if len(subscription_rows) != 46:
        raise ValueError(
            "Expected 46 subscription ranking rows, "
            f"found {len(subscription_rows)}"
        )

    for locale in args.languages:
        output_dir = repository_root / "charts" / locale
        render_token_ranking(token_rows, locale, output_dir)
        render_cost_overview(
            api_rows,
            filter_thresholds(threshold_rows, "api"),
            locale,
            "api",
            output_dir,
        )
        render_complete_cost_ranking(
            api_rows,
            locale,
            "api",
            output_dir,
        )
        render_cost_overview(
            subscription_rows,
            filter_thresholds(threshold_rows, "subscription_first"),
            locale,
            "subscription",
            output_dir,
        )
        render_complete_cost_ranking(
            subscription_rows,
            locale,
            "subscription",
            output_dir,
        )

    print(
        "rendered ranking images: "
        f"languages={len(args.languages)} assets={len(args.languages) * 10}"
    )


if __name__ == "__main__":
    main()
