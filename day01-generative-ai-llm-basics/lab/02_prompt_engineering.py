"""실습 1-2: 프롬프트 엔지니어링 4가지 기법

기법 목록
1. 역할 지정 (Role Prompting)
2. Few-shot (예시 학습)
3. 사고의 사슬 (CoT, Chain-of-Thought)
4. JSON 구조화 출력 (Structured Output)

실행
    .venv\\Scripts\\activate
    python day01-generative-ai-llm-basics\\lab\\02_prompt_engineering.py
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import get_llm


def role_prompting() -> None:
    print(f"\n{'=' * 70}\n[1] 역할 지정\n{'=' * 70}")
    llm = get_llm(temperature=0.0)
    result = llm.invoke(
        [
            # 1. 역할 부여
            ("system", "당신은 보안 지침에 능숙한 기업 정보보호 담당자입니다. "
                       "답변은 '보안 관점'에서 우선하고, 공식적 어조를 유지하세요."),
            # 2. 실제 요청
            ("human", "사내 문서를 직원 개인 클라우드에 저장해도 될까요?"),
        ]
    )
    print(result.content)


def few_shot() -> None:
    print(f"\n{'=' * 70}\n[2] Few-shot (예시로 형식 학습)\n{'=' * 70}")
    llm = get_llm(temperature=0.0)
    result = llm.invoke(
        [
            ("system", "입력 문장을 감정(name, reason) 2가지로 단답형으로 분류한다."),
            # 예시 2개로 원하는 형식을 알려준다
            ("human", "급여 명세서가 늦어져서 속상합니다."),
            ("assistant", "분노/불만, 급여 지연"),
            ("human", "새 노트북이 너무 마음에 들어요."),
            ("assistant", "만족, 장비 제공"),
            ("human", "고객이 계약서를 계속 미루고 있어서 걱정됩니다."),
        ]
    )
    print(result.content)


def chain_of_thought() -> None:
    print(f"\n{'=' * 70}\n[3] 사고의 사슬 (CoT)\n{'=' * 70}")
    llm = get_llm(temperature=0.0)
    # '단계적으로 생각해' 지시를 추가해 추론을 유도
    result = llm.invoke(
        "주말(토,일) 제외 영업일 기준으로, "
        "3월 1일(보통 공휴일이라 가정) 다음 영업일이 보고 마감일이면 제공 기한을 계산해. "
        "단계적으로 계산해주세요."
    )
    print(result.content)


def structured_output() -> None:
    print(f"\n{'=' * 70}\n[4] JSON 구조화 출력\n{'=' * 70}")
    llm = get_llm(temperature=0.0)
    result = llm.invoke(
        "다음 문장에서 요구사항을 추출해 JSON으로만 응답하세요.\n"
        "문장: 새 계약서를 최대한 빨리 검토해주시고, 예상 비용과 검토 기간을 말씀해주세요.\n"
        "필드: {task, is_urgent, amount, duration_days} (is_urgent는 bool, "
        "명시되지 않은 필드는 null)"
    )
    print(result.content)

    # 실제 파싱
    data = json.loads(result.content)
    print(f"\n[파싱 결과] task={data['task']}, is_urgent={data['is_urgent']}")


if __name__ == "__main__":
    role_prompting()
    few_shot()
    chain_of_thought()
    structured_output()