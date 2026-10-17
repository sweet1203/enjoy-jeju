"""튜링 페르소나 자동 검증 프로그램 (선택 심화 3단계 · 완성본)

questions.csv에 적은 검증 질문을 차례로 튜링에게 보내고,
검색된 자료와 답을 results.csv로 저장한다.

실행 방법 (persona-core 폴더에 app.py, data.json과 함께 둔다)
    python persona-core/eval.py                 # 모델 서버에 질문하고 결과 저장
    python persona-core/eval.py --dry-run       # 모델 없이 '어떤 자료가 검색되는지'만 확인
    python persona-core/eval.py --out after.csv # 수정 후 결과를 다른 이름으로 저장
"""

import argparse
import csv
from pathlib import Path

from app import SYSTEM_PROMPT, BASE_URL, MODEL_NAME, make_retriever, tokenize

ROOT = Path(__file__).resolve().parent


def load_questions(path):
    """questions.csv를 읽어 사전(dict)의 목록으로 돌려준다."""
    with open(path, encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def find_evidence(retriever, question):
    """app.py의 chat()과 같은 규칙으로 자료 1건을 찾는다.

    검증은 질문마다 새 대화로 보므로 '직전 질문'은 비워 둔다.
    """
    query = question + " " + question
    scores = retriever.vectorizer.get_scores(tokenize(query))
    docs = retriever.invoke(query)

    for doc in docs:
        index = doc.metadata["index"]
        if scores[index] > 0:
            doc_id = doc.metadata["evidence"].split(".")[0]
            return doc_id, doc.metadata["evidence"], round(float(scores[index]), 2)
    return "-", "관련 자료가 검색되지 않았다.", 0.0


def make_chain():
    """app.py의 main()과 같은 방법으로 '프롬프트 → 모델 → 문자열' 체인을 만든다."""
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        base_url=BASE_URL,
        model=MODEL_NAME,
        api_key="EMPTY",
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
    return prompt | llm | StrOutputParser()


def main():
    parser = argparse.ArgumentParser(description="튜링 페르소나 자동 검증")
    parser.add_argument("--questions", default=str(ROOT / "questions.csv"))
    parser.add_argument("--out", default=str(ROOT / "results.csv"))
    parser.add_argument("--dry-run", action="store_true", help="모델을 부르지 않고 검색 결과만 확인")
    args = parser.parse_args()

    retriever = make_retriever()
    questions = load_questions(args.questions)
    chain = None if args.dry_run else make_chain()
    intro = "저는 튜링 선생님의 답을 확인하러 온 학생이에요."

    rows = []
    hit = 0
    for item in questions:
        question = item["질문"].strip()
        if not question:
            continue
        doc_id, evidence, score = find_evidence(retriever, question)

        if chain is None:
            answer = "(dry-run: 모델을 부르지 않음)"
        else:
            # 서버는 한 번에 한 질문만 처리하므로, 반복문이 차례로 하나씩 보낸다.
            answer = chain.invoke({
                "intro": intro,
                "history": [],
                "question": question,
                "evidence": evidence,
            }).strip()

        expected = item.get("예상자료", "").strip()
        match = "○" if expected and expected == doc_id else ("×" if expected else "")
        if match == "○":
            hit += 1

        rows.append({
            "번호": item.get("번호", ""),
            "유형": item.get("유형", ""),
            "질문": question,
            "예상자료": expected,
            "검색자료": doc_id,
            "검색점수": score,
            "자료적중": match,
            "튜링의 답": answer,
            "판정": "",  # 정확 / 사실 오류 / 지어낸 답 / 어색한 말투 — 사람이 직접 적는다
        })
        print(f"[{len(rows):2}] {question} → {doc_id} ({score})")
        if chain is not None:
            print(f"     튜링: {answer}")

    with open(args.out, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    checked = sum(1 for r in rows if r["예상자료"])
    print(f"\n질문 {len(rows)}개 · 예상 자료 적중 {hit}/{checked} · 결과 파일: {args.out}")
    print("results.csv를 열어 '판정' 칸을 채우고, 수정 전과 후를 비교해 보세요.")


if __name__ == "__main__":
    main()
