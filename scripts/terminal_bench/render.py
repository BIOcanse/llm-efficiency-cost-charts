"""Bilingual scientific exports from normalized Terminal-Bench observations."""
from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path as MplPath
from matplotlib.text import Text
from matplotlib.transforms import Bbox

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_coding_agent_charts import candidate_offsets, offset_alignment, padded, text_box
from core import ranked, frontier_rows, FRONTIER_KEYS

COLORS = ["#315efb", "#e76f2e", "#7b4ce2", "#168c6a", "#d63c72", "#8a6a17", "#087ea4", "#b34b9b", "#4e7d2b", "#c5522d", "#5368a6", "#7a5a9e"]
EFFORT = {"low": "低", "medium": "中", "high": "高", "xhigh": "超高", "max": "Max", "ultra": "Ultra", "none": "无", "minimal": "最低", "not_reported": "未公布"}
METRICS = {
    "subscription": ("subscription_per_attempt", "01_subscription", "套餐折算成本与任务成功率", "Subscription-equivalent cost vs. task success", "平均每次尝试成本（美元，越低越好）", "Mean USD per attempt · lower is better"),
    "api": ("api_per_attempt", "02_api", "API 成本与任务成功率", "API cost vs. task success", "平均每次尝试 API 成本（美元，越低越好）", "Mean API USD per attempt · lower is better"),
    "token": ("total_tokens_million", "03_token", "Token 消耗与任务成功率", "Token consumption vs. task success", "平均每次尝试 Token 消耗（百万，越低越好）", "Mean total Tokens per attempt (millions) · lower is better"),
}


def color(model: str) -> str:
    value = 0
    for char in model:
        value = (value * 31 + ord(char)) & 0xFFFFFFFF
    return COLORS[value % len(COLORS)]


def configure() -> None:
    plt.rcParams.update({"font.family": ["Microsoft YaHei", "Segoe UI", "DejaVu Sans"], "svg.fonttype": "none", "axes.unicode_minus": False, "text.parse_math": False})


def save(figure, destination: Path, stem: str) -> list[str]:
    destination.mkdir(parents=True, exist_ok=True)
    names = []
    for extension in ("png", "svg"):
        name = f"{stem}.{extension}"
        figure.savefig(destination / name, dpi=200, facecolor=figure.get_facecolor())
        names.append(name)
    plt.close(figure)
    return names


