// =====================================================
//  사이트 내용 데이터 — 이 파일만 고치면 사이트 내용이 바뀝니다.
//  "작성 예정"이라고 된 부분을 각자 채워 주세요.
// =====================================================

const TEAM = [
  { name: "구정화", school: "대성여자고등학교", region: "전남광주통합특별시", role: "CEO", roleDesc: "Team Leader", img: "assets/team/junghwa-sprite.webp" },
  { name: "장원재", school: "춘천고등학교", region: "춘천시", role: "CTO", roleDesc: "Technology", img: "assets/team/wonjae-sprite.webp" },
  { name: "임태현", school: "경문고등학교", region: "서울 성동구", role: "CTO", roleDesc: "Technology", img: "assets/team/taehyun-sprite.webp" },
  { name: "김세라", school: "울산광역시교육청 중등교육과", region: "울주군", role: "CDO", roleDesc: "진척도관리", img: "assets/team/sera-sprite.webp" },
  { name: "구현주", school: "신원고등학교", region: "고양시", role: "CDO", roleDesc: "웹페이지관리", img: "assets/team/hyunju-sprite.webp" },
  { name: "박혜경", school: "강동중학교", region: "대구광역시", role: "CHRO", roleDesc: "기구관리", img: "assets/team/hyekyung-sprite.webp" },
];

// 수업계획안 — 빈칸("")은 사이트에 "작성 예정"으로 표시됩니다.
const LESSONS = [
  {
    id: "turing-persona-ai", teacher: "", area: "생성형 AI", icon: "🤖",
    subject: "인공지능 기초",
    title: "앨런 튜링 페르소나 AI 만들기",
    summary: "4차시 공개수업 · 환각을 찾아 고치는 ‘튜링 페르소나 디버깅’",
    grade: "고등학교 2학년", periods: "4/5차시 (공개수업)",
    // 원본 지도안 파일 (assets/docs 폴더) — 상세 계획안과 자료실에 내려받기 버튼이 생깁니다.
    file: { href: "assets/docs/lesson4-plan.hwp", name: "4차시_교수학습지도안.hwp", label: "4차시 교수·학습 지도안" },
    standards: "4. 인공지능 프로젝트 - 앨런 튜링 페르소나 AI (4/5차시)\n[12인기04-04] 평가 결과를 반영해 성능 개선 · [12인기03-04] 윤리적 딜레마 분석",
    goals: [
      "페르소나 AI의 답변에서 환각을 찾아 근거 자료와 비교해 원인을 분석할 수 있다.",
      "평가 결과를 반영해 data.json과 app.py의 프롬프트를 고치고 성능을 개선할 수 있다.",
      "실존 인물을 흉내 내는 AI의 윤리적 문제를 설명할 수 있다.",
    ],
    flow: {
      intro: "[동기 유발 및 학습 목표 확인]\n• 함정 질문하기: “선생님이 마지막에 베어 문 사과가 지금의 애플(Apple) 회사 로고가 된 것이 사실인가요?”\n• AI가 튜링이 하지 않은 말, 모르는 상황에 대한 말을 지어내면 생길 문제 생각하기\n• 학습 목표 확인: 환각을 찾고 고쳐 ‘더 튜링다운’ AI 만들기",
      main: "[개념 설명]\n• 환각: 언어 모델이 사실이 아닌 내용을 그럴듯하게 지어내는 현상\n• 원인: 다음 단어를 확률로 예측하는 모델 특성, 자료에 없는 질문\n• 환각을 줄이는 방법\n  1. 자료 보강(RAG): data.json에 근거 자료 추가·수정 → app.py가 검색\n  2. 특정 상황 규칙 추가: “자료에 없는 내용은 모른다고 답한다”\n  3. 올바른 말투 및 성격 설정: 1인칭, 1950년대 영국 수학자다운 말투\n\n[모둠활동 : 튜링 페르소나 디버깅]\n• 1단계 테스트: 검증 질문 10개로 페르소나와 대화(CLI)\n  (사실 확인 5 · 자료 밖 질문 3 · 말투 확인 2)\n• 2단계 판정: 조사 자료와 비교해 ‘환각 기록표’ 작성\n  - 사실 오류 / 지어낸 답 / 어색한 말투로 분류\n• 3단계 수정: data.json 보강 또는 app.py 프롬프트 수정\n• 4단계 재검증: 같은 질문으로 다시 대화하기\n  - 정답률 전·후 비교, ‘가장 그럴듯했던 환각’ 공유\n  - 서버는 한 번에 한 질문만 처리 → 모둠 대표가 질문",
      close: "[정리 및 평가]\n• 윤리 토의: AI가 튜링이 하지 않은 말을 지어낸다면 누구의 책임일까?\n  - 우리 페르소나에 넣을 ‘AI임을 알리는 안내 문구’ 정하기\n• 차시 예고: 웹·Roblox NPC 연결, ‘튜링다움’ 상호 평가",
    },
    // 지도안 표의 ‘학습자료 및 비고사항’ 칸 (단계별)
    flowMaterials: {
      intro: "- 교사 제작 PPT\n- 튜링 페르소나\n  CLI 실습 서버",
      main: "- 교사 제작 PPT\n- 튜링 data.json\n- app.py\n■ 환각 기록표\n   활동지",
      close: "■ 자기평가\n  (성찰 일지)\n■ 수정 전·후\n  정답률 기록표",
    },
    assessment: "자기평가(성찰 일지), 수정 전·후 정답률 기록표",
    materials: "도입: 교사 제작 PPT, 튜링 페르소나 CLI 실습 서버\n전개: 교사 제작 PPT, 튜링 data.json, app.py, 환각 기록표 활동지",
    tips: "장소는 컴퓨터실. 서버는 한 번에 한 질문만 처리하므로 모둠 대표가 차례로 질문합니다.",
  },
];

