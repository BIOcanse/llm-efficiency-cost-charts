const SVG_NAMESPACE = "http://www.w3.org/2000/svg";

const SERIES_COLORS = [
  "#315efb",
  "#e76f2e",
  "#7b4ce2",
  "#168c6a",
  "#d63c72",
  "#8a6a17",
  "#087ea4",
  "#b34b9b",
  "#4e7d2b",
  "#c5522d",
  "#5368a6",
  "#7a5a9e",
];

let nextChartId = 1;

function svgElement(name, attributes = {}) {
  const element = document.createElementNS(SVG_NAMESPACE, name);
  Object.entries(attributes).forEach(([key, value]) => {
    element.setAttribute(key, String(value));
  });
  return element;
}

function clamp(value, minimum, maximum) {
  return Math.min(maximum, Math.max(minimum, value));
}

function modelColor(model) {
  let hash = 0;
  let index = 0;
  while (index < model.length) {
    hash = (hash * 31 + model.charCodeAt(index)) >>> 0;
    index += 1;
  }
  return SERIES_COLORS[hash % SERIES_COLORS.length];
}

function rowKey(row) {
  return `${row.model}\u0000${row.effort}`;
}

function groupByModel(rows) {
  const groups = new Map();
  rows.forEach((row) => {
    if (!groups.has(row.model)) {
      groups.set(row.model, []);
    }
    groups.get(row.model).push(row);
  });
  groups.forEach((modelRows) => {
    modelRows.sort(
      (left, right) =>
        Number(left.effort_order) - Number(right.effort_order) ||
        Number(left.score) - Number(right.score),
    );
  });
  return groups;
}

function paretoKeys(rows, xKey) {
  const ordered = [...rows].sort(
    (left, right) =>
      Number(left[xKey]) - Number(right[xKey]) ||
      Number(right.score) - Number(left.score),
  );
  const result = new Set();
  let bestScore = Number.NEGATIVE_INFINITY;
  ordered.forEach((row) => {
    const score = Number(row.score);
    if (score > bestScore) {
      result.add(rowKey(row));
      bestScore = score;
    }
  });
  return result;
}

function linearTicks(minimum, maximum, count) {
  const ticks = [];
  let index = 0;
  while (index <= count) {
    ticks.push(minimum + ((maximum - minimum) * index) / count);
    index += 1;
  }
  return ticks;
}

function boxesOverlap(left, right, padding = 0) {
  return !(
    left.x + left.width + padding <= right.x ||
    right.x + right.width + padding <= left.x ||
    left.y + left.height + padding <= right.y ||
    right.y + right.height + padding <= left.y
  );
}

function boxContainsPoint(box, point, padding = 0) {
  return (
    point.x >= box.x - padding &&
    point.x <= box.x + box.width + padding &&
    point.y >= box.y - padding &&
    point.y <= box.y + box.height + padding
  );
}

function pointToBoxDistance(point, box) {
  const dx = Math.max(box.x - point.x, 0, point.x - box.x - box.width);
  const dy = Math.max(box.y - point.y, 0, point.y - box.y - box.height);
  return Math.hypot(dx, dy);
}

function lineSegmentsIntersect(first, second) {
  const denominator =
    (second.y2 - second.y1) * (first.x2 - first.x1) -
    (second.x2 - second.x1) * (first.y2 - first.y1);
  if (Math.abs(denominator) < 0.00001) {
    return false;
  }
  const numeratorA =
    (second.x2 - second.x1) * (first.y1 - second.y1) -
    (second.y2 - second.y1) * (first.x1 - second.x1);
  const numeratorB =
    (first.x2 - first.x1) * (first.y1 - second.y1) -
    (first.y2 - first.y1) * (first.x1 - second.x1);
  const a = numeratorA / denominator;
  const b = numeratorB / denominator;
  return a >= 0 && a <= 1 && b >= 0 && b <= 1;
}

