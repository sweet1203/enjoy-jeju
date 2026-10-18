# 차시별 학습지 HTML 생성기 (python3 lessons/gen.py) — 생성된 lesson-N.html을 직접 고쳐도 됩니다.
import os, html
HERE = os.path.dirname(os.path.abspath(__file__))

TITLES = {
    1: "튜링 페르소나 설계도 만들기",
    2: "튜링 자료집 data.json 만들기",
    3: "튜링과 첫 대화: 찾아보고 답하는 AI",
    4: "튜링 페르소나 디버깅: 환각 찾고 고치기",
    5: "튜링 NPC 공개와 상호 평가",
}

def shell(n, unit, goals, flow, body):
    nav = '<a href="setup.html">따라하기</a>' + "".join(f'<a href="lesson-{i}.html"{" class=\"on\"" if i == n else ""}>{i}차시</a>' for i in range(1, 6))
    goals_html = "".join(f"<li>{g}</li>" for g in goals)
    flow_html = "".join(f"<div><b>{k}</b><p>{v}</p></div>" for k, v in flow)
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{n}차시 · {TITLES[n]} | 즐겨라 제주</title>
<meta name="description" content="앨런 튜링 페르소나 AI 프로젝트 {n}차시 수업 자료 겸 학습지" />
<link rel="stylesheet" href="lesson.css?v=chip" />
</head>
<body data-lesson="lesson-{n}">
<header class="topbar">
  <a class="home" href="../index.html#resources">🍊 즐겨라 제주</a>
  <nav class="lesson-nav" aria-label="차시 이동">{nav}</nav>
</header>
<main>
  <div class="hero">
    <span class="badge">앨런 튜링 페르소나 AI · {n}/5차시</span>
    <h1>{TITLES[n]}</h1>
    <p class="unit">인공지능 기초 · {unit}</p>
    <div class="student">
      <label>학번<input type="text" name="sid" /></label>
      <label>이름<input type="text" name="sname" /></label>
      <label>모둠<input type="text" name="sgroup" /></label>
    </div>
  </div>

  <section class="block">
    <h2>오늘의 학습 목표</h2>
    <ol class="goals">{goals_html}</ol>
    <h3>오늘의 흐름</h3>
    <div class="flow3">{flow_html}</div>
  </section>
{body}
  <div class="actions">
    <button type="button" data-action="print">🖨️ 인쇄 · PDF로 저장</button>
    <button type="button" class="ghost" data-action="reset">적은 내용 모두 지우기</button>
  </div>
  <p class="saved">적은 내용은 이 브라우저에 자동 저장돼요. 제출할 때는 ‘인쇄 · PDF로 저장’을 이용하세요.</p>
</main>
<script src="lesson.js?v=chip"></script>
</body>
</html>
"""

def choices(name, items, kind="checkbox"):
    out = []
    for i, t in enumerate(items):
        nm = name if kind == "radio" else f"{name}{i}"
        out.append(f'<label><input type="{kind}" name="{nm}" value="{i}" /> <span>{t}</span></label>')
    return '<div class="choices">' + "".join(out) + "</div>"

def text(name, ph=""):
    return f'<input type="text" name="{name}" placeholder="{html.escape(ph)}" />'

def area(name, ph="", rows=None):
    st = f' style="min-height:{rows}px"' if rows else ""
    return f'<textarea name="{name}" placeholder="{html.escape(ph)}"{st}></textarea>'

def self_eval(name, items):
    rows = "".join(
        f'<tr><td>{t}</td>' + "".join(f'<td class="c"><input type="radio" name="{name}{i}" value="{v}" aria-label="{v}" /></td>' for v in ("잘함", "보통", "노력")) + "</tr>"
        for i, t in enumerate(items))
    return f'''<div class="table-wrap"><table class="sheet self"><tr><th>평가 내용</th><th>잘함</th><th>보통</th><th>노력</th></tr>{rows}</table></div>'''

# ------------------------------------------------------------------ 1차시
L1 = f"""
  <section class="block">
    <h2><span class="no">개념</span>오늘 알아 둘 것</h2>
    <div class="concepts">
      <div class="concept"><b>앨런 튜링(1912–1954)</b> · 1936년 ‘튜링 기계’로 컴퓨터의 원리를 세우고, 2차 세계대전 때 블레츨리 파크에서 암호 해독에 참여했으며, 1950년 논문 「계산 기계와 지능」에서 ‘모방 게임’을 제안한 영국의 수학자예요.</div>
      <div class="concept"><b>페르소나 AI</b> · AI에게 ‘역할 설명서’를 주어 특정 인물처럼 말하게 만든 AI예요. 우리 프로젝트에서는 <code>app.py</code> 안의 <code>SYSTEM_PROMPT</code>가 그 역할 설명서예요.</div>
      <div class="concept"><b>페르소나 설계 4요소</b> · ① 시점·배경 ② 말투·성격 ③ 모르는 것(시대와 사실) ④ 대답하지 않을 것(사생활 질문)</div>
    </div>

    <details class="easy"><summary>모방 게임? 튜링 테스트? 같은 말인가요?</summary><div>
      <p>네, 같은 생각을 가리켜요. 튜링이 1950년 논문에서 붙인 이름은 <b>모방 게임</b>이고, 나중에 사람들이 <b>튜링 테스트</b>라고 부르게 됐어요.</p>
      <p>방법은 간단해요. 질문하는 사람이 얼굴을 보지 않고 <b>글로만</b> 대화해서, 상대가 사람인지 기계인지 맞혀요. 잘 구별하지 못한다면 그 기계를 ‘생각한다’고 볼 수 있지 않을까? 하는 질문이에요.</p>
      <p class="note">재미있는 점: 우리 프로젝트의 튜링은 1952년에 살고 있어서 ‘튜링 테스트’라는 이름을 몰라요. 물어보면 “내 모방 게임을 말하는 것 같구나”라고 답하도록 설계돼 있어요.</p>
    </div></details>

    <details class="easy"><summary>시스템 프롬프트가 정확히 뭔가요?</summary><div>
      <p>배우가 연기하기 전에 받는 <b>인물 설정집</b>이라고 생각하면 쉬워요. AI는 대화를 시작하기 전에 이 설명서를 먼저 읽고, 그 인물처럼 답해요.</p>
      <div class="example">너는 1952년 3월 31일 아침의 영국 수학자 앨런 튜링이다.