// 자료실 · 차시별 수업 자료 겸 학습지 (웹페이지, lessons 폴더)
const LESSON_PAGES = [
  { no: 1, title: "튜링 페르소나 설계도 만들기", desc: "모방 게임, 시스템 프롬프트, 설계도 4요소", href: "lessons/lesson-1.html", plan: "assets/docs/lesson1-plan.hwp", planImg: "assets/docs/lesson1-plan.webp",
    goals: ["튜링 테스트(모방 게임)의 뜻을 알고 지능적 판단의 기준을 설명할 수 있다.", "앨런 튜링을 조사하여 페르소나의 시점·말투·지식의 한계를 정할 수 있다.", "페르소나가 대답하지 않을 내용을 정하고 그 이유를 설명할 수 있다."],
    flow: { intro: "‘기계는 생각할 수 있을까?’ 모방 게임으로 문 열기", main: "앨런 튜링 조사 노트 → 모둠 튜링 설계도(시점 · 말투 · 모르는 것 · 답하지 않을 것) → 시스템 프롬프트 초안", close: "VESSL 첫 접속(5분) · 스스로 평가하기" },
    acts: ["앨런 튜링 조사 노트", "우리 모둠 튜링의 설계도", "시스템 프롬프트(역할 설명서) 초안", "VESSL 첫 접속"] },
  { no: 2, title: "튜링 자료집 data.json 만들기", desc: "JSON 문법, 3인칭 서술, 키워드, JSON 검사기", href: "lessons/lesson-2.html", plan: "assets/docs/lesson2-plan.hwp", planImg: "assets/docs/lesson2-plan.webp",
    goals: ["페르소나에 필요한 자료를 선정하고 출처를 확인하여 수집할 수 있다.", "수집한 자료를 id, content, keywords 구조의 JSON으로 정리할 수 있다.", "검색이 잘 되도록 자료마다 핵심 키워드를 뽑을 수 있다."],
    flow: { intro: "‘자료가 틀리면 AI도 틀린다’ · JSON 구조 알아보기", main: "조사 노트를 주제별 문서로 나누기 → 문서 쓰기와 키워드 뽑기 → JSON 형식 검사기", close: "내 작업공간에 data.json 올리기(10분) · 스스로 평가하기" },
    acts: ["주제별 문서 나누기", "문서 쓰기 · 키워드 뽑기", "JSON 형식 검사기", "작업공간에 data.json 올리기"] },
  { no: 3, title: "튜링과 첫 대화: 찾아보고 답하는 AI", desc: "RAG · BM25 · 2글자 자르기 체험, 검색 예측", href: "lessons/lesson-3.html", plan: "assets/docs/lesson3-plan.hwp", planImg: "assets/docs/lesson3-plan.webp",
    goals: ["검색 후 답하기(RAG)의 과정을 정보 이용 탐색의 관점에서 설명할 수 있다.", "질문에 맞는 자료가 검색될지 예측하고 CLI 대화로 확인할 수 있다.", "언어 모델(딥러닝)이 서버에서 답을 만드는 구조를 설명할 수 있다."],
    flow: { intro: "교사 화면을 따라 터미널에서 튜링 열기(10분)", main: "RAG · BM25 · 2글자 자르기 이해 → 자료집 문서 목록 보며 검색 예측 기록지 → CLI 대화로 확인", close: "OPENING 한 줄 고치고 다시 실행(4차시 준비) · 스스로 평가하기" },
    acts: ["따라 하며 튜링 열기", "검색 예측 기록지", "고치고 다시 실행하기", "선택 심화: app.py 1·2단계"] },
  { no: 4, title: "튜링 페르소나 디버깅: 환각 찾고 고치기", desc: "환각 기록표, 수정 전·후 정답률 자동 계산", href: "lessons/lesson-4.html", plan: "assets/docs/lesson4-plan.hwp", planImg: "assets/docs/lesson4-plan.webp",
    goals: ["페르소나 AI의 답변에서 환각을 찾아 근거 자료와 비교해 원인을 분석할 수 있다.", "평가 결과를 반영해 data.json과 app.py의 프롬프트를 고치고 성능을 개선할 수 있다.", "실존 인물을 흉내 내는 AI의 윤리적 문제를 설명할 수 있다."],
    flow: { intro: "함정 질문으로 환각 만나기", main: "검증 질문 10개 → 환각 기록표 → 수정 계획과 실행 → 재검증(수정 전 · 후 정답률)", close: "윤리 토의(누구의 책임일까?) · 자기평가" },
    acts: ["검증 질문 10개", "환각 기록표", "수정 전 · 후 정답률", "선택 심화: eval.py"] },
  { no: 5, title: "튜링 NPC 공개와 상호 평가", desc: "웹·Roblox 연결, ‘튜링다움’ 평가표", href: "lessons/lesson-5.html", plan: "assets/docs/lesson5-plan.hwp", planImg: "assets/docs/lesson5-plan.webp",
    goals: ["완성한 페르소나를 웹 채팅이나 Roblox NPC로 연결하여 실행할 수 있다.", "평가 기준에 따라 다른 모둠의 페르소나를 평가하고 피드백할 수 있다.", "비판적 자세로 인간과 AI의 공존 방안을 제시할 수 있다."],
    flow: { intro: "서버 · API로 튜링이 웹과 Roblox에 이어지는 구조 알기", main: "우리 튜링 연결하기 → ‘튜링다움’ 상호 평가표 → 받은 피드백 정리", close: "인간과 AI의 공존 토의 · 프로젝트 성찰" },
    acts: ["웹 · Roblox NPC 연결", "‘튜링다움’ 상호 평가표", "피드백 정리", "공존 토의와 성찰"] },
];

// 자료실 — 코드 파일 (선택 심화 · 확장 트랙)
const CODE_FILES = [
  { name: "eval_starter.py", href: "assets/code/eval_starter.py", desc: "4차시 선택 심화 · 빈칸 5개 자동 검증 프로그램" },
  { name: "eval.py", href: "assets/code/eval.py", desc: "eval_starter.py 완성본 (교사용)" },
  { name: "questions.csv", href: "assets/code/questions.csv", desc: "검증 질문 10개 예시" },
  { name: "app_missions.py", href: "assets/code/app_missions.py", desc: "확장 트랙 3 미션 1~6 예시 답안 (교사용)" },
];

// 의견 나누기 — 패들릿 주소. 바꾸면 버튼 링크가 바뀝니다.
const FEEDBACK_FORM_URL = "https://padlet.com/daesunggirlshighschool/padlet-s024l52tic5gfq6wz0qa";
