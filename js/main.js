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

// 수업계획안 카드 + 영역 필터
function renderLessons(area) {
  const list = area ? LESSONS.filter((l) => l.area === area) : LESSONS;
  $("#lesson-grid").innerHTML = list.map((l) => `
    <button class="lesson-card" data-id="${l.id}">
      <span class="lesson-icon">${l.icon}</span>
      <span class="tag">${esc(l.area)}</span>
      <h3>${esc(l.title)}</h3>
      <p>${val(l.summary)}</p>
      <span class="lesson-meta">${[l.grade, l.periods, l.teacher].filter(Boolean).map(esc).join(" · ") || "세부 내용 작성 예정"}</span>
    </button>`).join("");
}

function renderFilters() {
  const areas = ["전체", ...new Set(LESSONS.map((l) => l.area))];
  $("#filters").innerHTML = areas.map((a, i) =>
    `<button class="chip${i === 0 ? " active" : ""}" data-area="${esc(a)}">${esc(a)}</button>`).join("");
  $("#filters").addEventListener("click", (e) => {
    const chip = e.target.closest(".chip");
    if (!chip) return;
    document.querySelectorAll(".chip").forEach((c) => c.classList.toggle("active", c === chip));
    renderLessons(chip.dataset.area === "전체" ? null : chip.dataset.area);
  });
}

// 상세 계획안 (통일 양식)
const modal = $("#lesson-modal");
function openLesson(id) {
  const l = LESSONS.find((x) => x.id === id);
  $("#modal-body").innerHTML = `
    <span class="tag">${esc(l.area)}</span>
    <h2>${l.icon} ${esc(l.title)}</h2>
    <table class="info-table">
      <tr><th>교과</th><td>정보</td><th>대상</th><td>${val(l.grade)}</td></tr>
      <tr><th>차시</th><td>${val(l.periods)}</td><th>담당</th><td>${val(l.teacher)}</td></tr>
    </table>
    <h3>성취기준</h3><p>${val(l.standards)}</p>
    <h3>학습 목표</h3>${l.goals.length ? `<ul>${l.goals.map((g) => `<li>${esc(g)}</li>`).join("")}</ul>` : `<p>${val("")}</p>`}
    <h3>수업 흐름</h3>
    <div class="flow">
      <div><b>도입</b><p>${val(l.flow.intro)}</p></div>
      <div><b>전개</b><p>${val(l.flow.main)}</p></div>
      <div><b>정리</b><p>${val(l.flow.close)}</p></div>
    </div>
    <h3>평가 계획</h3><p>${val(l.assessment)}</p>
    <h3>준비물 · 자료</h3><p>${val(l.materials)}</p>
    <h3>💡 수업 팁</h3><p>${val(l.tips)}</p>`;
  modal.showModal();
}
$("#lesson-grid").addEventListener("click", (e) => {
  const card = e.target.closest(".lesson-card");
  if (card) openLesson(card.dataset.id);
});
$(".modal-close").addEventListener("click", () => modal.close());
modal.addEventListener("click", (e) => { if (e.target === modal) modal.close(); });

// 자료실
$("#resource-list").innerHTML = LESSONS.map((l) => `
  <div class="resource-item">
    <span>${l.icon} <b>${esc(l.title)}</b> <small>${esc(l.teacher || "")}</small></span>
    <span class="resource-files">활동지 · PPT · 루브릭 <em>(업로드 예정)</em></span>
  </div>`).join("");

// 팀 소개
$("#team-grid").innerHTML = TEAM.map((m) => `
  <div class="member">
    <img src="${m.img}" alt="${esc(m.name)} 캐릭터" loading="lazy" />
    <span class="role">${esc(m.role)}</span>
    <h3>${esc(m.name)} <small class="subject">정보 교사</small></h3>
    <p class="role-desc">${esc(m.roleDesc)}</p>
  </div>`).join("");

// 의견 남기기
const fb = $("#feedback-btn");
if (FEEDBACK_FORM_URL) fb.href = FEEDBACK_FORM_URL;
else { fb.textContent = "의견 폼 준비 중"; fb.classList.add("disabled"); fb.removeAttribute("href"); }

renderFilters();
renderLessons();
