/* Shared navigation and data access for the local ERP and the Pages edition. */
(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src);
  const isStatic = Boolean(window.PM_SITE);
  const stages = ['S0', 'S0A', 'S1', 'S1A', 'S2', 'S3', 'S4'];
  const key = 'moapay.pm.stage:' + base.pathname;
  let memoryStage = 'S0', worker, serial = 0;
  const pending = new Map();
  function currentStage() {
    try { const value = localStorage.getItem(key); if (stages.includes(value)) memoryStage = value; } catch (_) {}
    return memoryStage;
  }
  function href(path) {
    if (!isStatic) return path;
    const u = new URL(path, location.origin);
    const routes = {'/': 'erp.html', '/learn': 'learn.html', '/guide': 'guide.html', '/start': 'index.html', '/resources': 'resources.html'};
    if (u.pathname === '/download') return new URL('templates/' + encodeURIComponent(u.searchParams.get('name')), base).href;
    return new URL((routes[u.pathname] || u.pathname.replace(/^\//, '')) + u.search + u.hash, base).href;
  }
  function stopWorker(message) {
    if (worker) worker.terminate(); worker = null;
    for (const p of pending.values()) { clearTimeout(p.timer); p.reject(Error(message)); }
    pending.clear();
  }
  function request(route, params = {}, body = {}, stage = currentStage()) {
    if (!worker) {
      worker = new Worker(new URL('sqlite-worker.js', base));
      worker.onmessage = ({data}) => {
        const p = pending.get(data.id); if (!p) return;
        clearTimeout(p.timer); pending.delete(data.id);
        data.error ? p.reject(Error(data.error)) : p.resolve(data.result);
      };
      worker.onerror = () => stopWorker('자료를 열지 못했습니다. 페이지를 새로고침한 뒤 다시 조회하세요.');
    }
    return new Promise((resolve, reject) => {
      const id = ++serial;
      const timer = setTimeout(() => stopWorker('조회 시간이 길어 중단했습니다. 조건을 좁혀 다시 조회하세요.'), route === '/api/sql' ? 4000 : 20000);
      pending.set(id, {resolve, reject, timer});
      worker.postMessage({id, route, params, body, stage});
    });
  }
  async function api(path, options) {
    if (!isStatic) {
      const r = await fetch(path, options), data = await r.json();
      if (!r.ok) throw Error(data.error || '자료를 읽지 못했습니다.');
      return data;
    }
    const u = new URL(path, location.origin), params = Object.fromEntries(u.searchParams);
    const body = options?.body ? JSON.parse(options.body) : {};
    const stage = currentStage();
    if (u.pathname === '/api/stage') {
      if (!stages.includes(body.stage)) throw Error('자료 단계가 올바르지 않습니다.');
      await request('/api/meta', {}, {}, body.stage);
      memoryStage = body.stage;
      try { localStorage.setItem(key, memoryStage); } catch (_) {}
      return {stage: memoryStage, message: '선택한 자료를 열었습니다. 다른 학습 탭도 같은 시점으로 갱신됩니다.'};
    }
    if (u.pathname === '/api/lesson') {
      const unit = Number(params.unit);
      if (!Number.isInteger(unit) || unit < 0 || unit > 9) throw Error('단원은 0~9입니다.');
      const response = await fetch(new URL(`lessons/${stage}/${String(unit).padStart(2, '0')}.json`, base));
      if (!response.ok) throw Error('교재를 열지 못했습니다. 새로고침 후 다시 시도하세요.');
      const lesson = await response.json(), state = await request('/api/state', {}, {}, stage);
      delete lesson.exercises; delete lesson.readerHtml;
      return {...lesson, ...state, currentStage: stage, availableStages: stages};
    }
    return request(u.pathname, params, body, stage);
  }
  async function exportCSV(params, filename) {
    if (!isStatic) {
      const a = document.createElement('a'); a.href = '/api/list?' + params; a.download = filename; a.click(); return;
    }
    const data = await api('/api/list?' + params);
    const quote = v => '"' + String(v ?? '').replace(/"/g, '""') + '"';
    const csv = '\ufeff' + [data.columns, ...data.rows.map(r => data.columns.map(c => r[c]))].map(r => r.map(quote).join(',')).join('\r\n');
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], {type: 'text/csv;charset=utf-8'}));
    a.download = filename; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  window.PMApp = {api, href, isStatic, currentStage, exportCSV};
  if (isStatic) window.addEventListener('storage', event => { if (event.key === key) location.reload(); });
})();
