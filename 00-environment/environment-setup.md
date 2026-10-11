# 00. 개발 환경 설정 가이드 (Windows)

> 5일 과정 전체에서 동일하게 사용하는 공통 환경입니다.
> **목표: 최종적으로 아무 실습 스크립트나 `python labs/01_xxx.py`로 실행 가능한 상태를 만든다.**

---

## 0. 과정 전체 기술 스택

| 구성 | 사용 도구 |
|---|---|
| 언어 | Python 3.11+ (본 과정 검증: 3.12) |
| LLM API | OpenAI 호환 API (기본) / Ollama(로컬, 옵션) |
| 오케스트레이션 | LangChain, LangGraph |
| 벡터 DB | Chroma(영속), FAISS(인메모리), BM25(키워드) |
| UI | Streamlit |
| 에이전트 표준 | MCP (Model Context Protocol) |
| 평가 | RAGAS |

---

## 1. 사전 설치 항목

| 항목 | 필요 여부 | 설치 방법 |
|---|---|---|
| Python 3.11+ | 필수 | https://www.python.org/downloads/ (설치 시 "Add python.exe to PATH" 체크) |
| VS Code | 권장 | https://code.visualstudio.com/ |
| VS Code 확장 | 권장 | Python(ms-python), Jupyter, Korean Language Pack, Error Lens |
| Git | 선택 | https://git-scm.com/ |
| Ollama | 3일차 보안 시연용(선택) | https://ollama.com/ (`ollama pull llama3.1:8b` 또는 `qwen2.5:7b`) |
| Chrome/Edge | 필수 | Streamlit UI 확인용 |

> 1일차 오전 첫 시간에 이 부분을 **전체 수강생과 함께** 검증한다.
> 수강생 수가 많으면 실행 전 `setup.bat`이 정상 종료됐는지 칸반으로 체크한다.

---

## 2. 프로젝트 폴더 구조

```
rag-agent-curriculum-5days/
├── README.md                         # 전체 커리큘럼 개요
├── requirements.txt                  # 공통 패키지 목록
├── setup.bat                         # 원클릭 환경 설정 스크립트
├── .env.example                      # 환경변수 템플릿
├── .env                              # (본인이 생성) API 키 입력
├── common/
│   └── llm.py                        # 공용 get_llm()/get_embeddings() 헬퍼
├── 00-environment/
│   ├── environment-setup.md          # 본 문서
│   └── sample-data/                  # 과정 공용 샘플 "사내 문서"
├── day01-generative-ai-llm-basics/   # 1일차 커리큘럼 + lab/
├── day02-rag-basics/                 # 2일차 커리큘럼 + lab/
├── day03-rag-advanced/               # 3일차 커리큘럼 + lab/
├── day04-ai-agent-langgraph/         # 4일차 커리큘럼 + lab/
└── day05-mcp-multiagent-project/     # 5일차 커리큘럼 + lab/
```

---

## 3. 설치 절차 (원클릭)

저장소 루트에서 `setup.bat`을 더블클릭(또는 명령 프롬프트에서 실행):

```
setup.bat
```

스크립트가 하는 일:
1. Python 버전 확인
2. `.venv` 가상환경 생성
3. `.venv` 활성화 + pip 업그레이드
4. `requirements.txt` 설치
5. `.env.example` → `.env` 복사

수동으로 할 경우:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

---

## 4. API 키 설정 (.env)

저장소 루트의 `.env` 파일을 열고 아래 항목을 채운다.

```ini
OPENAI_API_KEY=sk-xxxx-your-key
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
LLM_BASE_URL=
```

- **보안**: `.env`는 절대 Git에 올리지 말 것(이미 .gitignore에 등록됨). 발표·링크·캡처 화면에도 키를 노출하지 않는다.
- **비용 관리**: 수강 인원 수만큼별 키를 발급할 경우 사용량 한도(limit)를 사전에 설정하고, 임베딩 계산(2일차 이후)이 자주 호출되므로 모델/타임아웃을 낮게 유지한다.
- `LLM_BASE_URL`을 채우면 Ollama 등 OpenAI 호환 로컬 서버로 우회한다.

### (옵션) Ollama 로컬 LLM 연동

```bat
ollama pull llama3.1:8b
```
```ini
# .env
LLM_MODEL=llama3.1:8b
LLM_BASE_URL=http://localhost:11434/v1
```

---

## 5. 환경 검증

아래 코드를 실행해 LLM API 연결을 확인한다.

```bat
.venv\Scripts\activate
python -c "import sys; sys.path.insert(0,'.'); from common.llm import get_llm; r=get_llm().invoke('Hello, reply with: OK'); print(r.content)"
```

정상 출력 예시: `OK` 또는 유사 응답.

**Streamlit UI 검증** (1일차 오후에 실습):
```bat
.venv\Scripts\activate
streamlit run day01-generative-ai-llm-basics/lab/03_streamlit_chatbot.py
```

---

## 6. 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `python` 인식 안 됨 | PATH 미설정 | Python 재설치 시 "Add to PATH" 체크, 재로그인 |
| `pip install` 오류 (SSL/네트워크) | 사내 프록시/보안 | `pip config set global.index-url http://pypi.kr/... ` (사내 미러) 또는 `--trusted-host` 옵션 |
| `OpenAIError: Please set OPENAI_API_KEY` | .env 미설정 | `.env`에 키 입력 후 스크립트 재실행 (터미널 재시작) |
| `Connection error` | base_url/방화벽 | `LLM_BASE_URL` 값 확인, 게이트웨이 허용 IP 확인 |
| 첫 `CrossEncoder` 실행이 느림 | 모델 다운로드 | 사전 실행해 캐시(기본 `~/.cache`) 확보, 미러 설정 |
| `ragas` 설치 시 충돌 | 버전 호환 | 파이썬 3.12에서 `pip install ragas` 권장; 오류 시 다른 패키지와 분리 venv 생성 |
| Streamlit 로그 한글 깨짐 | 콘솔 인코딩 | `chcp 65001` 후 실행 |

---

## 7. 담당자 체크리스트 (강의 시작 전)

- [ ] 수강생 전원 Python 3.11+ 확인
- [ ] `setup.bat` 정상 완료 (패키지 설치 완료 접수)
- [ ] `.env` API 키 입력 및 `python -c ...` 검증 통과
- [ ] Streamlit 실행(1일차 오후)으로 UI 구동 확인
- [ ] (3일차 대비) Ollama 선택 설치
- [ ] 평가셋/발표용 계정(강사용) 비용 한도 설정