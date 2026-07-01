"""Builds the research+outreach prompt and generates content (live or mock)."""

import logging
from typing import Optional, Tuple

from . import mock_data
from .config import Settings
from .llm_client import LLMError, generate_structured_response

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """You are a B2B GTM research analyst working for ApexGTM.

ApexGTM helps AI software companies generate qualified pipeline through
AI-powered outbound, sales automation, and GTM strategy.

Research the following prospect and produce personalized outreach content.

Company name: {company_name}
Website: {website}
Website content excerpt (may be partial or unavailable): {website_text}

Return ONLY a single valid JSON object (no markdown, no commentary) with
exactly these keys:

- "company_summary": string, 2-4 sentences describing what the company does.
- "ideal_buyer_persona": object with "title", "department", "seniority", "description".
- "pain_points": array of 3-5 strings describing pain points ApexGTM can solve.
- "outreach": object with:
    - "cold_email": object with "subject" and "body"
    - "follow_up_email": object with "subject" and "body"
    - "linkedin_dm": string
    - "cold_call_opener": string
- "crm_notes": string, a concise CRM-ready note summarizing the research and outreach plan.
- "recommended_next_action": string, the single best next step for the rep.

Use "{{first_name}}" and "{{sender_name}}" as placeholders for personalization
fields the rep will fill in. Keep outreach concise, specific to the company,
and free of generic filler. Do not include any text outside the JSON object.
"""


def build_prompt(company_name: str, website: str, website_text: Optional[str]) -> str:
    return PROMPT_TEMPLATE.format(
        company_name=company_name,
        website=website,
        website_text=website_text or "Not available.",
    )


def generate_content(
    company_name: str,
    website: str,
    website_text: Optional[str],
    settings: Settings,
) -> Tuple[dict, str]:
    """Return (content_dict, mode) where mode is 'live' or 'mock'."""
    if settings.use_mock:
        return mock_data.build_mock_content(company_name, website), "mock"

    prompt = build_prompt(company_name, website, website_text)
    try:
        content = generate_structured_response(prompt, settings)
        return content, "live"
    except LLMError as exc:
        logger.warning(
            "LLM generation failed for %s (%s); falling back to mock data", company_name, exc
        )
        return mock_data.build_mock_content(company_name, website), "mock"
