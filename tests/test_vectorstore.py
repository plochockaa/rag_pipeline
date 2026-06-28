"""Tests for src/rag_pipeline/vectorstore.py."""

import pytest


class TestBuildIndex:
    def test_index_saved_to_disk(self, tmp_path):
        # TODO: build_index(chunks, save_path=tmp_path/"idx"), assert path exists
        pytest.skip("not implemented yet")

    def test_roundtrip_save_load(self, tmp_path):
        # TODO: build_index then load_index, assert same number of vectors
        pytest.skip("not implemented yet")


class TestLoadIndex:
    def test_raises_on_missing_path(self, tmp_path):
        # TODO: load_index(tmp_path / "nonexistent") raises FileNotFoundError
        pytest.skip("not implemented yet")
