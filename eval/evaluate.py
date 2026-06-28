"""Ragas evaluation harness against the golden question set.

Run with: uv run python -m eval.evaluate
Requires OPENAI_API_KEY (Ragas uses an LLM judge by default).
"""

from __future__ import annotations

import json
from pathlib import Path

# TODO:
# from datasets import Dataset
# from ragas import evaluate
# from ragas.metrics import answer_relevancy, context_recall, faithfulness
# from rag_pipeline.pipeline import ask

_GOLDEN_PATH = Path(__file__).parent / "golden_questions.json"


def run_evaluation() -> dict:
    """Run Ragas metrics over all golden questions and return the scores."""
    questions = json.loads(_GOLDEN_PATH.read_text())

    # TODO:
    # results = []
    # for q in questions:
    #     response = ask(q["question"])
    #     results.append({
    #         "question": q["question"],
    #         "answer": response.answer,
    #         "contexts": [c for c in response.sources],
    #         "ground_truth": q["ground_truth"],
    #     })
    # dataset = Dataset.from_list(results)
    # scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_recall])
    # return scores

    raise NotImplementedError("Implement pipeline.ask() first")


if __name__ == "__main__":
    scores = run_evaluation()
    print(scores)
