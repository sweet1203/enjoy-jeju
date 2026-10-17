"""튜링 페르소나 자동 검증 프로그램 (선택 심화 3단계 · 학생용 빈칸 버전)

할 일: ① ~ ⑤ 의 빈칸(____)을 채워서 완성하세요.
완성하면 questions.csv의 질문을 하나씩 튜링에게 보내고 results.csv로 저장합니다.

실행:  python persona-core/eval_starter.py --dry-run   (먼저 검색만 확인)
       python persona-core/eval_starter.py             (모델에게 질문)
"""

import argparse
import csv
from pathlib import Path

from app import SYSTEM_PROMPT, BASE_URL, MODEL_NAME, make_retriever, tokenize

ROOT = Path(__file__).resolve().parent


def load_questions(path):
    with open(path, encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def find_evidence(retriever, question):
    """app.py와 같은 규칙으로 자료 1건을 찾는다."""
    query = question + " " + question
    # ① 질문을 2글자 조각으로 잘라 자료마다 점수를 매긴다. (힌트: app.py의 tokenize 함수)
    scores = retriever.vectorizer.get_scores(____(query))
    docs = retriever.invoke(query)

    for doc in docs:
        index = doc.metadata["index"]
        # ② 점수가 0보다 클 때만 자료로 인정한다.
        if scores[index] ____ 0:
            doc_id = doc.metadata["evidence"].split(".")[0]
            return doc_id, doc.metadata["evidence"], round(float(scores[index]), 2)
    return "-", "관련 자료가 검색되지 않았다.", 0.0


def make_chain():
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        base_url=BASE_URL, model=MODEL_NAME, api_key="EMPTY",
        max_tokens=400, temperature=0.2, seed=42, max_retries=0,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ])
    return prompt | llm | StrOutputParser()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", default=str(ROOT / "questions.csv"))
    parser.add_argument("--out", default=str(ROOT / "results.csv"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    retriever = make_retriever()
    questions = load_questions(args.questions)
    chain = None if args.dry_run else make_chain()

    rows = []
    # ③ 질문 목록을 하나씩 꺼내는 반복문을 완성하세요.
    for item in ____:
        question = item["질문"].strip()
        if not question:
            continue
        doc_id, evidence, score = find_evidence(retriever, question)

        if chain is None:
            answer = "(dry-run)"
        else:
            # ④ 튜링에게 보낼 값을 채우세요. (질문 변수 이름과 검색된 자료 변수 이름)
            answer = chain.invoke({
                "intro": "검증하러 온 학생이에요.",
                "history": [],
                "question": ____,
                "evidence": ____,
            }).strip()

        expected = item.get("예상자료", "").strip()
        rows.append({
            "번호": item.get("번호", ""),
            "질문": question,
            "예상자료": expected,
            "검색자료": doc_id,
            "자료적중": "○" if expected == doc_id else "×",
            "튜링의 답": answer,
            "판정": "",
        })
        print(question, "→", doc_id, answer)

    # ⑤ 결과를 CSV 파일로 저장하세요. (힌트: writer.writerows)
    with open(args.out, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.____(rows)

    print("저장 완료:", args.out)


if __name__ == "__main__":
    main()
