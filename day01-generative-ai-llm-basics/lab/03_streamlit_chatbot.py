"""실습 1-3: Streamlit 대화형 챗봇 (대화 이력 유지)

특징
- st.session_state로 이전 대화 유지
- st.write_stream으로 LLM 응답 스트리밍
- 사이드바에서 모델·temperature 조절

실행 (저장소 루트에서)
    .venv\\Scripts\\activate
    streamlit run day01-generative-ai-llm-basics\\lab\\03_streamlit_chatbot.py
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import get_llm

st.set_page_config(page_title="LLM 챗봇", page_icon="🤖")

# ---------- 사이드바: 설정 ----------
with st.sidebar:
    st.header("⚙️ 챗봇 설정")
    model = st.selectbox("모델", ["gpt-4o-mini", "gpt-4o"])
    temperature = st.slider("temperature", 0.0, 1.5, 0.7, 0.1)
    system_prompt = st.text_area(
        "시스템 프롬프트",
        value="당신은 친절하고 정확한 한국어 AI 비서입니다.",
    )
    if st.button("대화 초기화"):
        st.session_state.clear()
        st.rerun()

llm = get_llm(model=model, temperature=temperature)

# ---------- 세션 상태: 메시지 이력 ----------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt},
    ]

# ---------- 대화 출력 ----------
st.title("💬 LLM 챗봇")
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# ---------- 입력 처리 ----------
if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # LangChain 메시지 객체로 변환
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    lc_messages = [
        {"system": SystemMessage, "assistant": AIMessage, "user": HumanMessage}[m["role"]](content=m["content"])
        for m in st.session_state["messages"]
    ]

    with st.chat_message("assistant"):
        stream = llm.stream(lc_messages)
        answer = st.write_stream(stream)

    st.session_state["messages"].append({"role": "assistant", "content": answer})