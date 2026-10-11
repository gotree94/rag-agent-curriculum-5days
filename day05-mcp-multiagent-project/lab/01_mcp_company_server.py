"""실습 5-1: 사내 문서/직원 조회 MCP 서버 (FastMCP)

MCP 서버는 클라이언트(에이전트)가 자식 프로세스로 실행한다(stdio 전송).
단독 실행하지 말 것. 필요 시 확인용으로:

    python day05-mcp-multiagent-project\\lab\\01_mcp_company_server.py
    (표준입출력으로 프로토콜을 기다리며 대기 — Ctrl+C로 종료)
"""

import csv
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SAMPLE_DIR = Path(__file__).resolve().parents[2] / "00-environment" / "sample-data"

mcp = FastMCP("futuretech-tools")


@mcp.tool()
def list_policy_documents() -> str:
    """조회 가능한 사내 문서 목록을 반환합니다."""
    files = sorted(p.name for p in SAMPLE_DIR.glob("*.md"))
    return "사용 가능한 문서: " + ", ".join(files)


@mcp.tool()
def read_policy(filename: str) -> str:
    """문서 파일명을 받아 전체 내용을 반환합니다. 예: 'company-policy.md'"""
    path = SAMPLE_DIR / filename
    if not path.exists():
        return f"'{filename}' 문서를 찾을 수 없습니다. {list_policy_documents()}"
    return path.read_text(encoding="utf-8")


@mcp.tool()
def search_policies(keyword: str) -> str:
    """사내 문서에서 키워드가 포함된 문장·조항을 검색합니다."""
    keyword = keyword.strip()
    hits: list[str] = []
    for md in sorted(SAMPLE_DIR.glob("*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            if keyword and keyword in line:
                hits.append(f"[{md.name}] {line.strip()}")
    if not hits:
        return f"'{keyword}' 관련 내용을 문서에서 찾지 못했습니다."
    return "\n".join(hits[:8])


@mcp.tool()
def search_employees(keyword: str) -> str:
    """이름/부서/직함으로 직원 정보를 검색합니다. 예: '김민준' 또는 'R&D'"""
    keyword = keyword.strip()
    rows = []
    with (SAMPLE_DIR / "employees.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if keyword in " ".join(row.values()):
                rows.append(
                    f"{row['name']} | {row['department']} | {row['title']} | "
                    f"{row['email']} | {row['phone']}"
                )
    if not rows:
        return f"'{keyword}' 직원을 찾지 못했습니다."
    return "\n".join(rows)


if __name__ == "__main__":
    mcp.run()
