let sharedDevicePromise = null;

function requestSharedDevice() {
  if (sharedDevicePromise) {
    return sharedDevicePromise;
  }
  sharedDevicePromise = (async () => {
    if (!globalThis.navigator?.gpu) {
      throw new Error("WebGPU is unavailable");
    }
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) {
      throw new Error("No WebGPU adapter is available");
    }
    const device = await adapter.requestDevice();
    return {
      device,
      format: navigator.gpu.getPreferredCanvasFormat(),
    };
  })();
  return sharedDevicePromise;
}

function nextBufferCapacity(requiredBytes) {
  let capacity = 4096;
  while (capacity < requiredBytes) {
    capacity *= 2;
  }
  return capacity;
}

function appendVertex(target, x, y, color) {
  target.push(x, y, color[0], color[1], color[2], color[3]);
}

function appendTriangle(target, first, second, third, color) {
  appendVertex(target, first.x, first.y, color);
  appendVertex(target, second.x, second.y, color);
  appendVertex(target, third.x, third.y, color);
}

function appendLine(target, line) {
  const deltaX = line.x2 - line.x1;
  const deltaY = line.y2 - line.y1;
  const length = Math.hypot(deltaX, deltaY);
  if (length < 0.0001 || line.color[3] <= 0) {
    return;
  }
  const halfWidth = line.width / 2;
  const perpendicularX = (-deltaY / length) * halfWidth;
  const perpendicularY = (deltaX / length) * halfWidth;
  const firstLeft = {
    x: line.x1 + perpendicularX,
    y: line.y1 + perpendicularY,
  };
  const firstRight = {
    x: line.x1 - perpendicularX,
    y: line.y1 - perpendicularY,
  };
  const secondLeft = {
    x: line.x2 + perpendicularX,
    y: line.y2 + perpendicularY,
  };
  const secondRight = {
    x: line.x2 - perpendicularX,
    y: line.y2 - perpendicularY,
  };
  appendTriangle(target, firstLeft, secondLeft, secondRight, line.color);
  appendTriangle(target, firstLeft, secondRight, firstRight, line.color);
}

function appendDisc(target, centerX, centerY, radius, color) {
  if (radius <= 0 || color[3] <= 0) {
    return;
  }
  const segments = 18;
  let index = 0;
  while (index < segments) {
    const firstAngle = (Math.PI * 2 * index) / segments;
    const secondAngle = (Math.PI * 2 * (index + 1)) / segments;
    appendTriangle(
      target,
      { x: centerX, y: centerY },
      {
        x: centerX + Math.cos(firstAngle) * radius,
        y: centerY + Math.sin(firstAngle) * radius,
      },
      {
        x: centerX + Math.cos(secondAngle) * radius,
        y: centerY + Math.sin(secondAngle) * radius,
      },
      color,
    );
    index += 1;
  }
}

function buildVertices(scene) {
  const vertices = [];
  scene.lines.forEach((line) => appendLine(vertices, line));
  scene.points.forEach((point) => {
    if (point.outlineColor && point.outlineWidth > 0) {
      appendDisc(
        vertices,
        point.x,
        point.y,
        point.radius + point.outlineWidth,
        point.outlineColor,
      );
    }
    appendDisc(
      vertices,
      point.x,
      point.y,
      point.radius,
      point.color,
    );
  });
  return new Float32Array(vertices);
}

export class WebGpuScatterLayer {
  constructor(canvas, { onBackendChange } = {}) {
    this.canvas = canvas;
    this.onBackendChange = onBackendChange;
    this.backend = "initializing";
    this.width = 1;
    this.height = 1;
    this.pixelRatio = 1;
    this.scene = { lines: [], points: [] };
    this.device = null;
    this.context = null;
    this.pipeline = null;
    this.uniformBuffer = null;
    this.vertexBuffer = null;
    this.vertexBufferCapacity = 0;
    this.bindGroup = null;
    this.initialization = this.initialize();
  }

  async initialize() {
    try {
      const { device, format } = await requestSharedDevice();
      const context = this.canvas.getContext("webgpu");
      if (!context) {
        throw new Error("WebGPU canvas context is unavailable");
      }
      context.configure({
        device,
        format,
        alphaMode: "premultiplied",
      });
      const shader = device.createShaderModule({
        label: "Scatter mark shader",
        code: `
          struct CanvasUniforms {
            size: vec2f,
          }

          struct VertexOutput {
            @builtin(position) position: vec4f,
            @location(0) color: vec4f,
          }

          @group(0) @binding(0) var<uniform> canvas: CanvasUniforms;

          @vertex
          fn vertexMain(
            @location(0) position: vec2f,
            @location(1) color: vec4f,
          ) -> VertexOutput {
            var output: VertexOutput;
            let normalized = position / canvas.size;
            output.position = vec4f(
              normalized.x * 2.0 - 1.0,
              1.0 - normalized.y * 2.0,
              0.0,
              1.0,
            );
            output.color = color;
            return output;
          }

          @fragment
          fn fragmentMain(input: VertexOutput) -> @location(0) vec4f {
            return input.color;
          }
        `,
      });
      const pipeline = device.createRenderPipeline({
        label: "Scatter mark pipeline",
        layout: "auto",
        vertex: {
          module: shader,
          entryPoint: "vertexMain",
          buffers: [
            {
              arrayStride: 24,
              attributes: [
                {
                  shaderLocation: 0,
                  offset: 0,
                  format: "float32x2",
                },
                {
                  shaderLocation: 1,
                  offset: 8,
                  format: "float32x4",
                },
              ],
            },
          ],
        },
        fragment: {
          module: shader,
          entryPoint: "fragmentMain",
          targets: [
            {
              format,
              blend: {
                color: {
                  srcFactor: "src-alpha",
                  dstFactor: "one-minus-src-alpha",
                  operation: "add",
                },
                alpha: {
                  srcFactor: "one",
                  dstFactor: "one-minus-src-alpha",
                  operation: "add",
                },
              },
            },
          ],
        },
        primitive: {
          topology: "triangle-list",
        },
      });
      const uniformBuffer = device.createBuffer({
        label: "Scatter canvas uniforms",
        size: 16,
        usage:
          globalThis.GPUBufferUsage.UNIFORM |
          globalThis.GPUBufferUsage.COPY_DST,
      });
      this.device = device;
      this.context = context;
      this.pipeline = pipeline;
      this.uniformBuffer = uniformBuffer;
      this.bindGroup = device.createBindGroup({
        label: "Scatter canvas bind group",
        layout: pipeline.getBindGroupLayout(0),
        entries: [
          {
            binding: 0,
            resource: { buffer: uniformBuffer },
          },
        ],
      });
      device.lost.then((information) =>
        this.useFallback(information.message || "WebGPU device lost"),
      );
      this.setBackend("webgpu");
      this.resize(this.width, this.height, this.pixelRatio);
      this.render(this.scene);
      return true;
    } catch (error) {
      this.useFallback(
        error instanceof Error ? error.message : "WebGPU initialization failed",
      );
      return false;
    }
  }

