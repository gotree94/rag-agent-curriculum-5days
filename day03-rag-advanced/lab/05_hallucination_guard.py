"""실습 3-1: Hallucination 유발 질문 테스트 → 가드레일 적용

목표
- 문서에 없는 질문에서 "프롬프트 없이"(baseline) 답변이 환각을 내는지 확인한다.
- 근거 인용 강제 + 답변 거절 + 유사도 임계값의 "가드레일" 프롬프트/로직을 적용해 비교한다.

실행
    .venv\\Scripts\\activate
    python day03-rag-advanced\\lab\\05_hallucination_guard.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.llm import get_llm  # noqa: E402
from rag_utils import build_vector_store  # noqa: E402

# 문서에 없는(정답이 없는) 질문 + 문서에 있는 질문
QUESTIONS = [
    "미래테크의 CEO 이름은 무엇인가요?",     # 문서에 없음 → 거절해야 함
    "연차는 언제 15일이 발생하나요?",        # 문서에 있음 → 정상 답변
]

BASELINE_PROMPT = """당신은 사내 문서 기반 Q&A 어시스턴트입니다. 아래 문맥을 참고해 답하세요.

[문맥]
{context}

[질문]
{question}
"""

GUARD_PROMPT = """당신은 사내 문서 기반 Q&A 어시스턴트입니다.
아래 [문맥]에 명시된 사실만 근거로 답하고, 문맥에 근거가 없으면 반드시 다음처럼 답하세요:
"제공된 문서에서 해당 정보를 찾을 수 없습니다."

[문맥]
{context}

[질문]
{question}

[출력 형식]
- 반드시 (출처: 파일명) 을 포함
- 근거 문장을 그대로 인용
"""


def build_context(docs) -> str:
    if not docs:
        return "(관련 문서 없음)"
    return "\n\n".join(f"<출처:{d.metadata['source']}>\n{d.page_content}" for d in docs)


def ask(store, question: str, prompt: str, threshold: float):
    scored = store.similarity_search_with_relevance_scores(question, k=3)
    docs = [d for d, _ in scored]
    best = max((s for _, s in scored), default=0.0)

    print(f"  · 최고 유사도 점수: {best:.3f} (임계값 {threshold})")
    if best < threshold:
        return "제공된 문서에서 해당 정보를 찾을 수 없습니다. (검색 신뢰도 부족)"

    context = build_context(docs)
    return get_llm(temperature=0.0).invoke(
        prompt.format(context=context, question=question)
    ).content


def main() -> None:
    store = build_vector_store()
    threshold = 0.25  # 문서에 없는 질문을 걸러내기 위한 임계값 (조정 가능)

    for q in QUESTIONS:
        print("\n" + "=" * 74)
        print(f"질문: {q}")
        print("=" * 74)
        print("[baseline 프롬프트 + 가드 없음]")
        ctx = build_context(store.similarity_search(q, k=3))
        print(get_llm(temperature=0.0).invoke(BASELINE_PROMPT.format(context=ctx, question=q)).content)

        print("\n[가드레일 프롬프트 + 유사도 임계값]")
        print(ask(store, q, GUARD_PROMPT, threshold))


if __name__ == "__main__":
    main()