"""실습 4-1: 도구 호출(Tool Calling) 직접 구현

목표
- LLM에 도구를 등록(bind_tools)하면 호출 요청(tool_calls)이 어떻게 오는지 확인한다.
- 요청을 해석해 실제 파이썬 도구를 실행하고, 결과를 다시 LLM에 전달하는 루프를 구현한다.

실행
    .venv\\Scripts\\activate
    python day04-ai-agent-langgraph\\lab\\01_tool_calling.py
"""

import json
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage, ToolMessage

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from agent_tools import TOOL_MAP, TOOLS  # noqa: E402
from common.llm import get_llm  # noqa: E402


def run_agent(question: str) -> None:
    llm = get_llm(temperature=0.0).bind_tools(TOOLS)
    messages = [HumanMessage(question)]

    print(f"\n질문: {question}")
    for step in range(1, 6):
        ai = llm.invoke(messages)
        messages.append(ai)

        if not ai.tool_calls:
            print(f"\n[최종 답변]\n{ai.content}")
            return

        for call in ai.tool_calls:
            tool_fn = TOOL_MAP[call["name"]]
            print(f"  [{step}] 도구 호출: {call['name']}({json.dumps(call['args'], ensure_ascii=False)})")
            result = tool_fn.invoke(call["args"])
            print(f"       관찰 결과: {str(result)[:100]}")
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    print("[경고] 최대 반복 횟수를 초과했습니다.")


def main() -> None:
    questions = [
        "지금 몇 시인지 알려줘.",
        "연차가 15일 발생하는 시점이 언제인지 문서에서 찾아줘.",
        "김민준 담당자의 부서와 연락처를 알려줘.",
        "엔터프라이즈 패키지 구축비 7500만원에 부가세 10%를 더하면 얼마야? 계산해줘.",
    ]
    for q in questions:
        print("=" * 74)
        run_agent(q)


if __name__ == "__main__":
    main()