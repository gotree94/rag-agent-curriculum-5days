"""공용 헬퍼 모듈.

모든 일차 실습 스크립트가 이 모듈을 통해 LLM/임베딩을 일관되게 생성한다.
사용법(각 실습 스크립트 상단):

    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[2]))  # 저장소 루트
    from common.llm import get_llm, get_embeddings

API 키/모델은 저장소 루트의 .env 파일에서 읽는다.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA_DIR = PROJECT_ROOT / "00-environment" / "sample-data"

load_dotenv(PROJECT_ROOT / ".env")


def get_llm(model: str | None = None, temperature: float = 0.2, max_tokens: int | None = None):
    """OpenAI 호환 ChatOpenAI 인스턴스를 반환한다.

    - 기본: OPENAI_API_KEY + LLM_MODEL(.env)
    - LLM_BASE_URL을 채우면 해당 엔드포인트(Ollama, 게이트웨이 등)로 우회한다.
    """
    from langchain_openai import ChatOpenAI

    model = model or os.getenv("LLM_MODEL", "gpt-4o-mini")
    kwargs: dict = {
        "model": model,
        "temperature": temperature,
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
    base_url = os.getenv("LLM_BASE_URL", "").strip()
    if base_url:
        kwargs["base_url"] = base_url
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    return ChatOpenAI(**kwargs)


def get_embeddings(model: str | None = None):
    """OpenAI 임베딩 모델 인스턴스를 반환한다."""
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=model or os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )