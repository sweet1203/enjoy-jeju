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
document.querySelectorAll(".track-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".track-tab").forEach((t) => {
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
        ${l.file ? `<button type="button" class="btn-mini plan-peek" data-img="${esc(l.file.href.replace(/\.hwp$/, ".webp"))}">📄 지도안 미리보기</button>` : ""}
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

// 자료실 — 차시 카드 + 지도안 미리보기(한글 파일 모양 그대로)
$("#resource-list").innerHTML = `
  <a class="res-setup" href="lessons/setup.html"><b>🔑 실습 준비 · 튜링 실행 따라하기 카드</b><span>각자 VESSL 로그인 → 작업공간 → 터미널 실행 → 고치고 다시 실행 · 자주 나는 오류 (1~3차시)</span></a>
  <div class="lesson-pages">${LESSON_PAGES.map((p) => `
    <div class="lesson-page" data-no="${p.no}">
      <a class="lp-main" href="${esc(p.href)}">
        <span class="lp-no">${p.no}차시</span>
        <b>${esc(p.title)}</b>
        <small>${esc(p.desc)}</small>
        <span class="lp-go">수업 자료 · 학습지 열기 →</span>
      </a>
      ${p.planImg ? `<button type="button" class="lp-plan" data-no="${p.no}" aria-expanded="false" aria-controls="plan-viewer">📄 ${p.no}차시 지도안 보기</button>` : ""}
    </div>`).join("")}</div>
  <div class="plan-viewer" id="plan-viewer" hidden></div>`;

const viewer = $("#plan-viewer");
let shownPlan = null;
function showPlan(no) {
  const p = LESSON_PAGES.find((x) => x.no === no);
  const same = shownPlan === no && !viewer.hidden;
  document.querySelectorAll(".lp-plan").forEach((b) => {
    const on = !same && Number(b.dataset.no) === no;
    b.setAttribute("aria-expanded", String(on));
    b.closest(".lesson-page").classList.toggle("on", on);
    b.textContent = `📄 ${b.dataset.no}차시 지도안 ${on ? "닫기" : "보기"}`;
  });
  if (same) { viewer.hidden = true; shownPlan = null; return; }
  shownPlan = no;
  viewer.innerHTML = `
    <div class="pv-head">
      <b>${p.no}차시 교수·학습 지도안</b>
      <span class="pv-actions">
        <button type="button" class="btn-mini ghost pv-close">닫기 ✕</button>
      </span>
    </div>
    <div class="pv-paper"><img src="${esc(p.planImg)}" alt="${p.no}차시 교수·학습 지도안 (한글 문서 미리보기)" /></div>`;
  viewer.hidden = false;
  viewer.scrollIntoView({ behavior: "smooth", block: "start" });
}
$("#resource-list").addEventListener("click", (e) => {
  const b = e.target.closest(".lp-plan");
  if (b) showPlan(Number(b.dataset.no));
  if (e.target.closest(".pv-close")) showPlan(shownPlan);
});

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
if (FEEDBACK_FORM_URL) {
  fb.href = FEEDBACK_FORM_URL;
  // 패들릿 주소 끝의 보드 ID로 화면 안에 넣을 임베드 주소를 만든다.
  const padletId = FEEDBACK_FORM_URL.split("/").pop().split("-").pop();
  $("#padlet-frame").src = `https://padlet.com/embed/${padletId}`;
}
else { fb.textContent = "의견 폼 준비 중"; fb.classList.add("disabled"); fb.removeAttribute("href"); }

// 현재 위치 바 (오른쪽) — 스크롤하면 지금 보고 있는 섹션이 표시됩니다.
function renderSpy() {
  const spy = $("#spy");
  if (!spy) return;
  const secs = [
    { el: $(".hero"), label: "처음" },
    ...[...document.querySelectorAll("main section[id]")].map((el) => ({
      el, label: el.querySelector("h2").textContent.replace(/^[^\p{L}]+/u, "").trim(),
    })),
  ];
  spy.innerHTML = `<div class="spy-track"><i class="spy-fill"></i></div>
    <ol>${secs.map((s, i) => `<li><a href="#${s.el.id || "top"}" data-i="${i}"><span>${esc(s.label)}</span></a></li>`).join("")}</ol>`;
  const links = [...spy.querySelectorAll("a")];
  const fill = spy.querySelector(".spy-fill");

  function update() {
    const y = window.scrollY + window.innerHeight * 0.4;
    let cur = 0;
    secs.forEach((s, i) => { if (s.el.offsetTop <= y) cur = i; });
    links.forEach((a, i) => {
      a.classList.toggle("active", i === cur);
      a.classList.toggle("passed", i < cur);
    });
    const max = document.documentElement.scrollHeight - window.innerHeight;
    fill.style.height = (max > 0 ? Math.min(100, (window.scrollY / max) * 100) : 0) + "%";
  }
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
}

renderLessons();
renderSpy();

// 코드 파일 미리보기 (내려받지 않고 아래에 펼치기)
document.querySelectorAll("a.code-peek").forEach((link) => {
  link.addEventListener("click", async (ev) => {
    ev.preventDefault();
    const viewer = link.closest(".plan-block").querySelector(".code-viewer");
    const url = link.getAttribute("href");
    const name = url.split("/").pop();
    const peers = link.closest(".plan-block").querySelectorAll("a.code-peek");
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
      body.textContent = "파일을 불러오지 못했어요. ‘내려받기’로 열어 보세요.";
    }
    viewer.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
});
document.querySelectorAll(".code-viewer").forEach((viewer) => {
  viewer.querySelector(".cv-close").addEventListener("click", () => {
    viewer.hidden = true;
    viewer.closest(".plan-block").querySelectorAll("a.code-peek").forEach((a) => a.classList.remove("on"));
  });
  viewer.querySelector(".cv-copy").addEventListener("click", async (ev) => {
    try { await navigator.clipboard.writeText(viewer.dataset.text || ""); ev.target.textContent = "✅ 복사됨"; }
    catch (e) { ev.target.textContent = "복사 실패"; }
    setTimeout(() => (ev.target.textContent = "📋 복사"), 1500);
  });
});
