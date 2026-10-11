"""실습 3-4: 메타데이터 필터로 검색 범위 제한

목표
- 문서 출처(source=파일명)를 메타데이터로 활용해 특정 문서에서만 검색한다.
- 부서/권한/문서종류 필터링의 기초를 실습한다 (보안 파트와 연결).

실행
    .venv\\Scripts\\activate
    python day03-rag-advanced\\lab\\04_metadata_filter.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from rag_utils import build_vector_store

QUERY = "상한 금액은 얼마인가요?"  # 필터에 따라 정답 문서가 달라짐


def main() -> None:
    store = build_vector_store()

    print("=" * 74)
    print(f"질문: {QUERY}\n")
    print("[필터 없음]")
    for d in store.similarity_search(QUERY, k=3):
        print(f"  - [{d.metadata['source']}] {d.page_content[:60]}...")

    print("\n[필터: source == 'company-policy.md']")
    for d in store.similarity_search(
        QUERY, k=3, filter={"source": "company-policy.md"}
    ):
        print(f"  - [{d.metadata['source']}] {d.page_content[:60]}...")

    print("\n[필터: source == 'customer-faq.md']")
    for d in store.similarity_search(
        QUERY, k=3, filter={"source": "customer-faq.md"}
    ):
        print(f"  - [{d.metadata['source']}] {d.page_content[:60]}...")


if __name__ == "__main__":
    main()