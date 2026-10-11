"""실습 5-4: 멀티 에이전트 (Supervisor 패턴)

구조
    START → supervisor ──(rag_worker)──> rag_worker ─┐
                      ├─(tool_worker)─> tool_worker ─┤→ supervisor (반복)
                      ├─(policy_worker)> policy_worker┤
                      └─(FINISH)──────> END

- supervisor: 사용자 요청을 보고 담당 전문가를 선택(라우팅)
- rag_worker: 사내 문서를 검색해 근거 기반으로 답변
- tool_worker: 계산/시간 등 도구를 사용해 답변
- policy_worker: 규정/정책 키워드를 검색해 요약

실행
    .venv\\Scripts\\activate
    python day05-mcp-multiagent-project\\lab\\04_supervisor_agent.py
"""

import re
import sys
from pathlib import Path
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR, get_llm  # noqa: E402

from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402

MEMBERS = ["rag_worker", "tool_worker", "policy_worker"]


# ----------------------------------------------------------------------
# 도구 정의 (tool_worker용)
# ----------------------------------------------------------------------
@tool
def calculator(expression: str) -> str:
    """사칙연산 수식을 계산합니다. 예: '(7500*1.1)'"""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "오류: 허용되지 않은 문자"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception as e:  # noqa: BLE001
        return f"계산 오류: {e}"


@tool
def get_current_time() -> str:
    """현재 날짜와 시간을 반환합니다."""
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


TOOL_MAP = {t.name: t for t in [calculator, get_current_time]}


# ----------------------------------------------------------------------
# 사내 문서 검색용 간이 BM25
# ----------------------------------------------------------------------
def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[0-9a-zA-Z가-힣]+", text.lower())
    toks = list(words)
    for w in words:
        if len(w) >= 2 and re.search(r"[가-힣]", w):
            toks += [w[i:i + 2] for i in range(len(w) - 1)]
    return toks


def _build_corpus() -> list[tuple[str, str]]:
    """(source, 문장) 리스트 구성."""
    corpus = []
    for md in sorted(SAMPLE_DATA_DIR.glob("*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if len(line) >= 8:
                corpus.append((md.name, line))
    return corpus


CORPUS = _build_corpus()
from rank_bm25 import BM25Okapi  # noqa: E402

BM25 = BM25Okapi([_tokenize(s) for _, s in CORPUS])


def bm25_search(query: str, k: int = 4) -> list[tuple[str, str]]:
    scores = BM25.get_scores(_tokenize(query))
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [CORPUS[i] for i in order]


# ----------------------------------------------------------------------
# 그래프 상태
# ----------------------------------------------------------------------
class TeamState(TypedDict):
    messages: Annotated[list, add_messages]
    next: str


class Route(BaseModel):
    next: Literal["rag_worker", "tool_worker", "policy_worker", "FINISH"]


SUPERVISOR_PROMPT = (
    "당신은 사내 AI 지원팀의 관리자(Supervisor)입니다. "
    "아래 전문가 중 다음 작업을 수행할 한 명을 고르세요.\n"
    "- rag_worker: 사내 문서 지식을 검색해 답하는 담당\n"
    "- tool_worker: 계산·시간 등 도구가 필요한 담당\n"
    "- policy_worker: 규정/정책 키워드 검색·요약 담당\n"
    "- FINISH: 이미 충분히 답변되었고 최종 답을 낼 때\n"
    "요청이 해결되지 않았다면 반드시 전문가를 한 명 이상 선택하세요."
)


def _last_human(messages) -> str:
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            return m.content
    return ""


def supervisor_node(state: TeamState) -> TeamState:
    router = get_llm(temperature=0.0).with_structured_output(Route)
    messages = [SystemMessage(SUPERVISOR_PROMPT)] + [
        m for m in state["messages"] if isinstance(m, (HumanMessage, AIMessage))
    ]
    decision = router.invoke(messages)

    # 아직 아무 전문가도 답하지 않았는데 FINISH면 rag_worker 강제
    has_worker_reply = any(
        isinstance(m, AIMessage) and str(m.content).startswith("[") for m in state["messages"]
    )
    nxt = decision.next
    if nxt == "FINISH" and not has_worker_reply:
        nxt = "rag_worker"
    print(f"  [supervisor] → {nxt}")
    return {"next": nxt}


def rag_worker_node(state: TeamState) -> TeamState:
    q = _last_human(state["messages"])
    hits = bm25_search(q)
    context = "\n".join(f"[{src}] {text}" for src, text in hits)
    answer = get_llm(temperature=0.0).invoke(
        f"사내 문서만 근거로 질문에 답하고 (출처: 파일명)을 표시하세요.\n\n"
        f"[문서]\n{context}\n\n[질문]\n{q}"
    ).content
    return {"messages": [AIMessage(content=f"[RAG 전문가] {answer}")]}


def policy_worker_node(state: TeamState) -> TeamState:
    q = _last_human(state["messages"])
    hits = bm25_search(q)
    context = "\n".join(f"[{src}] {text}" for src, text in hits)
    answer = get_llm(temperature=0.0).invoke(
        f"다음 규정 조항을 이용해 질문에 간결히 답하세요. 출처를 표시하세요.\n\n"
        f"[조항]\n{context}\n\n[질문]\n{q}"
    ).content
    return {"messages": [AIMessage(content=f"[정책 전문가] {answer}")]}


def tool_worker_node(state: TeamState) -> TeamState:
    q = _last_human(state["messages"])
    llm = get_llm(temperature=0.0).bind_tools(list(TOOL_MAP.values()))
    messages = [HumanMessage(q)]
    for _ in range(4):
        ai = llm.invoke(messages)
        messages.append(ai)
        if not ai.tool_calls:
            break
        for c in ai.tool_calls:
            result = TOOL_MAP[c["name"]].invoke(c["args"])
            print(f"  [tool_worker] {c['name']}({c['args']}) → {result}")
            messages.append(ToolMessage(content=str(result), tool_call_id=c["id"]))
    final = messages[-1].content if hasattr(messages[-1], "content") else "도구 실행을 완료했습니다."
    return {"messages": [AIMessage(content=f"[도구 전문가] {final}")]}


def build_graph():
    builder = StateGraph(TeamState)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("rag_worker", rag_worker_node)
    builder.add_node("tool_worker", tool_worker_node)
    builder.add_node("policy_worker", policy_worker_node)

    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        lambda state: state["next"],
        {"rag_worker": "rag_worker", "tool_worker": "tool_worker",
         "policy_worker": "policy_worker", "FINISH": END},
    )
    for worker in MEMBERS:
        builder.add_edge(worker, "supervisor")
    return builder.compile()


def main() -> None:
    graph = build_graph()
    print("=" * 74)
    print("[멀티 에이전트 그래프]")
    print("=" * 74)
    print(graph.get_graph().draw_mermaid())

    questions = [
        "복지포인트 규정을 찾아줘.",
        "엔터프라이즈 패키지 구축비 7500만원에 부가세 10% 더하면 얼마야?",
    ]
    for q in questions:
        print("\n" + "=" * 74)
        print(f"사용자: {q}")
        print("-" * 74)
        result = graph.invoke({"messages": [HumanMessage(q)], "next": ""})
        print("\n[최종 답변]")
        print(result["messages"][-1].content)


if __name__ == "__main__":
    main()