"""실습 1-1: 모델별 동일 질문 비교 + temperature 효과

목표
- 동일한 질문을 여러 모델에 보내 응답 차이를 관찰한다.
- temperature(0 vs 1)에 따른 결정적/창의적 응답 차이를 확인한다.
- 토큰 사용량(usage)을 이해한다.

실행
    .venv\\Scripts\\activate
    python day01-generative-ai-llm-basics\\lab\\01_model_comparison.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import get_llm

QUESTION = (
    "한국 중소 제조기업이 생성형 AI를 처음 도입할 때 "
    "가장 먼저 해야 할 일을 3가지로 요약해 주세요."
)

# 계정에서 사용 가능한 모델만 남겨두세요. (예: "gpt-4o-mini", "gpt-4o")
MODELS = [
    ("gpt-4o-mini", "저비용 경량 모델"),
    ("gpt-4o", "고성능 모델"),
]


def compare_models() -> None:
    print(f"\n{'=' * 70}\n[1] 모델별 동일 질문 비교\n{'=' * 70}")
    for model, desc in MODELS:
        print(f"\n>>> {model} ({desc})")
        try:
            llm = get_llm(model=model, temperature=0.3)
            resp = llm.invoke(QUESTION)
            print(resp.content)
            usage = resp.usage_metadata or {}
            print(f"\n[사용 토큰] input={usage.get('input_tokens')} "
                  f"output={usage.get('output_tokens')}")
        except Exception as e:
            print(f"[오류] {model}: {e}")


def compare_temperature() -> None:
    print(f"\n{'=' * 70}\n[2] temperature 효과 비교 (동일 모델)\n{'=' * 70}")
    for temp in (0.0, 1.3):
        print(f"\n>>> temperature = {temp}")
        llm = get_llm(temperature=temp)
        # 온도 변화가 잘 드러나는 창의형 질문
        resp = llm.invoke("영어 시험 답신을 친근하게 시작하는 3가지 표현을 제안해")
        print(resp.content)


if __name__ == "__main__":
    compare_models()
    compare_temperature()