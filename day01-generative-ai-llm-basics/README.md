# Day 1. 생성형 AI · LLM 기초와 개발 환경

> **산출물: 모델 비교 리포트 + 프롬프트 실습 + LLM API 챗봇 (Streamlit)**
> 하루 7시간 (오전 10:00~13:00 / 오후 14:00~18:00)

## 1. 학습 목표

- 생성형 AI와 판별형 AI의 차이, LLM의 원리(토큰·컨텍스트·파라미터)를 설명한다.
- 주요 LLM(GPT·Claude·Gemini·Llama/Qwen)의 특징을 비교하고 용도에 맞게 선택한다.
- 역할지정·Few-shot·CoT·JSON 구조화 등 프롬프트 엔지니어링 기법을 적용한다.
- Python + LangChain으로 LLM API를 호출하고, `.env`로 키를 안전하게 관리한다.
- Streamlit으로 대화 이력을 유지하는 챗봇 UI를 만든다.

## 2. 일과표 (7h)

### 오전 — 생성형 AI · LLM 개념 (10:00~13:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 10:00~10:30 | 오리엔테이션 | 과정 소개, 평가 방식, 환경 체크리스트 | 00-environment/environment-setup.md |
| 10:30~10:50 | 강의 1-1 | 생성형 AI 정의와 판별형 AI 비교, 활용 사례 | 발표자료 |
| 10:50~11:00 | 휴식 | | |
| 11:00~11:50 | 강의 1-2 | LLM 원리 (토큰화, 컨텍스트 윈도우, 파라미터, temperature) | 발표자료 |
| 11:50~12:00 | 휴식 | | |
| 12:00~12:40 | 강의 1-3 | 대표 모델 비교 (GPT/Claude/Gemini/오픈소스), 산업 적용 사례 | 발표자료 |
| 12:40~13:00 | 실습 1-1 | **모델별 동일 질문 비교 + temperature 효과** | lab/01_model_comparison.py |

### 오후 — 프롬프트 & API 개발 (14:00~18:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 14:00~14:50 | 강의 1-4 | 프롬프트 엔지니어링: 역할지정, Few-shot, CoT, 구조화 출력 | 발표자료 |
| 14:50~15:00 | 휴식 | | |
| 15:00~15:50 | 실습 1-2 | **프롬프트 기법 4종 + JSON 구조화 출력** | lab/02_prompt_engineering.py |
| 15:50~16:00 | 휴식 | | |
| 16:00~16:50 | 강의 1-5 | 개발환경: venv, .env 키 관리, LangChain 개요, Jupyter/VS Code | 00-environment/environment-setup.md |
| 16:50~17:00 | 휴식 | | |
| 17:00~17:50 | 실습 1-3 | **Streamlit 대화형 챗봇 제작** | lab/03_streamlit_chatbot.py |
| 17:50~18:00 | 정리 | 과제 안내, 1일차 체크리스트 리뷰 | |

## 3. 교수안 상세

### 3-1. 오리엔테이션 + 환경 점검 (30분)
- 과정 목표·일정·평가(실습 50% + 최종 프로젝트 50%) 소개
- `setup.bat`으로 가상환경 설치가 끝났는지 일괄 확인
- `.env` 생성 및 API 키 입력, 연결 검증
  ```bat
  .venv\Scripts\activate
  python -c "import sys; sys.path.insert(0,'.'); from common.llm import get_llm; print(get_llm().invoke('OK라고만 답해').content)"
  ```

### 3-2. 생성형 AI 이해 (20분)
- **정의**: 입력 데이터의 분포를 학습해 새로운 내용(텍스트/이미지/음성)을 생성
- **판별형 vs 생성형**: 분류(라벨 예측) vs 생성(새 데이터)
- **LLM = 대규모 언어모델**: 방대한 말뭉치에서 "다음 토큰"을 예측하도록 학습
- 활용 사례: 고객 응대, 문서 요약/작성, 코드 생성, 사내 지식 검색(🤖 본 과정의 주제)

