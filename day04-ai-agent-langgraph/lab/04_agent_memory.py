"""실습 4-4: 메모리(단기) — thread_id 단위로 대화를 기억하는 에이전트

목표
- checkpointer(MemorySaver)로 그래프 상태를 저장해 여러 턴의 대화를 이어간다.
- thread_id가 다르면 대화가 분리됨을 확인한다.

실행
    .venv\\Scripts\\activate
    python day04-ai-agent-langgraph\\lab\\04_agent_memory.py
"""

import sys
from pathlib import Path
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from agent_tools import TOOLS  # noqa: E402
from common.llm import get_llm  # noqa: E402

from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from langgraph.graph import START, StateGraph  # noqa: E402
from langgraph.graph.message import add_messages  # noqa: E402
from langgraph.prebuilt import ToolNode, tools_condition  # noqa: E402


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph():
    llm_with_tools = get_llm(temperature=0.0).bind_tools(TOOLS)

    def agent_node(state: AgentState):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    builder = StateGraph(AgentState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    # ★ checkpointer를 붙여야 상태(대화 이력)가 thread별로 저장된다
    return builder.compile(checkpointer=MemorySaver())


def chat(graph, thread_id: str, text: str) -> None:
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke({"messages": [HumanMessage(text)]}, config)
    answer = result["messages"][-1].content
    print(f"[thread={thread_id}] 나: {text}")
    print(f"                AI: {str(answer)[:180]}\n")


def main() -> None:
    graph = build_graph()

    print("=" * 74)
    print("[thread A] 대화 이어가기 — 2번째 질문에 '그'가 무엇인지 기억해야 함")
    print("=" * 74)
    chat(graph, "thread-A", "우리 회사 연차 규정 알려줘.")
    chat(graph, "thread-A", "그 규정을 개정하려면 어떻게 해야 해?")  # 앞 문맥 참조

    print("=" * 74)
    print("[thread B] 별도 스레드는 앞 대화를 기억하지 못함")
    print("=" * 74)
    chat(graph, "thread-B", "그 규정을 개정하려면 어떻게 해야 해?")


if __name__ == "__main__":
    main()