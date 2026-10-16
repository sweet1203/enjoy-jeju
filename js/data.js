// =====================================================
//  사이트 내용 데이터 — 이 파일만 고치면 사이트 내용이 바뀝니다.
//  "작성 예정"이라고 된 부분을 각자 채워 주세요.
// =====================================================

const TEAM = [
  { name: "구정화", region: "전남광주통합특별시 나주시", role: "CEO", roleDesc: "Team Leader", img: "assets/team/junghwa.png" },
  { name: "장원재", region: "춘천", role: "CTO", roleDesc: "Technology", img: "assets/team/wonjae.png" },
  { name: "임태현", region: "서울 성동구", role: "CTO", roleDesc: "Technology", img: "assets/team/taehyun.png" },
  { name: "김세라", region: "울주군", role: "CDO", roleDesc: "진척도관리", img: "assets/team/sera.webp" },
  { name: "구현주", region: "고양시", role: "CDO", roleDesc: "웹페이지관리", img: "assets/team/hyunju.webp" },
  { name: "박혜경", region: "대구", role: "CHRO", roleDesc: "기구관리", img: "assets/team/hyekyung.webp" },
];

// 수업계획안 — 빈칸("")은 사이트에 "작성 예정"으로 표시됩니다.
const LESSONS = [
  {
    id: "persona-ai", teacher: "", area: "생성형 AI", icon: "🤖",
    title: "페르소나 AI 만들기",
    summary: "",
    grade: "", periods: "",
    standards: "", goals: [],
    flow: { intro: "", main: "", close: "" },
    assessment: "", materials: "", tips: "",
  },
  {
    id: "object-detection", teacher: "", area: "컴퓨터 비전", icon: "🎯",
    title: "Object Detection 모델 만들기",
    summary: "Object Detection 모델 만들기 → Roboflow → 아이유 얼굴 따라가기 모델 만들기",
    grade: "", periods: "",
    standards: "", goals: [],
    flow: { intro: "", main: "", close: "" },
    assessment: "", materials: "", tips: "",
  },
];

// 의견 남기기 — 구글 폼 주소를 넣으면 버튼이 연결됩니다.
const FEEDBACK_FORM_URL = "";
