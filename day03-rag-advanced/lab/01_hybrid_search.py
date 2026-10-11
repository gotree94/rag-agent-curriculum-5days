"""실습 3-1: 하이브리드 검색 (BM25 키워드 + 벡터 의미, RRF 결합)

목표
- 벡터 검색(의미)과 BM25(키워드)의 결과 차이를 확인한다.
- RRF(Reciprocal Rank Fusion)로 두 결과를 결합한다.

실행
    .venv\\Scripts\\activate
    python day03-rag-advanced\\lab\\01_hybrid_search.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from rag_utils import build_vector_store, load_sample_docs, tokenize_ko

QUERIES = [
    "배우자 출산 경조 휴가는 며칠인가요?",
    "SMA-2024 표준 패키지 구축 기간",  # 고유명사/코드형 질문 → 키워드 유리
]


def rrf_fuse(vector_ids, bm25_ids, k: int = 60) -> list[int]:
    """RRF: 순위의 역수를 합산해 결합. vector_ids/bm25_ids는 인덱스 순위 리스트."""
    scores: dict[int, float] = {}
    for rank, doc_idx in enumerate(vector_ids):
        scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    for rank, doc_idx in enumerate(bm25_ids):
        scores[doc_idx] = scores.get(doc_idx, 0.0) + 1.0 / (k + rank + 1)
    return [i for i, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]


def main() -> None:
    docs = load_sample_docs()
    texts = [d.page_content for d in docs]
    store = build_vector_store(docs)

    # BM25 준비
    from rank_bm25 import BM25Okapi

    bm25 = BM25Okapi([tokenize_ko(t) for t in texts])

    for q in QUERIES:
        print("\n" + "=" * 74)
        print(f"질문: {q}")
        print("=" * 74)

        # 1) 벡터 검색
        vec_results = store.similarity_search(q, k=3)
        vec_ids = [docs.index(d) if d in docs else -1 for d in vec_results]

        # 2) BM25 검색
        scores = bm25.get_scores(tokenize_ko(q))
        bm25_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]

        # 3) RRF 결합
        fused = rrf_fuse(vec_ids, bm25_ids)[:3]

        print("[벡터 검색 top3]")
        for i in vec_ids:
            if i >= 0:
                print(f"  - [{docs[i].metadata['source']}] {texts[i][:55]}...")
        print("[BM25 검색 top3]")
        for i in bm25_ids:
            print(f"  - [{docs[i].metadata['source']}] {texts[i][:55]}...")
        print("[하이브리드(RRF) top3]")
        for i in fused:
            print(f"  - [{docs[i].metadata['source']}] {texts[i][:55]}...")


if __name__ == "__main__":
    main()