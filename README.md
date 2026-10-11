# RAG 기반 AI 에이전트 개발 (5일 / 35시간)

## 과정 개요

| 항목 | 내용 |
|---|---|
| 교육 기간 | 5일 (일 7시간, 총 35시간) |
| 일과 | 오전 10:00 ~ 13:00 (3h) / 오후 14:00 ~ 18:00 (4h) |
| 핵심 기술 | LLM API, RAG, LangChain, LangGraph, MCP |
| 최종 산출물 | 팀별 "사내 업무 지원 AI 어시스턴트" |

## 전체 구조

| 일차 | 주제 | 핵심 산출물 |
|---|---|---|
| 1일차 | 생성형 AI·LLM 기초와 개발 환경 | LLM API 호출 챗봇 |
| 2일차 | RAG 기본 구현 | 문서 QA 시스템 v1 |
| 3일차 | RAG 고도화·평가·보안 | 성능 개선된 RAG v2 + 평가 리포트 |
| 4일차 | AI 에이전트와 LangGraph | 도구 사용 에이전트 |
| 5일차 | MCP·멀티 에이전트·최종 프로젝트 | 팀 프로젝트 발표 |

## 교안 자료 (일자별 상세 커리큘럼 + 실습 소스)

각 일차는 **상세 교수안(README.md)**과 **실습 소스(lab/)**를 별도 폴더로 구성했습니다.
1일 7시간(오전 10:00~13:00 / 오후 14:00~18:00) 수업이 가능하도록 교시별 시간표와 교수안을 포함합니다.

| 폴더 | 내용 | 주요 실습 |
|---|---|---|
| [`00-environment/`](00-environment/environment-setup.md) | 환경 설정 가이드 + 공용 샘플 문서 | venv/API키 설정, `setup.bat` |
| [`day01-generative-ai-llm-basics/`](day01-generative-ai-llm-basics/README.md) | 1일차 교안 | 모델 비교, 프롬프트 엔지니어링, Streamlit 챗봇 |
| [`day02-rag-basics/`](day02-rag-basics/README.md) | 2일차 교안 | 임베딩/유사도, 문서 로딩·청킹, 벡터 DB, 문서 QA v1 |
| [`day03-rag-advanced/`](day03-rag-advanced/README.md) | 3일차 교안 | 하이브리드 검색, 리랭커, 환각 가드레일, RAGAS 평가 |
| [`day04-ai-agent-langgraph/`](day04-ai-agent-langgraph/README.md) | 4일차 교안 | Tool calling, ReAct, LangGraph, 메모리, HITL, Self-RAG |
| [`day05-mcp-multiagent-project/`](day05-mcp-multiagent-project/README.md) | 5일차 교안 | MCP 서버/클라이언트, Supervisor 멀티 에이전트, [프로젝트 가이드](day05-mcp-multiagent-project/project-guide.md) |

### 빠른 시작

```bat
:: 1) 환경 설정 (가상환경 + 패키지 설치 + .env 생성)
setup.bat

:: 2) .env 에 OPENAI_API_KEY 입력 후 검증
.venv\Scripts\activate
python -c "import sys; sys.path.insert(0,'.'); from common.llm import get_llm; print(get_llm().invoke('OK').content)"

:: 3) 1일차 실습 예시
python day01-generative-ai-llm-basics\lab\01_model_comparison.py
```

### 저장소 구조

```
rag-agent-curriculum-5days/
├── README.md                 # 본 문서 (전체 개요)
├── requirements.txt          # 공통 패키지
├── setup.bat                 # 원클릭 환경 설정
├── .env.example              # 환경변수 템플릿
├── common/llm.py             # 공용 get_llm()/get_embeddings()
├── 00-environment/           # 환경설정 + 공용 샘플 문서
├── day01-generative-ai-llm-basics/
├── day02-rag-basics/
├── day03-rag-advanced/
├── day04-ai-agent-langgraph/
└── day05-mcp-multiagent-project/
```

---

## 1일차: 생성형 AI·LLM 기초와 개발 환경

### 오전 (10:00~13:00, 3h)
- 생성형 AI의 정의 및 활용 사례
- LLM의 기본 개념 (토큰, 컨텍스트 윈도우, 파라미터)
- 대표 모델 비교 (GPT, Claude, Gemini, 오픈소스)
- 산업 적용 사례 분석
- **실습**: 모델별 동일 질문 비교

### 오후 (14:00~18:00, 4h)
- 프롬프트 엔지니어링 (역할 지정, few-shot, 구조화 출력)
- LLM API 활용 (Python)
- 개발환경 구성 (venv, API 키 관리, Jupyter/VS Code)
- Streamlit 챗봇 UI 기초
- **실습**: 대화 이력을 유지하는 간단 챗봇 제작

