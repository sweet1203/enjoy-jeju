// =====================================================
//  사이트 내용 데이터 — 이 파일만 고치면 사이트 내용이 바뀝니다.
//  "작성 예정"이라고 된 부분을 각자 채워 주세요.
// =====================================================

const TEAM = [
  { name: "구정화", role: "CEO", roleDesc: "Team Leader", img: "assets/team/junghwa.png" },
  { name: "장원재", role: "CTO", roleDesc: "Technology", img: "assets/team/wonjae.png" },
  { name: "임태현", role: "CTO", roleDesc: "Technology", img: "assets/team/taehyun.png" },
  { name: "김세라", role: "CDO", roleDesc: "진척도관리", img: "assets/team/sera.webp" },
  { name: "구현주", role: "CDO", roleDesc: "웹페이지관리", img: "assets/team/hyunju.webp" },
  { name: "박혜경", role: "CHRO", roleDesc: "기구관리", img: "assets/team/hyekyung.webp" },
];

// 수업계획안 — 주제는 (안)입니다. 자유롭게 바꾸세요.
const LESSONS = [
  {
    id: "culture", teacher: "구정화", area: "디지털 문화", icon: "🛡️",
    title: "제주 여행 정보, 믿어도 될까?",
    summary: "가짜 리뷰·과장 광고를 판별하며 디지털 정보 윤리와 미디어 리터러시를 기른다.",
    grade: "중학교 1학년", periods: "2차시",
    standards: "작성 예정", goals: ["작성 예정"],
    flow: { intro: "작성 예정", main: "작성 예정", close: "작성 예정" },
    assessment: "작성 예정", materials: "작성 예정", tips: "작성 예정",
  },
  {
    id: "algorithm", teacher: "장원재", area: "알고리즘", icon: "🗺️",
    title: "최단 경로로 제주 한 바퀴",
    summary: "제주 관광지를 그래프로 표현하고 최단 경로를 찾는 알고리즘을 설계한다.",
    grade: "중학교 2학년", periods: "3차시",
    standards: "작성 예정", goals: ["작성 예정"],
    flow: { intro: "작성 예정", main: "작성 예정", close: "작성 예정" },
    assessment: "작성 예정", materials: "작성 예정", tips: "작성 예정",
  },
  {
    id: "programming", teacher: "임태현", area: "프로그래밍", icon: "💬",
    title: "제주 여행 안내 챗봇 만들기",
    summary: "조건문과 반복문으로 관광지·음식을 추천하는 챗봇 프로그램을 만든다.",
    grade: "중학교 2학년", periods: "3차시",
    standards: "작성 예정", goals: ["작성 예정"],
    flow: { intro: "작성 예정", main: "작성 예정", close: "작성 예정" },
    assessment: "작성 예정", materials: "작성 예정", tips: "작성 예정",
  },
  {
    id: "data", teacher: "김세라", area: "자료와 정보", icon: "📊",
    title: "제주 관광객 데이터 탐험대",
    summary: "공공데이터로 월별 관광객 수를 분석하고 시각화해 의미를 해석한다.",
    grade: "중학교 3학년", periods: "2차시",
    standards: "작성 예정", goals: ["작성 예정"],
    flow: { intro: "작성 예정", main: "작성 예정", close: "작성 예정" },
    assessment: "작성 예정", materials: "작성 예정", tips: "작성 예정",
  },
  {
    id: "ai", teacher: "구현주", area: "인공지능", icon: "🍊",
    title: "귤 품질 분류 AI 만들기",
    summary: "이미지 학습 도구로 귤의 상태를 분류하는 AI 모델을 만들고 한계를 토의한다.",
    grade: "중학교 3학년", periods: "2차시",
    standards: "작성 예정", goals: ["작성 예정"],
    flow: { intro: "작성 예정", main: "작성 예정", close: "작성 예정" },
    assessment: "작성 예정", materials: "작성 예정", tips: "작성 예정",
  },
  {
    id: "system", teacher: "박혜경", area: "컴퓨팅 시스템", icon: "🌊",
    title: "제주 바다 지킴이 센서",
    summary: "센서와 피지컬 컴퓨팅 보드로 해양 쓰레기 문제를 알리는 장치를 만든다.",
    grade: "중학교 1학년", periods: "3차시",
    standards: "작성 예정", goals: ["작성 예정"],
    flow: { intro: "작성 예정", main: "작성 예정", close: "작성 예정" },
    assessment: "작성 예정", materials: "작성 예정", tips: "작성 예정",
  },
];

// 의견 남기기 — 구글 폼 주소를 넣으면 버튼이 연결됩니다.
const FEEDBACK_FORM_URL = "";