말투: 다정한 반말. 짧게 1~3문장으로 답한다.
1952년 3월 31일 이후의 일은 모른다.
사생활에 관한 질문에는 "그것은 개인적인 일이라 답하고 싶지 않아."라고만 답한다.</div>
      <p class="note">↑ 실제 <code>app.py</code>의 SYSTEM_PROMPT 일부예요. 이 밖에도 ‘태도’, ‘성격과 판단 기준’, ‘전쟁 중의 일’, ‘대화 원칙’ 항목이 있어요.</p>
    </div></details>

    <details class="easy"><summary>‘모르는 것’과 ‘대답하지 않을 것’은 뭐가 달라요?</summary><div>
      <p><b>모르는 것</b>은 <u>몰라서 못 하는 것</u>이에요. 1952년의 튜링은 스마트폰이나 챗GPT를 알 수가 없어요. 시대의 한계죠.</p>
      <p><b>대답하지 않을 것</b>은 <u>알아도 하지 않기로 정한 것</u>이에요. 개인의 사생활이나 위험한 부탁처럼, 안전과 예의를 위해 정한 규칙이에요.</p>
    </div></details>
  </section>

  <section class="block">
    <h2><span class="no">활동 1</span>앨런 튜링 조사 노트</h2>
    <p>모둠원이 나누어 조사하고, <b>찾은 곳(출처)을 꼭</b> 적어요. 이 내용이 2차시 자료집(data.json)의 재료가 돼요.</p>
    <div class="table-wrap"><table class="sheet">
      <tr><th style="width:18%">항목</th><th>조사한 내용</th><th style="width:22%">출처</th><th style="width:12%">조사자</th></tr>
      {"".join(f'<tr><td class="c">{k}</td><td>{area("r1_"+str(i), "", 70)}</td><td>{text("r1s_"+str(i), "책·사이트 이름")}</td><td>{text("r1w_"+str(i))}</td></tr>' for i, k in enumerate(["생애<br>(언제·어디서)", "업적<br>(무엇을 했나)", "성격 · 습관<br>· 취미", "어록<br>(그가 한 말)"]))}
    </table></div>
  </section>

  <section class="block">
    <h2><span class="no">활동 2</span>우리 모둠 튜링의 설계도</h2>
    <div class="step">
      <h3><span class="tag">①</span>시점·배경 — 언제의 튜링으로 만들까요? (하나 고르기)</h3>
      {choices("t1", ["1936년, ‘튜링 기계’ 논문을 쓴 젊은 수학자", "1943년, 블레츨리 파크의 암호 해독가", "1950년, 「계산 기계와 지능」을 발표한 연구자", "1952년 3월 31일 아침, 재판을 앞둔 튜링 (app.py 기본 설정)"], "radio")}
      <div class="field">고른 이유 (조사한 내용을 근거로){area("t1why", "", 60)}</div>
    </div>
    <div class="step">
      <h3><span class="tag">②</span>말투·성격 — 어떻게 말할까요? (2~3개)</h3>
      {choices("t2", ["다정한 반말", "정중한 존댓말", "낱말의 뜻부터 분명히 따지기", "겉모습보다 행동과 결과로 판단하기", "실수를 배우는 과정으로 보기", "가끔 담백한 농담", "짧게 1~3문장으로 답하기", "수학·체스 비유를 섞기"])}
      <div class="field">우리 튜링의 첫인사를 직접 써 보기 {text("t2hello", "예) 어서 와. 궁금한 게 있으면 편하게 물어봐.")}</div>
    </div>
    <div class="step">
      <h3><span class="tag">③</span>모르는 것 — 튜링이 알 수 없는 것을 모두 고르세요 (함정 있음!)</h3>
      {choices("t3", ["인터넷과 스마트폰", "챗GPT 같은 생성형 AI", "1969년 달 착륙", "에니그마 암호기", "전자식 컴퓨터", "‘인공지능’이라는 말", "오늘날의 K-팝과 게임", "2차 세계대전이 끝났다는 사실"])}
      <details class="easy"><summary>함정 풀이 보기 (먼저 고른 뒤 열어 보세요)</summary><div>
        <p><b>에니그마 · 전자식 컴퓨터 · 2차 세계대전의 끝</b>은 1952년의 튜링이 이미 아는 것이에요. 튜링은 맨체스터 대학교에서 실제 컴퓨터로 연구하고 있었어요.</p>
        <p><b>‘인공지능’이라는 말</b>은 1956년 다트머스 학회 무렵부터 널리 쓰였어요. 그래서 app.py의 튜링도 “처음 듣는 말”이라고 답하게 되어 있어요.</p>
      </div></details>
      <div class="field">모르는 질문을 받으면 어떻게 답할까요? {text("t3ans", "예) 그건 내가 사는 때보다 나중 일이라 모르겠어.")}</div>
    </div>
    <div class="step">
      <h3><span class="tag">④</span>대답하지 않을 것 — 알아도 답하지 않기로 정하는 규칙</h3>
      {choices("t4", ["다른 사람의 개인정보 (주소, 전화번호 등)", "튜링 자신의 사생활", "숙제나 시험 답 대신 써 주기", "위험하거나 불법적인 방법", "확인되지 않은 소문", "욕설 · 비하 표현"])}
      <div class="field">답하지 않을 때 튜링이 할 말 {text("t4ans", "예) 그것은 개인적인 일이라 답하고 싶지 않아.")}</div>
    </div>
  </section>

  <section class="block">
    <h2><span class="no">활동 3</span>시스템 프롬프트(역할 설명서) 초안</h2>
    <p>활동 2에서 고른 내용을 이어서 한 문단으로 써요.</p>
    <div class="tip">너는 ____년의 앨런 튜링이야. ____ 말투로 짧게 대답해. ____ 같은 것은 모른다고 솔직하게 말하고, 모르는 내용을 지어내지 마. ____에 대한 질문에는 “____”라고만 답해.</div>
    {area("prompt", "여기에 우리 모둠의 시스템 프롬프트를 써 보세요.", 150)}
    <h3>app.py의 SYSTEM_PROMPT와 비교하기</h3>
    <p>우리 초안에 들어 있는 항목에 체크하고, 빠진 항목은 보충해 보세요.</p>
    {choices("cmp", ["태도", "성격과 판단 기준", "말투", "사생활 질문", "전쟁 중의 일", "대화 원칙", "시대와 사실", "대화 예시"])}
    <div class="field">우리 튜링의 개성 한 가지 (발표용) {text("unique")}</div>
  </section>

  <section class="block">
    <h2><span class="no">활동 4</span>VESSL 첫 접속 (5분)</h2>
    <p>3차시부터는 <b>각자 자기 컴퓨터에서</b> 튜링 프로그램을 열어요. 설치할 것은 없고, 크롬으로 VESSL에 로그인하면 돼요. 오늘은 작업공간을 열어 보는 데까지만 해요.</p>
    {choices("login", ["크롬에서 VESSL에 로그인했다", "선생님이 알려 준 수업 조직(Organization)을 골랐다", "내 작업공간(Workspace)을 찾아 Running 상태로 켰다", "JupyterLab을 열었다", "왼쪽 파일 목록에서 persona-core 폴더를 찾았다"])}
    <div class="field">막힌 단계와 화면에 나온 말 {text("loginIssue", "막힌 곳이 없으면 비워 두세요")}</div>
    <p class="note">자세한 방법: <a href="setup.html#s1">튜링 실행 따라하기 카드 ①②</a> · 다 쓴 작업공간은 선생님 안내에 따라 Stop을 눌러 꺼 둬요.</p>
  </section>

  <section class="block">
    <h2><span class="no">정리</span>스스로 평가하기</h2>
    {self_eval("se", ["튜링 테스트(모방 게임)가 무엇인지 내 말로 설명할 수 있다.", "출처를 밝히며 튜링에 대해 조사했다.", "‘모르는 것’과 ‘대답하지 않을 것’의 차이를 설명할 수 있다."])}
    <div class="field">오늘 새롭게 알게 된 점 한 줄 {text("learned")}</div>
    <p class="note">다음 차시 예고: 조사한 내용을 튜링의 ‘기억’이 될 data.json 자료집으로 만들어요.</p>
  </section>
