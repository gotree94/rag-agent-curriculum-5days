"""실습 3-3: Multi-query 쿼리 변환으로 재현율 향상

목표
- LLM이 하나의 질문을 여러 표현으로 확장(Multi-query)해 검색한다.
- 생성된 변형 질의와 병합된 결과를 확인한다.

실행
    .venv\\Scripts\\activate
    python day03-rag-advanced\\lab\\03_multi_query.py
"""

import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))  # 저장소 루트
sys.path.append(str(Path(__file__).resolve().parents[1]))  # day03 (rag_utils)
from rag_utils import build_vector_store
from common.llm import get_llm  # noqa: E402

logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

QUERY = "휴가 신청은 언제까지 해야 하나요?"


def main() -> None:
    from langchain.retrievers.multi_query import MultiQueryRetriever

    store = build_vector_store()
    base_retriever = store.as_retriever(search_kwargs={"k": 3})

    print("=" * 74)
    print(f"질문: {QUERY}\n")
    print("[기본 벡터 검색 top3]")
    for d in base_retriever.invoke(QUERY):
        print(f"  - [{d.metadata['source']}] {d.page_content[:60]}...")

    print("\n[Multi-query 결과] (위 로그에서 생성된 변형 질의 확인)")
    mq_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever, llm=get_llm(temperature=0.0)
    )
    seen = set()
    for d in mq_retriever.invoke(QUERY):
        key = d.page_content[:50]
        if key in seen:
            continue
        seen.add(key)
        print(f"  - [{d.metadata['source']}] {d.page_content[:60]}...")


if __name__ == "__main__":
    main()