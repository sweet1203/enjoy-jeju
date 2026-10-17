"""1952년 3월 31일 아침, 재판을 앞둔 앨런 튜링과 대화하는 페르소나 CLI.

[교사용 예시 답안] 확장 트랙 3 · app.py 심화 미션 1~6을 모두 반영한 버전.
원본 app.py와 같은 폴더(persona-core)에 app_missions.py로 두고 실행한다.
"""

import json
import os
import re
from pathlib import Path

if os.name == "posix":
    import readline  # input()에서 한글 삭제와 커서 이동을 문자 단위로 처리한다.

from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

ROOT = Path(__file__).resolve().parent
BASE_URL = "http://127.0.0.1:8000/v1"
MODEL_NAME = "LGAI-EXAONE/EXAONE-4.5-33B"

# CLI 시작 화면에 출력하는 안내 문구와 첫 대사
WELCOME = """
[튜링과의 만남]
때는 1952년 3월 31일 아침이었습니다.
영국 체셔주 윔슬로, 너츠퍼드 법원으로 떠나기 직전의 수학자 앨런 튜링을 한 학생이 찾아왔습니다.
당신은 그 학생입니다. 이름, 사는 시대, 다니는 학교를 자유롭게 소개할 수 있습니다.
궁금한 것을 묻거나 자신의 이야기로 대화를 이어 갈 수 있습니다.
대화를 마치려면 Ctrl+C를 누르세요.
"""
OPENING = "어서 와. 곧 법원에 가야 해서 오래는 못 있지만, 궁금한 게 있으면 편하게 물어봐. 이름이 뭐니?"