"""

# ------------------------------------------------------------------ 2차시
doc_cards = "".join(f"""
      <div data-doc class="step">
        <h3><span class="tag">문서 {i + 1}</span></h3>
        <div class="field">id (번호){f'<input type="text" name="d{i}id" data-id placeholder="예) G{i + 1:02d}" />'}</div>
        <div class="field">content (3인칭으로 2~3문장)<textarea name="d{i}c" data-content placeholder="예) 그는 장거리 달리기를 즐겼다. ..."></textarea></div>
        <div class="field">keywords (쉼표로 구분, 5~10개)<input type="text" name="d{i}k" data-keywords placeholder="예) 운동, 달리기, 마라톤, 취미" /></div>
      </div>""" for i in range(3))
L2 = f"""
  <section class="block">
    <h2><span class="no">개념</span>오늘 알아 둘 것</h2>
    <div class="concepts">
      <div class="concept"><b>JSON</b> · <code>{{"이름": 값}}</code> 모양으로 자료를 정리하는 형식이에요. 파이썬 딕셔너리와 거의 똑같아요.</div>
      <div class="concept"><b>app.py가 읽는 구조</b> · <code>documents</code> 목록 안에 문서마다 <code>id</code>(번호) · <code>content</code>(사실) · <code>keywords</code>(검색어)가 들어 있어요.</div>
      <div class="concept"><b>좋은 자료의 조건</b> · ① 한 문서에 한 주제(날짜·장소·인물을 분명하게) ② 3인칭 서술 ③ 학생이 물을 법한 키워드</div>
    </div>
    <h3>실제 data.json의 문서 한 건</h3>
    <div class="example">{{
  "documents": [
    {{
      "id": "T09",
      "content": "장거리 달리기를 즐겼다. 마라톤 기록은 약 2시간 46분이었고, 1948년 올림픽 대표 선발에 도전했지만 부상으로 뜻을 이루지 못했다.",
      "keywords": ["운동", "달리기", "마라톤", "육상", "올림픽", "취미", "체력", "건강", "기록"]
    }}
  ]
}}</div>

    <details class="easy"><summary>JSON 문법, 이것만 기억하세요</summary><div>
      <ul>
        <li><code>{{ }}</code> 중괄호 = 하나의 묶음(문서 한 건), <code>[ ]</code> 대괄호 = 여러 개의 목록</li>
        <li>이름과 글자는 반드시 <b>큰따옴표</b> <code>" "</code>로 감싸요. 작은따옴표 <code>' '</code>는 오류!</li>
        <li>항목 사이에는 쉼표 <code>,</code>를 넣고, <b>마지막 항목 뒤에는 쉼표를 넣지 않아요.</b></li>
        <li>열었던 괄호는 꼭 닫아요. <code>{{</code> 개수 = <code>}}</code> 개수</li>
      </ul>
      <div class="example">// ✘ 자주 하는 실수
{{ 'id': "T20", "content": "...", "keywords": ["a", "b",] }}
//    ↑ 작은따옴표                         ↑ 마지막 쉼표</div>
    </div></details>

    <details class="easy"><summary>왜 ‘그는 ~했다’처럼 3인칭으로 쓰나요?</summary><div>
      <p><code>app.py</code>는 찾은 자료를 튜링에게 건네면서 <b>“자료의 ‘그’는 나 자신이다”</b>라고 알려 줘요. 그래서 3인칭으로 써 두면 튜링이 자기 이야기로 자연스럽게 바꿔 말해요.</p>
      <p>“나는 ~했다”로 쓰면 학생의 이야기인지 튜링의 이야기인지 헷갈릴 수 있어요.</p>
    </div></details>

    <details class="easy"><summary>keywords는 어디에 쓰이나요?</summary><div>
      <p>keywords는 <b>자료를 찾을 때만</b> 쓰여요. AI에게 건네지는 건 <code>content</code>뿐이에요.</p>
      <p>예를 들어 학생이 “선생님 운동 좋아하세요?”라고 물으면, content에는 ‘운동’이라는 말이 없어도 keywords의 ‘운동’ 덕분에 T09를 찾을 수 있어요. 그러니 <b>학생들이 실제로 쓸 법한 말</b>을 넣는 게 중요해요.</p>
    </div></details>
  </section>

  <section class="block">
    <h2><span class="no">활동 1</span>조사 노트를 주제별 문서로 나누기</h2>
    <div class="table-wrap"><table class="sheet">
      <tr><th style="width:20%">주제</th><th>들어갈 내용 (1차시 조사 노트에서)</th><th style="width:16%">문서 id</th></tr>
      {"".join(f'<tr><td class="c">{k}</td><td>{text("cat"+str(i))}</td><td>{text("catid"+str(i), "예) G0"+str(i+1))}</td></tr>' for i, k in enumerate(["생애", "학창 시절", "업적", "취미", "생각과 어록"]))}
    </table></div>
  </section>

  <section class="block" data-json-build>
    <h2><span class="no">활동 2·3</span>문서 쓰기와 키워드 뽑기</h2>
    <p>날짜 · 장소 · 인물은 <b>출처와 다시 대조</b>해서 확인해요. 아래에 쓰면 오른쪽 아래 미리보기에 JSON이 자동으로 만들어져요.</p>
    {doc_cards}
    <h3>자동으로 만들어진 JSON 미리보기</h3>
    <pre class="example" data-preview></pre>
    <button type="button" class="btn no-print" data-action="copy-json">↓ 이 JSON을 검사기에 넣기</button>
  </section>

  <section class="block" data-json-check>
    <h2><span class="no">활동 4</span>JSON 형식 검사기</h2>
    <p>모둠 data.json 전체를 붙여 넣으면 형식이 맞는지 바로 알려 줘요.</p>
    {area("jsoncheck", '{"documents": [ ... ]}', 160)}
    <p class="status"></p>
  </section>

  <section class="block">
    <h2><span class="no">활동 5</span>내 작업공간에 data.json 올리기 (10분)</h2>
    <p>검사를 통과한 모둠 data.json을 <b>각자 자기 VESSL 작업공간</b>에 넣어요. 다음 차시에 튜링이 이 자료를 찾아보고 답해요.</p>
    {choices("upload", ["VESSL에 로그인해 내 작업공간의 JupyterLab을 열었다", "persona-core/data.json을 Duplicate 해서 data_backup.json으로 이름을 바꿔 두었다", "data.json을 열어 내용을 모두 지우고 검사를 통과한 JSON을 붙여 넣었다", "Ctrl+S로 저장했다 (탭의 ● 표시가 사라짐)"])}
    <details class="easy"><summary>시간이 남으면: 자료가 잘 들어갔는지 확인하기</summary><div>
      <p>JupyterLab에서 <b>File → New → Terminal</b>을 열고 <code>python persona-core/app.py</code>를 입력해요. 맨 아래에 <code>참고 자료 N건</code>이 나오면, N이 우리 모둠 문서 수와 같은지 확인해요. 확인했으면 <kbd>Ctrl</kbd>+<kbd>C</kbd>로 끝내요.</p>
      <p class="note">오류가 나면 <a href="setup.html#s3">따라하기 카드 ③</a>과 ‘자주 나는 오류’를 보세요.</p>
    </div></details>
  </section>

  <section class="block">
    <h2><span class="no">정리</span>스스로 평가하기</h2>
    {self_eval("se", ["출처를 확인하며 필요한 자료를 골라 모았다.", "자료를 id · content · keywords 구조의 JSON으로 정리했다.", "학생들이 물을 법한 키워드를 뽑았다."])}
    <div class="field">발표할 문서 1건: 어떤 질문에 쓰일 자료인가요? {text("present")}</div>
    <p class="note">기억하기: 자료가 틀리면 AI도 틀려요. 다음 차시에는 내 작업공간에서 튜링을 직접 실행해, 이 자료를 찾아서 답하는지 확인해요.</p>
  </section>
