# WebGPU scatter rendering specification

Snapshot baseline: **2026-07-24**

## Purpose

Move frequently redrawn scatter marks away from the SVG DOM while preserving
the released chart's permanent labels, axes, accessibility, and interaction.
The chart contains only tens of points, so WebGPU is not used to justify
removing information or changing the visual result.

## Layering

```text
interactive chart plot
  -> WebGPU canvas: visible same-model line segments and point discs
  -> SVG: grid, axes, permanent labels, label leaders, transparent point hit targets
  -> HTML: tooltip
```

`site/assets/webgpu-scatter-layer.js` owns only the canvas device, pipeline,
buffers, and draw submission. `site/assets/interactive-scatter.js` owns chart
state and supplies an already-resolved scene in chart coordinates.

## Backend contract

- Requested backend: `webgpu`.
- Successful state: `data-renderer="webgpu"`.
- Unavailable, initialization-failed, or device-lost state:
  `data-renderer="svg-fallback"`.
- Fallback is explicit and uses the existing visible SVG lines and points.
- One adapter/device promise is shared across all three charts.
- The vertex buffer is reused and grows only when the current scene exceeds its
  capacity.
- No external JavaScript, shader, font, or runtime dependency is loaded.

## Geometry

- Line segments are expanded into two triangles in chart coordinates so their
  width is deterministic across devices.
- Point discs are triangle fans.
- Pareto points receive a dark outer disc before their colored inner disc.
- Inactive emphasis uses the same opacity values as the SVG fallback.
- Canvas dimensions follow the chart view box and device-pixel ratio; uniforms
  transform chart coordinates into WebGPU clip space.

## Interaction boundary

The WebGPU canvas has `pointer-events: none`. SVG circles remain the only
pointer and keyboard targets, even when their visible paint is transparent.
Tooltips, pinned state, filtering, label layout, and accessibility therefore do
not depend on GPU readback or hit testing.

## Acceptance

- WebGPU and SVG fallback show the same filtered model curves, point colors,
  point radii, Pareto outlines, and emphasis state.
- Switching model provider, frontier scope, language, zoom, or pan cannot leave stale GPU
  geometry.
- Device loss switches to the SVG fallback without removing labels or
  interaction.
- Three charts reuse one WebGPU device and produce no console errors.
