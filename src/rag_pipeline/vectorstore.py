"""FAISS vector store: create from documents or pre-computed vectors, save, load, query."""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.embeddings import Embeddings

from .config import INDEX_PATH
from .embeddings import get_embeddings


def build_index(chunks: list[Document], save_path: Path = INDEX_PATH) -> FAISS:
    """Embed chunks, build a FAISS index, and persist to disk."""
    store = FAISS.from_documents(
        chunks,
        get_embeddings(),
        distance_strategy=DistanceStrategy.COSINE,
    )
    save_path.mkdir(parents=True, exist_ok=True)
    store.save_local(str(save_path))
    return store


def load_index(path: Path = INDEX_PATH) -> FAISS:
    """Load a persisted FAISS index from disk."""
    return FAISS.load_local(
        str(path),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def build_index_from_vectors(
    texts: list[str],
    vectors: list[list[float]],
    metadatas: list[dict] | None = None,
    embedding: Embeddings | None = None,
) -> FAISS:
    """Build a FAISS index from pre-computed vectors.

    Use this when embeddings already exist (e.g. stored in a database) and you
    want to avoid re-embedding. The embedding model passed here (or the default
    from get_embeddings()) is used at query time — it must match the model that
    produced the vectors.

    govscan usage:
        import numpy as np
        from rag_pipeline import build_index_from_vectors

        rows = conn.execute("SELECT id, llm_summary, embedding FROM repos ...").fetchall()
        texts   = [r["llm_summary"] for r in rows]
        vectors = [np.frombuffer(r["embedding"], dtype=np.float32).tolist() for r in rows]
        metas   = [{"source": r["id"]} for r in rows]

        store = build_index_from_vectors(texts, vectors, metas)
    """
    emb = embedding or get_embeddings()
    return FAISS.from_embeddings(
        text_embeddings=list(zip(texts, vectors)),
        embedding=emb,
        metadatas=metadatas,
        distance_strategy=DistanceStrategy.COSINE,
    )
