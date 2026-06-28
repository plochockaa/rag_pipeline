"""Tests for src/rag_pipeline/generator.py."""

import pytest


class TestGenerate:
    def test_response_contains_answer_and_sources(self):
        # TODO: mock LLM, assert response.answer != "" and response.sources is list
        pytest.skip("not implemented yet")

    def test_sources_deduplicated(self):
        # TODO: two chunks from same file → sources list has one entry
        pytest.skip("not implemented yet")

    def test_does_not_call_llm_with_empty_context(self):
        # TODO: generate(query, []) raises ValueError before hitting the API
        pytest.skip("not implemented yet")


class TestGetLlm:
    def test_returns_openai_by_default(self):
        # TODO: monkeypatch LLM_PROVIDER="openai", assert type is ChatOpenAI
        pytest.skip("not implemented yet")

    def test_returns_anthropic_when_configured(self):
        # TODO: monkeypatch LLM_PROVIDER="anthropic", assert type is ChatAnthropic
        pytest.skip("not implemented yet")
