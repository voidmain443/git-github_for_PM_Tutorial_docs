/* A finite, user-invoked illustration of document handoffs, not an ERP action. */
export async function mountScene(host, {onSelect = () => {}, onError = () => {}} = {}) {
  if (!host || host.nodeType !== 1) throw new TypeError('3D 장면을 표시할 영역이 필요합니다.');
  const THREE = await import('./vendor/three.module.min.js');
  const doc = host.ownerDocument, win = doc.defaultView;
  const geometries = new Set(), materials = new Set(), textures = new Set();
  const listeners = [];
  const palette = {ink:0x173443, slate:0x607480, paper:0xf8faf8, mist:0xe7eeec, pine:0x176a62, gold:0xd4a653};
  let renderer, canvas, resizeObserver, intersectionObserver, motionQuery;
  let disposed = false, failed = false, inViewport = true, frameId = 0;
  let animation = null, lastTimestamp = null, activeStage = 0;
  let pointerStart = null, hovered = -1;
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-6, 6, 4, -4, 0.1, 60);
  camera.position.set(5.7, 10.8, 13.8);
  camera.lookAt(0, 0, 0);
  const groups = [], paperHits = [], accents = [], routeSegments = [];
  const positions = [
    new THREE.Vector3(-3.45, 0.1, 0.9),
    new THREE.Vector3(-1.76, 0.1, -1.13),
    new THREE.Vector3(0, 0.1, 0.78),
    new THREE.Vector3(1.77, 0.1, -1.15),
    new THREE.Vector3(3.42, 0.1, 0.86),
  ];
  const names = ['근거', '헌장', '계획', '변경', '인계'];
  const resource = (set, value) => {set.add(value); return value;};
  const geometry = value => resource(geometries, value);
  const material = value => resource(materials, value);
  const texture = value => resource(textures, value);
  const standard = (color, extra = {}) => material(new THREE.MeshStandardMaterial({color, roughness:0.78, metalness:0.04, ...extra}));
  const paperMaterial = standard(palette.paper);
  const paperEdge = standard(0xd8e2dd);
  const inkMaterial = standard(palette.ink);
  const goldMaterial = standard(palette.gold, {roughness:0.45, metalness:0.2});
  const pineMaterial = standard(palette.pine);
  const baseMaterial = standard(0x29444f, {roughness:0.91});
  let packet, keyLight;

  function listen(target, name, fn, options) {
    target.addEventListener(name, fn, options);
    listeners.push(() => target.removeEventListener(name, fn, options));
  }
  function visible() {return !disposed && !failed && inViewport && !doc.hidden;}
  function stopFrame() {
    if (frameId) win.cancelAnimationFrame(frameId);
    frameId = 0;
    lastTimestamp = null;
  }
  function dispose() {
    if (disposed) return;
    disposed = true;
    animation = null;
    stopFrame();
    resizeObserver?.disconnect();
    intersectionObserver?.disconnect();
    listeners.splice(0).forEach(remove => remove());
    geometries.forEach(value => value.dispose());
    materials.forEach(value => value.dispose());
    textures.forEach(value => value.dispose());
    keyLight?.shadow.map?.dispose();
    keyLight?.shadow.mapPass?.dispose();
    renderer?.renderLists?.dispose();
    renderer?.dispose();
    // Return the GPU context as well as its buffers when the illustration closes.
    renderer?.forceContextLoss();
    canvas?.remove();
    scene.clear();
    geometries.clear(); materials.clear(); textures.clear();
  }
  function fail(error) {
    if (failed || disposed) return;
    failed = true;
    stopFrame();
    try {onError(error);} catch { /* Host callbacks cannot start a retry loop. */ }
    finally {dispose();}
  }
  function roundedGeometry(width, depth, height, radius = 0.04) {
    const x = -width / 2, y = -depth / 2, r = Math.min(radius, width / 2, depth / 2);
    const shape = new THREE.Shape();
    shape.moveTo(x + r, y);
    shape.lineTo(x + width - r, y);
    shape.quadraticCurveTo(x + width, y, x + width, y + r);
    shape.lineTo(x + width, y + depth - r);
    shape.quadraticCurveTo(x + width, y + depth, x + width - r, y + depth);
    shape.lineTo(x + r, y + depth);
    shape.quadraticCurveTo(x, y + depth, x, y + depth - r);
    shape.lineTo(x, y + r);
    shape.quadraticCurveTo(x, y, x + r, y);
    const g = new THREE.ExtrudeGeometry(shape, {depth:height, bevelEnabled:false, curveSegments:4, steps:1});
    g.rotateX(-Math.PI / 2);
    return geometry(g);
  }
  function panel(parent, width, depth, height, mat, x = 0, y = 0, z = 0, radius = 0.04) {
    const mesh = new THREE.Mesh(roundedGeometry(width, depth, height, radius), mat);
    mesh.position.set(x, y, z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
  }
  function documentTexture(index, secondary = false) {
    const surface = doc.createElement('canvas');
    surface.width = 512; surface.height = 672;
    const ctx = surface.getContext('2d');
    if (!ctx) throw new Error('문서 장면을 그릴 수 없습니다.');
    ctx.fillStyle = '#f8faf8'; ctx.fillRect(0, 0, 512, 672);
    ctx.fillStyle = secondary ? '#607480' : '#173443';
    ctx.font = '600 45px system-ui, sans-serif';
    ctx.fillText(names[index], 44, 82);
    ctx.fillStyle = '#176a62'; ctx.fillRect(44, 108, 76, 7);
    const line = (x, y, width, color = '#c9d6d0', thickness = 7) => {
      ctx.fillStyle = color; ctx.fillRect(x, y, width, thickness);
    };
    const label = (text, x, y) => {
      ctx.font = '500 23px system-ui, sans-serif'; ctx.fillStyle = '#607480'; ctx.fillText(text, x, y);
    };
    if (index === 0) {
      label('원천자료', 44, 166);
      for (let row = 0; row < 6; row++) {
        line(44, 190 + row * 51, row % 2 ? 324 : 416, row === 2 ? '#93b8ae' : '#c9d6d0');
        line(44, 211 + row * 51, 240, '#e0e7e3', 4);
      }
      line(44, 563, 155, '#176a62', 9);
    } else if (index === 1) {
      ['목적', '범위', '권한'].forEach((text, row) => {
        label(text, 44, 174 + row * 135);
        line(44, 197 + row * 135, 411);
        line(44, 220 + row * 135, 306, '#dce5df', 6);
        line(44, 242 + row * 135, 361, '#dce5df', 6);
      });
      line(44, 612, 186, '#d4a653', 6);
    } else if (index === 2) {
      label('일정과 자원', 44, 170);
      for (let col = 0; col < 7; col++) line(118 + col * 51, 210, 2, '#e0e7e3', 335);
      for (let row = 0; row < 6; row++) {
        line(44, 228 + row * 54, 49, '#a7bcb1', 8);
        line(119, 253 + row * 54, 339, '#e0e7e3', 2);
      }
      [[0, 0, 2], [1, 1, 2], [2, 2, 3], [3, 2, 2], [4, 4, 2], [5, 5, 1]].forEach(([row, start, width]) => {
        line(120 + start * 50, 217 + row * 54, width * 48, row === 3 ? '#d4a653' : '#176a62', 22);
      });
      line(44, 594, 351, '#c9d6d0', 6);
    } else if (index === 3) {
      label('영향 비교', 44, 170);
      line(44, 193, 412, '#a7bcb1', 2);
      line(252, 193, 2, '#d4a653', 346);
      for (let row = 0; row < 5; row++) {
        line(44, 220 + row * 63, row === 2 ? 118 : 161, '#c9d6d0', 8);
        line(281, 220 + row * 63, row === 2 ? 165 : 132, row === 2 ? '#d4a653' : '#93b8ae', 8);
        line(44, 250 + row * 63, 412, '#e0e7e3', 2);
      }
      line(281, 582, 174, '#176a62', 8);
    } else {
      label('운영 인계', 44, 170);
      ['문서', '담당', '후속 확인'].forEach((text, row) => {
        ctx.strokeStyle = '#93b8ae'; ctx.lineWidth = 3; ctx.strokeRect(46, 208 + row * 108, 25, 25);
        label(text, 91, 229 + row * 108);
        line(92, 255 + row * 108, 340, '#dce5df', 6);
      });
      line(44, 591, 197, '#d4a653', 7);
    }
    const map = texture(new THREE.CanvasTexture(surface));
    map.colorSpace = THREE.SRGBColorSpace;
    map.anisotropy = Math.min(2, renderer.capabilities.getMaxAnisotropy());
    return map;
  }
  function sheet(parent, {index, x = 0, y = 0, z = 0, turn = 0, printed = false, width = 1.35, depth = 1.79} = {}) {
    const page = new THREE.Group();
    page.position.set(x, y, z); page.rotation.y = turn; parent.add(page);
    panel(page, width, depth, 0.024, paperMaterial);
    if (printed) {
      const face = new THREE.Mesh(
        geometry(new THREE.PlaneGeometry(width - 0.045, depth - 0.045)),
        material(new THREE.MeshBasicMaterial({map:documentTexture(index), toneMapped:false})),
      );
      face.rotation.x = -Math.PI / 2;
      face.position.y = 0.025;
      page.add(face);
      paperHits.push(face);
    }
    return page;
  }
  function buildDocument(index) {
    const group = new THREE.Group(); group.userData.stage = index; scene.add(group);
    const accent = standard(palette.slate, {roughness:0.55});
    accents.push(accent);
    if (index === 0) {
      sheet(group, {index, x:-0.13, z:0.1, turn:-0.12});
      sheet(group, {index, x:0.13, y:0.045, z:-0.08, turn:0.1});
      sheet(group, {index, y:0.09, printed:true});
    } else if (index === 1) {
      panel(group, 1.48, 1.94, 0.055, inkMaterial, 0, 0, 0, 0.065);
      sheet(group, {index, y:0.059, printed:true});
      panel(group, 0.48, 0.16, 0.04, goldMaterial, 0, 0.097, -0.85, 0.025);
    } else if (index === 2) {
      panel(group, 1.48, 1.94, 0.045, paperEdge);
      sheet(group, {index, x:0.035, y:0.05, z:0.025});
      sheet(group, {index, x:-0.028, y:0.092, z:-0.016});
      sheet(group, {index, y:0.135, printed:true});
      panel(group, 0.18, 0.31, 0.019, pineMaterial, 0.72, 0.15, -0.24, 0.012);
    } else if (index === 3) {
      sheet(group, {index, x:-0.12, z:0.04, turn:-0.08});
      sheet(group, {index, x:0.08, y:0.048, z:-0.02, turn:0.035, printed:true});
      panel(group, 0.22, 0.25, 0.014, goldMaterial, 0.66, 0.08, -0.65, 0.01);
    } else {
      panel(group, 1.56, 2.02, 0.065, pineMaterial, 0, 0, 0, 0.065);
      panel(group, 0.65, 0.23, 0.032, pineMaterial, -0.37, 0.02, -1.04, 0.045);
      sheet(group, {index, y:0.07, z:-0.015});
      sheet(group, {index, y:0.11, printed:true});
      panel(group, 1.56, 0.35, 0.033, pineMaterial, 0, 0.14, 0.89, 0.04);
    }
    panel(group, 0.6, 0.045, 0.035, accent, 0, 0.015, 1.12, 0.015);
    // A small structural tab links each packet to the reading-stage controls.
    const ring = new THREE.Mesh(geometry(new THREE.CylinderGeometry(0.055, 0.055, 0.025, 14)), accent);
    ring.position.set(-0.46, 0.025, 1.12); group.add(ring);
    group.position.copy(positions[index]);
    return group;
  }
  function routePoint(index) {return new THREE.Vector3(positions[index].x, 0.045, positions[index].z + 1.38);}
  function createRoute() {
    for (let i = 0; i < positions.length - 1; i++) {
      const start = routePoint(i), end = routePoint(i + 1);
      const curve = new THREE.CatmullRomCurve3([
        start,
        start.clone().lerp(end, 0.35).add(new THREE.Vector3(0, 0, 0.14)),
        end.clone().lerp(start, 0.2).add(new THREE.Vector3(0, 0, 0.14)),
        end,
      ]);
      const mat = standard(0x72888b, {roughness:0.8});
      const mesh = new THREE.Mesh(geometry(new THREE.TubeGeometry(curve, 20, 0.016, 5, false)), mat);
      scene.add(mesh); routeSegments.push({curve, material:mat});
      const dot = new THREE.Mesh(geometry(new THREE.CylinderGeometry(0.043, 0.043, 0.017, 12)), mat);
      dot.position.copy(start); scene.add(dot);
    }
    packet = new THREE.Group();
    panel(packet, 0.2, 0.25, 0.035, goldMaterial, 0, 0, 0, 0.025);
    panel(packet, 0.11, 0.016, 0.003, paperMaterial, 0, 0.039, -0.05, 0.003);
    panel(packet, 0.08, 0.013, 0.003, paperMaterial, -0.015, 0.039, 0.013, 0.003);
    packet.visible = false; scene.add(packet);
  }
  function targets(stage) {
    return positions.map((position, index) => ({
      position:position.clone().add(new THREE.Vector3(0, index === stage ? 0.48 : index < stage ? 0.015 : 0, 0)),
      angle:index <= stage ? 0 : [0, -0.045, 0.065, -0.055, 0.04][index],
      scale:index === stage ? 1.045 : 1,
    }));
  }
  function snapshot() {return groups.map(group => ({position:group.position.clone(), angle:group.rotation.y, scale:group.scale.x}));}
  function apply(progress) {
    if (!animation) return;
    const eased = 1 - Math.pow(1 - progress, 3);
    groups.forEach((group, index) => {
      const from = animation.from[index], to = animation.to[index];
      group.position.copy(from.position).lerp(to.position, eased);
      group.rotation.y = from.angle + (to.angle - from.angle) * eased;
      group.scale.setScalar(from.scale + (to.scale - from.scale) * eased);
    });
    if (animation.route && progress < 1) {
      packet.visible = true;
      packet.position.copy(animation.route.getPoint(eased));
      packet.position.y += Math.sin(progress * Math.PI) * 0.15;
      const tangent = animation.route.getTangent(eased);
      packet.rotation.y = Math.atan2(tangent.x, tangent.z);
    } else packet.visible = false;
  }
  function reducedMotion() {return !!motionQuery?.matches;}
  function requestFrame() {
    if (visible() && !frameId) frameId = win.requestAnimationFrame(draw);
  }
  function draw(timestamp) {
    frameId = 0;
    if (!visible()) {lastTimestamp = null; return;}
    if (animation) {
      if (lastTimestamp !== null) animation.elapsed += Math.max(0, timestamp - lastTimestamp);
      const progress = reducedMotion() ? 1 : Math.min(1, animation.elapsed / 700);
      apply(progress);
      if (progress === 1) animation = null;
    }
    lastTimestamp = timestamp;
    try {
      renderer.shadowMap.needsUpdate = true;
      renderer.render(scene, camera);
    } catch (error) {fail(error); return;}
    if (animation) requestFrame();
    else lastTimestamp = null;
  }
  function resize() {
    if (disposed || failed) return;
    const rect = host.getBoundingClientRect();
    const width = Math.max(1, Math.round(rect.width));
    const height = Math.max(1, Math.round(rect.height));
    renderer.setPixelRatio(Math.min(1.5, win.devicePixelRatio || 1));
    renderer.setSize(width, height, false);
    const aspect = width / height;
    // Fit the rotated desk as well as its document packets on narrow screens.
    const halfHeight = Math.max(3.85, 6.3 / aspect);
    camera.left = -halfHeight * aspect;
    camera.right = halfHeight * aspect;
    camera.top = halfHeight;
    camera.bottom = -halfHeight;
    camera.updateProjectionMatrix();
    requestFrame();
  }
  function setStage(index) {
    if (disposed || failed) return;
    if (!Number.isInteger(index) || index < 0 || index > 4) throw new RangeError('단계는 0부터 4까지입니다.');
    if (index === activeStage) return;
    const previous = activeStage;
    activeStage = index;
    const points = [];
    const direction = index > previous ? 1 : -1;
    for (let step = previous; step !== index + direction; step += direction) points.push(routePoint(step));
    animation = {from:snapshot(), to:targets(index), elapsed:0, route:new THREE.CatmullRomCurve3(points)};
    lastTimestamp = null;
    accents.forEach((mat, stage) => mat.color.set(stage === index ? palette.gold : stage < index ? palette.pine : palette.slate));
    routeSegments.forEach((segment, stage) => segment.material.color.set(stage < index ? palette.pine : 0x72888b));
    if (reducedMotion()) {apply(1); animation = null;}
    requestFrame();
  }
  function hit(event) {
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return -1;
    const pointer = new THREE.Vector2((event.clientX - rect.left) / rect.width * 2 - 1, -(event.clientY - rect.top) / rect.height * 2 + 1);
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(pointer, camera);
    const results = raycaster.intersectObjects(paperHits, false);
    if (!results.length) return -1;
    let object = results[0].object;
    while (object && object.userData.stage === undefined) object = object.parent;
    return object?.userData.stage ?? -1;
  }

  try {
    renderer = new THREE.WebGLRenderer({alpha:true, antialias:true, powerPreference:'low-power'});
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.08;
    renderer.setClearColor(0x000000, 0);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.shadowMap.autoUpdate = false;
    canvas = renderer.domElement;
    canvas.setAttribute('aria-hidden', 'true');
    canvas.setAttribute('data-pm-scene', '');
    canvas.tabIndex = -1;
    canvas.style.cssText = 'display:block;width:100%;height:100%;outline:none;touch-action:pan-y;';
    listen(canvas, 'webglcontextlost', event => {
      event.preventDefault();
      fail(new Error('3D 표시가 중단되었습니다. 기본 그림으로 이어서 볼 수 있습니다.'));
    });
    scene.add(new THREE.HemisphereLight(0xf6fbf8, 0x607480, 2.0));
    keyLight = new THREE.DirectionalLight(0xffffff, 2.7);
    keyLight.position.set(-4, 9, 5);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(512, 512);
    keyLight.shadow.camera.left = -7; keyLight.shadow.camera.right = 7;
    keyLight.shadow.camera.top = 6; keyLight.shadow.camera.bottom = -6;
    keyLight.shadow.camera.near = 0.5; keyLight.shadow.camera.far = 25;
    keyLight.shadow.normalBias = 0.035;
    keyLight.shadow.bias = -0.0002;
    keyLight.shadow.radius = 3;
    scene.add(keyLight);
    const fill = new THREE.DirectionalLight(0xc8e5dc, 0.65);
    fill.position.set(6, 4, -5); scene.add(fill);
    panel(scene, 10.1, 6.18, 0.24, baseMaterial, 0, -0.25, 0, 0.32);
    // A narrow binding rail grounds the five packets as one working portfolio.
    panel(scene, 8.5, 0.038, 0.012, standard(0x49616b), 0, 0.002, -2.75, 0.009);
    for (let i = 0; i < 5; i++) groups.push(buildDocument(i));
    createRoute();
    groups.forEach((group, index) => {
      group.position.y += 0.38 + index * 0.07;
      group.position.x += [0.11, -0.09, 0.08, -0.12, 0.06][index];
      group.rotation.y = [-0.13, 0.14, -0.07, 0.1, -0.12][index];
    });
    accents[0].color.set(palette.gold);
    motionQuery = win.matchMedia('(prefers-reduced-motion: reduce)');
    animation = {from:snapshot(), to:targets(0), elapsed:0, route:null};
    if (reducedMotion()) {apply(1); animation = null;}
    host.append(canvas);
    listen(doc, 'visibilitychange', () => {
      if (!visible()) stopFrame();
      else requestFrame();
    });
    const motionChanged = () => {
      if (reducedMotion() && animation) {apply(1); animation = null; stopFrame();}
      requestFrame();
    };
    if (motionQuery.addEventListener) listen(motionQuery, 'change', motionChanged);
    else {
      motionQuery.addListener(motionChanged);
      listeners.push(() => motionQuery.removeListener(motionChanged));
    }
    listen(canvas, 'pointerdown', event => {
      if (event.isPrimary && event.button === 0) pointerStart = {x:event.clientX, y:event.clientY, id:event.pointerId};
    });
    listen(canvas, 'pointercancel', () => {pointerStart = null;});
    listen(canvas, 'pointerup', event => {
      const start = pointerStart; pointerStart = null;
      if (!start || start.id !== event.pointerId || Math.hypot(event.clientX-start.x, event.clientY-start.y) > 8) return;
      const index = hit(event);
      if (index >= 0) {
        setStage(index);
        onSelect(index);
      }
    });
    listen(canvas, 'pointermove', event => {
      if (event.pointerType !== 'mouse' || !visible()) return;
      const next = hit(event);
      if (next !== hovered) {hovered = next; canvas.style.cursor = next >= 0 ? 'pointer' : 'default';}
    }, {passive:true});
    listen(canvas, 'pointerleave', () => {hovered = -1; canvas.style.cursor = 'default';});
    if (win.ResizeObserver) {
      resizeObserver = new win.ResizeObserver(resize);
      resizeObserver.observe(host);
    } else listen(win, 'resize', resize, {passive:true});
    if (win.IntersectionObserver) {
      intersectionObserver = new win.IntersectionObserver(entries => {
        inViewport = entries.some(entry => entry.isIntersecting);
        if (!inViewport) stopFrame();
        else requestFrame();
      }, {threshold:0.01});
      intersectionObserver.observe(host);
    }
    resize();
    return {setStage, dispose};
  } catch (error) {
    dispose();
    throw error;
  }
}
