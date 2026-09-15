import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

import { createSceneControls } from "./src/sceneControls.js";

const app = getRequiredElement("#app");
const previewShell = getRequiredElement("#preview-shell");
const RENDER_FPS = 30;
const RENDER_TIMELINE_TOTAL_FRAMES = 90;
const TIMELINE_DURATION_MS = (RENDER_TIMELINE_TOTAL_FRAMES / RENDER_FPS) * 1000;
const EXPORT_WIDTH = 2048;
const EXPORT_HEIGHT = 1152;
const EXPORT_ASPECT_RATIO = EXPORT_WIDTH / EXPORT_HEIGHT;
const EXPORT_RENDER_SCALES = new Set([1, 2]);
const DEFAULT_EXPORT_RENDER_SCALE = 1;
const ZIP_VERSION_NEEDED = 20;
const ZIP_STORE_METHOD = 0;
const TWO_PI = Math.PI * 2;

const query = new URLSearchParams(window.location.search);
const renderOptions = readRenderOptions(query);

applyRenderLayout();

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x02050a, 0.045);

const camera = new THREE.PerspectiveCamera(42, EXPORT_ASPECT_RATIO, 0.1, 100);
const renderer = new THREE.WebGLRenderer({
  antialias: true,
  preserveDrawingBuffer: true,
});
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.domElement.className = "webgl-canvas scene-canvas";
previewShell.prepend(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.08, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 2.4;
controls.maxDistance = 10;
controls.enabled = false;
controls.update();

const sceneObjects = createTemplateScene();
scene.add(sceneObjects.root);

const crc32Table = createCrc32Table();
let freeCameraEnabled = false;
let renderControls = null;
let currentRenderFrame = 0;
let timelinePlaying = !renderOptions.isExportMode;
let timelineStartTime = null;
let isSceneReady = false;

const cameraControlsPanel = createSceneControls({
  camera,
  isFreeCameraEnabled: () => freeCameraEnabled,
  onToggleFreeCamera: setFreeCameraEnabled,
});

resizeRenderers();
renderControls = bindRenderControls();
installSceneExportBridge();
setRenderFrame(0, { playing: timelinePlaying });
isSceneReady = true;
syncRenderControls();
requestAnimationFrame(animate);

function getRequiredElement(selector) {
  const element = document.querySelector(selector);
  if (!element) {
    throw new Error(`Missing required element: ${selector}`);
  }

  return element;
}

function readRenderOptions(params) {
  const exportMode = params.get("exportMode");
  const renderScale = Number(params.get("renderScale"));

  return {
    isExportMode:
      exportMode === "composite" || exportMode === "composite-transparent",
    renderScale: Number.isFinite(renderScale)
      ? THREE.MathUtils.clamp(renderScale, 1, 16)
      : DEFAULT_EXPORT_RENDER_SCALE,
  };
}

function applyRenderLayout() {
  if (!renderOptions.isExportMode) {
    return;
  }

  app.classList.add("app-export");
  document.body.classList.add("is-export-mode");
  previewShell.style.width =
    `${Math.round(EXPORT_WIDTH * renderOptions.renderScale)}px`;
  previewShell.style.height =
    `${Math.round(EXPORT_HEIGHT * renderOptions.renderScale)}px`;
}

function createTemplateScene() {
  const root = new THREE.Group();
  const titleGroup = new THREE.Group();
  const accentGroup = new THREE.Group();
  const cubes = [];
  const rings = [];

  const ambient = new THREE.AmbientLight(0x8fb6ff, 0.62);
  const keyLight = new THREE.DirectionalLight(0xffffff, 2.8);
  keyLight.position.set(4.2, 5.4, 6.4);
  const rimLight = new THREE.PointLight(0x61d394, 13, 12);
  rimLight.position.set(-3.2, 1.8, 3.6);
  root.add(ambient, keyLight, rimLight);

  const grid = createFloorGrid();
  grid.position.y = -1.45;
  root.add(grid);

  const starfield = createStarfield();
  root.add(starfield);

  const titleTexture = createTitleTexture();
  const titlePlane = new THREE.Mesh(
    new THREE.PlaneGeometry(5.8, 1.45),
    new THREE.MeshBasicMaterial({
      map: titleTexture,
      transparent: true,
      depthWrite: false,
      side: THREE.DoubleSide,
    })
  );
  titlePlane.position.set(0, 0.35, 0.35);
  titleGroup.add(titlePlane);
  titleGroup.add(createTitleFrame());
  root.add(titleGroup);

  const torus = new THREE.Mesh(
    new THREE.TorusKnotGeometry(1.42, 0.022, 260, 10, 2, 3),
    new THREE.MeshStandardMaterial({
      color: 0x55e6ff,
      emissive: 0x0a5c72,
      emissiveIntensity: 1.2,
      roughness: 0.28,
      metalness: 0.78,
      transparent: true,
      opacity: 0.92,
    })
  );
  torus.position.set(0, 0.12, -0.88);
  accentGroup.add(torus);

  const outerRingMaterial = new THREE.MeshBasicMaterial({
    color: 0xf5c451,
    transparent: true,
    opacity: 0.44,
    side: THREE.DoubleSide,
  });
  for (let index = 0; index < 3; index += 1) {
    const ring = new THREE.Mesh(
      new THREE.RingGeometry(1.72 + index * 0.18, 1.73 + index * 0.18, 160),
      outerRingMaterial.clone()
    );
    ring.position.set(0, 0.1, -0.9 - index * 0.04);
    ring.rotation.x = Math.PI * 0.5;
    rings.push(ring);
    accentGroup.add(ring);
  }

  const cubeGeometry = new THREE.BoxGeometry(0.18, 0.18, 0.18);
  const cubeMaterials = [0x61d394, 0x55e6ff, 0xf5c451, 0xff7a90].map(
    (color) =>
      new THREE.MeshStandardMaterial({
        color,
        emissive: color,
        emissiveIntensity: 0.28,
        roughness: 0.34,
        metalness: 0.5,
        transparent: true,
        opacity: 0.78,
      })
  );
  for (let index = 0; index < 18; index += 1) {
    const cube = new THREE.Mesh(
      cubeGeometry,
      cubeMaterials[index % cubeMaterials.length].clone()
    );
    cube.userData.motion = {
      phase: (index / 18) * TWO_PI,
      radius: 2.0 + (index % 4) * 0.28,
      vertical: 0.55 + (index % 3) * 0.12,
      speed: 0.72 + (index % 5) * 0.06,
    };
    cubes.push(cube);
    accentGroup.add(cube);
  }

  root.add(accentGroup);

  return {
    root,
    titleGroup,
    accentGroup,
    torus,
    rings,
    cubes,
    grid,
    starfield,
    rimLight,
  };
}

function createTitleTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = 2048;
  canvas.height = 512;
  const context = canvas.getContext("2d");
  if (!context) {
    throw new Error("Canvas 2D context is unavailable.");
  }

  const glow = context.createRadialGradient(1024, 256, 40, 1024, 256, 900);
  glow.addColorStop(0, "rgba(85, 230, 255, 0.28)");
  glow.addColorStop(0.5, "rgba(97, 211, 148, 0.1)");
  glow.addColorStop(1, "rgba(0, 0, 0, 0)");
  context.fillStyle = glow;
  context.fillRect(0, 0, canvas.width, canvas.height);

  context.textAlign = "center";
  context.textBaseline = "middle";
  context.font = "800 164px system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif";
  context.shadowColor = "rgba(85, 230, 255, 0.58)";
  context.shadowBlur = 34;
  context.fillStyle = "#f4fbff";
  context.fillText("vibe motion 3d", 1024, 250);

  context.shadowBlur = 0;
  context.strokeStyle = "rgba(245, 196, 81, 0.82)";
  context.lineWidth = 3;
  context.beginPath();
  context.moveTo(494, 365);
  context.lineTo(1554, 365);
  context.stroke();

  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 8;
  return texture;
}

