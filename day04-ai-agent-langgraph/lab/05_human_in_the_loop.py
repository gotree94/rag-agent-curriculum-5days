"""실습 4-5: Human-in-the-loop — 승인 후에만 위험한 도구 실행

목표
- interrupt()로 사람의 승인을 요청하고 그래프를 일시 정지시킨다.
- Command(resume=...)로 승인/거절 결과를 받아 실행 여부를 결정한다.

시나리오: 환불(송금) 요청 → 담당자 승인 → 승인 시에만 실행

실행
    .venv\\Scripts\\activate
    python day04-ai-agent-langgraph\\lab\\05_human_in_the_loop.py
"""

import sys
from pathlib import Path
from typing import TypedDict

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import get_llm  # noqa: E402

from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.types import Command, interrupt  # noqa: E402


class State(TypedDict):
    request: str
    amount: int
    decision: str
    result: str


def plan(state: State) -> State:
    """환불 요청을 해석해 실행 계획을 세운다."""
    print(f"  [plan] 요청 분석: {state['request']}")
    return {"amount": 120000}


def human_review(state: State) -> State:
    """사람에게 승인을 요청한다. interrupt가 호출되면 그래프는 여기서 일시정지된다."""
    decision = interrupt(
        {
            "질문": f"{state['amount']:,}원 환불을 승인하시겠습니까?",
            "요청": state["request"],
        }
    )
    print(f"  [human_review] 승인 결과: {decision}")
    return {"decision": decision}


def execute(state: State) -> State:
    """승인된 경우에만 실행."""
    if state.get("decision") == "approve":
        return {"result": f"{state['amount']:,}원 환불을 실행했습니다."}
    return {"result": "승인이 거절되어 환불을 실행하지 않았습니다."}


def build_graph():
    builder = StateGraph(State)
    builder.add_node("plan", plan)
    builder.add_node("human_review", human_review)
    builder.add_node("execute", execute)
    builder.add_edge(START, "plan")
    builder.add_edge("plan", "human_review")
    builder.add_edge("human_review", "execute")
    builder.add_edge("execute", END)
    return builder.compile(checkpointer=MemorySaver())


def main() -> None:
    graph = build_graph()
    config = {"configurable": {"thread_id": "refund-1"}}

    print("=" * 74)
    print("[1단계] 환불 요청 실행 → human_review 에서 중단")
    print("=" * 74)
    try:
        graph.invoke({"request": "고객 요청으로 환불 처리해줘", "amount": 0, "decision": "", "result": ""}, config)
    except Exception as e:  # GraphInterrupt
        print(f"  >> 그래프가 일시정지되었습니다 ({type(e).__name__})")

    # 중단 상태에서 사람이 승인
    decision = input("\n승인하시겠습니까? (approve/deny): ").strip() or "approve"

    print("=" * 74)
    print("[2단계] 승인 결과를 주입해 재개")
    print("=" * 74)
    final = graph.invoke(Command(resume=decision), config)
    print(f"\n[최종 결과] {final['result']}")


if __name__ == "__main__":
    main()