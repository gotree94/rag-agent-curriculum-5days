"""실습 3-2: 리랭커 (Cross-Encoder) 로 정밀도 향상

목표
- 벡터 검색으로 후보 N개를 뽑고, Cross-Encoder로 재정렬해 상위 3개만 사용.
- 리랭킹 전후 결과를 비교한다.

※ 최초 실행 시 cross-encoder 모델을 다운로드합니다(수십 MB).

실행
    .venv\\Scripts\\activate
    python day03-rag-advanced\\lab\\02_reranker.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from rag_utils import build_vector_store

QUERY = "출장 정산 절차와 숙박비 상한은 어떻게 되나요?"


def main() -> None:
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain.retrievers.document_compressors import CrossEncoderReranker
    from langchain_community.cross_encoders import HuggingFaceCrossEncoder

    store = build_vector_store()
    base_retriever = store.as_retriever(search_kwargs={"k": 6})

    encoder = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
    reranker = CrossEncoderReranker(model=encoder, top_n=3)
    rerank_retriever = ContextualCompressionRetriever(
        base_compressor=reranker, base_retriever=base_retriever
    )

    print("=" * 74)
    print(f"질문: {QUERY}\n")
    print("[리랭킹 전 (벡터 top6)]")
    for d in base_retriever.invoke(QUERY):
        print(f"  - [{d.metadata['source']}] {d.page_content[:60]}...")

    print("\n[리랭킹 후 (Cross-Encoder top3)]")
    for d in rerank_retriever.invoke(QUERY):
        print(f"  - [{d.metadata['source']}] {d.page_content[:60]}...")


if __name__ == "__main__":
    main()