function segmentIntersectsBox(segment, box, padding = 0) {
  const expanded = {
    x: box.x - padding,
    y: box.y - padding,
    width: box.width + padding * 2,
    height: box.height + padding * 2,
  };
  const first = { x: segment.x1, y: segment.y1 };
  const second = { x: segment.x2, y: segment.y2 };
  if (
    boxContainsPoint(expanded, first) ||
    boxContainsPoint(expanded, second)
  ) {
    return true;
  }
  if (
    Math.max(segment.x1, segment.x2) < expanded.x ||
    Math.min(segment.x1, segment.x2) > expanded.x + expanded.width ||
    Math.max(segment.y1, segment.y2) < expanded.y ||
    Math.min(segment.y1, segment.y2) > expanded.y + expanded.height
  ) {
    return false;
  }
  const left = expanded.x;
  const right = expanded.x + expanded.width;
  const top = expanded.y;
  const bottom = expanded.y + expanded.height;
  return [
    { x1: left, y1: top, x2: right, y2: top },
    { x1: right, y1: top, x2: right, y2: bottom },
    { x1: right, y1: bottom, x2: left, y2: bottom },
    { x1: left, y1: bottom, x2: left, y2: top },
  ].some((edge) => lineSegmentsIntersect(segment, edge));
}

function closestPointOnBox(point, box) {
  return {
    x: clamp(point.x, box.x, box.x + box.width),
    y: clamp(point.y, box.y, box.y + box.height),
  };
}

function createButton(className) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = className;
  return button;
}

export class InteractiveScatterChart {
  constructor(container) {
    this.container = container;
    this.chartId = nextChartId;
    nextChartId += 1;
    this.data = [];
    this.config = null;
    this.metric = "";
    this.fullBounds = null;
    this.view = null;
    this.selectedModel = "";
    this.hoveredRow = null;
    this.pinnedRow = null;
    this.dragState = null;
    this.pointElements = [];
    this.lineElements = [];
    this.labelElements = [];
    this.labelLeaderElements = [];
    this.dimensions = null;
    this.buildStructure();
    this.bindControls();
    this.resizeObserver = new ResizeObserver(() => this.render());
    this.resizeObserver.observe(this.plot);
  }

  buildStructure() {
    this.container.replaceChildren();

    this.toolbar = document.createElement("div");
    this.toolbar.className = "interactive-chart-toolbar";

    this.modelLabel = document.createElement("label");
    this.modelLabel.className = "interactive-model-control";
    this.modelLabelText = document.createElement("span");
    this.modelSelect = document.createElement("select");
    this.modelSelect.className = "interactive-model-select";
    this.modelLabel.append(this.modelLabelText, this.modelSelect);

    this.zoomControls = document.createElement("div");
    this.zoomControls.className = "interactive-zoom-controls";
    this.zoomOutButton = createButton("interactive-chart-button");
    this.zoomOutButton.textContent = "−";
    this.zoomInButton = createButton("interactive-chart-button");
    this.zoomInButton.textContent = "+";
    this.resetButton = createButton("interactive-chart-button reset");
    this.zoomControls.append(
      this.zoomOutButton,
      this.zoomInButton,
      this.resetButton,
    );
    this.toolbar.append(this.modelLabel, this.zoomControls);

    this.plot = document.createElement("div");
    this.plot.className = "interactive-chart-plot";
    this.svg = svgElement("svg", {
      class: "interactive-chart-svg",
      role: "group",
    });
    this.tooltip = document.createElement("div");
    this.tooltip.className = "interactive-chart-tooltip";
    this.tooltip.setAttribute("role", "tooltip");
    this.tooltip.hidden = true;
    this.plot.append(this.svg, this.tooltip);

    this.hint = document.createElement("p");
    this.hint.className = "interactive-chart-hint";
    this.readout = document.createElement("p");
    this.readout.className = "interactive-chart-readout";
    this.readout.setAttribute("aria-live", "polite");

    this.container.append(
      this.toolbar,
      this.plot,
      this.hint,
      this.readout,
    );
  }

