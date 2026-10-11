"""실습 5-2: MCP 클라이언트 — 서버 도구 목록 조회 및 호출

목표
- stdio 전송으로 MCP 서버를 자식 프로세스로 실행한다.
- ClientSession으로 초기화(handshake)하고 도구 목록·호출 결과를 확인한다.

실행
    .venv\\Scripts\\activate
    python day05-mcp-multiagent-project\\lab\\02_mcp_client.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).with_name("01_mcp_company_server.py")


async def main() -> None:
    # 서버를 현재 파이썬 인터프리터로 실행 (stdio)
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()  # handshake

            print("=" * 74)
            print("[1] 서버가 제공하는 도구 목록")
            print("=" * 74)
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"  - {t.name}: {t.description}")

            print("\n" + "=" * 74)
            print("[2] 도구 호출: search_employees('김민준')")
            print("=" * 74)
            res = await session.call_tool("search_employees", {"keyword": "김민준"})
            print(res.content[0].text)

            print("\n" + "=" * 74)
            print("[3] 도구 호출: search_policies('복지포인트')")
            print("=" * 74)
            res = await session.call_tool("search_policies", {"keyword": "복지포인트"})
            print(res.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())