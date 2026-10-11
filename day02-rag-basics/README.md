# Day 2. RAG 기본 구현

> **산출물: 사내 문서 QA 시스템 v1 (LangChain + Chroma + Streamlit)**
> 하루 7시간 (오전 10:00~13:00 / 오후 14:00~18:00)

## 1. 학습 목표

- RAG의 개념·등장 배경을 설명하고 LLM 단독 사용과의 차이를 이해한다.
- 임베딩의 원리와 코사인 유사도를 이해하고 직접 계산한다.
- 문서 수집→청킹→임베딩→벡터 저장(Indexing) 파이프라인을 구축한다.
- 문서 QA 시스템 v1(질문→검색→재생성)을 LangChain으로 완성한다.

## 2. 일과표 (7h)

### 오전 — RAG 개념과 검색 원리 (10:00~13:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 10:00~10:50 | 강의 2-1 | RAG 개념·등장 배경, LLM 단독 vs RAG, 파인튜닝과의 비교 | 발표자료 |
| 10:50~11:00 | 휴식 | | |
| 11:00~11:50 | 강의 2-2 | RAG 구성요소(Indexer/Retriever/Generator), 임베딩 원리 | 발표자료 |
| 11:50~12:00 | 휴식 | | |
| 12:00~12:40 | 강의 2-3 | 유사도 검색 (코사인 유사도, top-k), 청킹 전략 | 발표자료 |
| 12:40~13:00 | 실습 2-1 | **임베딩·코사인 유사도 계산 + 시각화** | lab/01_embedding_similarity.py |

### 오후 — 문서 QA 시스템 v1 구축 (14:00~18:00)

| 시간 | 구분 | 내용 | 자료/실습 |
|---|---|---|---|
| 14:00~14:40 | 강의 2-4 | 문서 로딩 (PDF/DOCX/MD/HTML) | lab/02_document_loading.py |
| 14:40~15:20 | 실습 2-2 | **청킹 실습 (chunk_size/overlap 비교)** | lab/03_chunking.py |
| 15:20~15:30 | 휴식 | | |
| 15:30~16:10 | 실습 2-3 | **벡터 DB 저장·검색 (Chroma/FAISS)** | lab/04_vector_store.py |
| 16:10~16:50 | 실습 2-4 | **LangChain RAG 파이프라인 (검색+생성+근거)** | lab/05_rag_pipeline.py |
| 16:50~17:00 | 휴식 | | |
| 17:00~17:50 | 실습 2-5 | **문서 QA 시스템 v1 완성 (Streamlit UI)** | lab/06_streamlit_qa_v1.py |
| 17:50~18:00 | 정리 | v1 체크리스트, 3일차 예고(고도화) | |

## 3. 교수안 상세

### 3-1. RAG 개념과 등장 배경 (50분)
- **문제**: LLM의 지식은 학습 시점에 고정(비용 큼), 최신/사내 데이터 부재, 환각
- **RAG (Retrieval-Augmented Generation)**: 검색한 문서를 프롬프트에 넣고 생성
  → "사내 규정을 근거로 답하는 AI", "최신 문서 기반 답변"
- **파인튜닝 vs RAG**: 파인튜닝은 모델 자체 학습(비용·유지 어려움), RAG은 데이터만 교체(빠름, 근거 추적 가능)
- 전체 파이프라인 미리보기 도식:
  `문서 → 로드 → 청킹 → 임베딩 → 벡터 DB` / `질문 → 임베딩 → 상위 k개 검색 → LLM 생성`

### 3-2. RAG 구성요소와 임베딩 (50분)
- Indexer(색인), Retriever(검색), Generator(생성)
- **임베딩**: 텍스트 → 숫자 벡터(예: 1536차원). 의미가 가까우면 벡터도 가까움
- **코사인 유사도**: 두 벡터의 방향 일치 정도 (-1~1)
- 벡터 DB의 역할: 대량 벡터의 유사도 검색 최적화 (ANN)

### 3-3. 청킹 전략 (40분)
- 문서를 격 크기 단위(청크)로 자르는 이유(임베딩은 문맥 한계가 있음)
- `RecursiveCharacterTextSplitter`: chunk_size/chunk_overlap
- 청크 크기 트레이드오프: 작으면 정확히 떨어짐, 크면 문맥 풍부하지만 노이즈

### 3-4 ~ 3-7. 실습 중심 (인덱싱→검색→QA)
- 로더: `TextLoader`(md/txt), `PyPDFLoader`(pdf), `Docx2txtLoader`(docx), `BSHTMLLoader`(html), `CSVLoader`(csv)
- 벡터 DB: Chroma(영속, 다음 실행에 재사용), FAISS(인메모리, 빠른 실험) 비교
- RAG 체인: retriever → 문맥 포맷팅 → 프롬프트 → LLM
- **근거 인용**: 답변에 출처(원본 파일명/문장)를 함께 출력 → 1차 신뢰성 확보

## 4. 실습 가이드

| 실습 | 파일 | 핵심 |
|---|---|---|
| 2-1 임베딩/유사도 | `lab/01_embedding_similarity.py` | 문장 임베딩, 코사인 유사도 행렬, 2D 시각화 |
| 2-2 문서 로딩 | `lab/02_document_loading.py` | 샘플 사내 문서 로드 |
| 2-3 청킹 | `lab/03_chunking.py` | chunk_size/overlap 별 분할 비교 |
| 2-4 벡터 저장·검색 | `lab/04_vector_store.py` | Chroma 영속 저장, 유사도 검색 |
| 2-5 RAG 파이프라인 | `lab/05_rag_pipeline.py` | 검색+생성+근거 출력 |
| 2-6 QA v1 UI | `lab/06_streamlit_qa_v1.py` | 완성된 문서 QA v1 |

실행 방법:
```bat
.venv\Scripts\activate
python day02-rag-basics\lab\01_embedding_similarity.py
streamlit run day02-rag-basics\lab\06_streamlit_qa_v1.py
```

## 5. 평가 체크리스트

- [ ] 코사인 유사도를 직접 계산해 유사·비유사 문장을 구분했다
- [ ] PDF/DOCX/MD/HTML 각 1종 이상 로드에 성공했다
- [ ] 청킹 size/overlap을 바꾸며 문서 수 변화를 설명했다
- [ ] Chroma 벡터 DB에 저장 후 재실행 때 재사용된다
- [ ] QA v1이 정확한 근거를 인용하며 답변한다

## 6. 참고 자료

- 임베딩 개념: OpenAI Embeddings 문서
- LangChain 문서 로더: https://python.langchain.com/docs/integrations/document_loaders/
- Chroma: https://docs.trychroma.com/