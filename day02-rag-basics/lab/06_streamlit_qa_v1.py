"""실습 2-6: 문서 QA 시스템 v1 (Streamlit)

기능
- 최초 실행 시 sample-data 문서를 인덱싱(Chroma), 이후 재사용
- 질문 → 유사도 검색(top-k) → 근거 기반 답변
- 답변과 함께 참조한 출처를 expander로 표시

실행 (저장소 루트에서)
    .venv\\Scripts\\activate
    streamlit run day02-rag-basics\\lab\\06_streamlit_qa_v1.py
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import SAMPLE_DATA_DIR, get_embeddings, get_llm

CHROMA_DIR = Path(__file__).resolve().parents[2] / ".chroma_db_v1"

PROMPT_TEMPLATE = """당신은 사내 문서 기반 Q&A 어시스턴트입니다.
아래 [문서 내용]만 근거로 답변하고, 없는 내용은 "문서에서 찾을 수 없습니다"라고 하세요.

[문서 내용]
{context}

[질문]
{question}

[답변] 출처 파일명을 (출처: 파일명) 형식으로 반드시 표시하세요."""


@st.cache_resource(show_spinner="문서를 인덱싱하는 중입니다...")
def get_store():
    from langchain_chroma import Chroma
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import TextLoader

    if CHROMA_DIR.exists():
        return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=get_embeddings())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    docs = []
    for md in sorted(SAMPLE_DATA_DIR.glob("*.md")):
        loaded = TextLoader(str(md), encoding="utf-8").load()
        for d in loaded:
            d.metadata["source"] = md.name
        docs.extend(loaded)
    return Chroma.from_documents(
        documents=splitter.split_documents(docs),
        embedding=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


st.set_page_config(page_title="사내 문서 QA v1", page_icon="📚")
st.title("📚 사내 문서 QA v1")
st.caption("문서 근거 기반 RAG 시스템 (2일차)")

with st.sidebar:
    st.header("설정")
    top_k = st.slider("검색 문서 수 (top-k)", 1, 6, 4)
    show_sources = st.checkbox("검색된 원문 표시", value=True)

store = get_store()
retriever = store.as_retriever(search_kwargs={"k": top_k})

question = st.text_input("질문을 입력하세요", value="연차는 어떻게 발생하나요?")

if st.button("질문하기") and question.strip():
    with st.spinner("답변 생성 중..."):
        docs = retriever.invoke(question)
        context = "\n\n".join(
            f"<출처:{d.metadata.get('source')}>\n{d.page_content}" for d in docs
        )
        answer = get_llm(temperature=0.0).invoke(
            PROMPT_TEMPLATE.format(context=context, question=question)
        ).content

    st.subheader("🤖 답변")
    st.write(answer)

    if show_sources:
        with st.expander(f"📄 검색된 문서 {len(docs)}건"):
            for i, d in enumerate(docs, 1):
                st.markdown(f"**{i}. {d.metadata.get('source')}**")
                st.text(d.page_content[:400])