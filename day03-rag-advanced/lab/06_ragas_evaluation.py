"""실습 3-5: RAGAS로 RAG 품질 정량 평가

평가 파이프라인
- eval_questions.json (질문 + ground_truth)을 로드한다.
- v1 RAG 파이프라인을 실행해 답변 + 검색 문맥을 수집한다.
- RAGAS 지표(faithfulness, answer_relevancy, context_precision, context_recall) 평가.

※ RAGAS는 평가용 LLM 호출이 많아 비용이 발생합니다. 처음엔 3문항만 평가합니다.

실행
    .venv\\Scripts\\activate
    python day03-rag-advanced\\lab\\06_ragas_evaluation.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[1]))
from common.llm import get_embeddings, get_llm  # noqa: E402
from rag_utils import build_vector_store, load_eval_questions  # noqa: E402

PROMPT = """아래 문맥만 근거로 질문에 답하세요. 문맥에 없으면 "문서에서 찾을 수 없습니다"라고 하세요.

[문맥]
{context}

[질문]
{question}
"""


def run_rag(store, question: str):
    docs = store.similarity_search(question, k=4)
    context = "\n\n".join(d.page_content for d in docs)
    answer = get_llm(temperature=0.0).invoke(
        PROMPT.format(context=context, question=question)
    ).content
    return answer, [d.page_content for d in docs]


def main() -> None:
    store = build_vector_store()
    eval_items = load_eval_questions()[:3]  # 비용 절감을 위해 3문항만

    from ragas import EvaluationDataset, SingleTurnSample, evaluate
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.llms import LangchainLLMWrapper
    from ragas.metrics import (
        answer_relevancy,
        context_precision,
        context_recall,
        faithfulness,
    )

    samples = []
    for item in eval_items:
        answer, contexts = run_rag(store, item["question"])
        print(f"\nQ: {item['question']}\nA: {answer[:120]}...")
        samples.append(
            SingleTurnSample(
                user_input=item["question"],
                response=answer,
                retrieved_contexts=contexts,
                reference=item["ground_truth"],
            )
        )

    dataset = EvaluationDataset(samples=samples)
    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=LangchainLLMWrapper(get_llm(temperature=0.0)),
        embeddings=LangchainEmbeddingsWrapper(get_embeddings()),
    )
    print("\n" + "=" * 74)
    print("[RAGAS 평가 결과 — v1]")
    print("=" * 74)
    print(result)

    df = result.to_pandas()
    out = Path(__file__).with_name("ragas_report_v1.csv")
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"\n[저장] {out.name}")


if __name__ == "__main__":
    main()