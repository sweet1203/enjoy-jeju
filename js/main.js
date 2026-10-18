// 화면 그리기 — 내용은 data.js에서 고치세요.

const $ = (sel) => document.querySelector(sel);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
// 빈칸은 "작성 예정"으로 표시
const val = (s) => (s && String(s).trim() ? esc(s) : '<span class="todo">작성 예정</span>');

// 모바일 메뉴
const toggle = $(".nav-toggle");
const links = $(".nav-links");
toggle.addEventListener("click", () => {
  const open = links.classList.toggle("open");
  toggle.setAttribute("aria-expanded", open);
});
links.addEventListener("click", (e) => {
  if (e.target.tagName === "A") links.classList.remove("open");
});

// 메인 사진 카드: 누르면 180도 뒤집기
document.querySelectorAll(".flip-card").forEach((card) => {
  card.addEventListener("click", () => {
    const on = card.classList.toggle("flipped");
    card.setAttribute("aria-pressed", String(on));
  });
});

// 확장 트랙 탭
document.querySelectorAll(".track-tab[aria-controls]").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".track-tab[aria-controls]").forEach((t) => {
      const on = t === tab;
      t.classList.toggle("on", on);
      t.setAttribute("aria-selected", String(on));
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
  });
});

// 수업계획안 카드
function renderLessons() {
  $("#lesson-grid").innerHTML = LESSONS.map((l) => `
    <button class="lesson-card" data-id="${l.id}" aria-expanded="false" aria-controls="lesson-detail">
      <span class="tag">${esc(l.area)}</span>
      <h3>${l.icon} ${esc(l.title)}</h3>
      <p>${val(l.summary)}</p>
      <span class="lesson-meta">${[l.grade, l.periods, l.teacher].filter(Boolean).map(esc).join(" · ") || "세부 내용 작성 예정"}</span>
      <span class="lesson-open">자세히 보기 ▼</span>
    </button>`).join("");
}

// 상세 계획안 — 카드를 누르면 아래로 펼쳐지고, 한글(.hwpx) 파일로 저장할 수 있습니다.
const detail = $("#lesson-detail");
let openId = null;

// 수업 흐름을 한글 지도안 표 모양으로: [제목] 줄은 소제목, 그 아래 줄들은 테두리 상자
function stageHTML(text) {
  if (!text || !String(text).trim()) return `<p>${val("")}</p>`;
  const out = []; let box = [];
  const flush = () => { if (box.length) out.push(`<div class="plan-box">${box.map((t) => `<p class="${/^\s*[-0-9(]/.test(t) ? "sub" : ""}">${esc(t.trim())}</p>`).join("")}</div>`); box = []; };
  for (const line of String(text).split("\n")) {
    if (!line.trim()) { flush(); continue; }
    if (/^\s*\[.*\]\s*$/.test(line)) { flush(); out.push(`<p class="plan-head">${esc(line.trim())}</p>`); }
    else box.push(line);
  }
  flush();
  return out.join("");
}
function flowTable(l) {
  const fm = l.flowMaterials || {};
  const row = (name, key) => `<tr><th class="stage">${name}</th><td class="act">${stageHTML(l.flow[key])}</td><td class="mat">${fm[key] ? esc(fm[key]) : ""}</td></tr>`;
  return `<div class="table-wrap"><table class="hwp-flow">
    <thead><tr><th>학습단계</th><th>교수 · 학습 활동</th><th>학습자료 및 비고사항</th></tr></thead>
    <tbody>${row("도 입", "intro")}${row("전 개", "main")}${row("정 리", "close")}</tbody>
  </table></div>`;
}