def close_labels(ax, rows: list[dict], x_key: str, language: str, segments: list) -> dict:
    figure = ax.figure
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    font = FontProperties(fname=font_manager.findfont(FontProperties(family="Microsoft YaHei")), size=8.3, weight="bold")
    axes_box = padded(ax.get_window_extent(renderer), -6)
    points = {row["id"]: ax.transData.transform((row[x_key], row["score"])) for row in rows}
    point_boxes = {key: Bbox.from_extents(x - 10, y - 10, x + 10, y + 10) for key, (x, y) in points.items()}
    paths = [MplPath(ax.transData.transform(segment)) for segment in segments]
    rows = sorted(rows, key=lambda row: (-sum(math.dist(points[row["id"]], other) < 200 for other in points.values()), -row["score"]))
    placed, annotations = [], []
    offsets = sorted(candidate_offsets(), key=lambda pair: math.hypot(*pair))
    offsets += [(x, y) for radius in (125, 155, 190) for x, y in ((radius, 0), (-radius, 0), (0, radius), (0, -radius))]
    for row in rows:
        effort = EFFORT.get(row["effort"], row["effort"]) if language == "zh-CN" else row["effort"].replace("not_reported", "not reported")
        name = f"{row['base_model']} · {effort} · {row['score']:.2f}%"
        # The named harness is part of the observation, never hidden in a legend.
        name += f"\n{row['agent']}" + (f" {row['agent_version']}" if row["agent_version"] else "")
        measure = ax.text(-999, -999, name, fontproperties=font, linespacing=1.2)
        box = measure.get_window_extent(renderer)
        width, height = box.width * 1.03, box.height * 1.04
        measure.remove()
        point_x, point_y = points[row["id"]]
        best = None
        for dx, dy in offsets:
            ha, va = offset_alignment(dx, dy)
            candidate = text_box(point_x + dx * figure.dpi / 72, point_y + dy * figure.dpi / 72, width, height, ha, va)
            outside = max(axes_box.x0 - candidate.x0, 0) + max(candidate.x1 - axes_box.x1, 0) + max(axes_box.y0 - candidate.y0, 0) + max(candidate.y1 - axes_box.y1, 0)
            overlaps = sum(padded(candidate, 3).overlaps(existing) for existing in placed)
            on_points = sum(padded(candidate, 2).overlaps(point_box) for key, point_box in point_boxes.items())
            on_lines = sum(path.intersects_bbox(padded(candidate, 2), filled=False) for path in paths)
            penalty = outside * 1e7 + overlaps * 1e8 + on_points * 1e7 + on_lines * 1e6 + math.hypot(dx, dy)
            if best is None or penalty < best[0]:
                best = (penalty, dx, dy, ha, va, candidate)
            if not (outside or overlaps or on_points or on_lines):
                break
        _, dx, dy, ha, va, box = best
        annotation = ax.annotate(name, (row[x_key], row["score"]), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontproperties=font, linespacing=1.2, color=color(row["model"]), zorder=6, arrowprops={"arrowstyle": "-", "linewidth": 0.65, "color": color(row["model"]), "alpha": 0.55, "shrinkA": 3, "shrinkB": 7} if math.hypot(dx, dy) > 20 else None)
        placed.append(padded(box, 3))
        annotations.append(annotation)
    figure.canvas.draw()
    actual = [Text.get_window_extent(item, renderer=figure.canvas.get_renderer()) for item in annotations]
    collisions = sum(padded(left, 1).overlaps(padded(right, 1)) for i, left in enumerate(actual) for right in actual[i + 1:])
    bounds = sum(box.x0 < axes_box.x0 or box.x1 > axes_box.x1 or box.y0 < axes_box.y0 or box.y1 > axes_box.y1 for box in actual)
    return {"label_collisions": int(collisions), "out_of_bounds_labels": int(bounds), "labels": len(actual)}


