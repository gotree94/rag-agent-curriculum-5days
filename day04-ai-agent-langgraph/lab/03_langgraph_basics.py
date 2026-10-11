"""실습 4-3: LangGraph로 에이전트 그래프를 직접 구성

목표
- StateGraph / Node / Edge / 조건부 분기를 직접 작성한다.
- ToolNode + tools_condition으로 "에이전트 ↔ 도구" 반복 루프를 만든다.

그래프 구조:
    START → agent ──(도구 호출 있음)──> tools → agent
                 └─(도구 호출 없음, 최종 답변)──> END

실행
    .venv\\Scripts\\activate
    python day04-ai-agent-langgraph\\lab\\03_langgraph_basics.py
"""

import sys
from pathlib import Path
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from agent_tools import TOOLS  # noqa: E402
from common.llm import get_llm  # noqa: E402

from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.prebuilt import ToolNode, tools_condition  # noqa: E402


class AgentState(TypedDict):
    # add_messages: 새 메시지를 기존 리스트에 '병합'해주는 리듀서
    messages: Annotated[list, add_messages]


def build_graph():
    llm_with_tools = get_llm(temperature=0.0).bind_tools(TOOLS)

    def agent_node(state: AgentState):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "agent")
    # 조건부 분기: agent가 도구를 호출하면 "tools", 아니면 END
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    return builder.compile()


def main() -> None:
    graph = build_graph()
    print("=" * 74)
    print("[그래프 구조]")
    print("=" * 74)
    print(graph.get_graph().draw_mermaid())

    print("=" * 74)
    print("[실행]")
    print("=" * 74)
    result = graph.invoke(
        {"messages": [HumanMessage("표준 패키지 구축비 3000만원과 엔터프라이즈 7500만원의 차액을 계산해줘.")]}
    )
    for m in result["messages"]:
        if getattr(m, "tool_calls", None):
            for c in m.tool_calls:
                print(f"[도구 호출] {c['name']}({c['args']})")
        elif m.content:
            print(f"[{m.__class__.__name__}] {str(m.content)[:200]}")


if __name__ == "__main__":
    main()