function detailHTML(l) {
  return `
    <div class="detail-head">
      <div>
        <span class="tag">${esc(l.area)}</span>
        <h3 class="detail-title">${l.icon} ${esc(l.title)}</h3>
      </div>
      <div class="detail-actions">
        <button type="button" class="btn-mini hwpx-save" data-id="${esc(l.id)}">⬇ 한글(.hwpx)로 저장</button>
        ${l.file ? `<a class="btn-mini" href="${esc(l.file.href)}" download="${esc(l.file.name || "")}">⬇ 지도안 (.hwp)</a>` : ""}
        ${l.file ? `<button type="button" class="btn-mini ghost plan-peek" data-img="${esc(l.file.href.replace(/\.hwp$/, ".webp"))}">📄 지도안 미리보기</button>` : ""}
        <button class="btn-mini ghost fold-btn">접기 ▲</button>
      </div>
    </div>
    <div class="pv-paper plan-peek-box" hidden></div>
    <table class="info-table">
      <tr><th>교과</th><td>${esc(l.subject || "정보")}</td><th>대상</th><td>${val(l.grade)}</td></tr>
      <tr><th>차시</th><td>${val(l.periods)}</td><th>담당</th><td>${val(l.teacher)}</td></tr>
    </table>
    <h4>성취기준</h4><p>${val(l.standards)}</p>
    <h4>학습 목표</h4>${l.goals.length ? `<ul>${l.goals.map((g) => `<li>${esc(g)}</li>`).join("")}</ul>` : `<p>${val("")}</p>`}
    <h4>수업 흐름</h4>
    ${flowTable(l)}
    <h4>평가 계획</h4><p>${val(l.assessment)}</p>
    <h4>준비물 · 자료</h4><p>${val(l.materials)}</p>
    <h4>💡 수업 팁</h4><p>${val(l.tips)}</p>`;
}

function toggleLesson(id) {
  const same = openId === id && !detail.hidden;
  document.querySelectorAll(".lesson-card").forEach((c) =>
    c.setAttribute("aria-expanded", String(!same && c.dataset.id === id)));
  if (same) { detail.hidden = true; openId = null; return; }
  openId = id;
  detail.innerHTML = detailHTML(LESSONS.find((x) => x.id === id));
  detail.hidden = false;
  detail.classList.remove("opening"); void detail.offsetWidth; detail.classList.add("opening");
  detail.scrollIntoView({ behavior: "smooth", block: "start" });
}

$("#lesson-grid").addEventListener("click", (e) => {
  const card = e.target.closest(".lesson-card");
  if (card) toggleLesson(card.dataset.id);
});
detail.addEventListener("click", (e) => {
  if (e.target.closest(".fold-btn")) toggleLesson(openId);
  const save = e.target.closest(".hwpx-save");
  if (save) saveHwpx(save);
  const peek = e.target.closest(".plan-peek");
  if (peek) {
    const box = detail.querySelector(".plan-peek-box");
    const open = box.hidden;
    if (open && !box.innerHTML) box.innerHTML = `<img src="${peek.dataset.img}" alt="교수·학습 지도안 (한글 문서 미리보기)" />`;
    box.hidden = !open;
    peek.textContent = open ? "📄 지도안 닫기" : "📄 지도안 미리보기";
  }
});

// 한글(.hwpx) 파일 만들기 — 버튼을 누를 때만 변환 라이브러리를 불러옵니다.
const HWP_LIB = "https://cdn.jsdelivr.net/npm/hwp-convert@1.13.0/dist/browser/hwp-convert.browser.mjs";
const plain = (s) => (s && String(s).trim() ? esc(s).replace(/\n/g, "<br/>") : "작성 예정");

