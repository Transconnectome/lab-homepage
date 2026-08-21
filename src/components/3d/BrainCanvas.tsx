import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { BRAIN_HUBS } from './brainData';

interface Props {
  selectedId: string | null;
  hoveredId: string | null;
  onSelect: (id: string | null) => void;
  onHover: (id: string | null) => void;
  ariaLabel: string;
}

interface HubEntry {
  mesh: THREE.Mesh;
  material: THREE.MeshBasicMaterial;
  haloMaterial: THREE.MeshBasicMaterial;
  baseScale: number;
}

interface TractEntry {
  material: THREE.LineBasicMaterial;
  aId: string;
  bId: string;
}

export default function BrainCanvas({ selectedId, hoveredId, onSelect, onHover, ariaLabel }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  // The scene is built exactly once; rebuilding it on prop changes would leak
  // WebGL contexts. Event handlers and the animation loop read the latest
  // props through this ref instead.
  const propsRef = useRef({ selectedId, hoveredId, onSelect, onHover });
  propsRef.current = { selectedId, hoveredId, onSelect, onHover };
  const handlesRef = useRef<{
    hubEntries: Map<string, HubEntry>;
    tracts: TractEntry[];
    reducedMotion: boolean;
  } | null>(null);

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

    const geometries: THREE.BufferGeometry[] = [particleGeometry];
    const materials: THREE.Material[] = [particleMaterial];

    // Connecting curves between hub nodes. Control points use deterministic
    // per-tract offsets so the sketch looks identical on every load.
    const tractGroup = new THREE.Group();
    brainGroup.add(tractGroup);
    const tracts: TractEntry[] = [];
    let tractIndex = 0;
    for (let i = 0; i < BRAIN_HUBS.length; i++) {
      for (let j = i + 1; j < BRAIN_HUBS.length; j++) {
        const p1 = new THREE.Vector3(...BRAIN_HUBS[i].position);
        const p2 = new THREE.Vector3(...BRAIN_HUBS[j].position);
        const sway = Math.sin(tractIndex * 12.9898) * 0.4;
        const lift = Math.cos(tractIndex * 78.233) * 0.4;
        const mid = new THREE.Vector3()
          .addVectors(p1, p2)
          .multiplyScalar(0.5)
          .add(new THREE.Vector3(0, sway, lift));
        const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
        const tractGeometry = new THREE.BufferGeometry().setFromPoints(curve.getPoints(30));
        const tractMaterial = new THREE.LineBasicMaterial({
          color: new THREE.Color(BRAIN_HUBS[i].color),
          transparent: true,
          opacity: 0.35,
        });
        tractGroup.add(new THREE.Line(tractGeometry, tractMaterial));
        tracts.push({ material: tractMaterial, aId: BRAIN_HUBS[i].id, bId: BRAIN_HUBS[j].id });
        geometries.push(tractGeometry);
        materials.push(tractMaterial);
        tractIndex++;
      }
    }

    // Interactive hub meshes + dedicated invisible hit spheres. Picking must
    // NOT use the visible meshes: the halo child would be the first raycast
    // intersection and break the hub lookup (the original click-dead bug).
    const hubEntries = new Map<string, HubEntry>();
    const entryList: HubEntry[] = [];
    const hitMeshes: THREE.Mesh[] = [];
    const hubGroup = new THREE.Group();
    brainGroup.add(hubGroup);
    BRAIN_HUBS.forEach((hub) => {
      const material = new THREE.MeshBasicMaterial({
        color: new THREE.Color(hub.color),
        transparent: true,
        opacity: 0.9,
      });
      const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), material);
      mesh.position.set(...hub.position);
      const haloMaterial = new THREE.MeshBasicMaterial({
        color: new THREE.Color(hub.color),
        transparent: true,
        opacity: 0.25,
        wireframe: true,
      });
      const halo = new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 16), haloMaterial);
      mesh.add(halo);
      hubGroup.add(mesh);

      // visible:false skips rendering but keeps the sphere raycastable, so the
      // generous 0.32 radius costs nothing to draw.
      const hitMaterial = new THREE.MeshBasicMaterial({ visible: false });
      const hit = new THREE.Mesh(new THREE.SphereGeometry(0.32, 8, 8), hitMaterial);
      hit.position.set(...hub.position);
      hit.userData.hubId = hub.id;
      hubGroup.add(hit);
      hitMeshes.push(hit);

      const entry: HubEntry = { mesh, material, haloMaterial, baseScale: 1 };
      hubEntries.set(hub.id, entry);
      entryList.push(entry);
      geometries.push(mesh.geometry as THREE.BufferGeometry, halo.geometry as THREE.BufferGeometry, hit.geometry as THREE.BufferGeometry);
      materials.push(material, haloMaterial, hitMaterial);
    });

    handlesRef.current = { hubEntries, tracts, reducedMotion };

    const raycaster = new THREE.Raycaster();
    const pointer = new THREE.Vector2();
    let targetRotationX = 0;
    let lastHoverId: string | null = null;

    // Compute pointer NDC from the *current* rect so hit-testing stays
    // correct after resize, and works for both mouse and touch pointers.
    const setPointerFromEvent = (clientX: number, clientY: number) => {
      const rect = container.getBoundingClientRect();
      pointer.x = ((clientX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((clientY - rect.top) / rect.height) * 2 + 1;
    };

    const pickHub = (): string | null => {
      raycaster.setFromCamera(pointer, camera);
      const hits = raycaster.intersectObjects(hitMeshes, false);
      return hits.length > 0 ? (hits[0].object.userData.hubId as string) : null;
    };

    const onPointerMove = (event: PointerEvent) => {
      setPointerFromEvent(event.clientX, event.clientY);
      const rect = container.getBoundingClientRect();
      targetRotationX = (event.clientY - rect.top - rect.height / 2) * 0.001;
      const found = pickHub();
      if (found !== lastHoverId) {
        lastHoverId = found;
        propsRef.current.onHover(found);
      }
      container.style.cursor = found ? 'pointer' : 'default';
    };

    const onPointerLeave = () => {
      if (lastHoverId !== null) {
        lastHoverId = null;
        propsRef.current.onHover(null);
      }
      container.style.cursor = 'default';
    };

    const onClick = (event: MouseEvent) => {
      setPointerFromEvent(event.clientX, event.clientY);
      // Clicking empty space clears the selection.
      propsRef.current.onSelect(pickHub());
    };

    container.addEventListener('pointermove', onPointerMove);
    container.addEventListener('pointerleave', onPointerLeave);
    container.addEventListener('click', onClick);

    let animationFrameId: number;
    const clock = new THREE.Clock();
    let rotSpeed = 0.004;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();
      if (!reducedMotion) {
        // Ease rotation to a stop while the visitor is aiming at or reading a
        // node, so moving targets don't fight the pointer.
        const engaged =
          propsRef.current.hoveredId !== null || propsRef.current.selectedId !== null;
        rotSpeed += ((engaged ? 0 : 0.004) - rotSpeed) * 0.06;
        brainGroup.rotation.y += rotSpeed;
        brainGroup.rotation.x += (targetRotationX - brainGroup.rotation.x) * 0.05;
        entryList.forEach((entry, idx) => {
          const scale = entry.baseScale * (1.0 + Math.sin(elapsedTime * 3.0 + idx) * 0.12);
          entry.mesh.scale.setScalar(scale);
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
      container.removeEventListener('pointerleave', onPointerLeave);
      container.removeEventListener('click', onClick);
      cancelAnimationFrame(animationFrameId);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      handlesRef.current = null;
      geometries.forEach((g) => g.dispose());
      materials.forEach((m) => m.dispose());
      renderer.dispose();
    };
  }, []);

  // Selection/hover feedback: mutate materials and scales only — never rebuild
  // the scene. Runs after the scene-construction effect on first mount.
  useEffect(() => {
    const handles = handlesRef.current;
    if (!handles) return;
    const activeId = selectedId ?? hoveredId;
    handles.hubEntries.forEach((entry, id) => {
      const isActive = activeId === id;
      const dimmed = activeId !== null && !isActive;
      entry.baseScale = isActive ? 1.45 : 1.0;
      entry.material.opacity = dimmed ? 0.3 : 0.9;
      entry.haloMaterial.opacity = dimmed ? 0.08 : isActive ? 0.4 : 0.25;
      if (handles.reducedMotion) {
        entry.mesh.scale.setScalar(entry.baseScale);
      }
    });
    handles.tracts.forEach((tract) => {
      if (activeId === null) {
        tract.material.opacity = 0.35;
      } else {
        tract.material.opacity = tract.aId === activeId || tract.bId === activeId ? 0.75 : 0.06;
      }
    });
  }, [selectedId, hoveredId]);

  return <div ref={containerRef} className="w-full h-full" role="img" aria-label={ariaLabel} />;
}
