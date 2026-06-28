"""Tests for src/rag_pipeline/ingest.py."""

import pytest


class TestChunkDocuments:
    def test_chunk_size_respected(self):
        # TODO: create a long Document, assert all chunks <= chunk_size tokens
        pytest.skip("not implemented yet")

    def test_chunk_overlap_produces_shared_content(self):
        # TODO: assert adjacent chunks share chunk_overlap worth of content
        pytest.skip("not implemented yet")

    def test_empty_document_list_returns_empty(self):
        # TODO: chunk_documents([]) == []
        pytest.skip("not implemented yet")


class TestIngest:
    def test_metadata_fields_present(self):
        # TODO: every chunk must have source, page, chunk_index, ingested_at
        pytest.skip("not implemented yet")

    def test_pdf_produces_at_least_one_chunk(self, tmp_path):
        # TODO: write a minimal PDF, call ingest(), assert len > 0
        pytest.skip("not implemented yet")
