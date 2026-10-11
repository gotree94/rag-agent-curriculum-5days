"""실습 3-6: v1(벡터 단독) vs v2(하이브리드+리랭킹) 검색 품질 비교

지표 (eval_questions.json의 reference_source 활용)
- Hit@k : 상위 k개 안에 정답 문서(source)가 포함된 질문 비율
- Precision@k : 상위 k개 중 정답 문서 비율의 평균

리랭커는 무거우므로 기본은 "벡터 vs 하이브리드"만 비교하고,
--rerank 옵션을 주면 Cross-Encoder까지 포함한다.

실행
    .venv\\Scripts\\activate
    python day03-rag-advanced\\lab\\07_compare_v1_v2.py
    python day03-rag-advanced\\lab\\07_compare_v1_v2.py --rerank
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from rag_utils import (  # noqa: E402
    build_vector_store,
    load_eval_questions,
    load_sample_docs,
    tokenize_ko,
)

TOP_K = 3


def _index_by_content(docs):
    return {d.page_content: i for i, d in enumerate(docs)}


def vector_retrieve(store, docs, query):
    results = store.similarity_search(query, k=TOP_K)
    return [d.metadata["source"] for d in results]


def hybrid_retrieve(store, docs, bm25, query):
    idx = _index_by_content(docs)
    vec_docs = store.similarity_search(query, k=TOP_K * 2)
    vec_ids = [idx[d.page_content] for d in vec_docs if d.page_content in idx]

    scores = bm25.get_scores(tokenize_ko(query))
    bm25_ids = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: TOP_K * 2]

    fused, k = {}, 60  # RRF
    for rank, i in enumerate(vec_ids):
        fused[i] = fused.get(i, 0.0) + 1 / (k + rank + 1)
    for rank, i in enumerate(bm25_ids):
        fused[i] = fused.get(i, 0.0) + 1 / (k + rank + 1)
    top = [i for i, _ in sorted(fused.items(), key=lambda x: x[1], reverse=True)][:TOP_K]
    return [docs[i].metadata["source"] for i in top]


def build_rerank_retrieve(store):
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain.retrievers.document_compressors import CrossEncoderReranker
    from langchain_community.cross_encoders import HuggingFaceCrossEncoder

    base = store.as_retriever(search_kwargs={"k": TOP_K * 2})
    encoder = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
    rerank = CrossEncoderReranker(model=encoder, top_n=TOP_K)
    comp = ContextualCompressionRetriever(base_compressor=rerank, base_retriever=base)
    return lambda query: [d.metadata["source"] for d in comp.invoke(query)][:TOP_K]


def score(fn, eval_items):
    hit, prec = 0, 0.0
    for item in eval_items:
        sources = fn(item["question"])
        correct = [s for s in sources if s == item["reference_source"]]
        hit += 1 if correct else 0
        prec += len(correct) / TOP_K
    n = len(eval_items)
    return hit / n, prec / n


def main() -> None:
    docs = load_sample_docs()
    store = build_vector_store(docs)
    eval_items = load_eval_questions()

    from rank_bm25 import BM25Okapi

    bm25 = BM25Okapi([tokenize_ko(d.page_content) for d in docs])

    results = {
        "v1 (벡터 단독)": score(lambda q: vector_retrieve(store, docs, q), eval_items),
        "v2 (하이브리드 RRF)": score(lambda q: hybrid_retrieve(store, docs, bm25, q), eval_items),
    }
    if "--rerank" in sys.argv:
        results["v2+ (하이브리드+리랭킹)"] = score(build_rerank_retrieve(store), eval_items)

    print("=" * 66)
    print(f"{'방식':<26}{'Hit@' + str(TOP_K):>12}{'Precision@' + str(TOP_K):>18}")
    print("-" * 66)
    for name, (hit, prec) in results.items():
        print(f"{name:<26}{hit:>12.2f}{prec:>18.2f}")
    print("=" * 66)
    print("→ v1 대비 v2 개선 폭을 확인하세요.")


if __name__ == "__main__":
    main()