function createTitleFrame() {
  const width = 5.88;
  const height = 1.48;
  const z = 0.31;
  const points = [
    -width / 2,
    -height / 2,
    z,
    width / 2,
    -height / 2,
    z,
    width / 2,
    -height / 2,
    z,
    width / 2,
    height / 2,
    z,
    width / 2,
    height / 2,
    z,
    -width / 2,
    height / 2,
    z,
    -width / 2,
    height / 2,
    z,
    -width / 2,
    -height / 2,
    z,
  ];
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.Float32BufferAttribute(points, 3));
  const material = new THREE.LineBasicMaterial({
    color: 0x87f3ff,
    transparent: true,
    opacity: 0.44,
  });
  const frame = new THREE.LineSegments(geometry, material);
  frame.position.set(0, 0.35, 0.05);
  return frame;
}

function createFloorGrid() {
  const size = 9;
  const divisions = 28;
  const halfSize = size / 2;
  const step = size / divisions;
  const centerIndex = divisions / 2;
  const points = [];

  for (let index = 0; index <= divisions; index += 1) {
    if (index === centerIndex) {
      continue;
    }

    const offset = -halfSize + index * step;
    points.push(
      -halfSize,
      0,
      offset,
      halfSize,
      0,
      offset,
      offset,
      0,
      -halfSize,
      offset,
      0,
      halfSize
    );
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.Float32BufferAttribute(points, 3));

  const material = new THREE.LineBasicMaterial({
    color: 0x1e3540,
    transparent: true,
    opacity: 0.32,
  });

  return new THREE.LineSegments(geometry, material);
}