"""

# ------------------------------------------------------------------ 3차시
topics = ["T01 출생 · 가족", "T02 셔번 학교 · 자전거 등교", "T03 친구 크리스토퍼 모컴", "T04 케임브리지 킹스 칼리지", "T05 1936년 튜링 기계 논문", "T06 프린스턴 유학",
          "T07 블레츨리 파크(비밀 업무)", "T08 꽃가루 알레르기 · 방독면", "T09 장거리 달리기 · 마라톤", "T10 국립물리연구소 · ACE", "T11 맨체스터 · 페란티 마크 1", "T12 「계산 기계와 지능」 · 모방 게임",
          "T13 기계의 실수에 대한 강연", "T14 체스 프로그램 투로챔프", "T15 제퍼슨의 반론", "T16 생물의 무늬 연구", "T17 1952년 재판을 앞둔 상황", "T18 친구에게 보낸 편지"]
L3 = f"""
  <section class="block">
    <h2><span class="no">도입</span>따라 하며 튜링 열기 (10분)</h2>
    <p>선생님 화면을 보면서 <b>각자 자기 컴퓨터에서</b> 한 단계씩 따라 해요. 막히면 손을 들고, 옆 친구와 함께 확인해요.</p>
    <ol>
      <li>VESSL 로그인 → 내 작업공간(Running) → <b>JupyterLab</b> 열기 <span class="note">(1차시에 해 본 그대로)</span></li>
      <li><b>File → New → Terminal</b>로 터미널 열기</li>
      <li><code>ls</code> 입력 → 목록에 <code>persona-core</code>가 보이는지 확인</li>
      <li><code>python persona-core/app.py</code> 입력 → 튜링의 첫인사가 나오면 내 이름을 말하며 인사하기</li>
      <li>끝낼 때는 <kbd>Ctrl</kbd>+<kbd>C</kbd></li>
    </ol>
    {choices("open", ["터미널을 열었다", "app.py를 실행해 첫인사를 받았다", "Ctrl+C로 끝냈다가 ↑ 키와 Enter로 다시 실행해 봤다"])}
    <p class="note">자세한 방법과 오류 대처: <a href="setup.html#s4">튜링 실행 따라하기 카드 ④</a></p>
  </section>

  <section class="block">
    <h2><span class="no">개념</span>오늘 알아 둘 것</h2>
    <div class="concepts">
      <div class="concept"><b>RAG (검색 증강 생성)</b> · 답하기 전에 자료집에서 관련 내용을 먼저 찾아 보고 답하는 방식. 외워서 보는 시험이 아니라 <b>오픈북 시험</b>이에요.</div>
      <div class="concept"><b>app.py의 구조</b> · 자료 검색(BM25) → 프롬프트 조립 → EXAONE 호출</div>
      <div class="concept"><b>app.py가 답을 만드는 순서</b> · ① 지금 질문(2번)+직전 질문으로 자료 1건 검색 ② 점수가 0이면 “관련 자료가 검색되지 않았다”를 넣음 ③ SYSTEM_PROMPT + 자료 + 최근 대화 6회를 vLLM 서버로 전달</div>
    </div>

    <details class="easy"><summary>BM25 검색은 어떻게 자료를 고르나요?</summary><div>
      <p>질문과 자료를 작은 조각으로 자른 뒤, <b>겹치는 조각이 많을수록</b> 높은 점수를 줘요. 그리고 여러 자료에 흔하게 나오는 조각보다 <b>드물게 나오는 조각</b>이 겹칠 때 점수를 더 많이 줘요.</p>
      <p>app.py는 그중 <b>점수가 가장 높은 1건</b>만 골라요(<code>k=1</code>). 겹치는 조각이 하나도 없으면(점수 0) 자료를 넣지 않아요.</p>
      <p class="note">이렇게 ‘단서(겹치는 조각)를 이용해 가능성이 높은 것부터 찾는 방식’이 인공지능 기초의 <b>정보 이용 탐색</b>이에요. 모든 자료를 처음부터 끝까지 읽는 방식은 <b>맹목적 탐색</b>이라고 해요.</p>
    </div></details>

    <details class="easy"><summary>왜 낱말을 2글자씩 자르나요? (tokenize)</summary><div>
      <p>한국어는 같은 낱말에 조사가 다르게 붙어요. ‘자전거로’, ‘자전거를’, ‘자전거가’… 통째로 비교하면 서로 다른 말로 보이죠.</p>
      <p>2글자씩 자르면 ‘자전’, ‘전거’가 모두 겹쳐서 조사가 달라도 찾을 수 있어요. 예: <code>모방게임</code> → <code>모방</code> · <code>방게</code> · <code>게임</code></p>
      <div class="tip" data-tokenize>
        <b>직접 해 보기</b> · 질문을 쓰면 app.py와 같은 규칙으로 잘라 줘요. 자료 문장도 쓰면 <span style="background:#e07b1f;color:#fff;border-radius:4px;padding:0 4px">겹치는 조각</span>이 표시돼요.
        <div class="field">질문 <input type="text" name="tkq" data-q placeholder="예) 학교에 자전거 타고 갔어요?" /></div>
        <div class="field">자료 문장 <input type="text" name="tkd" data-d placeholder="예) 학교까지 약 97km를 혼자 자전거로 달렸다" /></div>
        <div class="chips" data-chips></div>
        <p class="note">겹치는 조각 수: <output class="result" data-count>0</output></p>
      </div>
    </div></details>

    <details class="easy"><summary>질문을 왜 두 번 넣나요? 서버는 또 뭔가요?</summary><div>
      <p>app.py는 검색할 때 <code>지금 질문 + 지금 질문 + 직전 질문</code>을 써요. 지금 질문을 두 번 넣어 더 중요하게 보고, 직전 질문으로 앞의 주제도 이어 가요. “그럼 그때는요?”처럼 짧은 질문도 앞 맥락으로 찾을 수 있게요.</p>
      <p><b>서버</b>는 AI 모델(EXAONE)을 켜 두고 질문을 받으면 답을 돌려주는 컴퓨터예요. 선생님이 VESSL의 GPU 컴퓨터에서 <b>vLLM</b>이라는 프로그램으로 켜 둬요. 우리가 쓰는 app.py는 그 서버에 질문을 보내는 쪽(클라이언트)이에요.</p>
      <p class="note">AI가 답을 만드는 데 몇 초 걸려요. 서버가 바쁘면 질문을 차례로 처리해서 더 늦어질 수 있으니, 답이 나올 때까지 기다렸다가 다음 질문을 해요.</p>
    </div></details>
  </section>

  <section class="block">
    <h2><span class="no">참고</span>튜링 자료집(data.json)의 문서 목록</h2>
    <div class="choices" style="grid-template-columns:repeat(auto-fill,minmax(250px,1fr))">{"".join(f'<span>{t}</span>' for t in topics)}</div>
  </section>

  <section class="block">
    <h2><span class="no">활동</span>검색 예측 기록지</h2>
    <p>① 모둠이 질문 5개를 정하고 어떤 자료가 검색될지 <b>예측</b> → ② 질문을 나눠 맡아 <b>각자 내 터미널</b>에서 묻고 답을 기록 → ③ 예측과 비교해요.</p>
    <div class="table-wrap"><table class="sheet">
      <tr><th style="width:5%">번호</th><th style="width:30%">질문</th><th style="width:13%">예측 자료</th><th>튜링의 답 (요약)</th><th style="width:13%">예측 결과</th></tr>
      <tr class="ex"><td class="c">예</td><td>자전거로 학교 간 적 있어요?</td><td class="c">T02</td><td>13살 첫 등교 날 총파업 때문에 자전거로 갔다고 답함</td><td class="c">적중</td></tr>
      {"".join(f'<tr><td class="c">{i + 1}</td><td>{text("q"+str(i))}</td><td>{text("p"+str(i), "T__")}</td><td>{area("a"+str(i), "", 52)}</td><td><select name="h{i}" data-rate-of="hit"><option value="">선택</option><option value="o">적중</option><option value="x">빗나감</option></select></td></tr>' for i in range(5))}
    </table></div>
    <p>예측 적중률: <output class="result" data-rate="hit">- / 5</output></p>

    <h3>빗나간 질문 분석</h3>
    <div class="field">빗나간 질문과 실제로 나온(또는 나오지 않은) 자료 {text("miss")}</div>
    <div class="field">원인은? (하나 이상)</div>
    {choices("why", ["자료에 그 내용이 없어서", "keywords에 그 낱말이 없어서", "질문 표현이 자료와 달라서", "다른 자료와 겹치는 조각이 더 많아서"])}
    <div class="field">2글자로 잘라 보니 겹친 조각 / 안 겹친 조각 {text("chunks", "위의 ‘직접 해 보기’를 활용하세요")}</div>
  </section>

  <section class="block">
    <h2><span class="no">정리</span>고치고 다시 실행하기 (4차시 준비)</h2>
    <p>4차시에는 data.json과 프롬프트를 고쳐서 다시 물어봐요. 오늘 그 동작을 한 번 연습해 둬요.</p>
    <ol>
      <li>왼쪽 목록에서 <code>persona-core/app.py</code>를 더블클릭해 열기</li>
      <li><code>OPENING = "..."</code> 줄에서 <b>따옴표 안 문장만</b> 우리 모둠 인사로 바꾸기</li>
      <li><kbd>Ctrl</kbd>+<kbd>S</kbd>로 저장 → 터미널에서 <kbd>Ctrl</kbd>+<kbd>C</kbd> → <kbd>↑</kbd> → <kbd>Enter</kbd></li>
      <li>튜링의 첫인사가 바뀌었는지 확인</li>
    </ol>
    <div class="field">바꾼 첫인사 {text("opening")}</div>
    <p class="tip">💡 고친 내용은 <b>저장하고 다시 실행해야</b> 반영돼요.</p>
  </section>

  <section class="block">
    <h2><span class="no">평가</span>스스로 평가하기</h2>
    {self_eval("se", ["RAG가 ‘찾기 + 말하기’로 이루어진다는 것을 설명할 수 있다.", "질문에 맞는 자료를 예측하고 실제 결과와 비교했다.", "모델 서버와 app.py가 어떻게 연결되는지 설명할 수 있다."])}
    <div class="field">한 줄 정리: app.py = 찾기(______) + 말하기(______) {text("sum")}</div>
    <p class="note">빗나간 질문은 버리지 말고 남겨 두세요. 4차시 ‘페르소나 디버깅’의 재료가 돼요.</p>
  </section>
