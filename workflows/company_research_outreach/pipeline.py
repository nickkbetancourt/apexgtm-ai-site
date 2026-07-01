"""Orchestrates Company Research -> Personalized Outreach -> CRM-ready Output."""

import logging
from dataclasses import replace
from datetime import datetime, timezone

from pydantic import ValidationError

from . import mock_data
from .config import get_settings
from .generator import generate_content
from .models import WorkflowOutput
from .research import fetch_website_text

logger = logging.getLogger(__name__)


class WorkflowError(Exception):
    """Raised when the workflow cannot produce a usable result."""


def run(company_name: str, website: str, force_mock: bool = False) -> dict:
    """Run the full workflow and return a JSON-serializable dict matching WorkflowOutput."""
    if not company_name or not company_name.strip():
        raise ValueError("company_name is required")
    if not website or not website.strip():
        raise ValueError("website is required")

    company_name = company_name.strip()
    website = website.strip()

    settings = get_settings()
    if force_mock:
        settings = replace(settings, force_mock=True)

    website_text = None
    if not settings.use_mock:
        website_text = fetch_website_text(website, timeout=settings.request_timeout_seconds)

    content, mode = generate_content(company_name, website, website_text, settings)

    output = _build_output(company_name, website, mode, content)
    if output is None:
        # Content came back live but failed schema validation - fall back to mock
        # rather than surfacing a broken result to the caller.
        content = mock_data.build_mock_content(company_name, website)
        output = _build_output(company_name, website, "mock", content)
        if output is None:
            raise WorkflowError("Failed to build workflow output from mock data")

    return output.model_dump()


def _build_output(company_name: str, website: str, mode: str, content: dict):
    try:
        return WorkflowOutput(
            company_name=company_name,
            website=website,
            generated_at=datetime.now(timezone.utc).isoformat(),
            mode=mode,
            **content,
        )
    except (ValidationError, TypeError) as exc:
        logger.warning("Generated content failed schema validation: %s", exc)
        return None
