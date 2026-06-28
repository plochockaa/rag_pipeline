"""Semantic retrieval: top-k search with optional score threshold and metadata filtering."""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from .config import SCORE_THRESHOLD, TOP_K


def retrieve(
    store: FAISS,
    query: str,
    k: int = TOP_K,
    score_threshold: float | None = SCORE_THRESHOLD,
    filter: dict | None = None,
) -> list[Document]:
    """Return the top-k most relevant chunks for query.

    Args:
        store: FAISS index (from build_index, load_index, or build_index_from_vectors).
        query: user question string.
        k: number of chunks to return.
        score_threshold: drop chunks with relevance score below this (0–1, higher = stricter).
                         Defaults to SCORE_THRESHOLD env var, or None (no filtering).
        filter: metadata key/value pairs to restrict the search, e.g. {"source": "policy.pdf"}.
    """
    if score_threshold is not None:
        results = store.similarity_search_with_relevance_scores(
            query, k=k, filter=filter, score_threshold=score_threshold
        )
        return [doc for doc, _ in results]
    return store.similarity_search(query, k=k, filter=filter)