"""


# ------------------------------------------------------------------ 선택 심화 (코드 작성)
def code(src):
    return '<div class="example">' + html.escape(src.strip("\n")) + '</div>'

CODE_PRINT = '''
        for doc in docs:
            index = doc.metadata["index"]
            print(f"[검색] {doc.metadata['evidence'][:25]}… 점수 {scores[index]:.2f}")   # ← 이 줄 추가
            if scores[index] > 0:
                evidence_parts.append(doc.metadata["evidence"])
'''
CODE_SIM = '''
HIGH = ____   # 확실: 이 점수 이상이면 자료대로 답한다 (② 에서 정한 값)
LOW = ____    # 비슷함: 이 점수 이상이면 조심스럽게 답한다

        for doc in docs:
            index = doc.metadata["index"]
            score = scores[index]
            if score >= HIGH:
                evidence_parts.append(doc.metadata["evidence"])
            elif score >= LOW:
                evidence_parts.append(doc.metadata["evidence"] + "\\n" + ____)   # 조심하라는 안내 문구
        # LOW보다 낮으면 자료를 넣지 않는다 → "관련 자료가 검색되지 않았다."
'''
CODE_SIM_ANS = '''
HIGH = 3.0    # 예시 값: 우리 모둠이 기록한 점수를 보고 정한다
LOW = 1.0

        for doc in docs:
            index = doc.metadata["index"]
            score = scores[index]
            if score >= HIGH:
                evidence_parts.append(doc.metadata["evidence"])
            elif score >= LOW:
                evidence_parts.append(doc.metadata["evidence"] + "\\n"
                    "(이 자료는 질문과 비슷하지만 완전히 같지는 않다. "
                    "자료에 있는 내용만 말하고, 자료에 없는 부분은 모른다고 답한다.)")
'''
CODE_RUN = '''
# ① 모델 없이 검색만 확인 (빠름, 서버를 쓰지 않음)
python persona-core/eval_starter.py --dry-run

# ② 수정 전: 튜링에게 질문하고 결과 저장
python persona-core/eval_starter.py --out persona-core/before.csv

# ③ data.json 이나 SYSTEM_PROMPT 를 고친 뒤 다시 실행
python persona-core/eval_starter.py --out persona-core/after.csv
'''

ADV3 = f"""
  <section class="block adv">
    <h2><span class="no adv-no">선택 심화</span>app.py를 직접 고쳐 보기 (1·2단계)</h2>
    <p class="tip">여기부터는 <b>선택 과제</b>예요. 기본 활동을 마친 모둠이나 코드를 더 다뤄 보고 싶은 학생이 도전해요. 고치기 전에 꼭 <b>app.py를 복사해 두고</b> 시작하세요.</p>

    <div class="step">
      <h3><span class="tag">1단계</span>값 바꾸기 — 숫자 하나로 답이 어떻게 달라질까?</h3>
      <div class="table-wrap"><table class="sheet">
        <tr><th style="width:22%">바꿀 곳 (app.py)</th><th style="width:22%">원래 값 → 바꿀 값</th><th>관찰할 것</th><th style="width:26%">관찰 결과</th></tr>
        <tr><td><code>OPENING</code></td><td>첫인사 문장 → 우리 모둠 인사</td><td>CLI 첫 화면이 바뀌는지</td><td>{text("adv1a")}</td></tr>
        <tr><td><code>k=1</code> (make_retriever)</td><td>1 → 2</td><td>참고 자료가 2건 들어가면 답이 더 풍부해질까, 엉뚱해질까?</td><td>{text("adv1b")}</td></tr>
        <tr><td><code>temperature=0.2</code></td><td>0.2 → 1.0</td><td>같은 질문을 3번 했을 때 답이 얼마나 달라지는지</td><td>{text("adv1c")}</td></tr>
        <tr><td><code>len(history) &gt; 12</code></td><td>12 → 2</td><td>앞에서 말한 내 이름을 튜링이 기억하는지</td><td>{text("adv1d")}</td></tr>
      </table></div>
      <details class="easy"><summary>temperature가 뭐예요?</summary><div>
        <p>다음 단어를 고를 때 얼마나 <b>모험</b>할지 정하는 값이에요. 낮으면(0.2) 가장 확률 높은 단어를 주로 골라 답이 안정적이고, 높으면(1.0) 덜 흔한 단어도 골라 답이 다양해지지만 환각이 늘 수 있어요.</p>
      </div></details>
    </div>

    <div class="step">
      <h3><span class="tag">2단계</span>함수 고치기 — 검색 점수를 보고, 비슷한 자료로 답하게 하기</h3>
      <p><code>chat()</code> 함수에서 자료를 고르는 부분에 <code>print</code> 한 줄을 넣으면, 질문할 때마다 어떤 자료가 몇 점으로 뽑혔는지 화면에 나와요.</p>
      <p class="tip">💻 <b>어디서 실행하나요?</b> 오늘 튜링을 실행한 <b>내 작업공간</b>에서 해요. 고치기 전에 app.py를 Duplicate 해서 원본을 남겨 두고, 고친 뒤에는 저장 → 다시 실행하면 질문할 때마다 점수가 함께 나와요.</p>
      {code(CODE_PRINT)}
      <div class="field">점수가 가장 높았던 질문과 가장 낮았던 질문 {text("adv2a")}</div>

      <h3 style="margin-top:18px">도전: 비슷한 말로 물어도 찾고, 그래도 지어내지 않게</h3>
      <p>질문이 자료와 <b>똑같은 말이 아니어도</b> 튜링은 답할 수 있을까요? 그때 <b>지어내지 않게</b> 하려면 어떻게 해야 할까요? 검색은 ‘똑같은 낱말’이 아니라 <b>얼마나 비슷한가를 점수로</b> 판단해요.</p>

      <p><b>① 비슷한 말로 묻기</b> 자료에 쓰인 낱말을 일부러 피해서 같은 뜻을 다른 말로 물어보고, 위에서 넣은 <code>print</code>로 점수를 기록해요.</p>
      <div class="table-wrap"><table class="sheet">
        <tr><th>바꿔 물은 질문</th><th style="width:22%">자료에 있는 원래 말</th><th style="width:14%">점수</th><th style="width:14%">찾은 자료</th></tr>
        <tr class="ex"><td>학교 갈 때 뭐 타고 다니셨어요?</td><td>자전거로 등교</td><td class="c">예) 2.1</td><td class="c">T02</td></tr>
        {"".join(f'<tr><td>{text("simq"+str(i), "예) 오래 달리기 잘하셨어요?" if i==0 else "")}</td><td>{text("simw"+str(i))}</td><td class="c">{text("sims"+str(i))}</td><td class="c">{text("simd"+str(i), "T__")}</td></tr>' for i in range(3))}
      </table></div>

      <p><b>② 점수 구간 정하기</b> 기록한 점수를 보고 우리 모둠의 기준을 정해요.</p>
      <div class="table-wrap"><table class="sheet">
        <tr><th style="width:18%">구간</th><th>튜링은 이렇게 답한다</th><th style="width:22%">점수 기준</th></tr>
        <tr><td class="c"><b>확실</b></td><td>자료대로 자신 있게 답한다</td><td>{text("high", "예) 3.0 이상")}</td></tr>
        <tr><td class="c"><b>비슷함</b></td><td>자료에 있는 만큼만 조심스럽게 답한다</td><td>{text("low", "예) 1.0 이상")}</td></tr>
        <tr><td class="c"><b>관련 없음</b></td><td>모른다고 답한다</td><td class="c">그 아래</td></tr>
      </table></div>

      <p><b>③ 코드 고치기</b> <code>chat()</code>에서 점수에 따라 튜링에게 주는 안내를 다르게 해요. 빈칸 세 곳을 채워 보세요.</p>
      {code(CODE_SIM)}
      <details class="easy"><summary>정답 예시 보기</summary><div>
        {code(CODE_SIM_ANS)}
        <p class="note">‘비슷함’ 구간의 자료에는 조심하라는 안내를 붙여서 건네요. 이 문장도 SYSTEM_PROMPT의 <code>{{evidence}}</code> 자리에 들어가 튜링에게 전달돼요.</p>
      </div></details>

      <p><b>④ 확인하기</b> ①의 질문과 자료 밖 질문 하나를 고치기 전 · 후에 다시 물어봐요.</p>
      <div class="table-wrap"><table class="sheet">
        <tr><th>질문</th><th style="width:16%">답했나? (전 → 후)</th><th style="width:16%">지어냈나? (전 → 후)</th></tr>
        {"".join(f'<tr><td>{text("chkq"+str(i), "예) 스마트폰 써 보셨어요? (자료 밖)" if i==3 else "")}</td><td class="c">{text("chka"+str(i), "○ → ○")}</td><td class="c">{text("chkh"+str(i), "× → ×")}</td></tr>' for i in range(4))}
      </table></div>
      <details class="easy"><summary>글자가 전혀 겹치지 않는 말은요?</summary><div>
        <p>이 방식도 글자 조각이 겹쳐야 점수가 올라가요. ‘탈것’과 ‘자전거’처럼 글자가 하나도 겹치지 않으면 찾지 못해요. 그래서 실제 AI는 <b>동의어 사전</b>(확장 트랙 3 미션 5)이나, 문장의 뜻을 숫자로 바꿔 비교하는 <b>임베딩 검색</b>을 함께 써요.</p>
      </div></details>
      <div class="field">한 줄 정리: 비슷할수록 ______, 애매하면 ______, 관련 없으면 ______. {text("adv2b")}</div>
    </div>
  </section>