  bindControls() {
    this.modelSelect.addEventListener("change", () => {
      this.selectedModel = this.modelSelect.value;
      this.renderPlot();
    });
    this.zoomInButton.addEventListener("click", () => this.zoom(0.72));
    this.zoomOutButton.addEventListener("click", () => this.zoom(1.38));
    this.resetButton.addEventListener("click", () => this.resetView());

    this.plot.addEventListener(
      "wheel",
      (event) => {
        if (!this.view || !this.dimensions) {
          return;
        }
        event.preventDefault();
        const bounds = this.plot.getBoundingClientRect();
        const plot = this.dimensions.plot;
        const scaleX = this.dimensions.width / bounds.width;
        const scaleY = this.dimensions.height / bounds.height;
        const localX = event.clientX - bounds.left;
        const localY = event.clientY - bounds.top;
        const svgX = localX * scaleX;
        const svgY = localY * scaleY;
        const centerX = clamp((svgX - plot.left) / plot.width, 0, 1);
        const centerY = clamp((svgY - plot.top) / plot.height, 0, 1);
        const factor = clamp(Math.exp(event.deltaY * 0.0015), 0.78, 1.28);
        this.zoom(factor, centerX, centerY);
      },
      { passive: false },
    );

    this.plot.addEventListener("pointerdown", (event) => {
      if (!this.view || event.target.closest(".interactive-point")) {
        return;
      }
      this.dragState = {
        pointerId: event.pointerId,
        x: event.clientX,
        y: event.clientY,
        view: { ...this.view },
      };
      this.plot.setPointerCapture(event.pointerId);
      this.plot.classList.add("is-panning");
    });

    this.plot.addEventListener("pointermove", (event) => {
      if (!this.dragState || !this.dimensions) {
        return;
      }
      const bounds = this.plot.getBoundingClientRect();
      const deltaX =
        ((event.clientX - this.dragState.x) / bounds.width) *
        this.dimensions.width;
      const deltaY =
        ((event.clientY - this.dragState.y) / bounds.height) *
        this.dimensions.height;
      const plot = this.dimensions.plot;
      const original = this.dragState.view;
      const xSpan = original.xMax - original.xMin;
      const ySpan = original.yMax - original.yMin;
      this.view = {
        xMin: original.xMin - (deltaX / plot.width) * xSpan,
        xMax: original.xMax - (deltaX / plot.width) * xSpan,
        yMin: original.yMin + (deltaY / plot.height) * ySpan,
        yMax: original.yMax + (deltaY / plot.height) * ySpan,
      };
      this.clampView();
      this.renderPlot();
    });

    const finishPan = (event) => {
      if (!this.dragState || this.dragState.pointerId !== event.pointerId) {
        return;
      }
      this.dragState = null;
      this.plot.classList.remove("is-panning");
      if (this.plot.hasPointerCapture(event.pointerId)) {
        this.plot.releasePointerCapture(event.pointerId);
      }
    };
    this.plot.addEventListener("pointerup", finishPan);
    this.plot.addEventListener("pointercancel", finishPan);
  }

  update(rows, config) {
    const metricChanged = this.metric !== config.metric;
    this.metric = config.metric;
    this.config = config;
    this.data = rows.map((row) => ({
      ...row,
      score: Number(row.score),
      [config.xKey]: Number(row[config.xKey]),
      effort_order: Number(row.effort_order ?? 0),
    }));
    this.groups = groupByModel(this.data);
    this.frontier = paretoKeys(this.data, config.xKey);
    this.fullBounds = this.calculateBounds();
    if (metricChanged || !this.view) {
      this.view = { ...this.fullBounds };
      this.selectedModel = "";
      this.hoveredRow = null;
      this.pinnedRow = null;
    }
    this.populateModelSelect();
    this.updateLocalizedControls();
    this.render();
  }

  calculateBounds() {
    const xValues = this.data.map((row) => Number(row[this.config.xKey]));
    const yValues = this.data.map((row) => Number(row.score));
    const xMaximum = Math.max(...xValues);
    const yMinimum = Math.min(...yValues);
    const yMaximum = Math.max(...yValues);
    return {
      xMin: 0,
      xMax: xMaximum * 1.045,
      yMin: Math.max(0, yMinimum - 2),
      yMax: Math.min(100, yMaximum + 2),
    };
  }

