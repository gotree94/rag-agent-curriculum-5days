# Day 4. AI 에이전트와 LangGraph

> **산출물: 도구 사용 에이전트 + LangGraph Self-RAG 워크플로우**
> 하루 7시간 (오전 10:00~13:00 / 오후 14:00~18:00)

## 1. 학습 목표

- LLM과 에이전트의 차이를 설명하고, 에이전트 루프(관찰→사고→행동)를 이해한다.
- Function/Tool Calling과 ReAct 패턴을 구현한다.
- LangGraph의 State·Node·Edge·조건부 분기로 워크플로우를 구성한다.
- 메모리, Human-in-the-loop, Self-RAG(검색 후 재검색)를 구현한다.

## 2. 일과표 (7h)

### 오전 — 에이전트 개념과 도구 호출 (10:00~13:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 10:00~10:50 | 강의 4-1 | LLM vs 에이전트, 에이전트 구성요소(도구·메모리·계획) | 발표자료 |
| 10:50~11:00 | 휴식 | | |
| 11:00~11:40 | 강의 4-2 | Function / Tool Calling 원리, 도구 스키마 | 발표자료 |
| 11:40~12:20 | 실습 4-1 | **도구 호출 직접 구현 (날씨/계산기/문서검색)** | lab/01_tool_calling.py |
| 12:20~12:30 | 휴식 | | |
| 12:30~13:00 | 실습 4-2 | **ReAct 에이전트 (create_react_agent)** | lab/02_react_agent.py |

### 오후 — LangGraph (14:00~18:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 14:00~14:50 | 강의 4-3 | LangGraph 개론 (State/Node/Edge/조건부 분기) | lab/03_langgraph_basics.py |
| 14:50~15:30 | 실습 4-3 | **LangGraph로 에이전트 그래프 직접 구성** | lab/03_langgraph_basics.py |
| 15:30~15:40 | 휴식 | | |
| 15:40~16:20 | 실습 4-4 | **메모리(단기) — thread 단위 대화 유지** | lab/04_agent_memory.py |
| 16:20~17:00 | 실습 4-5 | **Human-in-the-loop (승인 후 실행)** | lab/05_human_in_the_loop.py |
| 17:00~17:10 | 휴식 | | |
| 17:10~17:50 | 실습 4-6 | **Self-RAG (검색 결과 평가 후 재검색)** | lab/06_self_rag.py |
| 17:50~18:00 | 정리 | 5일차 예고 (MCP, 멀티 에이전트) | |

## 3. 교수안 상세

### 4-1. LLM vs 에이전트 (50분)
- LLM: "말하는" 모델 (한 번의 응답)
- 에이전트: 목표를 위해 **도구를 스스로 선택·호출**하고 결과를 관찰해 반복
- 구성요소: **도구(Tools) · 메모리(Memory) · 계획(Planning) · 실행 루프**
- 예: "3월 급여명세서에서 실수령액 계산" → (문서검색 도구) → (계산 도구)

### 4-2. Tool Calling과 ReAct (40분)
- Tool Calling: LLM이 `{"name": 도구, "arguments": {...}}` 형태로 호출 요청
- 도구는 **이름·설명·파라미터 스키마**가 명확해야 잘 선택된다
- **ReAct = Reasoning + Acting**: Thought → Action(도구) → Observation 반복 → Final Answer
- 주의: 도구 남용/무한 루프 방지(최대 반복 제한), 호출 로그 남기기

### 4-3. LangGraph 개론 (50분)
- 그래프 = 노드(함수) + 엣지(흐름) + 상태(공유 데이터)
- `StateGraph(State)`: State는 TypedDict, 메시지는 `add_messages` 리듀서
- 조건부 엣지: `add_conditional_edges(노드, 라우팅함수, {...})`
- 컴파일 후 실행: `graph.invoke({...}, config)`
- 그래프 시각화: `graph.get_graph().draw_mermaid()`
- 왜 그래프인가: 복잡한 제어 흐름(분기/반복/재시도)을 명시적으로 표현

### 4-4~4-6. 메모리 · HITL · Self-RAG (실습 중심)
- **메모리**: `checkpointer`(MemorySaver) + `thread_id`로 대화 상태 유지
- **Human-in-the-loop**: `interrupt()`로 승인을 요청하고 `Command(resume=...)`로 재개
  → 결제/발송/삭제 등 위험한 도구 실행 전 승인
- **Self-RAG**: 검색 → 관련성 평가(LLM) → 부족하면 질의 재작성 후 재검색 → 답변
  → 4일차 오전~오후 학습 종합 실습

## 4. 실습 가이드

| 실습 | 파일 | 핵심 |
|---|---|---|
| 4-1 도구 호출 | `lab/01_tool_calling.py` | bind_tools + 수동 도구 실행 루프 |
| 4-2 ReAct | `lab/02_react_agent.py` | `create_react_agent` + 그래프 시각화 |
| 4-3 LangGraph | `lab/03_langgraph_basics.py` | StateGraph + ToolNode + 조건부 엣지 |
| 4-4 메모리 | `lab/04_agent_memory.py` | MemorySaver + thread_id |
| 4-5 HITL | `lab/05_human_in_the_loop.py` | interrupt / Command(resume) |
| 4-6 Self-RAG | `lab/06_self_rag.py` | 관련성 평가 + 재검색 루프 |

> 공용 도구 정의는 `lab/agent_tools.py`에 있습니다(시간, 계산기, 문서검색, 직원조회).

```bat
.venv\Scripts\activate
python day04-ai-agent-langgraph\lab\01_tool_calling.py
python day04-ai-agent-langgraph\lab\06_self_rag.py
```

## 5. 평가 체크리스트

- [ ] 도구 호출 요청(tool_calls)의 구조를 설명했다
- [ ] ReAct 에이전트가 도구를 선택하는 과정을 로그로 확인했다
- [ ] LangGraph에서 조건부 분기를 최소 1개 만들었다
- [ ] 같은 thread_id에서 이전 대화를 기억한다
- [ ] 승인이 있어야만 도구가 실행되는 흐름을 만들었다
- [ ] 검색이 부족할 때 재검색하는 Self-RAG 루프를 완성했다

## 6. 참고 자료

- LangGraph docs: https://langchain-ai.github.io/langgraph/
- ReAct 논문: "ReAct: Synergizing Reasoning and Acting in Language Models"
- Self-RAG: https://arxiv.org/abs/2310.11511