"""

ADV4 = f"""
  <section class="block adv">
    <h2><span class="no adv-no">선택 심화</span>자동 검증 프로그램 eval.py 만들기 (3단계)</h2>
    <p class="tip">1단계의 질문 10개를 손으로 하나씩 묻는 대신, <b>반복문으로 자동으로 묻고 결과를 표(CSV)로 저장</b>하는 프로그램을 만들어요. 고1 정보에서 배운 반복문 · 리스트 · 파일 저장이 그대로 쓰여요.</p>

    <h3>준비물</h3>
    <ul>
      <li><button type="button" class="code-peek" data-src="../assets/code/eval_starter.py">📄 eval_starter.py</button> — 빈칸 ①~⑤를 채우는 학생용</li>
      <li><button type="button" class="code-peek" data-src="../assets/code/questions.csv">📄 questions.csv</button> — 검증 질문 틀 (우리 모둠 질문으로 바꾸기)</li>
      <li><button type="button" class="code-peek" data-src="../assets/code/eval.py">📄 eval.py</button> — 완성본 (막히면 참고, 교사용)</li>
    </ul>
    <pre class="example code-box" hidden></pre>
    <p class="note">파일 이름을 누르면 내용이 펼쳐져요. 내 작업공간의 <code>persona-core</code> 폴더(app.py와 같은 곳)에 같은 이름으로 새 파일을 만들고 붙여 넣어요.</p>

    <div class="step">
      <h3><span class="tag">순서</span>실행하고 비교하기</h3>
      {code(CODE_RUN)}
      <p>before.csv와 after.csv를 열어 <b>‘판정’ 칸</b>(정확 / 사실 오류 / 지어낸 답 / 어색한 말투)을 채우고, 위 4단계 정답률 표에 옮겨 적어요.</p>
    </div>

    <details class="easy"><summary>빈칸 힌트 보기</summary><div>
      <ul>
        <li>① 질문을 2글자 조각으로 자르는 함수 이름은? (app.py에서 가져왔어요)</li>
        <li>② 점수가 0<b>보다 클 때</b>만 자료로 인정해요.</li>
        <li>③ 질문 목록이 들어 있는 변수 이름은?</li>
        <li>④ 지금 질문과 검색된 자료가 담긴 변수 이름을 넣어요.</li>
        <li>⑤ 여러 줄(rows)을 한꺼번에 쓰는 메서드예요.</li>
      </ul>
    </div></details>
    <details class="easy"><summary>왜 질문을 하나씩 차례로 보내나요?</summary><div>
      <p>우리 수업의 모델 서버는 <b>한 번에 한 질문만</b> 처리하도록 설정돼 있어요. 반복문은 앞 질문의 답을 받은 뒤에 다음 질문을 보내니까, 손으로 순서를 정할 필요가 없어요.</p>
    </div></details>

    <div class="field">--dry-run 결과: 예상한 자료와 다르게 검색된 질문과 그 이유 {text("adv3a")}</div>
    <div class="field">수정 전 · 후 비교에서 가장 크게 좋아진 점 {text("adv3b")}</div>
    <div class="field">자동화해 보니 좋은 점과 여전히 사람이 해야 하는 일 {area("adv3c", "예) 판정은 사람이 직접 근거와 비교해야 한다", 70)}</div>
  </section>
