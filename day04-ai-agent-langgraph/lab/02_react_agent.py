"""실습 4-2: ReAct 에이전트 (langgraph.prebuilt.create_react_agent)

목표
- 도구 호출 루프를 직접 짠 대신, LangGraph의 create_react_agent로 동일한 에이전트를 구성한다.
- 에이전트의 그래프 구조를 Mermaid로 확인하고, 실행 트레이스를 관찰한다.

실행
    .venv\\Scripts\\activate
    python day04-ai-agent-langgraph\\lab\\02_react_agent.py
"""

import sys
from pathlib import Path

from langchain_core.messages import HumanMessage

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from agent_tools import TOOLS  # noqa: E402
from common.llm import get_llm  # noqa: E402


def main() -> None:
    from langgraph.prebuilt import create_react_agent

    agent = create_react_agent(get_llm(temperature=0.0), TOOLS)

    print("=" * 74)
    print("[에이전트 그래프 구조 (Mermaid)]")
    print("=" * 74)
    print(agent.get_graph().draw_mermaid())

    print("=" * 74)
    print("[실행 트레이스]")
    print("=" * 74)
    result = agent.invoke(
        {"messages": [HumanMessage("연차 발생 시점을 찾아서, 15일이 되는 날부터 남은 날도 계산해줘.")]}
    )
    for m in result["messages"]:
        role = m.__class__.__name__
        if getattr(m, "tool_calls", None):
            for c in m.tool_calls:
                print(f"[{role}] → 도구 호출: {c['name']}({c['args']})")
        elif m.content:
            print(f"[{role}] {str(m.content)[:200]}")


if __name__ == "__main__":
    main()