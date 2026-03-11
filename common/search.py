"""基于 embedding 的检索公共函数。"""

from __future__ import annotations

from common.embedding import get_embeddings
from common.similarity import cosine_similarity


def search_chunks(
    query: str,
    chunks: list[str],
    embeddings: list[list[float]] | None = None,
    top_k: int = 3,
) -> list[tuple[int, float, str]]:
    """给定查询，从文本块中检索最相关的结果。"""
    if top_k <= 0:
        raise ValueError("top_k 必须大于 0")
    if not chunks:
        return []

    chunk_embeddings = embeddings if embeddings is not None else get_embeddings(chunks)
    if len(chunk_embeddings) != len(chunks):
        raise ValueError("embeddings 数量必须和 chunks 数量一致")

    query_embedding = get_embeddings([query])[0]
    results = [
        (index, cosine_similarity(query_embedding, embedding), chunk)
        for index, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings))
    ]
    results.sort(key=lambda item: item[1], reverse=True)
    return results[:top_k]
