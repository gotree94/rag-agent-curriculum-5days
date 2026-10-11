"""실습 2-3: 청킹 전략 비교 (chunk_size / chunk_overlap)

목표
- RecursiveCharacterTextSplitter의 동작을 이해한다.
- chunk_size·chunk_overlap 변경에 따른 청크 수와 내용을 비교한다.

실행
    .venv\\Scripts\\activate
    python day02-rag-basics\\lab\\03_chunking.py
"""

import sys
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR


def load_text() -> str:
    md_file = SAMPLE_DATA_DIR / "company-policy.md"
    return md_file.read_text(encoding="utf-8")


def split_with(size: int, overlap: int):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", "。", ".", " ", ""],
    )
    return splitter.split_text(load_text())


def main() -> None:
    text = load_text()
    print(f"원본 문서: {len(text):,} 자")

    configs = [
        (300, 0, "작은 청크"),
        (300, 50, "작은 청크 + 오버랩"),
        (800, 100, "중간 청크"),
        (1500, 200, "큰 청크"),
    ]
    for size, overlap, label in configs:
        chunks = split_with(size, overlap)
        print(f"  [{label}] chunk_size={size}, overlap={overlap} -> 청크 {len(chunks)}개")

    print("\n[1개 청크 샘플] chunk_size=300, overlap=50:")
    chunks = split_with(300, 50)
    print("  ----- 청크[0] -----")
    print("  " + chunks[0].replace("\n", "\n  ")[:300])
    print("  ----- 청크[1] 시작 (오버랩 효과 확인) -----")
    print("  " + chunks[1][:120])


if __name__ == "__main__":
    main()