function createStarfield() {
  const count = 520;
  const random = createSeededRandom(7);
  const positions = new Float32Array(count * 3);

  for (let index = 0; index < count; index += 1) {
    const radius = 7 + random() * 18;
    const theta = random() * TWO_PI;
    const phi = Math.acos(2 * random() - 1);
    positions[index * 3] = radius * Math.sin(phi) * Math.cos(theta);
    positions[index * 3 + 1] = radius * Math.cos(phi);
    positions[index * 3 + 2] = radius * Math.sin(phi) * Math.sin(theta);
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const material = new THREE.PointsMaterial({
    color: 0xcfe8ff,
    size: 0.03,
    sizeAttenuation: true,
    transparent: true,
    opacity: 0.72,
  });
  return new THREE.Points(geometry, material);
}

function createSeededRandom(seed) {
  let value = seed >>> 0;

  return () => {
    value += 0x6d2b79f5;
    let result = value;
    result = Math.imul(result ^ (result >>> 15), result | 1);
    result ^= result + Math.imul(result ^ (result >>> 7), result | 61);
    return ((result ^ (result >>> 14)) >>> 0) / 4294967296;
  };
}

function clampFrame(frame) {
  if (!Number.isFinite(frame)) {
    return 0;
  }

  return THREE.MathUtils.clamp(
    Math.round(frame),
    0,
    RENDER_TIMELINE_TOTAL_FRAMES - 1
  );
}

function getFrameProgress(frame) {
  if (RENDER_TIMELINE_TOTAL_FRAMES <= 1) {
    return 0;
  }

  return clampFrame(frame) / (RENDER_TIMELINE_TOTAL_FRAMES - 1);
}

function setSceneStateForFrame(frame) {
  const progress = getFrameProgress(frame);
  const timeSeconds = (clampFrame(frame) / RENDER_FPS);
  const loop = progress * TWO_PI;

  sceneObjects.titleGroup.position.y = Math.sin(loop) * 0.08;
  sceneObjects.titleGroup.rotation.x = Math.sin(loop * 0.7) * 0.035;
  sceneObjects.titleGroup.rotation.y = Math.sin(loop) * 0.16;
  sceneObjects.titleGroup.rotation.z = Math.sin(loop * 1.3) * 0.02;

  sceneObjects.accentGroup.rotation.y = loop * 0.34;
  sceneObjects.torus.rotation.x = timeSeconds * 0.58;
  sceneObjects.torus.rotation.y = timeSeconds * 1.08;
  sceneObjects.torus.rotation.z = timeSeconds * 0.22;

  sceneObjects.rings.forEach((ring, index) => {
    ring.rotation.z = loop * (index % 2 === 0 ? 0.5 : -0.42) + index * 0.65;
    ring.material.opacity = 0.28 + 0.14 * Math.sin(loop + index * 0.9);
  });

  sceneObjects.cubes.forEach((cube, index) => {
    const motion = cube.userData.motion;
    const angle = loop * motion.speed + motion.phase;
    cube.position.set(
      Math.cos(angle) * motion.radius,
      -0.28 + Math.sin(angle * 1.8 + index * 0.2) * motion.vertical,
      -0.72 + Math.sin(angle) * 1.04
    );
    cube.rotation.set(
      timeSeconds * (0.76 + index * 0.013),
      timeSeconds * (1.08 + index * 0.017),
      angle
    );
    const pulse = 0.5 + 0.5 * Math.sin(loop * 2 + motion.phase);
    cube.scale.setScalar(0.74 + pulse * 0.42);
    cube.material.opacity = 0.46 + pulse * 0.34;
  });

  sceneObjects.grid.position.z = (progress * 2.4) % 0.42;
  sceneObjects.starfield.rotation.y = loop * 0.045;
  sceneObjects.rimLight.position.x = Math.sin(loop) * 3.4;
  sceneObjects.rimLight.position.z = 3.6 + Math.cos(loop) * 1.4;

  if (!freeCameraEnabled) {
    const cameraAngle = loop * 0.18 - 0.46;
    camera.position.set(
      Math.sin(cameraAngle) * 0.62,
      1.0 + Math.sin(loop * 0.65) * 0.16,
      6.05 + Math.cos(loop * 0.85) * 0.22
    );
    camera.lookAt(0, 0.1, -0.1);
  }
}

function readPreviewSize() {
  return {
    width: Math.max(1, Math.round(previewShell.clientWidth || EXPORT_WIDTH)),
    height: Math.max(1, Math.round(previewShell.clientHeight || EXPORT_HEIGHT)),
  };
}

function resizeRenderersTo({ width, height, pixelRatio }) {
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setPixelRatio(pixelRatio);
  renderer.setSize(width, height, false);
}

function resizeRenderers() {
  const { width, height } = readPreviewSize();
  resizeRenderersTo({
    width,
    height,
    pixelRatio: renderOptions.isExportMode
      ? 1
      : Math.min(window.devicePixelRatio || 1, 2),
  });
}

function renderScene() {
  if (freeCameraEnabled) {
    controls.update();
  }
  cameraControlsPanel.update();
  renderer.render(scene, camera);
}

function setRenderFrame(frame, { playing = false } = {}) {
  if (freeCameraEnabled) {
    setFreeCameraEnabled(false);
  }

  currentRenderFrame = clampFrame(frame);
  timelinePlaying = Boolean(playing);
  timelineStartTime = null;
  setSceneStateForFrame(currentRenderFrame);
  renderScene();
  syncRenderControls();
}

function animate(now) {
  requestAnimationFrame(animate);

  if (renderOptions.isExportMode) {
    return;
  }

  if (freeCameraEnabled) {
    renderScene();
    return;
  }

  if (!timelinePlaying) {
    return;
  }

  if (timelineStartTime === null) {
    timelineStartTime = now - (currentRenderFrame / RENDER_FPS) * 1000;
  }

  const elapsedMs = (now - timelineStartTime) % TIMELINE_DURATION_MS;
  currentRenderFrame = clampFrame((elapsedMs / 1000) * RENDER_FPS);
  setSceneStateForFrame(currentRenderFrame);
  renderScene();
  syncRenderControls();
}

function handleWindowResize() {
  resizeRenderers();
  setSceneStateForFrame(currentRenderFrame);
  renderScene();
}

window.addEventListener("resize", handleWindowResize, false);

function setFreeCameraEnabled(enabled) {
  const nextEnabled = Boolean(enabled);
  if (freeCameraEnabled === nextEnabled) {
    return;
  }

  freeCameraEnabled = nextEnabled;
  if (freeCameraEnabled) {
    timelinePlaying = false;
    timelineStartTime = null;
    controls.enabled = true;
    controls.update();
  } else {
    controls.enabled = false;
    controls.screenSpacePanning = false;
    setRenderFrame(currentRenderFrame, { playing: false });
    return;
  }

  renderScene();
  syncRenderControls();
}

function setFreeCameraPanning(enabled) {
  if (!freeCameraEnabled) {
    return;
  }

  controls.screenSpacePanning = Boolean(enabled);
  controls.mouseButtons.LEFT = enabled ? THREE.MOUSE.PAN : THREE.MOUSE.ROTATE;
}

function isEditingText(element) {
  return (
    element instanceof HTMLInputElement ||
    element instanceof HTMLTextAreaElement ||
    element instanceof HTMLSelectElement ||
    element?.isContentEditable
  );
}

function syncFreeCameraPan(event, panning) {
  if (!freeCameraEnabled || event.code !== "Space" || isEditingText(event.target)) {
    return;
  }

  event.preventDefault();
  setFreeCameraPanning(panning);
}

window.addEventListener("keydown", (event) => {
  if (!event.repeat) {
    syncFreeCameraPan(event, true);
  }
});
window.addEventListener("keyup", (event) => syncFreeCameraPan(event, false));
window.addEventListener("blur", () => setFreeCameraPanning(false));

function bindRenderControls() {
  const frameInput = document.querySelector("#render-frame");
  const frameRange = document.querySelector("#render-frame-range");
  const frameCount = document.querySelector("#render-frame-count");
  const exportFrameButton = document.querySelector("#export-frame");
  const exportSequenceButton = document.querySelector("#export-sequence");
  const exportScaleSelect = document.querySelector("#export-scale");
  const exportStatus = document.querySelector("#export-status");

  if (!frameInput || !frameRange || !frameCount) {
    return null;
  }

  const controlsPanel = {
    frameInput,
    frameRange,
    frameCount,
    exportFrameButton,
    exportSequenceButton,
    exportScaleSelect,
    exportStatus,
  };

  exportScaleSelect.value = String(DEFAULT_EXPORT_RENDER_SCALE);
  frameInput.addEventListener("change", () => {
    setRenderFrame(Number(frameInput.value), { playing: false });
  });
  frameRange.addEventListener("input", () => {
    setRenderFrame(Number(frameRange.value), { playing: false });
  });
  exportFrameButton.addEventListener("click", () => {
    void exportCurrentFrame();
  });
  exportSequenceButton.addEventListener("click", () => {
    void exportSequence();
  });

  return controlsPanel;
}

function syncRenderControls() {
  if (!renderControls) {
    return;
  }

  const maxFrame = RENDER_TIMELINE_TOTAL_FRAMES - 1;
  renderControls.frameInput.max = String(maxFrame);
  renderControls.frameInput.value = String(currentRenderFrame);
  renderControls.frameRange.max = String(maxFrame);
  renderControls.frameRange.value = String(currentRenderFrame);
  renderControls.frameCount.value =
    `${currentRenderFrame + 1} / ${RENDER_TIMELINE_TOTAL_FRAMES}`;
  setExportButtonsDisabled(!isSceneReady);
}

function setExportButtonsDisabled(disabled) {
  if (!renderControls) {
    return;
  }

  renderControls.exportFrameButton.disabled =
    disabled || renderOptions.isExportMode;
  renderControls.exportSequenceButton.disabled =
    disabled || renderOptions.isExportMode;
}

function readExportRenderScale() {
  const value = Number(renderControls?.exportScaleSelect?.value);
  return EXPORT_RENDER_SCALES.has(value) ? value : DEFAULT_EXPORT_RENDER_SCALE;
}

function readExportSize(renderScale) {
  return {
    width: Math.round(EXPORT_WIDTH * renderScale),
    height: Math.round(EXPORT_HEIGHT * renderScale),
  };
}

async function exportCurrentFrame() {
  if (!renderControls?.exportStatus) {
    return;
  }

  const renderScale = readExportRenderScale();
  const exportSize = readExportSize(renderScale);
  const filename =
    `vibe-motion-3d-frame-${String(currentRenderFrame).padStart(4, "0")}.png`;
  const status = renderControls.exportStatus;

  setExportButtonsDisabled(true);
  status.textContent =
    `Exporting ${exportSize.width}x${exportSize.height} frame `
    + `${currentRenderFrame + 1}/${RENDER_TIMELINE_TOTAL_FRAMES}...`;

  try {
    const blob = await renderFixedSizePngBlob({
      frame: currentRenderFrame,
      renderScale,
    });
    downloadBlob(blob, filename);
    status.textContent = `PNG exported at ${exportSize.width}x${exportSize.height}.`;
  } catch (error) {
    status.textContent = `Export failed: ${error.message}`;
  } finally {
    setExportButtonsDisabled(false);
  }
}

async function exportSequence() {
  if (!renderControls?.exportStatus) {
    return;
  }

  const renderScale = readExportRenderScale();
  const exportSize = readExportSize(renderScale);
  const status = renderControls.exportStatus;
  const filename =
    `vibe-motion-3d-frames-${String(RENDER_TIMELINE_TOTAL_FRAMES).padStart(4, "0")}.zip`;

  setExportButtonsDisabled(true);
  status.textContent =
    `Exporting ${RENDER_TIMELINE_TOTAL_FRAMES} frames at `
    + `${exportSize.width}x${exportSize.height}...`;

  try {
    const blob = await renderFixedSizeZipBlob({
      startFrame: 0,
      endFrame: RENDER_TIMELINE_TOTAL_FRAMES - 1,
      renderScale,
      onFrame: (frame) => {
        status.textContent =
          `Exporting ${exportSize.width}x${exportSize.height} frame `
          + `${frame + 1}/${RENDER_TIMELINE_TOTAL_FRAMES}...`;
      },
    });
    downloadBlob(blob, filename);
    status.textContent = `ZIP exported at ${exportSize.width}x${exportSize.height}.`;
  } catch (error) {
    status.textContent = `Export failed: ${error.message}`;
  } finally {
    setExportButtonsDisabled(false);
  }
}

async function renderFixedSizePngBlob({ frame, renderScale }) {
  return await withFixedSizeRenderer(renderScale, async () => {
    setRenderFrame(frame, { playing: false });
    await waitForAnimationFrames(2);
    return await previewShellToPngBlob();
  });
}

async function renderFixedSizeZipBlob({
  startFrame,
  endFrame,
  renderScale,
  onFrame,
}) {
  return await withFixedSizeRenderer(renderScale, async () => {
    const entries = [];
    const clampedStartFrame = clampFrame(startFrame);
    const clampedEndFrame = Math.max(clampedStartFrame, clampFrame(endFrame));

    for (let frame = clampedStartFrame; frame <= clampedEndFrame; frame += 1) {
      onFrame?.(frame);
      setRenderFrame(frame, { playing: false });
      await waitForAnimationFrames(2);

      const blob = await previewShellToPngBlob();
      entries.push({
        name: formatFrameFileName(frame),
        data: new Uint8Array(await blob.arrayBuffer()),
      });
    }

    return createStoredZipBlob(entries);
  });
}

async function withFixedSizeRenderer(renderScale, task) {
  const { width, height } = readExportSize(renderScale);
  const previousPixelRatio = renderer.getPixelRatio();
  const previousFrame = currentRenderFrame;
  const previousTimelinePlaying = timelinePlaying;
  const previousWidth = previewShell.style.width;
  const previousHeight = previewShell.style.height;

  timelinePlaying = false;
  previewShell.style.width = `${width}px`;
  previewShell.style.height = `${height}px`;
  resizeRenderersTo({ width, height, pixelRatio: 1 });

  try {
    return await task();
  } finally {
    previewShell.style.width = previousWidth;
    previewShell.style.height = previousHeight;
    renderer.setPixelRatio(previousPixelRatio);
    resizeRenderers();
    setRenderFrame(previousFrame, { playing: previousTimelinePlaying });
    syncRenderControls();
  }
}

async function previewShellToPngBlob() {
  const { width, height } = readPreviewSize();
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;

  const context = canvas.getContext("2d");
  if (!context) {
    throw new Error("Canvas 2D context is unavailable.");
  }

  context.fillStyle = "#000";
  context.fillRect(0, 0, width, height);
  context.drawImage(renderer.domElement, 0, 0, width, height);

  return await canvasToBlob(canvas, "image/png");
}

function formatFrameFileName(frame) {
  return `frame-${String(frame).padStart(4, "0")}.png`;
}

function createStoredZipBlob(entries) {
  const encoder = new TextEncoder();
  const localParts = [];
  const centralParts = [];
  let offset = 0;
  let centralSize = 0;

  for (const entry of entries) {
    if (entry.data.length > 0xffffffff) {
      throw new Error("A ZIP entry is too large for browser export.");
    }

    const nameBytes = encoder.encode(entry.name);
    const crc = computeCrc32(entry.data);
    const localHeader = createZipLocalHeader({ nameBytes, data: entry.data, crc });
    const centralHeader = createZipCentralHeader({
      nameBytes,
      data: entry.data,
      crc,
      localHeaderOffset: offset,
    });

    localParts.push(localHeader, entry.data);
    centralParts.push(centralHeader);
    offset += localHeader.length + entry.data.length;
    centralSize += centralHeader.length;

    if (offset > 0xffffffff || centralSize > 0xffffffff) {
      throw new Error("ZIP is too large for browser export.");
    }
  }

  const centralOffset = offset;
  const endRecord = createZipEndRecord({
    entryCount: entries.length,
    centralSize,
    centralOffset,
  });

  return new Blob([...localParts, ...centralParts, endRecord], {
    type: "application/zip",
  });
}

function createZipLocalHeader({ nameBytes, data, crc }) {
  const header = new Uint8Array(30 + nameBytes.length);
  const view = new DataView(header.buffer);

  view.setUint32(0, 0x04034b50, true);
  view.setUint16(4, ZIP_VERSION_NEEDED, true);
  view.setUint16(8, ZIP_STORE_METHOD, true);
  view.setUint32(14, crc, true);
  view.setUint32(18, data.length, true);
  view.setUint32(22, data.length, true);
  view.setUint16(26, nameBytes.length, true);
  header.set(nameBytes, 30);
  return header;
}

function createZipCentralHeader({ nameBytes, data, crc, localHeaderOffset }) {
  const header = new Uint8Array(46 + nameBytes.length);
  const view = new DataView(header.buffer);

  view.setUint32(0, 0x02014b50, true);
  view.setUint16(4, ZIP_VERSION_NEEDED, true);
  view.setUint16(6, ZIP_VERSION_NEEDED, true);
  view.setUint16(10, ZIP_STORE_METHOD, true);
  view.setUint32(16, crc, true);
  view.setUint32(20, data.length, true);
  view.setUint32(24, data.length, true);
  view.setUint16(28, nameBytes.length, true);
  view.setUint32(42, localHeaderOffset, true);
  header.set(nameBytes, 46);
  return header;
}

function createZipEndRecord({ entryCount, centralSize, centralOffset }) {
  if (entryCount > 0xffff) {
    throw new Error("ZIP has too many files.");
  }

  const record = new Uint8Array(22);
  const view = new DataView(record.buffer);
  view.setUint32(0, 0x06054b50, true);
  view.setUint16(8, entryCount, true);
  view.setUint16(10, entryCount, true);
  view.setUint32(12, centralSize, true);
  view.setUint32(16, centralOffset, true);
  return record;
}

function computeCrc32(bytes) {
  let crc = 0xffffffff;

  for (const byte of bytes) {
    crc = crc32Table[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  }

  return (crc ^ 0xffffffff) >>> 0;
}

function createCrc32Table() {
  const table = new Uint32Array(256);

  for (let index = 0; index < table.length; index += 1) {
    let value = index;
    for (let bit = 0; bit < 8; bit += 1) {
      value = value & 1 ? 0xedb88320 ^ (value >>> 1) : value >>> 1;
    }
    table[index] = value >>> 0;
  }

  return table;
}

function canvasToBlob(canvas, type) {
  return new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (blob) {
        resolve(blob);
        return;
      }

      reject(new Error("Canvas export failed."));
    }, type);
  });
}

function downloadBlob(blob, filename) {
  const blobUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = blobUrl;
  link.download = filename;
  link.click();
  window.setTimeout(() => URL.revokeObjectURL(blobUrl), 0);
}

function installSceneExportBridge() {
  window.__SCENE_3D_EXPORT__ = {
    isReady: () => isSceneReady,
    getCurrentFrame: () => currentRenderFrame,
    getTotalFrames: () => RENDER_TIMELINE_TOTAL_FRAMES,
    getSize: () => ({
      width: EXPORT_WIDTH,
      height: EXPORT_HEIGHT,
      aspectRatio: EXPORT_ASPECT_RATIO,
      fps: RENDER_FPS,
    }),
    setFrame: async (frame) => {
      setRenderFrame(frame, { playing: false });
      await waitForAnimationFrames(2);
      return currentRenderFrame;
    },
  };
}

function waitForAnimationFrames(frameCount = 1) {
  return new Promise((resolve) => {
    let remaining = Math.max(1, frameCount);
    const tick = () => {
      remaining -= 1;
      if (remaining <= 0) {
        resolve();
        return;
      }
      window.requestAnimationFrame(tick);
    };
    window.requestAnimationFrame(tick);
  });
}
