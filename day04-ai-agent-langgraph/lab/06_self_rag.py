"""실습 4-6: Self-RAG — 검색 결과를 스스로 평가하고 부족하면 재검색

워크플로우:
    START → retrieve → grade ──(충분)──> generate → END
                          └─(부족 & 재시도 여유)──> rewrite → retrieve
                          └─(부족 & 재시도 소진)──> generate

실행
    .venv\\Scripts\\activate
    python day04-ai-agent-langgraph\\lab\\06_self_rag.py
"""

import sys
from pathlib import Path
from typing import TypedDict

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR, get_embeddings, get_llm  # noqa: E402

from langchain_community.document_loaders import TextLoader  # noqa: E402
from langchain_text_splitters import RecursiveCharacterTextSplitter  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402

MAX_ATTEMPTS = 2


def build_retriever():
    from langchain_community.vectorstores import FAISS

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    docs = []
    for md in sorted(SAMPLE_DATA_DIR.glob("*.md")):
        loaded = TextLoader(str(md), encoding="utf-8").load()
        for d in loaded:
            d.metadata["source"] = md.name
        docs.extend(loaded)
    store = FAISS.from_documents(splitter.split_documents(docs), get_embeddings())
    return store.as_retriever(search_kwargs={"k": 3})


RETRIEVER = build_retriever()


class State(TypedDict):
    question: str       # 현재 (재작성된) 검색 질의
    original: str       # 최초 질문
    docs: list[str]
    relevant: bool
    attempts: int
    answer: str


def retrieve(state: State) -> State:
    docs = RETRIEVER.invoke(state["question"])
    print(f"  [retrieve] '{state['question']}' → {len(docs)}건 검색")
    return {"docs": [d.page_content for d in docs], "attempts": state.get("attempts", 0) + 1}


def grade(state: State) -> State:
    """검색된 문맥이 질문에 답하기에 충분한지 LLM이 평가한다."""
    context = "\n\n".join(state["docs"])[:2000]
    verdict = get_llm(temperature=0.0).invoke(
        f"질문: {state['original']}\n\n문맥:\n{context}\n\n"
        "위 문맥만으로 질문에 답할 수 있으면 'YES', 부족하면 'NO' 라고만 답하세요."
    ).content.strip()
    relevant = "YES" in verdict.upper()
    print(f"  [grade] 문맥 충분? {relevant} (시도 {state['attempts']}회)")
    return {"relevant": relevant}


def rewrite(state: State) -> State:
    new_q = get_llm(temperature=0.0).invoke(
        f"다음 질문을 문서 검색이 더 잘 되도록 핵심 키워드 중심으로 바꿔 한 줄로만 출력하세요:\n{state['original']}"
    ).content.strip()
    print(f"  [rewrite] '{state['original']}' → '{new_q}'")
    return {"question": new_q}


def generate(state: State) -> State:
    context = "\n\n".join(state["docs"])
    answer = get_llm(temperature=0.0).invoke(
        f"문맥만 근거로 질문에 답하세요. 없으면 '문서에서 찾을 수 없습니다'.\n\n"
        f"[문맥]\n{context}\n\n[질문]\n{state['original']}"
    ).content
    return {"answer": answer}


def route_after_grade(state: State) -> str:
    if state["relevant"]:
        return "generate"
    if state["attempts"] >= MAX_ATTEMPTS:
        print("  [route] 재시도 소진 → 최선의 답변 생성")
        return "generate"
    return "rewrite"


def build_graph():
    builder = StateGraph(State)
    builder.add_node("retrieve", retrieve)
    builder.add_node("grade", grade)
    builder.add_node("rewrite", rewrite)
    builder.add_node("generate", generate)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "grade")
    builder.add_conditional_edges(
        "grade", route_after_grade, {"generate": "generate", "rewrite": "rewrite"}
    )
    builder.add_edge("rewrite", "retrieve")
    builder.add_edge("generate", END)
    return builder.compile()


def main() -> None:
    graph = build_graph()
    print("=" * 74)
    print("[그래프 구조]")
    print("=" * 74)
    print(graph.get_graph().draw_mermaid())

    question = "복지포인트랑 건강검진 지원 내용을 알려줘."  # 두 주제가 섞인 질문
    print("\n" + "=" * 74)
    print(f"질문: {question}")
    print("=" * 74)
    result = graph.invoke(
        {"question": question, "original": question, "docs": [], "relevant": False, "attempts": 0, "answer": ""}
    )
    print(f"\n[최종 답변]\n{result['answer']}")


if __name__ == "__main__":
    main()