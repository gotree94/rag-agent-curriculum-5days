"""4일차 공용 도구(Tool) 정의.

- get_current_time : 현재 시각
- calculator       : 사칙연산 계산
- search_policy    : 사내 문서 키워드 검색
- get_employee_info: 직원 정보 조회

langchain_core의 @tool 데코레이터를 사용하면 이름·설명·파라미터 스키마가
자동 생성되어 LLM이 도구를 선택(tool calling)할 수 있다.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path

from langchain_core.tools import tool

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR


@tool
def get_current_time() -> str:
    """현재 날짜와 시간을 'YYYY-MM-DD HH:MM:SS' 형식으로 반환합니다."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculator(expression: str) -> str:
    """사칙연산 수식을 계산합니다. 예: '(3000*1.1)+500'"""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "오류: 허용되지 않은 문자가 포함되어 있습니다."
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))  # noqa: S307
    except Exception as e:  # noqa: BLE001
        return f"계산 오류: {e}"


@tool
def search_policy(keyword: str) -> str:
    """사내 문서(sample-data)에서 특정 키워드와 관련된 문장을 검색합니다."""
    keyword = keyword.strip()
    hits: list[str] = []
    for md in sorted(SAMPLE_DATA_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        for line in text.splitlines():
            if keyword and keyword in line:
                hits.append(f"[{md.name}] {line.strip()}")
    if not hits:
        return f"'{keyword}' 관련 내용을 문서에서 찾지 못했습니다."
    return "\n".join(hits[:5])


@tool
def get_employee_info(name: str) -> str:
    """직원 이름으로 부서·직함·이메일·연락처를 조회합니다."""
    path = SAMPLE_DATA_DIR / "employees.csv"
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if name in row["name"] or row["name"] in name:
                return (
                    f"{row['name']} / {row['department']} / {row['title']} / "
                    f"{row['email']} / {row['phone']}"
                )
    return f"'{name}' 직원을 찾지 못했습니다."


TOOLS = [get_current_time, calculator, search_policy, get_employee_info]
TOOL_MAP = {t.name: t for t in TOOLS}


if __name__ == "__main__":
    # 도구 단독 테스트
    print(get_current_time.invoke({}))
    print(calculator.invoke({"expression": "(3000*1.1)+500"}))
    print(search_policy.invoke({"keyword": "연차"}))
    print(get_employee_info.invoke({"name": "김민준"}))