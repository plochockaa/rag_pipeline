"""rag-pipeline: modular RAG pipeline importable as a package.

Typical PDF-based usage:
    from rag_pipeline import build_index, retrieve, generate, ask

Database-backed usage (e.g. govscan — pre-computed embeddings in SQLite):
    from rag_pipeline import build_index_from_vectors, retrieve, generate
"""

from .embeddings import embed_documents, get_embeddings
from .generator import GeneratorResponse, generate, get_llm
from .pipeline import ask
from .retriever import retrieve
from .vectorstore import build_index, build_index_from_vectors, load_index

__all__ = [
    "ask",
    "build_index",
    "build_index_from_vectors",
    "embed_documents",
    "generate",
    "GeneratorResponse",
    "get_embeddings",
    "get_llm",
    "load_index",
    "retrieve",
]
