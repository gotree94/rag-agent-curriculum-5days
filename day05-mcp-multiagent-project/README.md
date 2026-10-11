# Day 5. MCP · 멀티 에이전트 · 최종 프로젝트

> **산출물: 사내 조회용 MCP 서버 + 멀티 에이전트 + 팀별 "사내 업무 지원 AI 어시스턴트"**
> 하루 7시간 (오전 10:00~13:00 / 오후 14:00~18:00)

## 1. 학습 목표

- MCP(Model Context Protocol)의 구조(호스트/클라이언트/서버)와 도구 표준화 의의를 이해한다.
- FastMCP로 사내 파일/DB 조회용 MCP 서버를 만들고 표준 클라이언트로 호출한다.
- LangGraph 에이전트에 MCP 도구를 연결한다.
- Supervisor 패턴으로 여러 전문 에이전트(멀티 에이전트)를 협업시킨다.
- 팀별 "사내 업무 지원 AI 어시스턴트"를 완성하고 발표한다.

## 2. 일과표 (7h)

### 오전 — MCP (10:00~13:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 10:00~10:50 | 강의 5-1 | MCP 개론 (등장 배경, 구조, 도구/리소스/프롬프트) | 발표자료 |
| 10:50~11:00 | 휴식 | | |
| 11:00~11:50 | 강의 5-2 + 실습 5-1 | **MCP 서버 제작 (사내 문서/직원 조회)** | lab/01_mcp_company_server.py |
| 11:50~12:00 | 휴식 | | |
| 12:00~12:40 | 실습 5-2 | **MCP 클라이언트로 도구 목록/호출** | lab/02_mcp_client.py |
| 12:40~13:00 | 실습 5-3 | **LangGraph + MCP 에이전트 연결** | lab/03_langgraph_mcp_agent.py |

### 오후 — 멀티 에이전트 + 최종 프로젝트 (14:00~18:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 14:00~14:40 | 강의 5-3 | 멀티 에이전트 설계 (Supervisor 패턴, 역할 분담) | 발표자료 |
| 14:40~15:20 | 실습 5-4 | **Supervisor 멀티 에이전트 구현** | lab/04_supervisor_agent.py |
| 15:20~15:30 | 휴식 + 프로젝트 팀 구성/주제 확정 | project-guide.md | |
| 15:30~17:00 | 프로젝트 개발 1 | 팀별 "사내 업무 지원 AI 어시스턴트" (1.5h) | |
| 17:00~17:10 | 휴식 | | |
| 17:10~17:50 | 프로젝트 개발 2 + 발표 준비 | 완성 및 발표 자료(데모 시나리오) 정리 (0.7h) | |
| 17:50~18:00 | 발표·리뷰·수료 | 팀별 데모, 상호 피드백, 정리 | |

## 3. 교수안 상세

### 5-1. MCP 개론 (50분)
- **문제**: 도구마다 연동 방식이 제각각 → 재사용·교체가 어렵다
- **MCP**: "AI 앱과 외부 도구/데이터를 연결하는 표준 프로토콜" (USB-C 비유)
- 구성: **호스트(AI 앱) · 클라이언트(연결 관리) · 서버(도구 제공)**
- 제공 요소: **Tools(실행) · Resources(데이터 열람) · Prompts(템플릿)**
- 전송: stdio(로컬), HTTP/SSE(원격)

### 5-2. MCP 서버 제작 + 연동 (실습 중심)
- FastMCP로 `@mcp.tool()` 데코레이터 한 줄로 도구 노출
- 사내 문서 검색, 직원 조회 등 실제 업무 도구를 만든다
- 표준 클라이언트로 `list_tools` / `call_tool` (프로토콜 확인)
- `langchain-mcp-adapters`로 MCP 도구를 LangChain 에이전트에 자동 변환

### 5-3. 멀티 에이전트 · Supervisor 패턴 (40분)
- 단일 에이전트 한계: 도구가 많아지면 혼선(컨텍스트/선택 오류)
- **Supervisor 패턴**: 관리자 에이전트가 요청을 보고 적합한 전문가에게 라우팅
- 구성 예(본 과정): `RAG 전문가`, `도구(계산/조회) 전문가`, `정책 검색 전문가`
- 각 전문가의 응답을 종합해 최종 답변 → 역할 분담으로 정확도·유지보수성 향상

## 4. 실습 가이드

| 실습 | 파일 | 핵심 |
|---|---|---|
| 5-1 MCP 서버 | `lab/01_mcp_company_server.py` | FastMCP 도구 3종(문서/직원/규정) |
| 5-2 MCP 클라이언트 | `lab/02_mcp_client.py` | 도구 목록 조회 + 호출 |
| 5-3 LangGraph+MCP | `lab/03_langgraph_mcp_agent.py` | `load_mcp_tools` → ReAct 에이전트 |
| 5-4 Supervisor | `lab/04_supervisor_agent.py` | 관리자 + 전문가 3명 라우팅 |
| 프로젝트 | `project-guide.md` | 주제·요구사항·평가 루브릭 |

MCP 서버는 **단독 실행하지 않고** 클라이언트가 자식 프로세스로 띄운다(stdio).
수동 확인용:
```bat
.venv\Scripts\activate
python day05-mcp-multiagent-project\lab\02_mcp_client.py
python day05-mcp-multiagent-project\lab\03_langgraph_mcp_agent.py
python day05-mcp-multiagent-project\lab\04_supervisor_agent.py
```

## 5. 최종 프로젝트 (약 2.5h + 발표 0.7h)

자세한 내용은 **[project-guide.md](project-guide.md)** 참고.

- 팀: 2~4인, 주제는 사내 업무 중 하나를 선택
- 필수 요소: (1) RAG (2) 도구/에이전트 (3) 출처 표시 (4) 간단한 UI 또는 CLI
- 발표: 문제 → 데모 → 아키텍처 → 개선점/회고 (팀당 5~7분)

## 6. 평가 체크리스트 (최종)

- [ ] MCP 서버가 도구를 표준 방식으로 제공한다
- [ ] 에이전트가 MCP 도구를 호출해 답한다
- [ ] Supervisor가 요청에 따라 전문가를 바꿔 라우팅한다
- [ ] 최종 프로젝트가 RAG+도구+출처 표시를 포함한다
- [ ] 발표에서 아키텍처와 개선점을 설명했다

## 7. 참고 자료

- MCP 공식: https://modelcontextprotocol.io
- Python MCP SDK: https://github.com/modelcontextprotocol/python-sdk
- LangChain MCP Adapters: https://github.com/langchain-ai/langchain-mcp-adapters