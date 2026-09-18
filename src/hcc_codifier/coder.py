"""Extracts an HCC/ICD-10 assessment from a clinical note via an LLM."""

from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI

from .config import settings
from .prompts import SYSTEM_PROMPT


def extract_assessment(clinical_note: str) -> str:
    """Run the clinical note through the coding LLM and return the assessment table.

    Args:
        clinical_note: The clinical note text, up to (but not including) the
            Assessment/Plan sections.

    Returns:
        The model's response: a table of ICD-10 code, description, and reasoning.
    """
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to your .env file.")

    messages = [
        ChatMessage(role="system", content=SYSTEM_PROMPT),
        ChatMessage(role="user", content=clinical_note),
    ]
    llm = OpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
    response = llm.chat(messages)
    return response.message.content