function exportHTML(l) {
  const cell = 'style="border:1px solid #999;padding:6px 8px;"';
  const head = 'style="border:1px solid #999;padding:6px 8px;background-color:#e6f4f9;font-weight:bold;"';
  const h = (t) => `<h3>${t}</h3>`;
  return `
    <h1 style="text-align:center;">${esc(l.title)} 수업계획안</h1>
    <table style="width:100%;border-collapse:collapse;">
      <tr><td ${head}>교과</td><td ${cell}>${esc(l.subject || "정보")}</td><td ${head}>대상</td><td ${cell}>${plain(l.grade)}</td></tr>
      <tr><td ${head}>차시</td><td ${cell}>${plain(l.periods)}</td><td ${head}>담당</td><td ${cell}>${plain(l.teacher)}</td></tr>
      <tr><td ${head}>영역</td><td ${cell} colspan="3">${esc(l.area)}</td></tr>
    </table>
    ${h("1. 성취기준")}<p>${plain(l.standards)}</p>
    ${h("2. 학습 목표")}${l.goals.length ? `<ol>${l.goals.map((g) => `<li>${esc(g)}</li>`).join("")}</ol>` : "<p>작성 예정</p>"}
    ${h("3. 수업 흐름")}
    <table style="width:100%;border-collapse:collapse;">
      <tr><td ${head}>학습단계</td><td ${head}>교수 · 학습 활동</td><td ${head}>학습자료 및 비고사항</td></tr>
      <tr><td ${head}>도입</td><td ${cell}>${plain(l.flow.intro)}</td><td ${cell}>${plain((l.flowMaterials || {}).intro)}</td></tr>
      <tr><td ${head}>전개</td><td ${cell}>${plain(l.flow.main)}</td><td ${cell}>${plain((l.flowMaterials || {}).main)}</td></tr>
      <tr><td ${head}>정리</td><td ${cell}>${plain(l.flow.close)}</td><td ${cell}>${plain((l.flowMaterials || {}).close)}</td></tr>
    </table>
    ${h("4. 평가 계획")}<p>${plain(l.assessment)}</p>
    ${h("5. 준비물 · 자료")}<p>${plain(l.materials)}</p>
    ${h("6. 수업 팁")}<p>${plain(l.tips)}</p>
    <p style="text-align:right;">팀 속전속결 · 즐겨라 제주</p>`;
}

async function saveHwpx(btn) {
  const l = LESSONS.find((x) => x.id === btn.dataset.id);
  const label = btn.textContent;
  btn.disabled = true; btn.textContent = "만드는 중…";
  try {
    const { htmlToHwpx } = await import(HWP_LIB);
    const bytes = await htmlToHwpx(exportHTML(l), { title: `${l.title} 수업계획안`, creator: "팀 속전속결", page: { size: "A4", orientation: "portrait" } });
    const url = URL.createObjectURL(new Blob([bytes], { type: "application/hwp+zip" }));
    const a = Object.assign(document.createElement("a"), { href: url, download: `${l.title} 수업계획안.hwpx` });
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  } catch (err) {
    console.error(err);
    alert("한글 파일을 만들지 못했어요. 잠시 후 다시 시도해 주세요.");
  } finally {
    btn.disabled = false; btn.textContent = label;
  }
}

// 지도안 내려받기 · 미리보기 버튼
const planDl = (p) => `<a class="btn-mini" href="${esc(p.plan)}" download="${p.no}차시_교수학습지도안.hwp">⬇ 지도안 (.hwp)</a>`;
const sheetBtn = (p) => `<a class="btn-mini ghost" href="${esc(p.href)}" target="_blank" rel="noopener">📝 학습지 열기</a>`;