def scatter(payload: dict, metric: str, language: str, destination: Path, frontier: bool = False) -> tuple[list[str], dict]:
    zh = language == "zh-CN"
    key, stem, title_zh, title_en, x_zh, x_en = METRICS[metric]
    rows = [row for row in payload["rows"] if row[key] is not None]
    figure = plt.figure(figsize=(24, 13.5), dpi=200, facecolor="#fafbf9")
    ax = figure.add_axes([0.065, 0.16, 0.9, 0.70], facecolor="#ffffff")
    ax.set(xlim=(0, max(row[key] for row in rows) * 1.14), ylim=(0, 100))
    ax.set_yticks(range(0, 101, 10))
    ax.grid(color="#e6e9ee", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9ba8b6")
    ax.tick_params(labelsize=10, colors="#566273")
    ax.set_xlabel(x_zh if zh else x_en, fontsize=12, labelpad=15)
    ax.set_ylabel("任务成功率（%，越高越好）" if zh else "Task success rate (%) · higher is better", fontsize=12, labelpad=14)
    groups = defaultdict(list)
    segments = []
    for row in rows:
        groups[row["model"]].append(row)
        if row["ci95_half_width"] is not None:
            ax.errorbar(row[key], row["score"], yerr=[[row["score"] - row["ci95_low"]], [row["ci95_high"] - row["score"]]], color=color(row["model"]), alpha=0.55, linewidth=1, capsize=3, zorder=2)
            segments.append([(row[key], row["ci95_low"]), (row[key], row["ci95_high"])])
        ax.scatter(row[key], row["score"], s=37, color=color(row["model"]), edgecolor="white", linewidth=0.8, zorder=4)
    for group in groups.values():
        group.sort(key=lambda row: row["effort_order"])
        if len(group) > 1:
            ax.plot([row[key] for row in group], [row["score"] for row in group], color=color(group[0]["model"]), linewidth=1.5, alpha=0.85)
            segments.extend([[(left[key], left["score"]), (right[key], right["score"])] for left, right in zip(group, group[1:])])
    if frontier:
        edge = frontier_rows(rows, metric)
        xs, ys = [], []
        for index, row in enumerate(edge):
            if index:
                xs.append(row[key]); ys.append(edge[index - 1]["score"])
            xs.append(row[key]); ys.append(row["score"])
        ax.plot(xs, ys, color="#172033", linewidth=1.6, linestyle=(0, (5, 4)), zorder=3)
        ax.scatter([row[key] for row in edge], [row["score"] for row in edge], s=80, facecolors="none", edgecolors="#172033", linewidths=1.2, zorder=5)
        segments.extend([[(x1, y1), (x2, y2)] for x1, y1, x2, y2 in zip(xs, ys, xs[1:], ys[1:])])
        stem = {"subscription": "07_subscription_frontier", "api": "08_api_frontier", "token": "09_token_frontier"}[metric]
    metrics = close_labels(ax, rows, key, language, segments)
    if frontier:
        metrics["frontier_ids"] = [row["id"] for row in edge]
    title = title_zh if zh else title_en
    figure.text(0.055, 0.949, f"{payload['benchmark']} · {title}", fontsize=23, weight="bold", color="#182435")
    subtitle = "左上更好  |  点＝模型＋Agent＋思考档位  |  竖线＝官方 95% 区间" if zh else "Upper left is better  |  Point = model + agent + effort  |  Whiskers = owner-reported 95% interval"
    figure.text(0.055, 0.91, subtitle, fontsize=12, color="#536476")
    if frontier:
        figure.text(0.055, 0.875, "深色虚线＝左上前沿（斩杀线） · 按点值计算，不代表统计显著；阶梯不是模型插值。" if zh else "Dark dashed steps = upper-left Pareto frontier · Point estimates, not statistical significance or model interpolation.", fontsize=10, color="#27374b")
    if metric == "subscription":
        caveat = "套餐为跑满额度的折算估计，含历史实测与建模；并非当前固定配额。GLM 为年付、标准时段。" if zh else "Subscriptions are full-use estimates, not guaranteed current quotas. Historical calibration/modeling; GLM annual commitment, standard credits."
    elif metric == "api":
        caveat = "采用该次运行公布的总成本，不替换供应商、不按新价静默重算。失败尝试计入成本。" if zh else "Published cost of the evaluated run; no provider substitution or silent repricing. Failed attempts count toward spending."
    else:
        caveat = "采用官方总 Token，包含缓存输入与输出，不重复加思考 Token；参数规模和 Agent 配置影响效率。" if zh else "Published total Tokens, including cached input and output; no double counting of reasoning. Scale and agent settings affect efficiency."
    figure.text(0.055, 0.083, caveat, fontsize=10, color="#536476")
    trials = sorted({row["trials"] for row in rows if row["trials"]})
    source = f"Source: tbench.ai/?version={payload['snapshot']['benchmark_version']}  |  {payload['snapshot']['retrieved_at_utc']}  |  {len(rows)} configurations · trials/run: {', '.join(map(str, trials))}"
    figure.text(0.055, 0.048, source, fontsize=9, color="#657487")
    figure.text(0.055, 0.024, "各版本独立比较；Agent 版本缺失时仅连接同名系统，不代表构建版本已核实。" if zh else "Compare within one benchmark version. Effort curves link named systems; omitted agent builds remain unverified.", fontsize=8.5, color="#657487")
    return save(figure, destination, stem), metrics


def table_pages(payload: dict, metric: str, language: str, destination: Path) -> tuple[list[str], list[dict]]:
    zh = language == "zh-CN"
    rows = payload["rows"] if metric == "success" else ranked(payload["rows"], metric)
    page_size = 22 if metric == "success" else 18
    count = math.ceil(len(rows) / page_size)
    names, checks = [], []
    titles = {"subscription": ("套餐性价比数据", "Subscription value data"), "api": ("API 性价比数据", "API value data"), "token": ("Token 消耗数据", "Token consumption data"), "success": ("最终成功率数据", "Final success-rate data")}
    for page in range(count):
        chunk = rows[page * page_size:(page + 1) * page_size]
        figure = plt.figure(figsize=(24, 13.5), dpi=200, facecolor="#fafbf9")
        title = titles[metric][0 if zh else 1]
        figure.text(0.045, 0.947, f"{payload['benchmark']} · {title}  {page + 1}/{count}", fontsize=23, weight="bold", color="#182435")
        lead = "按每个成功任务的平均消耗排序，失败尝试也计入。并非反复重试必然成功。" if zh else "Ranked by average resources per success, including failed attempts. This is not a guarantee that retries solve every task."
        if metric == "success":
            lead = "该版缺少可核实的消耗汇总，仅保留成功率；本项目冻结快照，不代表上游停止修订。" if zh else "No verifiable aggregate consumption for this version. Frozen project snapshot; upstream may still revise its leaderboard."
        figure.text(0.045, 0.909, lead, fontsize=11, color="#536476")
        columns = [(0.045, "排名" if zh else "Rank"), (0.083, "模型 / Agent / 档位" if zh else "Model / agent / effort"), (0.46, "成功率 · 95% 区间" if zh else "Success · 95% interval")]
        if metric != "success":
            columns += [(0.60, "消耗 / 尝试" if zh else "Usage / attempt"), (0.72, "消耗 / 成功任务" if zh else "Usage / success"), (0.84, "相对最高消耗" if zh else "% of highest usage"), (0.94, "相对性价比" if zh else "Value index")]
        else:
            columns += [(0.66, "Agent 版本" if zh else "Agent version"), (0.82, "日期" if zh else "Date")]
        for x, text in columns:
            figure.text(x, 0.866, text, fontsize=9, weight="bold", color="#536476", ha="right" if x > 0.58 and metric != "success" else "left")
        row_height = 0.74 / page_size
        for index, row in enumerate(chunk):
            y = 0.823 - index * row_height
            figure.add_artist(plt.Line2D([0.04, 0.965], [y - row_height * 0.43] * 2, transform=figure.transFigure, color="#dfe5eb", linewidth=0.6))
            figure.text(0.045, y, str(page * page_size + index + 1), fontsize=11, color="#536476")
            effort = EFFORT.get(row["effort"], row["effort"]) if zh else row["effort"].replace("not_reported", "not reported")
            figure.text(0.083, y + 0.002, ("† " if row["source_verified"] is False else "") + row["base_model"], fontsize=10, weight="bold", color=color(row["model"]))
            detail = f"{row['agent']} · {effort}"
            if metric == "subscription":
                detail += " · " + (row["access_label"] or "")
            figure.text(0.083, y - row_height * 0.29, detail, fontsize=6.9 if metric == "subscription" else 7.5, color="#657487")
            ci = f" ± {row['ci95_half_width']:.2f}" if row["ci95_half_width"] is not None else ""
            figure.text(0.46, y, f"{row['score']:.2f}%{ci}", fontsize=11, color="#27374b")
            if metric == "success":
                figure.text(0.66, y, row["agent_version"] or ("未公布" if zh else "Not reported"), fontsize=9, color="#536476")
                figure.text(0.82, y, row["submission_date"] or "—", fontsize=10, color="#536476")
            else:
                key1, key2 = {"subscription": ("subscription_per_attempt", "subscription_per_success"), "api": ("api_per_attempt", "api_per_success"), "token": ("token_per_attempt", "tokens_per_success")}[metric]
                formatter = (lambda value: f"{value / 1e6:.3f}M") if metric == "token" else (lambda value: f"${value:.4f}")
                for x, text in [(0.60, formatter(row[key1])), (0.72, formatter(row[key2])), (0.84, f"{row['relative_cost_percent']:.2f}%"), (0.94, f"{row['relative_value_percent']:.2f}%")]:
                    figure.text(x, y, text, fontsize=11, color="#27374b", ha="right")
        footer = "套餐：历史跑满额度估计；GLM 年付、标准时段。金额非当前固定配额承诺。" if zh else "Subscriptions: historical full-use estimates; GLM annual commitment / standard credits. No fixed current quota is promised."
        if metric != "subscription":
            footer = "同一测试集、不同模型＋Agent＋档位。不同版本不混排；缺失项不补零。" if zh else "Same benchmark; distinct model + agent + effort configurations. Versions stay separate; missing values are not zero."
        if metric == "success":
            footer += "  † 上游标记为未核验。" if zh else "  † Marked unverified by the source."
        figure.text(0.045, 0.059, footer, fontsize=9.5, color="#657487")
        source_label = "harbor-framework/terminal-bench-website · pinned TB1 data (130be845)" if payload["snapshot"]["benchmark_version"] == "1.0" else f"tbench.ai/?version={payload['snapshot']['benchmark_version']}"
        figure.text(0.045, 0.03, f"Source: {source_label}  |  {payload['snapshot']['retrieved_at_utc']}", fontsize=9, color="#657487", url=payload["owner_url"])
        figure.canvas.draw()
        boxes = [item.get_window_extent(figure.canvas.get_renderer()) for item in figure.texts]
        overlaps = sum(left.overlaps(right) for index, left in enumerate(boxes) for right in boxes[index + 1:])
        outside = sum(box.x0 < 0 or box.y0 < 0 or box.x1 > figure.bbox.width or box.y1 > figure.bbox.height for box in boxes)
        if overlaps or outside:
            raise ValueError(f"Ranking text layout: {payload['benchmark']} {language} {metric} page {page+1}: overlaps={overlaps}, outside={outside}")
        names += save(figure, destination, f"{ {'subscription': '04', 'api': '05', 'token': '06', 'success': '00'}[metric]}_{metric}_ranking_{page + 1:02d}")
        checks.append({"table": metric, "page": page + 1, "rows": len(chunk), "text_collisions": int(overlaps), "out_of_bounds": int(outside)})
    return names, checks


def render_all(payload: dict, destination: Path) -> tuple[dict, dict]:
    configure()
    exports, validation = {}, {}
    for language in ("zh-CN", "en"):
        exports[language], validation[language] = [], {}
        for metric in ("subscription", "api", "token"):
            if payload["counts"][metric]:
                names, checks = scatter(payload, metric, language, destination / language)
                exports[language] += names
                validation[language][metric] = checks
                if checks["label_collisions"] or checks["out_of_bounds_labels"]:
                    raise ValueError(f"Static label layout failed: {payload['benchmark']} {language} {metric}: {checks}")
                names, checks = table_pages(payload, metric, language, destination / language)
                exports[language] += names
                validation[language][f"{metric}_ranking"] = checks
        if not any(payload["counts"].values()):
            names, checks = table_pages(payload, "success", language, destination / language)
            exports[language] += names
            validation[language]["success"] = checks
    return exports, validation


def frontier_table(payload: dict, language: str, destination: Path) -> tuple[list[str], list[dict]]:
    zh = language == "zh-CN"
    entries = [(metric, row) for metric in FRONTIER_KEYS for row in frontier_rows(payload["rows"], metric)]
    page_size = 18
    pages = max(1, math.ceil(len(entries) / page_size))
    names, checks = [], []
    titles = {"subscription": "套餐" if zh else "Subscription", "api": "API", "token": "Token"}
    for page in range(pages):
        chunk = entries[page * page_size:(page + 1) * page_size]
        figure = plt.figure(figsize=(24, 13.5), dpi=200, facecolor="#fafbf9")
        figure.text(.045, .947, f"{payload['benchmark']} · " + ("左上前沿配置列表" if zh else "Upper-left frontier configurations") + f"  {page+1}/{pages}", fontsize=23, weight="bold", color="#182435")
        figure.text(.045, .901, "三指标分别计算，按每次尝试消耗递增排列；同坐标配置全部保留。" if zh else "Three independent frontiers, ordered by resources per attempt. Equal-coordinate configurations are all retained.", fontsize=12, color="#536476")
        columns = [(.045, "指标" if zh else "Metric"), (.125, "模型 / 档位 / Agent" if zh else "Model / effort / agent"), (.505, "成功率 · 95% 区间" if zh else "Success · 95% interval"), (.69, "消耗 / 尝试" if zh else "Usage / attempt"), (.84, "消耗 / 成功任务" if zh else "Usage / success"), (.94, "尝试数" if zh else "Attempts")]
        for x, value in columns:
            figure.text(x, .85, value, fontsize=10, weight="bold", color="#536476", ha="right" if x >= .69 else "left")
        for index, (metric, row) in enumerate(chunk):
            y = .808 - index * .038
            effort = EFFORT.get(row["effort"], row["effort"]) if zh else row["effort"].replace("not_reported", "not reported")
            figure.add_artist(plt.Line2D([.04, .965], [y-.016]*2, transform=figure.transFigure, color="#dfe5eb", linewidth=.6))
            figure.text(.045, y, titles[metric], fontsize=10, color="#27374b")
            figure.text(.125, y+.002, f"{row['base_model']} · {effort}", fontsize=10, weight="bold", color=color(row["model"]))
            detail = row["agent"]
            if metric == "subscription":
                detail += f" · {row['access_label']} · {row['access_confidence']}"
            figure.text(.125, y-.009, detail, fontsize=6.8, color="#657487")
            ci = f" ± {row['ci95_half_width']:.2f}" if row["ci95_half_width"] is not None else ""
            figure.text(.505, y, f"{row['score']:.2f}%{ci}", fontsize=11, color="#27374b")
            key2 = {"subscription": "subscription_per_success", "api": "api_per_success", "token": "tokens_per_success"}[metric]
            formatter = (lambda v: "—" if v is None else f"{v / 1e6:.3f}M") if metric == "token" else (lambda v: "—" if v is None else f"${v:.4f}")
            for x, value in [(.69, formatter(row[FRONTIER_KEYS[metric]])), (.84, formatter(row[key2])), (.94, str(row["trials"] or "—"))]:
                figure.text(x, y, value, fontsize=11, color="#27374b", ha="right")
        if not entries:
            figure.text(.125, .68, "套餐、API、Token：均无可核实的消耗汇总，无法计算左上前沿。\n成功率排名已单独保留；缺失数据不按零处理。" if zh else "Subscription / API / Tokens: verifiable consumption is unavailable.\nNo frontier can be computed. Success-rate rankings remain in separate exports.", fontsize=18, color="#536476", linespacing=1.8)
        figure.text(.045, .086, "没有其他配置同时做到消耗不高、成功率不低，且至少一项更好。按点值计算，不代表统计显著。" if zh else "No other configuration uses no more resources and achieves no less success, with one strict improvement. Point estimates, not statistical significance.", fontsize=10, color="#536476")
        figure.text(.045, .057, "套餐为充分使用额度的估算；不同版本独立计算。Token 单位：百万。" if zh else "Subscriptions assume full utilization of estimated allowances. Versions remain separate. Token unit: millions.", fontsize=9, color="#657487")
        figure.text(.045, .03, f"Source: Terminal-Bench · {payload['snapshot']['retrieved_at_utc']}", fontsize=9, color="#657487", url=payload["owner_url"])
        figure.canvas.draw()
        boxes = [item.get_window_extent(figure.canvas.get_renderer()) for item in figure.texts]
        overlaps = sum(left.overlaps(right) for i, left in enumerate(boxes) for right in boxes[i+1:])
        outside = sum(box.x0 < 0 or box.y0 < 0 or box.x1 > figure.bbox.width or box.y1 > figure.bbox.height for box in boxes)
        if overlaps or outside:
            raise ValueError(f"Frontier table layout {payload['benchmark']} {language}: {overlaps=}, {outside=}")
        names += save(figure, destination, f"10_frontier_list_{page+1:02d}")
        checks.append({"page": page+1, "rows": len(chunk), "text_collisions": int(overlaps), "out_of_bounds": int(outside)})
    return names, checks


def render_frontiers(payload: dict, destination: Path) -> tuple[dict, dict]:
    configure()
    exports, checks = {}, {}
    for language in ("zh-CN", "en"):
        exports[language], checks[language] = [], {}
        for metric in FRONTIER_KEYS:
            if payload["counts"][metric]:
                names, layout = scatter(payload, metric, language, destination / language, frontier=True)
                if layout["label_collisions"] or layout["out_of_bounds_labels"]:
                    raise ValueError(f"Frontier label layout failed: {payload['benchmark']} {language} {metric}")
                exports[language] += names
                checks[language][f"{metric}_frontier"] = layout
        names, layout = frontier_table(payload, language, destination / language)
        exports[language] += names
        checks[language]["frontier_list"] = layout
    return exports, checks
