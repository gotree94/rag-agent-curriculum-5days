"""실습 2-4: 벡터 DB 저장·검색 (Chroma 영속 / FAISS 인메모리)

목표
- 샘플 사내 문서를 청크 → 임베딩 → Chroma(영속)에 저장한다.
- 유사도 검색(similarity_search)으로 관련 청크를 찾는다.
- FAISS 인메모리 검색과 결과를 비교한다.

실행
    .venv\\Scripts\\activate
    python day02-rag-basics\\lab\\04_vector_store.py
"""

import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR, get_embeddings

CHROMA_DIR = Path(__file__).resolve().parents[2] / ".chroma_db"
QUERIES = [
    "연차는 몇 일이 발생하나요?",
    "출장 식비 정산 상한은 얼마인가요?",
    "복지포인트는 얼마가 지급되나요?",
]


def build_chunks():
    """sample-data의 모든 .md 문서를 청크로 만든다."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=80,
        separators=["\n\n", "\n", "。", ".", " ", ""],
    )
    from langchain_community.document_loaders import TextLoader

    all_docs = []
    for md in sorted(SAMPLE_DATA_DIR.glob("*.md")):
        docs = TextLoader(str(md), encoding="utf-8").load()
        for d in docs:
            d.metadata["source"] = md.name
        all_docs.extend(docs)
    return splitter.split_documents(all_docs)


def get_or_create_chroma():
    from langchain_chroma import Chroma

    if CHROMA_DIR.exists():
        return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=get_embeddings())
    print("[생성] 샘플 문서 인덱싱 중 (최초 1회)...")
    store = Chroma.from_documents(
        documents=build_chunks(),
        embedding=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )
    return store


def demo_faiss():
    print("\n" + "=" * 70)
    print("[FAISS (인메모리) 검색 비교]")
    print("=" * 70)
    from langchain_community.vectorstores import FAISS

    faiss_db = FAISS.from_documents(build_chunks(), get_embeddings())
    for q in QUERIES[:2]:
        print(f"\n  질문: {q}")
        for doc in faiss_db.similarity_search(q, k=2):
            print(f"    - [{doc.metadata.get('source')}] {doc.page_content[:60]}...")


def main() -> None:
    print("=" * 70)
    print("[Chroma 영속 DB 검색]")
    print("=" * 70)
    store = get_or_create_chroma()
    for q in QUERIES:
        print(f"\n  질문: {q}")
        for doc in store.similarity_search(q, k=2):
            print(f"    - [{doc.metadata.get('source')}] {doc.page_content[:60]}...")

    demo_faiss()


if __name__ == "__main__":
    main()