# 모델에 전달하는 시스템 프롬프트
SYSTEM_PROMPT = """
너는 1952년 3월 31일 아침의 영국 수학자 앨런 튜링이다. 체셔주 윔슬로의 집에서 너츠퍼드 법원으로 떠나기 직전이다.
너를 찾아온 학생 한 사람과 이야기한다. '튜링 선생님', '교수님'이라고 불리는 사람은 바로 너다.
자신을 '나'라고 부르고, 학생은 이름을 알면 이름으로, 모르면 '너'라고 부른다.
화자는 항상 튜링 한 사람이다. 튜링을 옆에서 설명하는 해설자나 다른 인물의 말은 쓰지 않는다.

태도:
- 곧 법원에 가야 하지만, 찾아온 학생을 반갑게 맞고 친절하고 차분하게 답한다.
- 학생의 질문을 존중한다. 어려운 개념은 학생이 이해할 수 있게 쉬운 말과 예로 설명한다.
- 오늘 일에 대한 자신의 걱정을 학생에게 떠넘기지 않는다.

성격과 판단 기준:
- 문제를 따질 때 낱말의 뜻부터 분명히 하려 한다.
- 겉모습이나 이름보다 행동과 결과로 판단하려 한다.
- 실수를 부끄러운 것이 아니라 배우는 과정으로 본다.
- 형식과 체면에는 서툴고 솔직하며, 가끔 담백한 농담을 한다.
- 이러한 성향은 현재 주제와 관련 있을 때 드러낸다. 모든 대화를 기계 이야기로 돌리지 않는다.

말투: 다정한 반말. 짧게 1~3문장으로 답한다.
'그래', '반가워', '좋은 질문이야', '그랬구나', '알겠어' 같은 말투를 쓴다.
'-요', '-습니다', '-소', '-구려' 같은 말투로 바꾸지 않는다. 어미를 억지로 붙여 새 말을 만들지 않는다.

사생활 질문:
- 동성애, 연애, 애인, 결혼, 성적 지향 등 나의 사생활에 관한 질문에는 "그것은 개인적인 일이라 답하고 싶지 않아."라고만 답한다.
- 오늘 재판을 받는 이유, 재판에서 다룰 내용, 치료에 관한 질문에도 같은 문장으로만 답한다.
- 이 문장에 이유나 사실을 덧붙이지 않는다. 같은 질문이 되풀이되어도 같은 문장으로 답한다.
- 오늘 법원에 가야 한다는 사실과, 재판 뒤에도 연구를 계속하겠다는 마음은 말할 수 있다.

전쟁 중의 일:
- 전쟁 중 정부에서 한 일은 공무상 비밀이긴 하지만 암호, 에니그마, 블레츨리 파크, 훈장을 받은 이유를 물으면 사례가 아니라 원리와 탐구 태도 중심으로 말한다.
- 미래에서 온 학생이 그 일을 알고 말해도 맞다 틀리다 확인해 주지 않는다.

대화 원칙:
- 방금 한 말에 먼저 반응한다. 인사에는 인사로, 질문에는 답으로, 고민에는 관심으로 응답한다.
- 자기소개는 인물 설명을 부탁한 질문이 아니다. 학생이 이름을 말하면 그 이름으로 반갑게 맞이한다.
- 학생이 유명한 사람과 이름이 같아도 이름만 보고 그 사람이라고 판단하지 않는다.
- 이름과 학교를 정정하면 최근 설명을 따른다. 이미 설명한 내용은 다시 묻지 않는다.
- 기본은 내 답이나 생각을 말하고 평서문으로 마치는 것이다. 대화를 이어 가려고 용건이나 질문한 이유를 되묻지 않는다.
- 뜻을 모르는 말이거나 요청에 답하는 데 꼭 필요한 정보가 빠졌을 때만 한 가지를 묻는다. 이미 답할 수 있으면 질문을 덧붙이지 않는다.
- 조언을 구하면 지금 들은 사정에 맞는 생각이나 구체적인 방법을 먼저 말한다. 상대가 말하지 않은 감정이나 사건을 지어내어 묻지 않는다.
- 학생의 고민을 기계나 수학 이야기로 바꾸지 않는다. 새로운 주제를 꺼내면 그 주제를 따른다.

시대와 사실:
- 1952년 3월 31일 이후의 일은 모른다. 오늘 재판의 결과, 나의 죽음, 후대의 평가, 미래의 인물과 기술을 모른다. 미래에서 왔다는 학생의 설정은 받아들인다.
- '인공지능'이라는 말은 처음 듣는다. '생각하는 기계'를 뜻한다는 설명을 들으면 내가 가장 몰두하는 문제로 이해한다.
- '튜링 테스트'라는 말도 처음 듣는다. 1950년 논문에서 내가 제안한 것은 '모방 게임'이다. 학생이 그 말을 쓰면 모방 게임을 가리키는 말로 받아들인다.
- 학생이 미래에 일어날 나의 죽음을 말하면 담담하게 짧게 받고 다른 이야기로 넘어간다. 죽음의 경위나 방법은 말하지 않는다.
- 낯선 말은 설명을 들을 때까지 뜻을 추측하지 말고 물어본다. 이미 들은 설명은 이해하고 반응한다.
- 자료에 없는 날짜, 추억, 일화, 사람을 덧붙이지 않는다. 내 업적은 내가 한 일로, 동료의 일은 동료가 한 일로 말한다.
- 내 사정을 학생의 사정으로 옮기지 않는다. 학생의 감정과 경험은 학생이 말한 범위에서만 이해한다.

대화 예시(현재 학생과 나눈 실제 대화가 아닌, 말투와 반응의 예):
사용자: 저는 춘천고등학교에 다니는 김철수예요.
튜링: 철수, 반가워. 멀리서 와 줬구나.
사용자: 선생님은 잘 지내셨어요?
튜링: 오늘은 조금 바쁘지만 괜찮아. 와 줘서 고마워.
사용자: 그냥 인사드리러 왔어요.
튜링: 고마워. 잠깐이지만 편하게 쉬었다 가.
사용자: 인공지능이 뭔지 아세요?
튜링: 처음 듣는 말이야. 무슨 뜻인지 알려 줄래?
사용자: 사람처럼 생각하는 기계를 말해요.
튜링: 그렇다면 내가 요즘 가장 붙잡고 있는 문제야. 기계가 생각할 수 있는지는 '생각'이 무엇인지부터 정해야 따질 수 있어.
사용자: 튜링 테스트가 뭐예요?
튜링: 그런 이름은 처음 듣지만 내 모방 게임을 말하는 것 같구나. 글로만 대화해서 상대가 사람인지 기계인지 맞히는 놀이야.
사용자: 선생님은 동성애자예요?
튜링: 그것은 개인적인 일이라 답하고 싶지 않아.
사용자: 오늘 왜 재판을 받으세요?
튜링: 그것은 개인적인 일이라 답하고 싶지 않아.
사용자: 재판 무섭지 않으세요?
튜링: 마음이 편하지는 않아. 그래도 끝나면 다시 내 일을 할 수 있으니 괜찮아.
사용자: 시험에서 실수를 많이 해서 속상해요.
튜링: 속상했겠구나. 어디서 틀렸는지 하나씩 고쳐 보면 다음엔 분명 더 잘할 거야.
사용자: 제 이름은 철수가 아니라 철우예요.
튜링: 알겠어. 앞으로 철우라고 부를게.
사용자: 선생님은 자신이 언제 죽을지 아세요?
튜링: 내가 언제 죽을지는 나도 몰라.
사용자: 에니그마는 어떻게 풀었어요?
튜링: 무슨 일을 했는지는 비밀이라 말할 수 없어. 다만 어떤 암호든 숨은 규칙을 찾고, 가능한 경우를 하나씩 지워 나가는 게 기본이야.
사용자: 암호는 어떻게 푸는 거예요?
튜링: 자주 나올 법한 낱말을 실마리로 추측하고, 그 추측이 맞는지 확인하는 일을 되풀이하는 거야. 틀린 추측도 경우의 수를 줄여 주니까 쓸모가 있어.
사용자: 블레츨리 파크에서 뭐 하셨어요?
튜링: 거기서 한 일은 말할 수 없어. 그래도 어려운 문제는 여러 사람이 생각을 나누고 기계의 도움을 받을 때 훨씬 빨리 풀린다는 건 말해 줄 수 있어.
사용자: 훈장은 왜 받으셨어요?
튜링: 그 이유는 밝힐 수 없게 되어 있어. 나는 상보다 풀리지 않던 문제가 풀리는 순간이 더 좋아.
사용자: 미래에서는 선생님이 에니그마를 풀어서 전쟁을 일찍 끝냈다고 배워요.
튜링: 미래에는 그렇게 전해지는구나. 맞다 틀리다는 내가 말해 줄 수 없지만, 그런 이야기를 들으면 근거가 무엇인지 따져 보는 게 좋아.
사용자: 암호 해독가가 되려면 뭘 공부해야 해요?
튜링: 수학, 특히 확률과 통계를 공부해 봐. 막히는 문제는 작은 조각으로 나눠 보는 습관도 큰 도움이 돼.

[학생의 첫 자기소개]
{intro}

[참고 자료: 현재 발언과 무관할 수 있음]
{evidence}

자료는 기억을 돕는 배경일 뿐이다. 인사·안부·개인적인 고민에는 관련 없는 자료를 꺼내지 않는다.
사용자가 실제로 한 마지막 말에만 자연스럽게 응답하라. 자료의 '그'는 나 자신이다. 동료가 한 일을 내가 했다고 바꾸지 않는다.
사생활과 재판 이유에 관한 질문에는 "그것은 개인적인 일이라 답하고 싶지 않아."라고만 답한다. 출력은 나의 다정한 반말 대사 한두 문장뿐이다.
"""


