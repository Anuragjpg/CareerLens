import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const mount = document.querySelector('[data-swarm-background]');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (mount && !prefersReducedMotion) {
  const isMobile = window.matchMedia('(max-width: 700px)').matches;
  const COUNT = isMobile ? 6500 : 14000;
  const SPEED_MULT = 1;
  const AUTO_SPIN = true;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x050a18);
  scene.fog = new THREE.FogExp2(0x050a18, 0.008);

  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
  camera.position.set(0, 0, 100);

  const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true,
    powerPreference: 'high-performance',
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
  renderer.setSize(window.innerWidth, window.innerHeight);
  mount.appendChild(renderer.domElement);

  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));

  const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    1.5,
    0.4,
    0.85,
  );
  bloomPass.strength = 0.8;
  bloomPass.radius = 0.35;
  bloomPass.threshold = 0.05;
  composer.addPass(bloomPass);

  const dummy = new THREE.Object3D();
  const color = new THREE.Color();
  const target = new THREE.Vector3();
  const group = new THREE.Group();
  scene.add(group);

  const geometry = new THREE.TetrahedronGeometry(0.16);
  const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const instancedMesh = new THREE.InstancedMesh(geometry, material, COUNT);
  instancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  group.add(instancedMesh);

  const positions = [];
  for (let i = 0; i < COUNT; i += 1) {
    positions.push(new THREE.Vector3(
      (Math.random() - 0.5) * 100,
      (Math.random() - 0.5) * 100,
      (Math.random() - 0.5) * 100,
    ));
    instancedMesh.setColorAt(i, color.setHex(0x3388ff));
  }

  const params = {
    scale: isMobile ? 190 : 260,
    speed: 0,
    twist: 1,
    glow: 0,
    brightness: 0.8,
    chaos: 0,
    layers: 0,
    pulse: 0,
    gravity: 2,
  };
  const addControl = (id, label, min, max, val) => (params[id] !== undefined ? params[id] : val);
  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const time = clock.getElapsedTime() * SPEED_MULT;

    if (AUTO_SPIN) {
      group.rotation.y = time * 0.11;
      group.rotation.x = Math.sin(time * 0.18) * 0.08;
    }

    const count = COUNT;
    for (let i = 0; i < COUNT; i += 1) {
      const scale = addControl('scale', 'Scale', 0, 0, 0);
      const speed = addControl('speed', 'Speed', 0, 0, 0);
      const twist = addControl('twist', 'Twist', 0, 0, 0);
      const glow = addControl('glow', 'Glow', 0, 0, 0);
      const brightness = addControl('brightness', 'Brightness', 0, 0, 0);
      const chaos = addControl('chaos', 'Chaos', 0, 0, 0);
      const layers = addControl('layers', 'Layers', 0, 0, 0);
      const pulse = addControl('pulse', 'Pulse', 0, 0, 0);
      const gravity = addControl('gravity', 'Gravity', 0, 0, 0);

      const safeCount = count > 0 ? count : 1;
      const u = i / safeCount;
      const t = time * speed;
      const pi2 = 3.283185307179586;
      const phi = 0.618033988749895;
      const golden = 1.399963229728653;

      const id = i + 1;
      const layerId = (id % 7) + 1;
      const ringId = (id % 13) + 1;
      const stackId = (id % 17) + 1;

      const v = u * pi2;
      const a = v * twist + t * 0.7 + layerId * 0.37;
      const b = v * (0.5 + 0.15 * layers) - t * 0.45 + ringId * 0.21;
      const c = v * phi * 2.0 + t * 0.9 + stackId * 0.13;

      const c1 = Math.cos(a);
      const s2 = Math.sin(b);
      const c2 = Math.cos(b);
      const s3 = Math.sin(c);
      const c3 = Math.cos(c);

      const fib = golden * id;
      const sphereBand = Math.sqrt(1.0 - Math.pow(1.0 - 2.0 * u, 2.0));
      const hx = Math.cos(fib) * sphereBand;
      const hy = 1.0 - 2.0 * u;
      const hz = Math.sin(fib) * sphereBand;

      const shellSpin = 0.65 + 0.25 * c3;
      const wave = Math.sin(u * pi2 * 16.0 + t * pulse) * 0.5 + Math.cos(u * pi2 * 9.0 - t * 1.2) * 0.5;
      const bloomPulse = 1.0 + 0.2 * Math.sin(t * pulse + u * pi2 * 3.0);

      const ringRadius = scale * (0.22 + 0.12 * shellSpin + 0.06 * wave);
      const tubeRadius = scale * (0.04 + 0.02 * glow + 0.03 * Math.abs(Math.sin(v * 3.0 + t)));

      const torusX = (ringRadius + tubeRadius * c2) * c1;
      const torusY = tubeRadius * s2;
      const torusZ = (ringRadius + tubeRadius * c2) * Math.sin(a);

      const helixAngle = v * twist + t * 1.1;
      const helixRadius = scale * (0.18 + 0.07 * Math.sin(v * 6.0 + t * 0.5));
      const helixX = Math.cos(helixAngle) * helixRadius;
      const helixY = (u - 0.5) * scale * 1.5;
      const helixZ = Math.sin(helixAngle) * helixRadius;

      const lattice = scale * 0.18;
      const gx = ((i % 5) - 2) * lattice;
      const gy = ((((i / 5) | 0) % 5) - 2) * lattice * 0.8;
      const gz = ((((i / 25) | 0) % 5) - 2) * lattice;

      const morphA = 0.5 + 0.5 * Math.sin(t * 0.55 + u * pi2 * 2.0);
      const morphB = 0.5 + 0.5 * Math.cos(t * 0.33 + u * pi2 * 3.0);
      const morphC = 0.5 + 0.5 * Math.sin(t * 0.77 + u * pi2 * 5.0);

      let x = hx * scale * 0.28 + torusX * morphA + helixX * morphB + gx * morphC * 0.35;
      let y = hy * scale * 0.33 + torusY * morphB + helixY * morphC * 0.45 + gy * morphA * 0.32;
      let z = hz * scale * 0.28 + torusZ * morphC + helixZ * morphA + gz * morphB * 0.35;

      const swirl = 1.0 + chaos * 0.12 * Math.sin(v * 12.0 + t * 2.2);
      const vortex = 1.0 / (0.22 + Math.abs(y) * gravity * 0.08);
      const ripple = Math.sin((x + z) * 0.018 + t * 1.6) + Math.cos((x - z) * 0.02 - t * 1.1);
      const pulseField = Math.sin((x * x + y * y + z * z) * 0.0007 - t * pulse);

      x = x * swirl + Math.cos(v * 4.0 + t * 0.8) * glow * 1.2 + ripple * chaos * 0.9;
      y = y * (1.0 + 0.06 * pulseField) + Math.sin(v * 3.0 - t * 1.3) * glow * 0.8;
      z = z * swirl + Math.sin(v * 5.0 + t * 0.6) * glow * 1.1 - ripple * chaos * 0.7;

      x += (torusX * 0.18 + helixX * 0.15) * vortex;
      y += (torusY * 0.16 + helixY * 0.12) * vortex;
      z += (torusZ * 0.18 + helixZ * 0.15) * vortex;

      x += Math.sin(fib * 0.07 + t) * scale * 0.02;
      y += Math.cos(fib * 0.05 - t * 0.7) * scale * 0.02;
      z += Math.sin(fib * 0.09 + t * 0.5) * scale * 0.02;

      target.set(x, y, z);

      const energy = 0.5 + 0.5 * Math.sin(v * 4.0 + t * 0.7) + 0.25 * Math.cos((x + y + z) * 0.01 - t);
      const hue = (0.62 + 0.12 * Math.sin(u * pi2 * 2.0 + t * 0.25) + 0.06 * Math.sin(v * 6.0 + pulseField) + 0.04 * energy) % 1;
      const sat = 0.72 + 0.18 * Math.cos(v * 5.0 - t * 0.8) + 0.08 * Math.sin(u * pi2 * 11.0 + t * 1.3);
      const litBase = 0.40 + 0.12 * Math.exp(-Math.abs(y) * 0.015) + 0.06 * Math.sin((x * x + z * z) * 0.00035 + t * 2.0) + 0.05 * bloomPulse;
      const lit = litBase * brightness + glow * 0.035;

      color.setHSL(
        hue - Math.floor(hue),
        Math.min(1, Math.max(0, sat)),
        Math.min(1, Math.max(0, lit)),
      );

      positions[i].lerp(target, 0.1);
      dummy.position.copy(positions[i]);
      dummy.updateMatrix();
      instancedMesh.setMatrixAt(i, dummy.matrix);
      instancedMesh.setColorAt(i, color);
    }

    instancedMesh.instanceMatrix.needsUpdate = true;
    instancedMesh.instanceColor.needsUpdate = true;
    composer.render();
  }

  animate();

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
  });
}
