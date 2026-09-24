import './game-guide.css';

let guides = new Map();

function fillList(id, values) {
  const list = document.getElementById(id);
  list.replaceChildren(...values.map(value => {
    const item = document.createElement('li');
    item.textContent = value;
    return item;
  }));
}

export async function loadGameGuides() {
  const response = await fetch('/game-guides.json');
  if (!response.ok) throw new Error(`游戏指南 HTTP ${response.status}`);
  const data = await response.json();
  if (!Array.isArray(data.guides)) throw new Error('游戏指南格式无效');
  const isText = value => typeof value === 'string' && value.trim().length > 0;
  const validSources = sources => Array.isArray(sources) && sources.every(source => {
    try { return isText(source.title) && new URL(source.url).protocol === 'https:'; }
    catch { return false; }
  });
  if (data.guides.some(guide => !guide || ![guide.modelId, guide.region, guide.mode, guide.summary, guide.tactics, guide.basis, guide.reviewedAt, guide.ammo?.advice, guide.ammo?.note].every(isText)
    || !Array.isArray(guide.strengths) || !guide.strengths.every(isText)
    || !Array.isArray(guide.limitations) || !guide.limitations.every(isText)
    || !validSources(guide.sources))
    || new Set(data.guides.map(guide => guide.modelId)).size !== data.guides.length) throw new Error('游戏指南内容无效');
  guides = new Map(data.guides.map(guide => [guide.modelId, guide]));
}

export function renderGameGuide(modelId) {
  const root = document.getElementById('game-guide');
  const guide = guides.get(modelId);
  root.hidden = !guide;
  if (!guide) return;

  document.getElementById('game-guide-scope').textContent = `${guide.region} · ${guide.mode}`;
  document.getElementById('game-guide-summary').textContent = guide.summary;
  fillList('game-guide-strengths', guide.strengths);
  fillList('game-guide-limitations', guide.limitations);
  document.getElementById('game-guide-tactics').textContent = guide.tactics;
  document.getElementById('game-guide-ammo').textContent = guide.ammo.advice;
  document.getElementById('game-guide-ammo-note').textContent = guide.ammo.note;
  document.getElementById('game-guide-basis').textContent = `${guide.basis} · 资料核对：${guide.reviewedAt}`;

  const sourceItems = guide.sources.map(source => {
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = source.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = source.title;
    item.append(link);
    return item;
  });
  document.getElementById('game-guide-sources').replaceChildren(...sourceItems);
}
