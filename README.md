# rag-pipeline

A modular retrieval-augmented generation (RAG) pipeline for grounding LLM answers
in a private document corpus, with a built-in evaluation harness and CI.

The design mirrors patterns used to take RAG systems from prototype to production in
regulated environments: a clear ingest → retrieve → generate split, automated quality
evaluation, and reproducible builds.

## Problem

General-purpose LLMs hallucinate and can't answer questions about documents they were
never trained on. This pipeline grounds responses in a specific corpus by retrieving the
most relevant passages at query time and conditioning generation on them — improving
factuality and giving every answer a traceable source.

The goal is not just to *work* but to be **measurable**: you should be able to change a
chunking strategy, prompt, or retriever and see the effect on factuality, context recall,
and answer relevance before shipping.

## Architecture

```
                    ┌──────────────┐
   documents ─────▶ │   ingest     │  load → chunk → embed → index
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ vector store │  FAISS (local, swappable)
                    └──────┬───────┘
                           ▼
   user query ──────▶┌──────────────┐
                    │  retrieve    │  semantic search → top-k passages
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │  generate    │  prompt + context → grounded answer + sources
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │   eval       │  Ragas: faithfulness, relevance, context recall
                    └──────────────┘
```

A thin Streamlit app sits on top of `retrieve` + `generate` for interactive testing.

## Stack

| Layer            | Choice                              |
|------------------|-------------------------------------|
| Orchestration    | LangChain                           |
| LLM / embeddings | OpenAI (provider abstracted)        |
| Vector store     | FAISS (CPU)                         |
| Evaluation       | Ragas                               |
| UI               | Streamlit                           |
| Packaging        | uv + `pyproject.toml`               |
| CI               | GitHub Actions                      |

## Design decisions

- **Ingest / retrieve / generate are separate modules.** Each stage is independently
  testable and replaceable — swap FAISS for a managed vector store, or OpenAI for another
  provider, without touching the rest.
- **The LLM provider is abstracted behind config**, so the same pipeline runs against a
  cloud API locally and a different deployment (e.g. Azure OpenAI) in production.
- **Evaluation is a first-class part of the repo, not an afterthought.** `eval/` holds a
  small golden set and a Ragas-based scorer so retrieval/prompt changes are judged on
  metrics, not vibes.
- **Reproducible builds with uv** and a pinned `pyproject.toml` keep local, CI, and
  deployment environments identical.
- **Secrets stay out of the repo** — configuration is read from environment variables
  (see `.env.example`).

## Quickstart

```bash
# install uv: https://docs.astral.sh/uv/
uv sync

# set your key
cp .env.example .env   # then edit OPENAI_API_KEY

# build the index from documents in ./data
uv run python -m rag_pipeline.ingest --source ./data

# ask a question
uv run python -m rag_pipeline.generate --query "What is the refund policy?"

# or use the UI
uv run streamlit run src/rag_pipeline/app.py

# run the evaluation harness
uv run python -m eval.evaluate
```

## Project layout

```
src/rag_pipeline/   pipeline code (ingest, retrieve, generate, app, config)
eval/               evaluation harness + golden questions
tests/              unit / smoke tests
notebooks/          exploration and analysis
.github/workflows/  CI
```

## Status

Scaffold. Module bodies are stubbed and marked with `TODO`; CI runs linting and tests on
every push.
