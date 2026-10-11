"""실습 2-5: LangChain RAG 파이프라인 (검색 → 생성 → 근거 인용)

목표
- 벡터 DB(retriever)에서 관련 청크를 검색한다.
- 검색된 문서를 프롬프트에 주입해 LLM이 근거를 따라 답변하게 한다.
- 답변과 함께 출처(파일명)를 함께 출력한다.

실행
    .venv\\Scripts\\activate
    python day02-rag-basics\\lab\\05_rag_pipeline.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import get_embeddings, get_llm

from langchain_chroma import Chroma

CHROMA_DIR = Path(__file__).resolve().parents[2] / ".chroma_db"

RAG_PROMPT_TEMPLATE = """당신은 사내 문서 기반 Q&A 어시스턴트입니다.
[질문과 관련된 문서] 내용만 근거로 답변하고, 문서에 없는 내용은 "문서에서 찾을 수 없습니다"라고 답하세요.

[문서 내용]
{context}

[질문]
{question}

[답변 규칙]
1) 문서를 인용할 때는 시작에 출처 파일명을 표시하세요. 예: (출처: company-policy.md)
2) 필요하면 여러 출처를 함께 표시하세요.
"""


def format_context(docs) -> str:
    return "\n\n".join(
        f"<출처:{d.metadata.get('source', 'unknown')}>\n{d.page_content}" for d in docs
    )


def ask(store: Chroma, question: str):
    top_k = 4
    docs = store.similarity_search(question, k=top_k)

    print(f"\n[검색 결과 {len(docs)}건]")
    for i, d in enumerate(docs):
        print(f"  {i+1}. {d.metadata.get('source')} | {d.page_content[:70]}...")

    prompt = RAG_PROMPT_TEMPLATE.format(
        context=format_context(docs), question=question
    )
    answer = get_llm(temperature=0.0).invoke(prompt).content
    print(f"\n[LLM 답변]\n{answer}")


def main() -> None:
    # 실습 2-4에서 만든 Chroma DB를 재사용 (없으면 안내)
    if not CHROMA_DIR.exists():
        print("[안내] 먼저 lab/04_vector_store.py를 실행해 Chroma DB를 만들어주세요.")
        sys.exit(1)

    store = Chroma(persist_directory=str(CHROMA_DIR), embedding_function=get_embeddings())

    for q in [
        "배우자 출산 시 경조 휴가는 며칠인가요?",
        "표준 패키지 구축 비용을 알려주세요.",
    ]:
        print("\n" + "=" * 70)
        print(f"질문: {q}")
        print("=" * 70)
        ask(store, q)


if __name__ == "__main__":
    main()