"""Thin wrapper around the Anthropic API for structured JSON generation."""

import json

from .config import Settings


class LLMError(Exception):
    """Raised when the LLM call fails or returns content the workflow can't use."""


def generate_structured_response(prompt: str, settings: Settings) -> dict:
    try:
        import anthropic
    except ImportError as exc:
        raise LLMError("The 'anthropic' package is not installed") from exc

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    try:
        message = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # network, auth, rate-limit, etc.
        raise LLMError(f"Anthropic API call failed: {exc}") from exc

    if not message.content:
        raise LLMError("Anthropic API returned an empty response")

    raw_text = message.content[0].text

    try:
        return json.loads(_extract_json(raw_text))
    except (json.JSONDecodeError, ValueError) as exc:
        raise LLMError(f"Failed to parse LLM response as JSON: {exc}") from exc


def _extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in LLM response")
    return text[start : end + 1]
