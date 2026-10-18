// 즐겨라 제주 · 차시별 학습지 공통 동작
// - 적은 내용은 이 브라우저에 자동 저장됩니다(다른 기기와는 공유되지 않음).
// - 인쇄 / PDF 저장, 지우기, 자동 계산, 2글자 자르기(tokenize) 체험, JSON 검사기
(() => {
  const page = document.body.dataset.lesson || "lesson";
  const KEY = "enjoyjeju-" + page;
  const fields = () => [...document.querySelectorAll("input[name], textarea[name], select[name]")];

  // ---------- 자동 저장 ----------
  function load() {
    let data = {};
    try { data = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { data = {}; }
    for (const el of fields()) {
      const v = data[el.name + (el.type === "radio" ? ":" + el.value : "")];
      if (v === undefined) continue;
      if (el.type === "checkbox" || el.type === "radio") el.checked = !!v;
      else el.value = v;
    }
  }
  let timer;
  function save() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      const data = {};
      for (const el of fields()) {
        if (el.type === "checkbox") data[el.name] = el.checked;
        else if (el.type === "radio") data[el.name + ":" + el.value] = el.checked;
        else data[el.name] = el.value;
      }
      try {
        localStorage.setItem(KEY, JSON.stringify(data));
        const s = document.querySelector(".saved");
        if (s) s.textContent = "이 브라우저에 자동 저장됨 · " + new Date().toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
      } catch (e) { /* 저장 불가 환경: 무시 */ }
    }, 300);
  }

  // ---------- 자동 계산 ----------
  // 합계: <output data-sum="g"> ← data-group="g" 인 숫자 입력칸 합
  // 비율: <output data-rate="g"> ← data-rate-of="g" 인 select 중 값이 "o" 인 개수 / 채운 개수
  function calc() {
    document.querySelectorAll("[data-sum]").forEach((out) => {
      const g = out.dataset.sum;
      let sum = 0;
      document.querySelectorAll(`[data-group="${g}"]`).forEach((el) => { sum += Number(el.value) || 0; });
      out.textContent = sum;
    });
    document.querySelectorAll("[data-rate]").forEach((out) => {
      const g = out.dataset.rate;
      const els = [...document.querySelectorAll(`[data-rate-of="${g}"]`)];
      const filled = els.filter((el) => el.value);
      const ok = filled.filter((el) => el.value === "o").length;
      out.textContent = filled.length ? `${ok}/${els.length} · ${Math.round((ok / els.length) * 100)}%` : `-/${els.length}`;
    });
  }

  // ---------- 2글자 자르기 (app.py의 tokenize와 같은 규칙) ----------
  function tokenize(text) {
    const words = (text.toLowerCase().match(/[가-힣a-z0-9]+/g)) || [];
    const tokens = [];
    for (const w of words) {
      if (w.length === 1) tokens.push(w);
      else for (let i = 0; i < w.length - 1; i++) tokens.push(w.slice(i, i + 2));
    }
    return tokens;
  }
  window.enjoyTokenize = tokenize;
  function renderTokens() {
    document.querySelectorAll("[data-tokenize]").forEach((box) => {
      const q = box.querySelector("[data-q]"), d = box.querySelector("[data-d]");
      const qt = tokenize(q ? q.value : ""), dt = d ? new Set(tokenize(d.value)) : null;
      const out = box.querySelector("[data-chips]");
      out.innerHTML = qt.map((t) => `<span class="${dt && dt.has(t) ? "hit" : ""}">${t.replace(/[<>&]/g, "")}</span>`).join("") || '<span style="background:none;color:#999">입력하면 여기에 조각이 나타나요</span>';
      const cnt = box.querySelector("[data-count]");
      if (cnt && dt) cnt.textContent = qt.filter((t) => dt.has(t)).length;
    });
  }

  // ---------- JSON 검사기 ----------
  function checkJSON() {
    document.querySelectorAll("[data-json-check]").forEach((box) => {
      const src = box.querySelector("textarea");
      const out = box.querySelector(".status");
      const text = src.value.trim();
      if (!text) { out.textContent = "검사할 JSON을 붙여 넣어 보세요."; out.className = "status"; return; }
      try {
        const obj = JSON.parse(text);
        const docs = Array.isArray(obj.documents) ? obj.documents : null;
        if (!docs) throw new Error("맨 바깥에 \"documents\": [ ... ] 목록이 있어야 해요.");
        const bad = docs.findIndex((d) => !d || typeof d.id !== "string" || typeof d.content !== "string" || !Array.isArray(d.keywords));
        if (bad >= 0) throw new Error(`${bad + 1}번째 문서에 id(글자) · content(글자) · keywords(목록) 중 빠진 것이 있어요.`);
        out.textContent = `✔ 올바른 형식이에요! 문서 ${docs.length}건 (app.py에서 ‘참고 자료 ${docs.length}건’으로 보일 거예요)`;
        out.className = "status good";
      } catch (e) {
        out.textContent = "✘ " + (e.message || "형식 오류") + " — 쉼표 · 따옴표 · 괄호 짝을 확인하세요.";
        out.className = "status bad";
      }
    });
  }
  function buildJSON() {
    document.querySelectorAll("[data-json-build]").forEach((box) => {
      const docs = [...box.querySelectorAll("[data-doc]")].map((d) => ({
        id: d.querySelector("[data-id]").value.trim(),
        content: d.querySelector("[data-content]").value.trim(),
        keywords: d.querySelector("[data-keywords]").value.split(",").map((s) => s.trim()).filter(Boolean),
      })).filter((d) => d.id || d.content);
      const pre = box.querySelector("[data-preview]");
      pre.textContent = JSON.stringify({ documents: docs }, null, 2);
    });
  }

  // ---------- 버튼 ----------
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-action]");
    if (!b) return;
    if (b.dataset.action === "print") window.print();
    if (b.dataset.action === "reset" && confirm("이 학습지에 적은 내용을 모두 지울까요?")) {
      try { localStorage.removeItem(KEY); } catch (err) {}
      location.reload();
    }
    if (b.dataset.action === "copy-json") {
      const pre = b.closest("[data-json-build]").querySelector("[data-preview]");
      const ta = document.querySelector("[data-json-check] textarea");
      if (ta) { ta.value = pre.textContent; refresh(); save(); }
    }
  });
  window.addEventListener("beforeprint", () => document.querySelectorAll("details").forEach((d) => (d.open = true)));

  function refresh() { calc(); renderTokens(); buildJSON(); checkJSON(); }
  document.addEventListener("input", () => { refresh(); save(); });
  document.addEventListener("change", () => { refresh(); save(); });
  load();
  refresh();
})();

// 코드 파일 미리보기 (내려받지 않고 펼쳐 보기)
document.querySelectorAll(".code-peek").forEach((link) => {
  link.addEventListener("click", async (ev) => {
    ev.preventDefault();
    const box = link.closest("section").querySelector(".code-box");
    if (!box) return;
    const url = link.dataset.src;
    const peers = link.closest("section").querySelectorAll(".code-peek");
    if (!box.hidden && box.dataset.src === url) { box.hidden = true; link.classList.remove("on"); return; }
    peers.forEach((b) => b.classList.toggle("on", b === link));
    box.dataset.src = url; box.hidden = false; box.textContent = "불러오는 중…";
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(res.status);
      box.textContent = "📄 " + url.split("/").pop() + "\n\n" + (await res.text()).replace(/^\uFEFF/, "");
    } catch (e) { box.textContent = "파일을 불러오지 못했어요."; }
  });
});