---

## 2일차: RAG 기본 구현

### 오전 (10:00~13:00, 3h)
- RAG의 개념과 등장 배경
- LLM과 RAG의 차이점과 보완 관계
- RAG 구성 요소 (Retriever, Generator, Indexer)
- 임베딩 원리와 유사도 검색
- **실습**: 임베딩 시각화, 코사인 유사도 직접 계산

### 오후 (14:00~18:00, 4h)
- 문서 수집 및 전처리 (PDF, DOCX, HTML 로더)
- 청킹(Chunking) 전략
- 벡터 DB를 이용한 인덱싱 및 검색 (Chroma / FAISS)
- LangChain을 활용한 RAG 파이프라인 구성
- **실습**: 사내 문서 QA 시스템 v1 완성

---

## 3일차: RAG 고도화·평가·보안

### 오전 (10:00~13:00, 3h)
- 기업 환경에서의 RAG 필요성
- 프라이빗 데이터 활용의 필요성
- Hallucination 문제 사례 및 해결 전략 (근거 인용, 답변 거절 처리)
- **실습**: Hallucination 유발 질문 테스트 후 방지 프롬프트 적용

### 오후 (14:00~18:00, 4h)
- 검색 품질 향상
  - 하이브리드 검색 (BM25 + 벡터)
  - 리랭커(Reranker)
  - 쿼리 변환 / Multi-query
  - 메타데이터 필터
- RAG 평가 (RAGAS, 평가셋 구성)
- 보안/비공개 데이터를 활용한 서비스 기획 방향 (접근 권한, 마스킹, 온프레미스·로컬 LLM 옵션)
- RAG 기술 스택 및 구현 흐름 (RAG 시스템 구현 아키텍처)
- **실습**: v1 → v2 개선 전후 지표 비교

---

## 4일차: AI 에이전트와 LangGraph

### 오전 (10:00~13:00, 3h)
- AI 에이전트 개념 (LLM vs 에이전트)
- Function / Tool Calling
- ReAct 패턴
- 프라이빗 데이터 기반 AI Agent: 내부문서 기반 챗봇 시나리오 구성
- **실습**: 계산기·검색·RAG를 도구로 갖는 에이전트

### 오후 (14:00~18:00, 4h)
- LangGraph 개론 (State, Node, Edge, 조건부 분기)
- 메모리 (단기/장기)
- Human-in-the-loop
- 에이전틱 RAG (검색 결과 평가 후 재검색)
- **실습**: LangGraph 기반 Self-RAG 워크플로우

---

## 5일차: MCP·멀티 에이전트·최종 프로젝트

### 오전 (10:00~13:00, 3h)
- MCP 개론 (구조, 서버/클라이언트, 도구 표준화)
- MCP 서버 제작과 연동
- LangGraph + MCP 기반 AI 에이전트 개발
- **실습**: 사내 DB/파일 조회용 MCP 서버 제작

### 오후 (14:00~18:00, 4h)
- 멀티 에이전트 설계 (Supervisor 패턴, 역할 분담)
- 최종 프로젝트 개발 (약 2.5h)
- 발표·상호 리뷰·피드백 (약 1.5h)
- **실습**: 팀별 "사내 업무 지원 AI 어시스턴트" 완성 및 발표

---

## 원안(2일 과정)과의 매핑

| 원안 항목 | 반영 위치 |
|---|---|
| 생성형 AI 및 LLM 개요 | 1일차 |
| RAG 기술 및 구조 | 2일차 오전 |
| 기업 환경에서의 RAG 필요성 | 3일차 오전 |
| 벡터 기반 검색 엔진 및 RAG 기반 QA 시스템 구현 | 2일차 오후, 3일차 오후 |
| 프라이빗 데이터 기반 AI Agent | 4일차 오전 |
| LangGraph + MCP 기반 멀티 에이전트 AI 어시스턴트 | 4일차 오후, 5일차 |

## 운영 참고사항

- **최종 프로젝트 주제 예시**: 사내 규정/매뉴얼 QA 봇, 기술문서(데이터시트) 검색 에이전트, 고객 문의 응대 어시스턴트, 설비 장애 조치 가이드 에이전트
- **평가 방식**: 일차별 실습 체크 50% + 최종 프로젝트 및 발표 50%
- **실습 환경**: 클라우드 API 기반이 가장 안정적이며, 3일차 보안 파트에서 로컬 LLM(Ollama 등) 대안을 시연하면 효과적. 수강생 수가 많으면 API 키 발급·비용 관리 방안을 사전에 결정
- **난이도 조절**: 3일차 오후와 4일차 오후가 가장 무거우므로, 수강생 수준에 따라 RAGAS 평가나 Human-in-the-loop는 시연 중심으로 축소 가능