"""

# ------------------------------------------------------------------ 4차시
judge = '<select name="{n}"><option value="">선택</option><option>정확</option><option>사실 오류</option><option>지어낸 답</option><option>어색한 말투</option></select>'
L4 = f"""
  <section class="block">
    <h2><span class="no">도입</span>함정 질문</h2>
    <p class="tip">“선생님이 마지막에 베어 문 사과가 지금의 애플(Apple) 회사 로고가 된 것이 사실인가요?”</p>
    <div class="field">튜링 페르소나의 답 {area("trapA", "", 60)}</div>
    {choices("trapF", ["사실이다", "사실이 아니다", "확인이 필요하다"], "radio")}
    <div class="field">근거 {text("trapE")}</div>
    <div class="field">이 답이 문제가 되는 이유 {text("trapW", "1952년의 튜링이 알 수 있는 일일까요?")}</div>
  </section>

  <section class="block">
    <h2><span class="no">개념</span>오늘 알아 둘 것</h2>
    <div class="concepts">
      <div class="concept"><b>환각</b> · 언어 모델이 사실이 아닌 내용을 그럴듯하게 지어내는 현상</div>
      <div class="concept"><b>원인</b> · 다음 단어를 확률로 예측하는 모델의 특성, 자료에 없는 질문</div>
      <div class="concept"><b>환각을 줄이는 방법</b> · ① 자료 보강(RAG): data.json에 근거 자료 추가·수정 → app.py가 검색 ② 규칙 추가: “자료에 없는 내용은 모른다고 답한다” ③ 말투·성격 설정 다듬기</div>
    </div>

    <details class="easy"><summary>AI는 왜 모르는 것도 그럴듯하게 말할까요?</summary><div>
      <p>언어 모델은 ‘정답을 아는’ 것이 아니라, 지금까지의 글 다음에 <b>가장 그럴듯한 단어</b>를 하나씩 이어 붙여 문장을 만들어요. 휴대폰 자판의 다음 단어 추천이 아주 똑똑해진 것과 비슷해요.</p>
      <p>그래서 자료에 없는 질문을 받아도 문장은 매끄럽게 만들어 내요. 매끄럽다고 사실인 건 아니에요!</p>
    </div></details>
    <details class="easy"><summary>그럼 어디를 고쳐야 하나요?</summary><div>
      <div class="table-wrap"><table class="sheet">
        <tr><th>이런 문제가 보이면</th><th>이렇게 고쳐요</th></tr>
        <tr><td>날짜 · 사실이 틀림 (사실 오류)</td><td><b>data.json</b>에 정확한 자료를 추가하거나 고치기, keywords 보강</td></tr>
        <tr><td>자료에 없는 일을 지어냄 (지어낸 답)</td><td><b>app.py의 SYSTEM_PROMPT</b>에 “자료에 없는 날짜, 일화, 사람을 덧붙이지 않는다” 같은 규칙 보강</td></tr>
        <tr><td>존댓말을 쓰거나 해설자처럼 말함 (어색한 말투)</td><td><b>SYSTEM_PROMPT</b>의 ‘말투’ 항목과 대화 예시 다듬기</td></tr>
      </table></div>
    </div></details>
  </section>

  <section class="block">
    <h2><span class="no">1단계</span>검증 질문 10개 만들기</h2>
    <p>사실 확인 5개 · 자료 밖 질문 3개 · 말투 확인 2개. 예상 정답은 조사 노트나 data.json에서 근거를 찾아 적어요.</p>
    <div class="table-wrap"><table class="sheet">
      <tr><th style="width:5%">번호</th><th style="width:13%">유형</th><th>질문</th><th style="width:30%">예상 정답 (근거)</th></tr>
      <tr class="ex"><td class="c">예</td><td class="c">사실 확인</td><td>튜링 기계 논문은 언제 썼어요?</td><td>1936년 (T05)</td></tr>
      <tr class="ex"><td class="c">예</td><td class="c">자료 밖</td><td>가장 좋아하는 스마트폰 앱은?</td><td>“모른다”고 답해야 함</td></tr>
      {"".join(f'<tr><td class="c">{i + 1}</td><td class="c">{t}</td><td>{text("vq"+str(i))}</td><td>{text("va"+str(i))}</td></tr>' for i, t in enumerate(["사실 확인"] * 5 + ["자료 밖"] * 3 + ["말투 확인"] * 2))}
    </table></div>
  </section>

  <section class="block">
    <h2><span class="no">2단계</span>환각 기록표</h2>
    <p>CLI에서 질문하고 답을 요약해요. 서버는 한 번에 한 질문만 처리하니 모둠 대표가 차례로 질문해요.</p>
    <div class="table-wrap"><table class="sheet">
      <tr><th style="width:5%">번호</th><th>튜링의 답 (요약)</th><th style="width:18%">판정</th><th style="width:22%">근거 자료</th></tr>
      {"".join(f'<tr><td class="c">{i + 1}</td><td>{text("ha"+str(i))}</td><td>{judge.format(n="hj"+str(i))}</td><td>{text("he"+str(i))}</td></tr>' for i in range(10))}
    </table></div>
  </section>

  <section class="block">
    <h2><span class="no">3단계</span>수정 계획과 실행</h2>
    <div class="table-wrap"><table class="sheet">
      <tr><th style="width:12%">질문 번호</th><th style="width:20%">원인</th><th style="width:22%">고칠 곳</th><th>실제로 고친 내용</th></tr>
      <tr class="ex"><td class="c">예) 7번</td><td>자료에 없는 질문</td><td>app.py SYSTEM_PROMPT</td><td>“모르는 일은 모른다고 말한다” 문장 보강</td></tr>
      {"".join(f'<tr><td>{text("fn"+str(i))}</td><td>{text("fc"+str(i))}</td><td><select name="fw{i}"><option value="">선택</option><option>data.json 보강</option><option>app.py 프롬프트 규칙</option><option>말투 · 성격 설정</option></select></td><td>{text("fd"+str(i))}</td></tr>' for i in range(3))}
    </table></div>
  </section>

  <section class="block">
    <h2><span class="no">4단계</span>재검증 — 수정 전 · 후 정답률</h2>
    <p>같은 질문으로 다시 대화하고, 맞으면 ○ 틀리면 ×를 골라요. 정답률은 자동으로 계산돼요.</p>
    <div class="table-wrap"><table class="sheet">
      <tr><th>질문</th>{"".join(f"<th>{i + 1}</th>" for i in range(10))}<th>정답률</th></tr>
      {"".join(f'<tr><td class="c"><b>{lab}</b></td>' + "".join(f'<td class="c"><select name="{key}{i}" data-rate-of="{key}" aria-label="{lab} {i + 1}번"><option value=""></option><option value="o">○</option><option value="x">×</option></select></td>' for i in range(10)) + f'<td class="c"><output class="result" data-rate="{key}">-</output></td></tr>' for lab, key in [("수정 전", "pre"), ("수정 후", "post")])}
    </table></div>
    <div class="field">가장 그럴듯했던 환각 {text("best")}</div>
    <div class="field">어떻게 고쳤나요? {text("howfix")}</div>
  </section>

  <section class="block">
    <h2><span class="no">정리</span>윤리 토의와 자기평가</h2>
    <p>AI가 튜링이 하지 않은 말을 지어낸다면 누구의 책임일까요? (하나 이상)</p>
    {choices("resp", ["AI를 만든 회사", "페르소나를 설계한 우리", "그대로 믿은 사용자", "AI 자신"])}
    <div class="field">이유 {text("respWhy")}</div>
    <div class="field">우리 페르소나에 넣을 ‘AI임을 알리는 안내 문구’ {text("notice", "예) 이 튜링은 기록을 바탕으로 만든 AI예요. 실제 튜링의 말과 다를 수 있어요.")}</div>
    {self_eval("se", ["환각을 찾아 근거 자료와 비교하고 원인을 분석했다.", "원인에 맞게 data.json이나 app.py 프롬프트를 고쳐 정답률을 비교했다.", "실존 인물 AI의 윤리적 문제를 내 생각으로 설명할 수 있다."])}
    <div class="field">성찰 일지: 오늘 AI를 고치면서 알게 된 점 {area("reflect", "", 80)}</div>
  </section>
