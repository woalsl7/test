const $ = (id) => document.getElementById(id);
const safe = (v) => String(v ?? '').trim();
function addText(parent, tag, content, cls) {
  const el = document.createElement(tag);
  el.textContent = safe(content);
  if (cls) el.className = cls;
  parent.append(el);
  return el;
}
function populate(select, rows, key) {
  [...new Set(rows.map(r => safe(r[key])).filter(Boolean))]
    .sort((a,b) => a.localeCompare(b, 'ko'))
    .forEach(value => {
      const opt = document.createElement('option');
      opt.value = value;
      opt.textContent = value;
      select.append(opt);
    });
}
function render(rows) {
  const matched = rows.filter(r =>
    (!$('type').value || safe(r.신고유형) === $('type').value) &&
    (!$('status').value || safe(r.처리상태) === $('status').value));
  $('count').textContent = `결과 ${matched.length}건`;
  $('cards').replaceChildren();
  $('empty').hidden = matched.length !== 0;
  for (const r of matched) {
    const card = document.createElement('article');
    card.className = 'case';
    const header = addText(card, 'div', '', 'case-top');
    addText(header, 'strong', r.신고유형 || '유형 미상');
    addText(header, 'span', r.처리상태 || '상태 미상', 'tag');
    const dl = addText(card, 'dl', '');
    for (const key of ['신고일자','신고유형','지역','처리상태']) {
      const entry = document.createElement('div');
      addText(entry, 'dt', key);
      addText(entry, 'dd', safe(r[key]) || '미기재');
      dl.append(entry);
    }
    $('cards').append(card);
  }
}
async function start() {
  try {
    const response = await fetch('data/reports.json');
    if (!response.ok) throw Error('신고 JSON 로딩 실패');
    const reports = await response.json();
    if (!Array.isArray(reports)) throw Error('신고 JSON 배열 형식이 아닙니다');
    populate($('type'), reports, '신고유형');
    populate($('status'), reports, '처리상태');
    for (const id of ['type','status']) $(id).addEventListener('change', () => render(reports));
    $('reset').addEventListener('click', () => {
      $('type').value = '';
      $('status').value = '';
      render(reports);
    });
    render(reports);
  } catch (error) {
    $('empty').hidden = false;
    $('empty').textContent = `신고 데이터를 불러올 수 없습니다: ${error.message}`;
  }
  try {
    const response = await fetch('data/news.json');
    if (!response.ok) throw Error('정책 소식 로딩 실패');
    const obj = await response.json();
    $('newsnote').textContent = obj.note || '';
    for (const entry of (obj.items || [])) {
      if (!/^https:\/\/(www\.)?korea\.kr\//.test(entry.url || '')) continue;
      const li = document.createElement('li');
      const anchor = document.createElement('a');
      anchor.href = entry.url;
      anchor.target = '_blank';
      anchor.rel = 'noopener noreferrer';
      anchor.textContent = entry.title;
      li.append(anchor);
      addText(li, 'time', entry.date || '');
      $('news').append(li);
    }
  } catch (error) {
    $('newsnote').textContent = '정책 소식을 불러오지 못했습니다.';
  }
}
start();
