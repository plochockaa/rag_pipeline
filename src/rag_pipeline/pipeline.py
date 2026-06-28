"""End-to-end pipeline: question in → grounded answer with citations out."""

from __future__ import annotations

from pathlib import Path

from .generator import GeneratorResponse, generate
from .retriever import retrieve
from .vectorstore import load_index


def ask(query: str, index_path: Path | None = None) -> GeneratorResponse:
    """Load the vector store, retrieve relevant chunks, and generate a grounded answer."""
    store = load_index(index_path) if index_path else load_index()
    docs = retrieve(store, query)
    return generate(query, docs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--index", type=Path, default=None)
    args = parser.parse_args()

    response = ask(args.query, index_path=args.index)
    print(response.answer)
    print("\nSources:", ", ".join(response.sources))