  populateModelSelect() {
    const current = this.selectedModel;
    const models = [...this.groups.keys()].sort((left, right) =>
      left.localeCompare(right),
    );
    this.modelSelect.replaceChildren();
    const allOption = document.createElement("option");
    allOption.value = "";
    allOption.textContent = this.config.allModelsLabel;
    this.modelSelect.append(allOption);
    models.forEach((model) => {
      const option = document.createElement("option");
      option.value = model;
      option.textContent = model;
      this.modelSelect.append(option);
    });
    this.selectedModel = models.includes(current) ? current : "";
    this.modelSelect.value = this.selectedModel;
  }

  updateLocalizedControls() {
    this.modelLabelText.textContent = this.config.modelControlLabel;
    this.zoomOutButton.setAttribute("aria-label", this.config.zoomOutLabel);
    this.zoomInButton.setAttribute("aria-label", this.config.zoomInLabel);
    this.resetButton.textContent = this.config.resetLabel;
    this.resetButton.setAttribute("aria-label", this.config.resetLabel);
    this.hint.textContent = this.config.interactionHint;
    if (!this.hoveredRow && !this.pinnedRow) {
      this.readout.textContent = this.config.readoutHint;
    }
  }

  resetView() {
    if (!this.fullBounds) {
      return;
    }
    this.view = { ...this.fullBounds };
    this.hoveredRow = null;
    this.pinnedRow = null;
    this.hideTooltip();
    this.renderPlot();
  }

  zoom(factor, centerX = 0.5, centerY = 0.5) {
    if (!this.view || !this.fullBounds) {
      return;
    }
    const xSpan = this.view.xMax - this.view.xMin;
    const ySpan = this.view.yMax - this.view.yMin;
    const nextXSpan = clamp(
      xSpan * factor,
      (this.fullBounds.xMax - this.fullBounds.xMin) / 40,
      this.fullBounds.xMax - this.fullBounds.xMin,
    );
    const nextYSpan = clamp(
      ySpan * factor,
      (this.fullBounds.yMax - this.fullBounds.yMin) / 20,
      this.fullBounds.yMax - this.fullBounds.yMin,
    );
    const anchorX = this.view.xMin + xSpan * centerX;
    const anchorY = this.view.yMax - ySpan * centerY;
    this.view = {
      xMin: anchorX - nextXSpan * centerX,
      xMax: anchorX + nextXSpan * (1 - centerX),
      yMin: anchorY - nextYSpan * (1 - centerY),
      yMax: anchorY + nextYSpan * centerY,
    };
    this.clampView();
    this.renderPlot();
  }

  clampView() {
    const full = this.fullBounds;
    const xSpan = Math.min(this.view.xMax - this.view.xMin, full.xMax - full.xMin);
    const ySpan = Math.min(this.view.yMax - this.view.yMin, full.yMax - full.yMin);
    let xMin = this.view.xMin;
    let yMin = this.view.yMin;
    xMin = clamp(xMin, full.xMin, full.xMax - xSpan);
    yMin = clamp(yMin, full.yMin, full.yMax - ySpan);
    this.view = {
      xMin,
      xMax: xMin + xSpan,
      yMin,
      yMax: yMin + ySpan,
    };
  }

  render() {
    if (!this.config || !this.data.length) {
      return;
    }
    const width = Math.max(1180, Math.round(this.plot.clientWidth || 1320));
    const height = Math.round((width * 9) / 16);
    const margins = { left: 82, right: 34, top: 30, bottom: 82 };
    this.dimensions = {
      width,
      height,
      plot: {
        left: margins.left,
        top: margins.top,
        width: width - margins.left - margins.right,
        height: height - margins.top - margins.bottom,
      },
    };
    this.svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    this.svg.style.height = `${height}px`;
    this.renderPlot();
  }

