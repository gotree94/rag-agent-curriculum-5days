"""실습 5-3: LangGraph 에이전트 + MCP 도구 연결

목표
- langchain-mcp-adapters(load_mcp_tools)로 MCP 서버의 도구를 LangChain 도구로 변환한다.
- 변환된 도구를 create_react_agent에 전달해 자연어로 MCP 도구를 사용한다.

실행
    .venv\\Scripts\\activate
    python day05-mcp-multiagent-project\\lab\\03_langgraph_mcp_agent.py
"""

import asyncio
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import get_llm  # noqa: E402

SERVER = Path(__file__).with_name("01_mcp_company_server.py")


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # MCP 도구 → LangChain 도구로 자동 변환
            tools = await load_mcp_tools(session)
            print("변환된 도구:", [t.name for t in tools])

            agent = create_react_agent(get_llm(temperature=0.0), tools)

            question = "김민준 담당자의 부서와 연락처를 알려주고, 복지포인트 규정도 찾아줘."
            print("\n질문:", question)
            result = await agent.ainvoke({"messages": [HumanMessage(question)]})

            for m in result["messages"]:
                if getattr(m, "tool_calls", None):
                    for c in m.tool_calls:
                        print(f"[MCP 도구 호출] {c['name']}({c['args']})")
            print("\n[최종 답변]")
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())