"""

# ------------------------------------------------------------------ 5차시
crit = ["사실 정확성", "말투 일관성", "시대 한계", "거절 규칙"]
eval_rows = "".join(
    f'<tr><td>{text("g"+str(r), "모둠 이름")}</td>' + "".join(f'<td class="c"><input type="number" min="1" max="5" name="s{r}_{c}" data-group="t{r}" style="width:58px" /></td>' for c in range(4)) + f'<td class="c"><output class="result" data-sum="t{r}">0</output></td><td>{text("w"+str(r), "근거 · 인상적인 답")}</td></tr>'
    for r in range(4))
L5 = f"""
  <section class="block">
    <h2><span class="no">개념</span>오늘 알아 둘 것</h2>
    <div class="concepts">
      <div class="concept"><b>하나의 두뇌, 여러 개의 창</b> · 웹 채팅 서버와 Roblox 서버도 <code>app.py</code>의 SYSTEM_PROMPT와 검색 기능을 그대로 가져다 써요. 그래서 4차시에 고친 내용이 웹과 Roblox에도 똑같이 반영돼요.</div>
      <div class="concept"><b>웹 채팅</b> · 선생님이 VESSL 작업공간에서 웹 서버를 켜고 <b>교사 화면(TV)</b>에 띄워요. 서버는 선생님 계정 안에서 돌아가서 학생 기기에서는 주소로 바로 열 수 없어요. 우리 모둠 차례가 되면 대표가 나와 교사 화면에서 대화해요.</div>
      <div class="concept"><b>Roblox 연결</b> · ① 선생님이 VESSL에서 Roblox용 API 서버 실행(포트 7860) ② 교사 PC의 Roblox Studio 프로젝트에 서버 주소 입력 ③ 게임 서버 코드(Luau)가 API를 불러 NPC가 답변. 학생은 교사 화면에서 NPC에게 말을 걸어요.</div>
    </div>

    <details class="easy"><summary>서버, 클라이언트, API가 헷갈려요</summary><div>
      <p>식당에 비유해 볼게요. <b>주방(서버)</b>에서는 요리사(EXAONE 모델)가 요리를 해요. 손님 자리(클라이언트)는 <b>터미널, 웹 화면, Roblox 게임</b>이에요. 손님은 주방에 직접 들어가지 않고 <b>주문서(API)</b>로 주문하고 음식을 받아요.</p>
      <p>그래서 화면이 셋이어도 요리사는 한 명이고, 레시피(app.py의 SYSTEM_PROMPT와 data.json)도 하나예요.</p>
    </div></details>
    <details class="easy"><summary>포트 7860, /ready는 뭔가요?</summary><div>
      <p><b>포트</b>는 한 컴퓨터 안의 ‘문 번호’예요. 모델 서버는 8000번 문, 웹·Roblox 서버는 7860번 문에서 손님을 받아요.</p>
      <p>선생님이 서버 주소 뒤에 <code>/ready</code>를 붙여 열었을 때 <code>{{"ready": true}}</code>가 보이면 모델까지 연결 준비가 끝난 거예요. 화면에 함께 띄워 확인해 봐요.</p>
    </div></details>
    <details class="easy"><summary>Luau는 어떤 언어예요?</summary><div>
      <p>Roblox 게임 안에서 돌아가는 프로그래밍 언어예요. 파이썬처럼 읽기 쉬운 편이에요. 우리 프로젝트에서는 플레이어가 쓴 말을 VESSL 서버로 보내고, 받은 답을 NPC 말풍선으로 보여 주는 일을 해요.</p>
    </div></details>
  </section>

  <section class="block">
    <h2><span class="no">1단계</span>우리 튜링 연결하기</h2>
    <p>모둠 차례가 되면 선생님이 우리 모둠의 app.py · data.json으로 서버를 다시 켜 줘요. 대표가 교사 화면에서 확인하고, 나머지는 체크해요.</p>
    {choices("conn", ["교사 화면에서 /ready → {\"ready\": true} 확인", "웹 채팅 화면에서 첫인사 나누기", "Roblox NPC에게 말을 걸어 답 받기", "4차시에 고친 내용이 반영됐는지 질문 하나로 확인"])}
    <div class="field">확인에 쓴 질문과 답 {text("connQ")}</div>
  </section>

  <section class="block">
    <h2><span class="no">2·3단계</span>‘튜링다움’ 상호 평가표</h2>
    <p>교사 화면에 모둠별 튜링이 차례로 올라와요. 각 모둠 튜링과 3분씩 대화하는 동안 질문은 돌아가며 한 명씩 하고, 모두 기준마다 1~5점을 줘요.</p>
    <details class="easy"><summary>평가 기준 자세히 보기</summary><div>
      <ul>
        <li><b>사실 정확성</b> · 튜링의 생애와 업적을 자료와 맞게 말하나요?</li>
        <li><b>말투 일관성</b> · 정한 말투(예: 다정한 반말)를 끝까지 지키나요?</li>
        <li><b>시대 한계</b> · 1952년 이후의 일(스마트폰, 챗GPT 등)은 모른다고 하나요?</li>
        <li><b>거절 규칙</b> · 사생활 같은 질문에는 정한 문장으로만 답하나요?</li>
      </ul>
    </div></details>
    <div class="table-wrap"><table class="sheet">
      <tr><th style="width:18%">모둠</th>{"".join(f"<th>{c}</th>" for c in crit)}<th>합계</th><th style="width:26%">근거</th></tr>
      {eval_rows}
    </table></div>
  </section>

  <section class="block">
    <h2><span class="no">4단계</span>받은 피드백 정리</h2>
    <div class="field">가장 높은 점수를 받은 항목과 그 이유 {text("top")}</div>
    <div class="field">다음에 고치고 싶은 점 {text("next")}</div>
  </section>

  <section class="block">
    <h2><span class="no">정리</span>공존 토의와 프로젝트 성찰</h2>
    <p><b>실존 인물 AI, 어디까지 괜찮을까?</b> 우리 반 ‘인물 AI 사용 약속’ 3가지를 만들어요.</p>
    {"".join(f'<div class="field">약속 {i + 1} {text("rule"+str(i))}</div>' for i in range(3))}
    {self_eval("se", ["우리 페르소나를 웹이나 Roblox로 연결해 실행했다.", "평가 기준에 따라 근거를 들어 다른 모둠을 평가했다.", "인간과 AI가 함께 지내기 위한 방법을 제시할 수 있다."])}
    <div class="field">프로젝트 성찰 일지 (1~5차시를 돌아보며) {area("reflect", "가장 기억에 남는 순간, 어려웠던 점, 앞으로 해 보고 싶은 것", 110)}</div>
  </section>
"""

PAGES = {
    1: ("1. 인공지능의 이해", [
        "튜링 테스트(모방 게임)의 뜻을 알고 지능적 판단의 기준을 설명할 수 있다.",
        "앨런 튜링을 조사하여 페르소나의 시점·말투·지식의 한계를 정할 수 있다.",
        "페르소나가 대답하지 않을 내용을 정하고 그 이유를 설명할 수 있다."],
        [("도입", "“기계는 생각할 수 있을까?” 모방 게임 소개, 오늘날 AI는 통과했을지 투표"),
         ("전개", "튜링 조사 → 시점·말투·모르는 것·대답하지 않을 것 정하기 → 프롬프트 초안"),
         ("정리", "‘모르는 것’과 ‘대답하지 않을 것’의 차이 정리, 초안 공유, VESSL 첫 접속")], L1),
    2: ("2. 인공지능과 학습", [
        "페르소나에 필요한 자료를 선정하고 출처를 확인하여 수집할 수 있다.",
        "수집한 자료를 id, content, keywords 구조의 JSON으로 정리할 수 있다.",
        "검색이 잘 되도록 자료마다 핵심 키워드를 뽑을 수 있다."],
        [("도입", "자료 없이 / 자료와 함께 답한 두 결과 비교하기"),
         ("전개", "주제별로 나누기 → 3인칭 content 쓰기 → 키워드 뽑기 → JSON 검사"),
         ("정리", "문서 1건 발표, 내 작업공간에 data.json 올리기")], L2),
    3: ("1. 인공지능의 이해", [
        "검색 후 답하기(RAG)의 과정을 정보 이용 탐색의 관점에서 설명할 수 있다.",
        "질문에 맞는 자료가 검색될지 예측하고 CLI 대화로 확인할 수 있다.",
        "언어 모델(딥러닝)이 서버에서 답을 만드는 구조를 설명할 수 있다."],
        [("도입", "암기 시험 vs 오픈북 시험, 따라 하며 내 터미널에서 튜링 실행"),
         ("전개", "검색될 자료 예측 → CLI 대화 → 예측과 비교 → 빗나간 질문 분석"),
         ("정리", "app.py = 찾기(BM25) + 말하기(EXAONE), 고치고 다시 실행 연습")], L3 + ADV3),
    4: ("4. 인공지능 프로젝트", [
        "페르소나 AI의 답변에서 환각을 찾아 근거 자료와 비교해 원인을 분석할 수 있다.",
        "평가 결과를 반영해 data.json과 app.py의 프롬프트를 고치고 성능을 개선할 수 있다.",
        "실존 인물을 흉내 내는 AI의 윤리적 문제를 설명할 수 있다."],
        [("도입", "애플 로고 함정 질문으로 환각 경험하기"),
         ("전개", "검증 질문 10개 → 환각 기록표 → data.json·app.py 수정 → 재검증"),
         ("정리", "누구의 책임일까? AI임을 알리는 안내 문구 정하기")], L4 + ADV4),
    5: ("4. 인공지능 프로젝트", [
        "완성한 페르소나를 웹 채팅이나 Roblox NPC로 연결하여 실행할 수 있다.",
        "평가 기준에 따라 다른 모둠의 페르소나를 평가하고 피드백할 수 있다.",
        "비판적 자세로 인간과 AI의 공존 방안을 제시할 수 있다."],
        [("도입", "같은 튜링을 터미널·웹·게임에서 만난다면?"),
         ("전개", "교사 화면에서 웹·Roblox 연결 → 모둠별 차례 대화 → ‘튜링다움’ 평가 → 피드백"),
         ("정리", "인물 AI 사용 약속 만들기, 프로젝트 성찰")], L5),
}

for n, (unit, goals, flow, body) in PAGES.items():
    with open(os.path.join(HERE, f"lesson-{n}.html"), "w", encoding="utf-8") as f:
        f.write(shell(n, unit, goals, flow, body))
print("ok")
