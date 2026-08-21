import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface BrainNode {
  name: string;
  nameKo: string;
  network: string;
  position: [number, number, number];
  color: string;
  description: string;
  labProjects: string[];
}

const BRAIN_HUBS: BrainNode[] = [
  {
    name: 'Default Mode Network (DMN)',
    nameKo: '디폴트 모드 네트워크 (DMN)',
    network: 'DMN',
    position: [0, 1.2, -1.0],
    color: '#38bdf8',
    description: 'Self-referential thought, autobiographical memory, and resting-state dynamics.',
    labProjects: ['NeuroMamba 4D fMRI modeling', 'Polygenic architecture of the developing brain (Nat Comms 2025)']
  },
  {
    name: 'Executive Control Network (ECN / FPN)',
    nameKo: '집행 제어 네트워크 (전두두정망)',
    network: 'Frontoparietal',
    position: [1.3, 1.0, 0.8],
    color: '#818cf8',
    description: 'Top-down cognitive control, working memory, and dynamic task switching.',
    labProjects: ['SwiFT 4D Swin Transformers (NeurIPS 2023)', 'Spatiotemporal multi-band dynamics']
  },
  {
    name: 'Salience Network (SN - Insula/dACC)',
    nameKo: '돌출성 네트워크 (Salience)',
    network: 'Salience',
    position: [-1.2, 0.4, 0.4],
    color: '#f43f5e',
    description: 'Detection of biologically and emotionally salient internal & external stimuli.',
    labProjects: ['Adolescent depression & suicide risk prediction', 'OB/Scene EEG art decoding']
  },
  {
    name: 'Visual & Sensory Cortex (V1/V2)',
    nameKo: '시각 및 감각 피질',
    network: 'Sensory',
    position: [0.9, -0.6, -1.6],
    color: '#34d399',
    description: 'Hierarchical visual representations and sensory state reconstruction.',
    labProjects: ['Mind the Gap: brain-LLM nonlinear alignment', 'Generative fMRI simulation']
  },
  {
    name: 'Subcortical & Hippocampal Complex',
    nameKo: '피질하 및 해마 복합체',
    network: 'Subcortical',
    position: [-0.6, -0.5, -0.2],
    color: '#fbbf24',
    description: 'Memory consolidation, affective valence, and psychiatric vulnerability nodes.',
    labProjects: ['Multigenerational polygenic transmission (Mol Psychiatry 2025)', 'Quantum ML graph kernels']
  },
  {
    name: 'Electrode Sensor Mesh (EEG DIVER-0)',
    nameKo: '전극 센서 메쉬 (EEG DIVER-0)',
    network: 'Sensor Point Cloud',
    position: [-1.4, 1.2, 0.0],
    color: '#c084fc',
    description: 'Channel-equivariant continuous coordinate manifold for EEG bio-signals.',
    labProjects: ['DIVER-0 channel-equivariant foundation model (ICML 2025 Workshop Spotlight)']
  }
];