// 차시별 안내 — 차시 버튼을 누르면 목표 · 흐름 · 활동과 자료 버튼이 보입니다.
let guideNo = 1;
function renderGuide(no) {
  guideNo = no;
  const p = LESSON_PAGES.find((x) => x.no === no) || LESSON_PAGES[0];
  $("#guide-tabs").innerHTML = LESSON_PAGES.map((x) => `
    <button class="track-tab${x.no === p.no ? " on" : ""}" role="tab" aria-selected="${x.no === p.no}" data-no="${x.no}">${x.no}차시</button>`).join("");
  $("#guide-body").innerHTML = `
    <div class="plan-block guide-card">
      <p class="lp-no">${p.no}차시</p>
      <h3>${esc(p.title)}</h3>
      <div class="guide-actions">
        ${planDl(p)}
        <button type="button" class="btn-mini ghost guide-peek" aria-expanded="false">📄 지도안 미리보기</button>
        ${sheetBtn(p)}
      </div>
      <div class="pv-paper guide-peek-box" hidden></div>
      <h4>🎯 학습 목표</h4>
      <ol class="guide-goals">${p.goals.map((g) => `<li>${esc(g)}</li>`).join("")}</ol>
      <h4>🔄 수업 흐름</h4>
      <div class="table-wrap"><table class="plan-table guide-flow"><tbody>
        <tr><th>도입</th><td>${esc(p.flow.intro)}</td></tr>
        <tr><th>전개</th><td>${esc(p.flow.main)}</td></tr>
        <tr><th>정리</th><td>${esc(p.flow.close)}</td></tr>
      </tbody></table></div>
      <h4>🧩 주요 활동</h4>
      <ul class="guide-acts">${p.acts.map((a) => `<li>${esc(a)}</li>`).join("")}</ul>
    </div>`;
}
$("#guide-tabs").addEventListener("click", (e) => {
  const b = e.target.closest(".track-tab");
  if (b) location.hash = `guide-${b.dataset.no}`;
});
$("#guide-body").addEventListener("click", (e) => {
  const peek = e.target.closest(".guide-peek");
  if (!peek) return;
  const p = LESSON_PAGES.find((x) => x.no === guideNo);
  const box = $("#guide-body .guide-peek-box");
  const open = box.hidden;
  if (open && !box.innerHTML) box.innerHTML = `<img src="${esc(p.planImg)}" alt="${p.no}차시 교수·학습 지도안 (한글 문서 미리보기)" />`;
  box.hidden = !open;
  peek.setAttribute("aria-expanded", String(open));
  peek.textContent = open ? "📄 미리보기 닫기" : "📄 지도안 미리보기";
});

// 자료실 — 차시별 지도안 · 학습지 표, 코드 파일
$("#resource-list").innerHTML = `
  <div class="table-wrap"><table class="plan-table res-table">
    <thead><tr><th>차시</th><th>주제</th><th>지도안</th><th>학습지</th></tr></thead>
    <tbody>${LESSON_PAGES.map((p) => `
      <tr><td>${p.no}</td>
        <td><b>${esc(p.title)}</b><small>${esc(p.desc)}</small></td>
        <td class="res-btns">${planDl(p)} <a class="btn-mini ghost" href="#guide-${p.no}">📄 미리보기</a></td>
        <td class="res-btns">${sheetBtn(p)}</td></tr>`).join("")}
    </tbody>
  </table></div>`;
$("#code-list").innerHTML = `<div class="tc-links">${CODE_FILES.map((f) => `
  <button type="button" class="tc-link code-peek code-card" data-src="${esc(f.href)}"><b>📄 ${esc(f.name)}</b><span>${esc(f.desc)}</span></button>`).join("")}</div>
  <div class="code-viewer" hidden>
    <div class="cv-head"><b class="cv-name"></b><span class="cv-btns"><button type="button" class="cv-copy">📋 복사</button><button type="button" class="cv-close" aria-label="닫기">✕</button></span></div>
    <div class="cv-body"></div>
  </div>`;

// 팀 소개 — 제주 게임 맵 위의 캐릭터, 머리 위에 소개 말풍선
$("#team-grid").innerHTML = TEAM.map((m, i) => `
  <div class="member npc" style="--d:${(i % 3) * 0.35}s">
    <div class="npc-bubble">
      <p class="npc-role"><span>${esc(m.role)}</span> ${esc(m.roleDesc)}</p>
      ${m.school ? `<p>🏫 ${esc(m.school)}</p>` : ""}
      ${m.region ? `<p>📍 ${esc(m.region)}</p>` : ""}
    </div>
    <img class="npc-sprite" src="${m.img}" alt="${esc(m.name)} 선생님 캐릭터" loading="lazy" />
    <p class="npc-name">${esc(m.name)} <small>정보 교사</small></p>
    <div class="npc-ground" aria-hidden="true"></div>
  </div>`).join("");

// 의견 나누기 (패들릿)
const fb = $("#feedback-btn");
if (FEEDBACK_FORM_URL) fb.href = FEEDBACK_FORM_URL;
else { fb.textContent = "의견 폼 준비 중"; fb.classList.add("disabled"); fb.removeAttribute("href"); }

