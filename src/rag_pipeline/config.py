import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 512))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 64))
TOP_K: int = int(os.getenv("TOP_K", 5))
SCORE_THRESHOLD: float | None = (
    float(os.getenv("SCORE_THRESHOLD")) if os.getenv("SCORE_THRESHOLD") else None
)

# Embeddings — fastembed (default, ONNX-based, no torch) | openai | sentence-transformers
EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "fastembed")
# Model name used by sentence-transformers or fastembed providers
EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-en-v1.5")

# LLM — openai | anthropic | gemini
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")

OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

INDEX_PATH: Path = Path(os.getenv("INDEX_PATH", "data/faiss_index"))
