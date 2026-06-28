"""Tests for src/rag_pipeline/embeddings.py."""

import pytest


class TestGetEmbeddings:
    def test_returns_sentence_transformers_by_default(self):
        # TODO: monkeypatch EMBEDDING_PROVIDER="sentence-transformers", assert type
        pytest.skip("not implemented yet")

    def test_returns_openai_embeddings_when_configured(self):
        # TODO: monkeypatch EMBEDDING_PROVIDER="openai", assert type
        pytest.skip("not implemented yet")


class TestEmbedDocuments:
    def test_output_length_matches_input(self):
        # TODO: embed_documents(["a", "b", "c"]) returns list of length 3
        pytest.skip("not implemented yet")

    def test_vectors_are_consistent(self):
        # TODO: same input → same vector (deterministic model)
        pytest.skip("not implemented yet")