export default function BrainViewer() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedHub, setSelectedHub] = useState<BrainNode | null>(null);
  const [hoveredHub, setHoveredHub] = useState<BrainNode | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const container = containerRef.current;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      45,
      container.clientWidth / (container.clientHeight || 500),
      0.1,
      1000
    );
    camera.position.set(0, 1.5, 5.5);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight || 500);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const brainGroup = new THREE.Group();
    scene.add(brainGroup);

    // Procedural two-lobe point cloud (illustrative, not anatomical data)
    const particleCount = 1600;
    const particleGeometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      const hemisphere = i % 2 === 0 ? 1 : -1;
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = 1.6 + (Math.random() - 0.5) * 0.3;
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta) * 0.9 + hemisphere * 0.55;
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta) * 0.75 + 0.2;
      positions[i * 3 + 2] = r * Math.cos(phi) * 1.25;

      const color = new THREE.Color();
      const t = (positions[i * 3 + 1] + 1.5) / 3.0;
      color.setHSL(0.55 + t * 0.2, 0.85, 0.65);
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMaterial = new THREE.PointsMaterial({
      size: 0.045,
      vertexColors: true,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending,
    });
    brainGroup.add(new THREE.Points(particleGeometry, particleMaterial));

    // Connecting curves between hub nodes
    const tractGroup = new THREE.Group();
    brainGroup.add(tractGroup);
    for (let i = 0; i < BRAIN_HUBS.length; i++) {
      for (let j = i + 1; j < BRAIN_HUBS.length; j++) {
        const p1 = new THREE.Vector3(...BRAIN_HUBS[i].position);
        const p2 = new THREE.Vector3(...BRAIN_HUBS[j].position);
        const mid = new THREE.Vector3()
          .addVectors(p1, p2)
          .multiplyScalar(0.5)
          .add(new THREE.Vector3(0, (Math.random() - 0.5) * 0.8, (Math.random() - 0.5) * 0.8));
        const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
        const tractGeometry = new THREE.BufferGeometry().setFromPoints(curve.getPoints(30));
        const tractMaterial = new THREE.LineBasicMaterial({
          color: new THREE.Color(BRAIN_HUBS[i].color),
          transparent: true,
          opacity: 0.35,
        });
        tractGroup.add(new THREE.Line(tractGeometry, tractMaterial));
      }
    }

    // Interactive hub meshes
    const hubMeshes: { mesh: THREE.Mesh; hub: BrainNode }[] = [];
    const hubGroup = new THREE.Group();
    brainGroup.add(hubGroup);
    BRAIN_HUBS.forEach((hub) => {
      const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(0.12, 16, 16),
        new THREE.MeshBasicMaterial({ color: new THREE.Color(hub.color), transparent: true, opacity: 0.9 })
      );
      mesh.position.set(...hub.position);
      const halo = new THREE.Mesh(
        new THREE.SphereGeometry(0.2, 16, 16),
        new THREE.MeshBasicMaterial({ color: new THREE.Color(hub.color), transparent: true, opacity: 0.25, wireframe: true })
      );
      mesh.add(halo);
      hubGroup.add(mesh);
      hubMeshes.push({ mesh, hub });
    });

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    let targetRotationX = 0;

    // Compute pointer NDC from the *current* rect so hit-testing stays
    // correct after resize, and works for both mouse and touch pointers.
    const setPointerFromEvent = (clientX: number, clientY: number) => {
      const rect = container.getBoundingClientRect();
      pointer.x = ((clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((clientY - rect.top) / rect.height) * 2 + 1;
    };

    const pickHub = () => {
      raycaster.setFromCamera(pointer, camera);
      const intersects = raycaster.intersectObjects(hubMeshes.map((h) => h.mesh));
      if (intersects.length > 0) {
        return hubMeshes.find((h) => h.mesh === intersects[0].object) || null;
      }
      return null;
    };

    const onPointerMove = (event: PointerEvent) => {
      setPointerFromEvent(event.clientX, event.clientY);
      const rect = container.getBoundingClientRect();
      targetRotationX = ((event.clientY - rect.top - rect.height / 2) * 0.001) * 1.0;
      const found = pickHub();
      setHoveredHub(found ? found.hub : null);
      container.style.cursor = found ? 'pointer' : 'default';
    };

    const onClick = (event: MouseEvent) => {
      setPointerFromEvent(event.clientX, event.clientY);
      const found = pickHub();
      if (found) setSelectedHub(found.hub);
    };

    container.addEventListener('pointermove', onPointerMove);
    container.addEventListener('click', onClick);

    let animationFrameId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();
      if (!reducedMotion) {
        brainGroup.rotation.y += 0.004;
        brainGroup.rotation.x += (targetRotationX - brainGroup.rotation.x) * 0.05;
        hubMeshes.forEach(({ mesh }, idx) => {
          const scale = 1.0 + Math.sin(elapsedTime * 3.0 + idx) * 0.18;
          mesh.scale.set(scale, scale, scale);
        });
      }
      renderer.render(scene, camera);
    };
    animate();

    const onResize = () => {
      if (!container) return;
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight || 500;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };
    window.addEventListener('resize', onResize);

    return () => {
      window.removeEventListener('resize', onResize);
      container.removeEventListener('pointermove', onPointerMove);
      container.removeEventListener('click', onClick);
      cancelAnimationFrame(animationFrameId);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      particleGeometry.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div className="relative w-full h-[500px] md:h-[580px] overflow-hidden rounded-2xl bg-deep border border-deep-line shadow-2xl">
      <div ref={containerRef} className="w-full h-full" role="img" aria-label="Interactive illustration of brain networks studied by the lab" />

      {/* Honest caption: this is an illustration, not anatomical data */}
      <div className="absolute top-5 left-5 px-3 py-1.5 rounded-full bg-slate-900/80 backdrop-blur-md border border-cyan-500/30 text-xs font-mono text-cyan-300">
        CONNECTOME SKETCH · ILLUSTRATIVE
      </div>
      <div className="absolute top-5 right-5 hidden sm:flex px-3 py-1.5 rounded-lg bg-slate-900/70 border border-slate-700 text-xs text-slate-400">
        Tap a node to see related lab research
      </div>

      {hoveredHub && !selectedHub && (
        <div className="absolute bottom-5 left-5 max-w-sm p-4 rounded-xl bg-slate-900/90 backdrop-blur-xl border border-cyan-500/40 text-slate-200 shadow-xl pointer-events-none">
          <div className="flex items-center gap-2 mb-1">
            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: hoveredHub.color }} />
            <h4 className="font-semibold text-white text-sm">{hoveredHub.name}</h4>
          </div>
          <p className="text-xs text-slate-300 mb-2">{hoveredHub.nameKo}</p>
          <p className="text-xs text-slate-400 leading-relaxed">{hoveredHub.description}</p>
        </div>
      )}

      {selectedHub && (
        <div className="absolute inset-x-4 bottom-4 md:inset-x-auto md:right-5 md:bottom-5 md:w-96 p-5 rounded-xl bg-slate-900/95 backdrop-blur-2xl border border-cyan-500/50 text-slate-200 shadow-2xl animate-in fade-in slide-in-from-bottom-4 duration-300 z-20">
          <div className="flex items-start justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="w-3.5 h-3.5 rounded-full ring-2 ring-cyan-400/40" style={{ backgroundColor: selectedHub.color }} />
              <h3 className="font-bold text-white text-base">{selectedHub.name}</h3>
            </div>
            <button
              onClick={() => setSelectedHub(null)}
              className="text-slate-400 hover:text-white text-xs px-2 py-1 rounded bg-slate-800 border border-slate-700"
              aria-label="Close details"
            >
              ✕
            </button>
          </div>
          <p className="text-xs text-cyan-300 font-medium mb-2">{selectedHub.nameKo}</p>
          <p className="text-sm text-slate-300 mb-3 leading-relaxed">{selectedHub.description}</p>

          <div className="border-t border-slate-800 pt-3">
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">Related lab research</div>
            <ul className="space-y-1">
              {selectedHub.labProjects.map((proj, idx) => (
                <li key={idx} className="text-sm flex items-start gap-1.5 text-slate-200">
                  <span className="text-cyan-400">▹</span>
                  <span>{proj}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="mt-4 flex gap-2">
            <a
              href="/research"
              className="flex-1 text-center py-2 px-3 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-sm transition"
            >
              Explore research
            </a>
            <button
              onClick={() => setSelectedHub(null)}
              className="py-2 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm transition"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
