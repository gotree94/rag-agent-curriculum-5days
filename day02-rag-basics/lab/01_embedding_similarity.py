"""실습 2-1: 임베딩과 코사인 유사도 확인 + 시각화

목표
- 문장을 임베딩 벡터로 변환하고 코사인 유사도를 직접 계산한다.
- 의미적으로 유사/비유사한 문장의 유사도 값을 비교한다.
- PCA로 2차원 투영해 시각적으로 확인한다.

실행
    .venv\\Scripts\\activate
    python day02-rag-basics\\lab\\01_embedding_similarity.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
from common.llm import get_embeddings

SENTENCES = [
    "연차는 입사 1년이 되는 날 15일이 발생합니다.",
    "입사 후 1년 미만은 매월 1일씩 연차가 발생합니다.",
    "출장 숙박비는 1박 최대 15만 원까지 정산됩니다.",
    "고양이가 창가에서 낮잠을 자고 있습니다.",
]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


def main() -> None:
    vectors = get_embeddings().embed_documents(SENTENCES)
    vec = np.array(vectors)

    print("문장 목록:")
    for i, s in enumerate(SENTENCES):
        print(f"  {i}: {s}")

    print("\n[코사인 유사도 행렬]")
    n = len(SENTENCES)
    for i in range(n):
        row = " ".join(f"{cosine_similarity(vec[i], vec[j]):.3f}" for j in range(n))
        print(f"  문장{i} | {row}")

    print("\n해석: 문장0-1(연차), 1-2(30%대), 3(무관)을 비교하세요.")

    # PCA 2차원 투영 시각화
    mean = vec.mean(axis=0)
    centered = vec - mean
    cov = centered.T @ centered
    eigval, eigvec = np.linalg.eigh(cov)
    top2 = eigvec[:, -2:]  # 상위 2개 주성분
    proj = centered @ top2

    plt.figure(figsize=(8, 6))
    for i, (x, y) in enumerate(proj):
        plt.scatter(x, y, s=120, c=f"C{i}")
        plt.annotate(f"S{i}: {SENTENCES[i][:18]}...", (x, y), textcoords="offset points", xytext=(8, 6))
    plt.axhline(0, color="gray", linewidth=0.5)
    plt.axvline(0, color="gray", linewidth=0.5)
    plt.title("문장 임베딩의 PCA 2D 투영")
    plt.tight_layout()
    plt.savefig(Path(__file__).with_name("embedding_pca.png"), dpi=120)
    print("\n[저장] embedding_pca.png 확인")


if __name__ == "__main__":
    main()