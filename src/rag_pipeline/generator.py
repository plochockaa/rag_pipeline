"""LLM generation: context + query → grounded answer with source citations."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document

from .config import ANTHROPIC_API_KEY, GEMINI_API_KEY, LLM_PROVIDER, OPENAI_API_KEY

_SYSTEM_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "system_prompt.txt"


@dataclass
class GeneratorResponse:
    answer: str
    sources: list[str] = field(default_factory=list)  # deduplicated source identifiers


def get_llm() -> BaseChatModel:
    """Return the configured LangChain chat model.

    LLM_PROVIDER=openai    (default) — requires OPENAI_API_KEY.
    LLM_PROVIDER=anthropic           — requires ANTHROPIC_API_KEY.
    LLM_PROVIDER=gemini              — requires GEMINI_API_KEY. Install: pip install rag-pipeline[google]
    """
    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model="claude-sonnet-4-6", api_key=ANTHROPIC_API_KEY)

    if LLM_PROVIDER == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)

    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)


def _build_context(docs: list[Document]) -> str:
    parts = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "")
        label = f"[{source}, page {page}]" if page != "" else f"[{source}]"
        parts.append(f"{label}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def generate(query: str, context_docs: list[Document]) -> GeneratorResponse:
    """Call the LLM with retrieved context and return a grounded answer with citations.

    Raises ValueError if context_docs is empty — the pipeline should always retrieve
    before generating to avoid hallucination.

    The system prompt is loaded from prompts/system_prompt.txt so it can be
    versioned and swapped without touching Python code.
    """
    if not context_docs:
        raise ValueError("context_docs is empty — retrieve documents before calling generate")

    system_prompt = _SYSTEM_PROMPT_PATH.read_text().replace(
        "{context}", _build_context(context_docs)
    )

    llm = get_llm()
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=query),
    ])

    # Deduplicate sources while preserving order
    seen: set[str] = set()
    sources: list[str] = []
    for doc in context_docs:
        s = doc.metadata.get("source", "unknown")
        if s not in seen:
            seen.add(s)
            sources.append(s)

    return GeneratorResponse(answer=str(response.content), sources=sources)
