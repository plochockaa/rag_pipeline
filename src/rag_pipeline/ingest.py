"""PDF ingestion: load → chunk → metadata-tagged Documents."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import CHUNK_OVERLAP, CHUNK_SIZE


def load_pdf(path: Path) -> list[Document]:
    """Return one Document per page with source and page metadata."""
    return PyPDFLoader(str(path)).load()


def chunk_documents(
    docs: list[Document],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[Document]:
    """Split documents into overlapping fixed-size chunks.

    Fixed-size with overlap so a sentence split exactly at a boundary doesn't
    make a relevant passage unretrievable. Size and overlap are env-var
    controlled (CHUNK_SIZE / CHUNK_OVERLAP) — see config.py.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)


def ingest(source_dir: Path) -> list[Document]:
    """Load all PDFs under source_dir, chunk, and tag metadata.

    Each chunk carries: source (filename), page, chunk_index, ingested_at (ISO timestamp).
    """
    ingested_at = datetime.now(timezone.utc).isoformat()
    chunks: list[Document] = []

    for pdf in sorted(source_dir.glob("**/*.pdf")):
        pages = load_pdf(pdf)
        doc_chunks = chunk_documents(pages)
        for i, chunk in enumerate(doc_chunks):
            chunk.metadata["source"] = pdf.name
            chunk.metadata["chunk_index"] = i
            chunk.metadata["ingested_at"] = ingested_at
            chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    result = ingest(args.source)
    print(f"Ingested {len(result)} chunks from {args.source}")
