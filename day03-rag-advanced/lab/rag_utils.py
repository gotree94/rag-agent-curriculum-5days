"""3일차 공용 유틸: 샘플 문서 인덱싱 / 리트리버 / 평가셋 로딩."""

import json
import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR, get_embeddings


def load_sample_docs():
    """sample-data/*.md 를 청크로 분할해 Document 리스트로 반환."""
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=80,
        separators=["\n\n", "\n", "。", ".", " ", ""],
    )
    docs = []
    for md in sorted(SAMPLE_DATA_DIR.glob("*.md")):
        loaded = TextLoader(str(md), encoding="utf-8").load()
        for d in loaded:
            d.metadata["source"] = md.name
        docs.extend(loaded)
    return splitter.split_documents(docs)


def build_vector_store(docs=None):
    """FAISS 인메모리 벡터스토어 생성 (실험용)."""
    from langchain_community.vectorstores import FAISS

    docs = docs or load_sample_docs()
    return FAISS.from_documents(docs, get_embeddings())


def load_eval_questions():
    path = SAMPLE_DATA_DIR / "eval_questions.json"
    return json.loads(path.read_text(encoding="utf-8"))


# --- 한국어 간이 토크나이저 (형태소 분석기 없이 BM25 성능 보완) ---
def tokenize_ko(text: str) -> list[str]:
    text = text.lower()
    words = re.findall(r"[0-9a-zA-Z가-힣]+", text)
    tokens = list(words)
    for w in words:
        if len(w) >= 2 and re.search(r"[가-힣]", w):
            tokens += [w[i:i + 2] for i in range(len(w) - 1)]  # 음절 바이그램
    return tokens