  setBackend(backend) {
    if (this.backend === backend) {
      return;
    }
    this.backend = backend;
    this.canvas.hidden = backend !== "webgpu";
    if (backend === "webgpu") {
      delete this.canvas.dataset.rendererError;
    }
    this.onBackendChange?.(backend);
  }

  useFallback(reason = "WebGPU unavailable") {
    this.canvas.dataset.rendererError = reason;
    this.setBackend("svg-fallback");
  }

  resize(width, height, pixelRatio = globalThis.devicePixelRatio || 1) {
    this.width = Math.max(1, Number(width));
    this.height = Math.max(1, Number(height));
    this.pixelRatio = Math.max(1, Number(pixelRatio));
    const physicalWidth = Math.max(1, Math.round(this.width * this.pixelRatio));
    const physicalHeight = Math.max(
      1,
      Math.round(this.height * this.pixelRatio),
    );
    if (
      this.canvas.width !== physicalWidth ||
      this.canvas.height !== physicalHeight
    ) {
      this.canvas.width = physicalWidth;
      this.canvas.height = physicalHeight;
    }
    this.canvas.style.width = `${this.width}px`;
    this.canvas.style.height = `${this.height}px`;
    if (this.backend === "webgpu") {
      this.render(this.scene);
    }
  }

  render(scene) {
    this.scene = scene;
    if (
      this.backend !== "webgpu" ||
      !this.device ||
      !this.context ||
      !this.pipeline
    ) {
      return false;
    }
    try {
      const vertices = buildVertices(scene);
      const requiredBytes = Math.max(4, vertices.byteLength);
      if (requiredBytes > this.vertexBufferCapacity) {
        this.vertexBuffer?.destroy();
        this.vertexBufferCapacity = nextBufferCapacity(requiredBytes);
        this.vertexBuffer = this.device.createBuffer({
          label: "Scatter vertices",
          size: this.vertexBufferCapacity,
          usage:
            globalThis.GPUBufferUsage.VERTEX |
            globalThis.GPUBufferUsage.COPY_DST,
        });
      }
      if (vertices.byteLength > 0) {
        this.device.queue.writeBuffer(this.vertexBuffer, 0, vertices);
      }
      this.device.queue.writeBuffer(
        this.uniformBuffer,
        0,
        new Float32Array([this.width, this.height, 0, 0]),
      );
      const encoder = this.device.createCommandEncoder({
        label: "Scatter render encoder",
      });
      const pass = encoder.beginRenderPass({
        label: "Scatter render pass",
        colorAttachments: [
          {
            view: this.context.getCurrentTexture().createView(),
            clearValue: { r: 0, g: 0, b: 0, a: 0 },
            loadOp: "clear",
            storeOp: "store",
          },
        ],
      });
      if (scene.clip) {
        const clipLeft = Number(scene.clip.x ?? scene.clip.left ?? 0);
        const clipTop = Number(scene.clip.y ?? scene.clip.top ?? 0);
        const clipX = Math.max(
          0,
          Math.floor(clipLeft * this.pixelRatio),
        );
        const clipY = Math.max(
          0,
          Math.floor(clipTop * this.pixelRatio),
        );
        const clipWidth = Math.max(
          1,
          Math.min(
            this.canvas.width - clipX,
            Math.ceil(scene.clip.width * this.pixelRatio),
          ),
        );
        const clipHeight = Math.max(
          1,
          Math.min(
            this.canvas.height - clipY,
            Math.ceil(scene.clip.height * this.pixelRatio),
          ),
        );
        pass.setScissorRect(clipX, clipY, clipWidth, clipHeight);
      }
      pass.setPipeline(this.pipeline);
      pass.setBindGroup(0, this.bindGroup);
      if (vertices.length > 0) {
        pass.setVertexBuffer(0, this.vertexBuffer);
        pass.draw(vertices.length / 6);
      }
      pass.end();
      this.device.queue.submit([encoder.finish()]);
      return true;
    } catch (error) {
      this.useFallback(
        error instanceof Error ? error.message : "WebGPU render failed",
      );
      return false;
    }
  }

  destroy() {
    this.vertexBuffer?.destroy();
    this.uniformBuffer?.destroy();
    this.vertexBuffer = null;
    this.uniformBuffer = null;
    this.context?.unconfigure();
  }
}