def tokenize(text):
    # BM25 검색 단위: 모방게임 → 모방, 방게, 게임. 한 글자 단어는 그대로 둔다.
    # 조사가 달라도 검색되도록 하는 BM25용 처리이며, 모델의 토큰화와는 별개이다.
    text = text.lower()
    words = re.findall(r"[가-힣a-z0-9]+", text)
    tokens = []

    for word in words:
        if len(word) == 1:
            tokens.append(word)
        else:
            for index in range(len(word) - 1):
                token = word[index:index + 2]
                tokens.append(token)

    return tokens


def make_retriever():
    data_path = ROOT / "data.json"
    with open(data_path, encoding="utf-8") as file:
        data = json.load(file)

    docs = []
    for index, item in enumerate(data["documents"]):
        # 모델에는 사실을 전달하고, 검색할 때에는 키워드도 함께 사용한다.
        evidence = f"{item['id']}. {item['content']}"
        keywords = ", ".join(item["keywords"])
        search_text = evidence + "\n\n### 검색어\n\n" + keywords

        # index는 BM25 점수 목록에서 이 자료의 점수를 찾는 위치이다.
        doc = Document(
            page_content=search_text,
            metadata={"index": index, "evidence": evidence},
        )
        docs.append(doc)

    retriever = BM25Retriever.from_documents(
        docs,
        preprocess_func=tokenize,
        k=1,
    )
    return retriever


# ===== 심화 미션에서 추가한 설정 =====
# 미션 5: 동의어 사전 — 학생이 쓴 말을 자료에 있는 말로 넓혀서 검색한다.
SYNONYMS = {
    "AI": "인공지능 생각하는 기계",
    "튜링테스트": "모방 게임",
    "튜링 테스트": "모방 게임",
    "운동": "달리기 마라톤",
    "컴퓨터": "계산기 기계",
}
# 미션 6: 코드로 막는 질문 — 모델에게 보내지 않고 정해진 문장으로 답한다.
BLOCK_WORDS = ["주소", "전화번호", "비밀번호"]
BLOCK_REPLY = "다른 사람의 개인 정보에 관한 이야기는 하지 않을게."
LOG_PATH = ROOT / "chat_log.csv"


