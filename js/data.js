// =====================================================
//  사이트 내용 데이터 — 이 파일만 고치면 사이트 내용이 바뀝니다.
//  "작성 예정"이라고 된 부분을 각자 채워 주세요.
// =====================================================

const TEAM = [
  { name: "구정화", school: "대성여자고등학교", region: "전남광주통합특별시 나주시", role: "CEO", roleDesc: "Team Leader", img: "assets/team/junghwa.png" },
  { name: "장원재", school: "춘천고등학교", region: "춘천", role: "CTO", roleDesc: "Technology", img: "assets/team/wonjae.png" },
  { name: "임태현", school: "경문고등학교", region: "서울 성동구", role: "CTO", roleDesc: "Technology", img: "assets/team/taehyun.png" },
  { name: "김세라", school: "울산광역시교육청 중등교육과", region: "울주군", role: "CDO", roleDesc: "진척도관리", img: "assets/team/sera.webp" },
  { name: "구현주", school: "신원고등학교", region: "고양시", role: "CDO", roleDesc: "웹페이지관리", img: "assets/team/hyunju.webp" },
  { name: "박혜경", school: "강동중학교", region: "대구", role: "CHRO", roleDesc: "기구관리", img: "assets/team/hyekyung.webp" },
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
    file: { href: "assets/docs/turing-lesson4-plan.hwp", name: "4차시_교수학습지도안.hwp", label: "4차시 교수·학습 지도안" },
    standards: "4. 인공지능 프로젝트 - 앨런 튜링 페르소나 AI (4/5차시)\n[12인기04-04] 평가 결과를 반영해 성능 개선 · [12인기03-04] 윤리적 딜레마 분석",
    goals: [
      "페르소나 AI의 답변에서 환각을 찾아 근거 자료와 비교해 원인을 분석할 수 있다.",
      "평가 결과를 반영해 프롬프트와 data.json을 고치고 성능을 개선할 수 있다.",
      "실존 인물을 흉내 내는 AI의 윤리적 문제를 설명할 수 있다.",
    ],
    flow: {
      intro: "[동기 유발 및 학습 목표 확인]\n• 함정 질문하기: “선생님이 마지막에 베어 문 사과가 지금의 애플(Apple) 회사 로고가 된 것이 사실인가요?”\n• AI가 튜링이 하지 않은 말, 모르는 상황에 대한 말을 지어내면 생길 문제 생각하기\n• 학습 목표 확인: 환각을 찾고 고쳐 ‘더 튜링다운’ AI 만들기",
      main: "[개념 설명]\n• 환각: 언어 모델이 사실이 아닌 내용을 그럴듯하게 지어내는 현상\n• 원인: 다음 단어를 확률로 예측하는 모델 특성, 자료에 없는 질문\n• 환각을 줄이는 방법\n  1. 자료 보강(RAG): data.json에 근거 자료 추가 및 수정\n  2. 특정 상황 규칙 추가: “자료에 없는 내용은 모른다고 답한다”\n  3. 올바른 말투 및 성격 설정: 1인칭, 1950년대 영국 수학자다운 말투\n\n[모둠활동 : 튜링 페르소나 디버깅]\n• 1단계 테스트: 검증 질문 10개로 페르소나와 대화(CLI)\n  (사실 확인 5 · 자료 밖 질문 3 · 말투 확인 2)\n• 2단계 판정: 조사 자료와 비교해 ‘환각 기록표’ 작성\n  - 사실 오류 / 지어낸 답 / 어색한 말투로 분류\n• 3단계 수정: data.json 보강 또는 프롬프트 수정\n• 4단계 재검증: 같은 질문으로 다시 대화하기\n  - 정답률 전·후 비교, ‘가장 그럴듯했던 환각’ 공유\n  - 서버는 한 번에 한 질문만 처리 → 모둠 대표가 질문",
      close: "[정리 및 평가]\n• 윤리 토의: AI가 튜링이 하지 않은 말을 지어낸다면 누구의 책임일까?\n  - 우리 페르소나에 넣을 ‘AI임을 알리는 안내 문구’ 정하기\n• 차시 예고: 웹·Roblox NPC 연결, ‘튜링다움’ 상호 평가",
    },
    // 지도안 표의 ‘학습자료 및 비고사항’ 칸 (단계별)
    flowMaterials: {
      intro: "- 교사 제작 PPT\n- 튜링 페르소나\n  CLI 실습 서버",
      main: "- 교사 제작 PPT\n- 튜링 data.json\n■ 환각 기록표\n   활동지",
      close: "■ 자기평가\n  (성찰 일지)\n■ 수정 전·후\n  정답률 기록표",
    },
    assessment: "자기평가(성찰 일지), 수정 전·후 정답률 기록표",
    materials: "도입: 교사 제작 PPT, 튜링 페르소나 CLI 실습 서버\n전개: 교사 제작 PPT, 튜링 data.json, 환각 기록표 활동지",
    tips: "장소는 컴퓨터실. 서버는 한 번에 한 질문만 처리하므로 모둠 대표가 차례로 질문합니다.",
  },
];

// 의견 남기기 — 구글 폼 주소를 넣으면 버튼이 연결됩니다.
const FEEDBACK_FORM_URL = "";