### 3-3. LLM 원리 (50분)
- **토큰(Token)**: 단어·음절 단위 조각. 토큰 수 = 비용/제한 기준
- **컨텍스트 윈도우**: 한 번에 처리 가능한 토큰 최대 길이
- **주요 하이퍼파라미터**:
  - `temperature`: 낮을수록 결정적(검색/추출), 높을수록 창의적(글쓰기)
  - `top_p`, `max_tokens`
- **파라미터 규모**: 모델 크기(수십억~수조 개)와 성능·비용 트레이드오프
- **한계**: 환각(hallucination), 지식 시점(학습 데이터 마감), 컨텍스트 한계 → (3일차에 대처법, 2일차부터 RAG)

### 3-4. 대표 모델 비교 (40분)
| 구분 | 모델 예 | 특징 |
|---|---|---|
| OpenAI | GPT-4o / gpt-4o-mini | 범용·API 생태계 최고, 저비용 mini |
| Anthropic | Claude | 긴 문서·코딩·보안 강세 |
| Google | Gemini | 멀티모달(이미지/음성), 구글 생태계 |
| 오픈소스 | Llama 3.1, Qwen2.5 | 온프레미스·데이터 기밀 요구 시 (3일차 Ollama 연동) |

### 3-5. 프롬프트 엔지니어링 (50분)
- **역할 지정**: "당신은 회계 전문가입니다" → 출력 품질 향상
- **Few-shot**: 예시 2~3개를 제시해 형식 학습
- **CoT (Chain-of-Thought)**: 단계별 reasoning 유도
- **구조화 출력**: JSON 스키마 요구, 필요한 키만 추출
- **출력 제약**: 모르면 모른다고 말하라(→ 3일차 환각 방지의 기초)
- ❗ 원칙: 프롬프트로 안 되는 것은 RAG(2일차)로 해결

### 3-6. 개발환경 & LangChain (50분)
- venv 격리 이유, `.env` 비밀키 보관, `.gitignore`
- LangChain 개요: LLM 공통 인터페이스(동일 코드로 모델 교체)
- invoke / stream / batch, 메시지(system/user/assistant) 개념

### 3-7. Streamlit (50분)
- `st.session_state`로 대화 이력 유지
- LLM 스트리밍 응답(`st.write_stream`)
- 사이드바에서 모델·temperature 변경 UI

## 4. 실습 가이드

| 실습 | 파일 | 핵심 |
|---|---|---|
| 1-1 모델·온도 비교 | `lab/01_model_comparison.py` | 동일 질문 × 모델/온도별 응답 비교, 토큰 사용량 확인 |
| 1-2 프롬프트 기법 | `lab/02_prompt_engineering.py` | 역할·Few-shot·CoT·JSON 4종 데모 |
| 1-3 챗봇 UI | `lab/03_streamlit_chatbot.py` | 대화 이력 유지 + 스트리밍 + 옵션 패널 |

실행 방법 (저장소 루트에서):
```bat
.venv\Scripts\activate
python day01-generative-ai-llm-basics\lab\01_model_comparison.py
streamlit run day01-generative-ai-llm-basics\lab\03_streamlit_chatbot.py
```

## 5. 평가 체크리스트

- [ ] 동일 질문을 2개 이상의 모델로 실행하고 응답 차이를 메모했다
- [ ] temperature 0 vs 1 차이를 확인했다
- [ ] 프롬프트 4종 각각을 실행하고 출력을 기존대로 제출했다
- [ ] JSON 출력을 파싱해 특정 필드만 추출했다
- [ ] 챗봇이 이전 대화를 기억하고 이어서 답한다

## 6. 참고 자료

- OpenAI API docs: https://platform.openai.com/docs
- LangChain docs: https://python.langchain.com/docs
- Streamlit docs: https://docs.streamlit.io