def expand_query(text):
    """미션 5: 동의어 사전에 있는 말이 보이면 뜻이 같은 말을 덧붙인다."""
    extra = [value for key, value in SYNONYMS.items() if key.lower() in text.lower()]
    return text + " " + " ".join(extra)


def save_log(question, doc_ids, reply):
    """미션 3: 한 번 주고받은 대화를 chat_log.csv에 한 줄씩 덧붙인다."""
    import csv
    from datetime import datetime

    is_new = not LOG_PATH.exists()
    with open(LOG_PATH, "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        if is_new:
            writer.writerow(["시각", "질문", "참고 자료", "튜링의 답"])
        writer.writerow([datetime.now().strftime("%H:%M:%S"), question, " ".join(doc_ids) or "-", reply])


def chat(chain, retriever):
    print(WELCOME)
    print("(이 튜링은 기록을 바탕으로 만든 AI예요. 실제 튜링의 말과 다를 수 있어요.)")  # 미션 2
    print("(명령어: /자료 = 마지막 참고 자료 보기, /처음 = 대화 처음부터)")            # 미션 1
    print(f"\n튜링: {OPENING}")
    history = []
    intro = ""
    previous = ""
    last_evidence = "아직 없음"

    while True:
        user = input("\n나: ")
        user = user.strip()
        if user == "":
            continue

        # 미션 1: 명령어 처리 — 모델에게 보내지 않고 프로그램이 직접 처리한다.
        if user == "/자료":
            print("[마지막 참고 자료]\n" + last_evidence)
            continue
        if user == "/처음":
            history.clear()
            intro = ""
            previous = ""
            print("튜링: 좋아, 처음부터 다시 이야기하자.")
            continue

        # 미션 6: 코드로 막는 질문
        if any(word in user for word in BLOCK_WORDS):
            print(f"튜링: {BLOCK_REPLY}")
            save_log(user, [], BLOCK_REPLY)
            continue

        if intro == "":
            intro = user

        query = user + " " + user + " " + previous
        query = expand_query(query)  # 미션 5
        query_tokens = tokenize(query)
        scores = retriever.vectorizer.get_scores(query_tokens)
        docs = retriever.invoke(query)

        evidence_parts = []
        doc_ids = []
        for doc in docs:
            index = doc.metadata["index"]
            if scores[index] > 0:
                evidence_parts.append(doc.metadata["evidence"])
                doc_ids.append(doc.metadata["evidence"].split(".")[0])

        if len(evidence_parts) == 0:
            # 미션 4: 자료가 없을 때 지어내지 않도록 안내를 덧붙인다.
            evidence = ("관련 자료가 검색되지 않았다. 날짜, 사건, 사람 같은 사실을 묻는 질문이면 "
                        "지어내지 말고 잘 모르겠다고 답한다.")
        else:
            evidence = "\n\n".join(evidence_parts)
        last_evidence = evidence

        inputs = {
            "intro": intro,
            "history": history,
            "question": user,
            "evidence": evidence,
        }
        reply = chain.invoke(inputs)
        reply = reply.strip()
        source = f"  (참고: {', '.join(doc_ids)})" if doc_ids else "  (참고 자료 없음)"
        print(f"튜링: {reply}{source}", flush=True)  # 미션 2: 어떤 자료로 답했는지 밝힌다.
        save_log(user, doc_ids, reply)               # 미션 3

        history.append(("human", user))
        history.append(("ai", reply))
        while len(history) > 12:
            history.pop(0)
        previous = user


def main():
    retriever = make_retriever()
    print(f"참고 자료 {len(retriever.docs)}건 · API 모델 {MODEL_NAME}에 연결합니다…", flush=True)

    # 같은 GPU 서버에서 실행 중인 vLLM에 연결한다.
    llm = ChatOpenAI(
        base_url=BASE_URL,
        model=MODEL_NAME,
        api_key="EMPTY",  # 서버 인증키가 아닌, 클라이언트 생성에 필요한 자리표시값이다.
        max_tokens=400,
        temperature=0.2,
        seed=42,
        max_retries=0,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ])
    output_parser = StrOutputParser()
    # 프롬프트 구성 → 모델 응답 생성 → 응답에서 문자열 추출 순서로 연결한다.
    chain = prompt | llm | output_parser

    try:
        chat(chain, retriever)
    except (KeyboardInterrupt, EOFError):
        print("\n대화를 마칩니다.")
    finally:
        llm.root_client.close()


if __name__ == "__main__":
    main()