  renderPlot() {
    if (!this.dimensions || !this.view) {
      return;
    }
    const { width, height, plot } = this.dimensions;
    const clipId = `interactive-chart-clip-${this.chartId}`;
    this.svg.replaceChildren();
    this.svg.setAttribute("aria-labelledby", `${clipId}-title ${clipId}-desc`);

    const title = svgElement("title", { id: `${clipId}-title` });
    title.textContent = this.config.accessibleTitle;
    const description = svgElement("desc", { id: `${clipId}-desc` });
    description.textContent = this.config.accessibleDescription;
    const definitions = svgElement("defs");
    const clipPath = svgElement("clipPath", { id: clipId });
    clipPath.append(
      svgElement("rect", {
        x: plot.left,
        y: plot.top,
        width: plot.width,
        height: plot.height,
      }),
    );
    definitions.append(clipPath);
    this.svg.append(title, description, definitions);

    const scaleX = (value) =>
      plot.left +
      ((Number(value) - this.view.xMin) /
        (this.view.xMax - this.view.xMin)) *
        plot.width;
    const scaleY = (value) =>
      plot.top +
      ((this.view.yMax - Number(value)) /
        (this.view.yMax - this.view.yMin)) *
        plot.height;
    this.scales = { x: scaleX, y: scaleY };

    const tickCount = 6;
    const grid = svgElement("g", { class: "interactive-grid" });
    linearTicks(this.view.yMin, this.view.yMax, tickCount).forEach((value) => {
      const y = scaleY(value);
      grid.append(
        svgElement("line", {
          x1: plot.left,
          x2: plot.left + plot.width,
          y1: y,
          y2: y,
        }),
      );
      const label = svgElement("text", {
        x: plot.left - 10,
        y: y + 4,
        "text-anchor": "end",
      });
      label.textContent = this.config.formatScoreTick(value);
      grid.append(label);
    });
    linearTicks(this.view.xMin, this.view.xMax, tickCount).forEach((value) => {
      const x = scaleX(value);
      grid.append(
        svgElement("line", {
          x1: x,
          x2: x,
          y1: plot.top,
          y2: plot.top + plot.height,
        }),
      );
      const label = svgElement("text", {
        x,
        y: plot.top + plot.height + 24,
        "text-anchor": "middle",
      });
      label.textContent = this.config.formatXAxisTick(value);
      grid.append(label);
    });
    this.svg.append(grid);

    const axes = svgElement("g", { class: "interactive-axes" });
    axes.append(
      svgElement("line", {
        x1: plot.left,
        x2: plot.left,
        y1: plot.top,
        y2: plot.top + plot.height,
      }),
      svgElement("line", {
        x1: plot.left,
        x2: plot.left + plot.width,
        y1: plot.top + plot.height,
        y2: plot.top + plot.height,
      }),
    );
    const xLabel = svgElement("text", {
      x: plot.left + plot.width / 2,
      y: height - 18,
      "text-anchor": "middle",
      class: "interactive-axis-title",
    });
    xLabel.textContent = this.config.xAxisLabel;
    const yLabel = svgElement("text", {
      x: 18,
      y: plot.top + plot.height / 2,
      "text-anchor": "middle",
      transform: `rotate(-90 18 ${plot.top + plot.height / 2})`,
      class: "interactive-axis-title",
    });
    yLabel.textContent = this.config.yAxisLabel;
    axes.append(xLabel, yLabel);
    this.svg.append(axes);

    const marks = svgElement("g", {
      class: "interactive-marks",
      "clip-path": `url(#${clipId})`,
    });
    this.lineElements = [];
    this.groups.forEach((rows, model) => {
      if (rows.length < 2) {
        return;
      }
      const line = svgElement("polyline", {
        class: "interactive-series-line",
        points: rows
          .map(
            (row) =>
              `${scaleX(row[this.config.xKey])},${scaleY(row.score)}`,
          )
          .join(" "),
        stroke: modelColor(model),
        "data-model": model,
      });
      this.lineElements.push(line);
      marks.append(line);
    });

    this.pointElements = [];
    this.data.forEach((row) => {
      const key = rowKey(row);
      const point = svgElement("circle", {
        class: "interactive-point",
        cx: scaleX(row[this.config.xKey]),
        cy: scaleY(row.score),
        r: 5,
        fill: modelColor(row.model),
        "data-model": row.model,
        "data-key": key,
        tabindex: 0,
        role: "button",
        "aria-label": this.config.pointAriaLabel(row),
      });
      if (this.frontier.has(key)) {
        point.classList.add("is-frontier");
      }
      point.addEventListener("pointerenter", () => {
        this.hoveredRow = row;
        this.showTooltip(row);
        this.refreshEmphasis();
      });
      point.addEventListener("pointerleave", () => {
        this.hoveredRow = null;
        if (this.pinnedRow) {
          this.showTooltip(this.pinnedRow);
        } else {
          this.hideTooltip();
        }
        this.refreshEmphasis();
      });
      point.addEventListener("focus", () => {
        this.hoveredRow = row;
        this.showTooltip(row);
        this.refreshEmphasis();
      });
      point.addEventListener("blur", () => {
        this.hoveredRow = null;
        if (this.pinnedRow) {
          this.showTooltip(this.pinnedRow);
        } else {
          this.hideTooltip();
        }
        this.refreshEmphasis();
      });
      point.addEventListener("click", () => this.togglePinnedRow(row));
      point.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          this.togglePinnedRow(row);
        }
        if (event.key === "Escape") {
          this.pinnedRow = null;
          this.hideTooltip();
          this.refreshEmphasis();
        }
      });
      this.pointElements.push(point);
      marks.append(point);
    });
    this.svg.append(marks);
    this.renderPointLabels(scaleX, scaleY, plot);
    this.refreshEmphasis();
    const displayRow = this.hoveredRow || this.pinnedRow;
    if (displayRow) {
      this.showTooltip(displayRow);
    } else {
      this.hideTooltip();
    }
  }

  renderPointLabels(scaleX, scaleY, plot) {
    const pointLocations = this.data
      .map((row) => ({
        row,
        x: scaleX(row[this.config.xKey]),
        y: scaleY(row.score),
      }))
      .filter(
        (point) =>
          point.x >= plot.left &&
          point.x <= plot.left + plot.width &&
          point.y >= plot.top &&
          point.y <= plot.top + plot.height,
      );
    const lineSegments = [];
    this.groups.forEach((rows) => {
      rows.slice(1).forEach((row, index) => {
        const previous = rows[index];
        lineSegments.push({
          x1: scaleX(previous[this.config.xKey]),
          y1: scaleY(previous.score),
          x2: scaleX(row[this.config.xKey]),
          y2: scaleY(row.score),
        });
      });
    });

    const leaderGroup = svgElement("g", {
      class: "interactive-label-leaders",
      "clip-path": `url(#interactive-chart-clip-${this.chartId})`,
    });
    const labelGroup = svgElement("g", {
      class: "interactive-point-labels",
      "clip-path": `url(#interactive-chart-clip-${this.chartId})`,
    });
    this.svg.append(leaderGroup, labelGroup);

    const measured = pointLocations.map((point) => {
      const label = svgElement("text", {
        class: "interactive-point-label",
        x: -10000,
        y: -10000,
        fill: modelColor(point.row.model),
        "data-model": point.row.model,
        "data-key": rowKey(point.row),
      });
      label.textContent =
        `${point.row.model} · ${this.config.effortLabel(point.row.effort)}`;
      labelGroup.append(label);
      const measuredWidth =
        typeof label.getComputedTextLength === "function"
          ? label.getComputedTextLength()
          : label.textContent.length * 6;
      return {
        ...point,
        label,
        width: Math.ceil(measuredWidth) + 2,
        height: 13,
        density: pointLocations.reduce((total, other) => {
          if (other === point) {
            return total;
          }
          const distance = Math.hypot(other.x - point.x, other.y - point.y);
          return total + Math.max(0, 110 - distance);
        }, 0),
      };
    });

    measured.sort(
      (left, right) =>
        Number(right.row.model === this.selectedModel) -
          Number(left.row.model === this.selectedModel) ||
        right.density - left.density ||
        right.y - left.y ||
        left.x - right.x,
    );

    const placedBoxes = [];
    const innerBounds = {
      x: plot.left + 4,
      y: plot.top + 4,
      width: plot.width - 8,
      height: plot.height - 8,
    };
    this.labelElements = [];
    this.labelLeaderElements = [];
    const associationDistances = [];

    measured.forEach((item) => {
      const candidates = this.labelCandidates(item, innerBounds);
      let bestCandidate = candidates[0];
      let bestScore = Number.POSITIVE_INFINITY;
      candidates.forEach((candidate, candidateIndex) => {
        let score =
          pointToBoxDistance(item, candidate) * 8 + candidateIndex * 0.08;
        placedBoxes.forEach((placed) => {
          if (boxesOverlap(candidate, placed, 2)) {
            score += 100000;
          }
        });
        pointLocations.forEach((point) => {
          if (
            rowKey(point.row) !== rowKey(item.row) &&
            boxContainsPoint(candidate, point, 5)
          ) {
            score += 30000;
          }
        });
        lineSegments.forEach((segment) => {
          if (segmentIntersectsBox(segment, candidate, 1)) {
            score += 220;
          }
        });
        if (score < bestScore) {
          bestCandidate = candidate;
          bestScore = score;
        }
      });

      placedBoxes.push({ ...bestCandidate, key: rowKey(item.row) });
      item.label.setAttribute("x", bestCandidate.x);
      item.label.setAttribute("y", bestCandidate.y + bestCandidate.height - 2);
      this.labelElements.push(item.label);

      const leaderEnd = closestPointOnBox(item, bestCandidate);
      const leaderDistance = Math.hypot(
        leaderEnd.x - item.x,
        leaderEnd.y - item.y,
      );
      associationDistances.push(leaderDistance);
      if (leaderDistance > 10) {
        const leader = svgElement("line", {
          class: "interactive-label-leader",
          x1: item.x,
          y1: item.y,
          x2: leaderEnd.x,
          y2: leaderEnd.y,
          stroke: modelColor(item.row.model),
          "data-model": item.row.model,
          "data-key": rowKey(item.row),
        });
        leaderGroup.append(leader);
        this.labelLeaderElements.push(leader);
      }
    });

    const labelCollisionCount = placedBoxes.reduce(
      (total, box, index) =>
        total +
        placedBoxes
          .slice(index + 1)
          .filter((other) => boxesOverlap(box, other, 1)).length,
      0,
    );
    this.svg.dataset.visibleLabels = String(placedBoxes.length);
    this.svg.dataset.labelCollisions = String(labelCollisionCount);
    this.svg.dataset.labelAverageDistance = (
      associationDistances.reduce((total, value) => total + value, 0) /
      Math.max(1, associationDistances.length)
    ).toFixed(1);
    this.svg.dataset.labelMaxDistance = Math.max(
      0,
      ...associationDistances,
    ).toFixed(1);
  }

  labelCandidates(item, bounds) {
    const result = [];
    const seen = new Set();
    const addCandidate = (x, y) => {
      const candidate = {
        x: clamp(x, bounds.x, bounds.x + bounds.width - item.width),
        y: clamp(y, bounds.y, bounds.y + bounds.height - item.height),
        width: item.width,
        height: item.height,
      };
      const key = `${Math.round(candidate.x)}:${Math.round(candidate.y)}`;
      if (!seen.has(key)) {
        seen.add(key);
        result.push(candidate);
      }
    };
    const preferRight = item.x < bounds.x + bounds.width * 0.72;
    const verticalOffsets = [
      0, -15, 15, -30, 30, -45, 45, -60, 60, -76, 76, -92, 92, -108, 108,
    ];
    verticalOffsets.forEach((offset) => {
      const rightX = item.x + 9;
      const leftX = item.x - item.width - 9;
      const y = item.y + offset - item.height / 2;
      if (preferRight) {
        addCandidate(rightX, y);
        addCandidate(leftX, y);
      } else {
        addCandidate(leftX, y);
        addCandidate(rightX, y);
      }
    });
    const horizontalOffsets = [
      0, -24, 24, -48, 48, -72, 72, -96, 96, -120, 120, -152, 152,
      -184, 184,
    ];
    horizontalOffsets.forEach((offset) => {
      addCandidate(
        item.x + offset - item.width / 2,
        item.y - item.height - 9,
      );
      addCandidate(item.x + offset - item.width / 2, item.y + 9);
    });
    let radius = 30;
    while (radius <= 210) {
      let angleIndex = 0;
      while (angleIndex < 16) {
        const angle = (Math.PI * 2 * angleIndex) / 16;
        const cosine = Math.cos(angle);
        const sine = Math.sin(angle);
        const x =
          item.x +
          cosine * radius -
          (cosine < 0 ? item.width : 0);
        const y = item.y + sine * radius - item.height / 2;
        addCandidate(x, y);
        angleIndex += 1;
      }
      radius += 18;
    }
    return result;
  }

  togglePinnedRow(row) {
    this.pinnedRow =
      this.pinnedRow && rowKey(this.pinnedRow) === rowKey(row) ? null : row;
    if (this.pinnedRow) {
      this.showTooltip(this.pinnedRow);
    } else if (this.hoveredRow) {
      this.showTooltip(this.hoveredRow);
    } else {
      this.hideTooltip();
    }
    this.refreshEmphasis();
  }

  refreshEmphasis() {
    if (!this.config) {
      return;
    }
    const activeRow = this.hoveredRow || this.pinnedRow;
    const activeModel = activeRow?.model || this.selectedModel;
    const activeKey = activeRow ? rowKey(activeRow) : "";

    this.lineElements.forEach((line) => {
      const isActive = !activeModel || line.dataset.model === activeModel;
      line.classList.toggle("is-muted", !isActive);
      line.classList.toggle(
        "is-active",
        Boolean(activeModel) && line.dataset.model === activeModel,
      );
    });
    this.pointElements.forEach((point) => {
      const isModelActive =
        !activeModel || point.dataset.model === activeModel;
      point.classList.toggle("is-muted", !isModelActive);
      point.classList.toggle(
        "is-active-model",
        Boolean(activeModel) && point.dataset.model === activeModel,
      );
      point.classList.toggle(
        "is-active-point",
        Boolean(activeKey) && point.dataset.key === activeKey,
      );
    });
    this.labelElements.forEach((label) => {
      const isModelActive =
        !activeModel || label.dataset.model === activeModel;
      label.classList.toggle("is-muted", !isModelActive);
      label.classList.toggle(
        "is-active-model",
        Boolean(activeModel) && label.dataset.model === activeModel,
      );
      label.classList.toggle(
        "is-active-point",
        Boolean(activeKey) && label.dataset.key === activeKey,
      );
    });
    this.labelLeaderElements.forEach((leader) => {
      const isModelActive =
        !activeModel || leader.dataset.model === activeModel;
      leader.classList.toggle("is-muted", !isModelActive);
      leader.classList.toggle(
        "is-active",
        Boolean(activeModel) && leader.dataset.model === activeModel,
      );
    });

    const displayRow = this.hoveredRow || this.pinnedRow;
    this.readout.textContent = displayRow
      ? this.config.readoutText(displayRow)
      : this.config.readoutHint;
  }

  showTooltip(row) {
    if (!this.scales || !this.dimensions) {
      return;
    }
    this.tooltip.replaceChildren();
    const heading = document.createElement("strong");
    heading.textContent = `${row.model} · ${this.config.effortLabel(row.effort)}`;
    this.tooltip.append(heading);
    this.config.tooltipRows(row).forEach(([label, value]) => {
      const line = document.createElement("span");
      const labelElement = document.createElement("b");
      labelElement.textContent = `${label}: `;
      line.append(labelElement, document.createTextNode(value));
      this.tooltip.append(line);
    });
    this.tooltip.hidden = false;

    const plotBounds = this.plot.getBoundingClientRect();
    const svgBounds = this.svg.getBoundingClientRect();
    const pointX =
      (this.scales.x(row[this.config.xKey]) / this.dimensions.width) *
      svgBounds.width;
    const pointY =
      (this.scales.y(row.score) / this.dimensions.height) * svgBounds.height;
    const tooltipBounds = this.tooltip.getBoundingClientRect();
    const left = clamp(
      pointX + 14,
      8,
      Math.max(8, plotBounds.width - tooltipBounds.width - 8),
    );
    const preferredTop = pointY - tooltipBounds.height - 14;
    const top = clamp(
      preferredTop,
      8,
      Math.max(8, svgBounds.height - tooltipBounds.height - 8),
    );
    this.tooltip.style.left = `${left}px`;
    this.tooltip.style.top = `${top}px`;
  }

  hideTooltip() {
    this.tooltip.hidden = true;
  }
}
