"""실습 2-2: 다양한 문서 포맷 로딩 (PDF, DOCX, MD, HTML, CSV)

목표
- 샘플 "사내 문서"(Markdown)를 TextLoader로 로드한다.
- PDF / DOCX / HTML 로더 사용법을 익히고, 직접 만든 파일로 확장한다.

실행
    .venv\\Scripts\\activate
    python day02-rag-basics\\lab\\02_document_loading.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR


def load_markdown_directory() -> None:
    from langchain_community.document_loaders import TextLoader

    print("=" * 70)
    print("[1] Markdown/Text 문서 로딩 (00-environment/sample-data)")
    print("=" * 70)
    for md_file in sorted(SAMPLE_DATA_DIR.glob("*.md")):
        # children=False 로딩: 원본 page_content는 그대로 두고, metadata에 출처 추가
        loader = TextLoader(str(md_file), encoding="utf-8")
        docs = loader.load()
        for d in docs:
            d.metadata["source"] = md_file.name
        print(f"  {md_file.name}: 문서 {len(docs)}건")
        print(f"    - 첫 60자: {docs[0].page_content[:60]}")

    from langchain_community.document_loaders import CSVLoader

    csv_file = SAMPLE_DATA_DIR / "employees.csv"
    loader = CSVLoader(str(csv_file), encoding="utf-8")
    rows = loader.load()
    print(f"\n  employees.csv: {len(rows)}건 로드")
    print(f"    - 샘플: {rows[0].page_content}")


def demo_conditional_loaders() -> None:
    """PDF/DOCX/HTML 로더는 해당 파일이 있을 때만 시연."""
    print("\n" + "=" * 70)
    print("[2] PDF / DOCX / HTML 로더 (선택 예제)")
    print("=" * 70)

    from langchain_community.document_loaders import (
        BSHTMLLoader,
        Docx2txtLoader,
        PyPDFLoader,
    )

    # 예시 파일이 만들어져 있으면 로드. 없으면 사용법 안내만.
    demos = {
        "pdf": (SAMPLE_DATA_DIR / "sample.pdf", PyPDFLoader),
        "docx": (SAMPLE_DATA_DIR / "sample.docx", Docx2txtLoader),
        "html": (SAMPLE_DATA_DIR / "sample.html", BSHTMLLoader),
    }
    for name, (path, loader_cls) in demos.items():
        if path.exists():
            docs = loader_cls(str(path)).load()
            print(f"  {name}: 문서 {len(docs)}건 로드 성공")
        else:
            print(f"  {name}: {path.name} 없음. 파일을 만들어 두면 실습 가능:")
            if name == "pdf":
                print("    - PyPDFLoader(pdf_path).load()")
            elif name == "docx":
                print("    - Docx2txtLoader(docx_path).load()")
            else:
                print("    - BSHTMLLoader(html_path).load()")


if __name__ == "__main__":
    load_markdown_directory()
    demo_conditional_loaders()