// 위 메뉴 탭 — 주소 끝(#)에 따라 한 화면씩 보여 줍니다.
const TABS = ["home", "overview", "guide", "resources", "course", "ai", "feedback"];
// 예전 주소(#team, #plan 등)로 들어와도 맞는 탭으로 보냅니다.
const OLD_HASH = { top: "home", team: "home", about: "home", plan: "overview", lessons: "resources", extend: "ai" };
function showTab() {
  const h = decodeURIComponent(location.hash.slice(1));
  const g = h.match(/^guide-(\d)$/);
  const tab = g ? "guide" : TABS.includes(h) ? h : OLD_HASH[h] || "home";
  if (g) renderGuide(Number(g[1]));
  document.querySelectorAll(".tab-panel").forEach((p) => (p.hidden = p.dataset.tab !== tab));
  document.querySelectorAll(".nav-links a").forEach((a) => {
    const on = a.dataset.tab === tab;
    a.classList.toggle("active", on);
    if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
  // 패들릿은 의견 나누기 탭을 처음 열 때 불러옵니다. (주소 끝의 보드 ID로 임베드 주소를 만든다)
  if (tab === "feedback" && FEEDBACK_FORM_URL && !$("#padlet-frame").src) {
    const padletId = FEEDBACK_FORM_URL.split("/").pop().split("-").pop();
    $("#padlet-frame").src = `https://padlet.com/embed/${padletId}`;
  }
  window.scrollTo({ top: 0 });
}
window.addEventListener("hashchange", showTab);

renderLessons();
renderGuide(1);
showTab();

// 코드 파일 미리보기 (내려받지 않고 아래에 펼치기)
document.querySelectorAll(".code-peek").forEach((link) => {
  link.addEventListener("click", async (ev) => {
    ev.preventDefault();
    const viewer = link.closest(".plan-block").querySelector(".code-viewer");
    const url = link.dataset.src;
    const name = url.split("/").pop();
    const peers = link.closest(".plan-block").querySelectorAll(".code-peek");
    if (!viewer.hidden && viewer.dataset.src === url) {
      viewer.hidden = true; link.classList.remove("on"); return;
    }
    peers.forEach((a) => a.classList.toggle("on", a === link));
    viewer.dataset.src = url;
    viewer.querySelector(".cv-name").textContent = "📄 " + name;
    const body = viewer.querySelector(".cv-body");
    body.textContent = "불러오는 중…";
    viewer.hidden = false;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(res.status);
      const text = (await res.text()).replace(/^\uFEFF/, "");
      viewer.dataset.text = text;
      if (name.endsWith(".csv")) {
        const rows = text.trim().split(/\r?\n/).map((r) => r.split(","));
        body.innerHTML = `<div class="table-wrap"><table class="plan-table cv-table"><thead><tr>${rows[0].map((c) => `<th>${esc(c)}</th>`).join("")}</tr></thead><tbody>${rows.slice(1).map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
      } else {
        const pre = document.createElement("pre");
        const code = document.createElement("code");
        code.textContent = text;
        pre.appendChild(code);
        body.replaceChildren(pre);
      }
    } catch (e) {
      body.textContent = "파일을 불러오지 못했어요. 잠시 후 다시 눌러 보세요.";
    }
    viewer.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
});
document.querySelectorAll(".code-viewer").forEach((viewer) => {
  viewer.querySelector(".cv-close").addEventListener("click", () => {
    viewer.hidden = true;
    viewer.closest(".plan-block").querySelectorAll(".code-peek").forEach((a) => a.classList.remove("on"));
  });
  viewer.querySelector(".cv-copy").addEventListener("click", async (ev) => {
    try { await navigator.clipboard.writeText(viewer.dataset.text || ""); ev.target.textContent = "✅ 복사됨"; }
    catch (e) { ev.target.textContent = "복사 실패"; }
    setTimeout(() => (ev.target.textContent = "📋 복사"), 1500);
  });
});
