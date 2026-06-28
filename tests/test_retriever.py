"""Tests for src/rag_pipeline/retriever.py."""

import pytest


class TestRetrieve:
    def test_returns_at_most_k_results(self):
        # TODO: mock FAISS store, assert len(retrieve(store, query, k=3)) <= 3
        pytest.skip("not implemented yet")

    def test_score_threshold_filters_low_scores(self):
        # TODO: set threshold high enough that low-score chunks are dropped
        pytest.skip("not implemented yet")

    def test_metadata_filter_applied(self):
        # TODO: insert chunks from two sources, filter to one, assert only that source returned
        pytest.skip("not implemented yet")

    def test_empty_store_returns_empty_list(self):
        # TODO: retrieve against empty index returns []
        pytest.skip("not implemented yet")
