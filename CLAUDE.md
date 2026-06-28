# CLAUDE.md — rag-pipeline

## Project purpose

A modular RAG (Retrieval-Augmented Generation) pipeline that grounds LLM answers in a
private document corpus. The design follows a strict ingest → retrieve → generate split so
each stage is independently testable and swappable. An evaluation harness (Ragas) is
first-class — metric regressions are caught in CI before merging.

## Folder structure

```
rag-pipeline/
├── src/
│   └── rag_pipeline/
│       ├── ingest.py        # PDF loading, chunking, metadata tagging
│       ├── embeddings.py    # sentence-transformers wrapper (optional OpenAI via env)
│       ├── vectorstore.py   # FAISS index creation, save/load, metadata storage
│       ├── retriever.py     # semantic search, top-k, metadata filter, score threshold
│       ├── generator.py     # LLM call, system prompt, citations
│       ├── pipeline.py      # wires ingest → retrieve → generate end-to-end
│       ├── app.py           # Streamlit UI
│       └── config.py        # centralised settings (env vars, defaults)
├── eval/
│   ├── golden_questions.json  # labelled QA pairs for Ragas
│   └── evaluate.py            # runs Ragas metrics, writes report
├── tests/
│   ├── test_ingest.py
│   ├── test_embeddings.py
│   ├── test_vectorstore.py
│   ├── test_retriever.py
│   └── test_generator.py
├── notebooks/
│   └── exploration.ipynb    # prototyping and chunk-size experiments
├── prompts/
│   └── system_prompt.txt    # versioned system prompt (loaded by generator.py)
├── data/                    # sample PDFs for local testing (git-ignored)
├── .github/
│   └── workflows/
│       └── test.yml         # CI: lint + tests on every push
├── pyproject.toml
├── .env.example
├── .gitignore
└── CLAUDE.md
```

## Stack

| Layer         | Choice                                        |
|---------------|-----------------------------------------------|
| Orchestration | LangChain                                     |
| LLM           | OpenAI (default) or Anthropic (env-switched)  |
| Embeddings    | sentence-transformers (default), OpenAI flag  |
| Vector store  | FAISS CPU                                     |
| Evaluation    | Ragas                                         |
| UI            | Streamlit                                     |
| Packaging     | uv + pyproject.toml                           |
| CI            | GitHub Actions                                |

## Commands

```bash
uv sync                                                   # install deps
uv run python -m rag_pipeline.ingest --source ./data      # build index
uv run python -m rag_pipeline.pipeline --query "..."      # end-to-end query
uv run streamlit run src/rag_pipeline/app.py              # UI
uv run pytest                                             # all tests
uv run python -m eval.evaluate                            # Ragas eval report
```

## Key design decisions

**Chunking (interviewers always ask this):** fixed-size with overlap (default 512 tokens,
64-token overlap) so chunks are dense enough for retrieval but don't exceed context limits.
Overlap prevents a sentence split right at a boundary from making a relevant chunk
unretrievable. The size and overlap are config knobs — see `config.py`.

**Embeddings:** sentence-transformers by default so the pipeline works fully offline with
no API key. Set `EMBEDDING_PROVIDER=openai` to switch — embeddings.py gates on this env
var.

**Provider abstraction:** `generator.py` reads `LLM_PROVIDER` (`openai` | `anthropic`) and
initialises the correct LangChain chat model. The rest of the code is provider-agnostic.

**Evaluation is mandatory, not optional:** `eval/` holds a small golden QA set and a Ragas
scorer. CI runs this on every push so a prompt or retrieval change that degrades
faithfulness fails the build.

**Secrets:** nothing sensitive is committed. `.env.example` documents every required key.
The application reads from environment variables only.

## Environment variables

See `.env.example` for the full list. Required at runtime:

```
OPENAI_API_KEY        # required if LLM_PROVIDER=openai (default)
ANTHROPIC_API_KEY     # required if LLM_PROVIDER=anthropic
EMBEDDING_PROVIDER    # openai | sentence-transformers (default: sentence-transformers)
LLM_PROVIDER          # openai | anthropic (default: openai)
CHUNK_SIZE            # int, default 512
CHUNK_OVERLAP         # int, default 64
TOP_K                 # int, default 5
```

## Build / implementation order

1. `pyproject.toml` + folder scaffold + CI skeleton
2. `ingest.py` — PDF parsing, chunking, metadata
3. `embeddings.py` + `vectorstore.py` — embed and index
4. `retriever.py` + `generator.py` + `pipeline.py` — end-to-end query path
5. `eval/` — Ragas harness against golden questions
6. `app.py` — Streamlit UI on top of retrieve + generate

## Testing conventions

- Unit tests live in `tests/`, one file per module.
- Tests must not call external APIs — mock at the LangChain wrapper boundary.
- `pytest` must pass with zero network access (`--block-network` if available).
- Ragas eval (`eval/evaluate.py`) is separate from unit tests and is allowed to call APIs.

## CI (`.github/workflows/test.yml`)

Runs on every push and PR to `main`:
1. `uv sync`
2. `ruff check src/ tests/`
3. `pytest tests/`

Ragas eval is not in CI by default (costs API calls) — run it manually or on a schedule.
