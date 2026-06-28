"""Embeddings wrapper — sentence-transformers by default, openai or fastembed via env flag."""

from __future__ import annotations

from langchain_core.embeddings import Embeddings

from .config import EMBEDDING_MODEL_NAME, EMBEDDING_PROVIDER, OPENAI_API_KEY


def get_embeddings() -> Embeddings:
    """Return the configured embeddings model.

    EMBEDDING_PROVIDER=fastembed (default) — ONNX-based, offline, no torch required.
                                             Matches govscan's BAAI/bge-small-en-v1.5 model.
    EMBEDDING_PROVIDER=openai              — requires OPENAI_API_KEY.
    EMBEDDING_PROVIDER=sentence-transformers — requires pip install rag-pipeline[sentence-transformers].

    Set EMBEDDING_MODEL_NAME to override the model (default: BAAI/bge-small-en-v1.5).
    """
    if EMBEDDING_PROVIDER == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    if EMBEDDING_PROVIDER == "sentence-transformers":
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # default: fastembed
    from langchain_community.embeddings import FastEmbedEmbeddings
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts and return their vectors."""
    return get_embeddings().embed_documents(texts)
