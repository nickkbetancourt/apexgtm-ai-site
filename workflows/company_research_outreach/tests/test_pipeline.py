import pytest

from workflows.company_research_outreach.pipeline import run


def test_run_mock_mode_returns_full_schema(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    result = run("Acme Robotics", "https://acme-robotics.example.com", force_mock=True)

    assert result["company_name"] == "Acme Robotics"
    assert result["website"] == "https://acme-robotics.example.com"
    assert result["mode"] == "mock"
    assert result["generated_at"]

    assert isinstance(result["company_summary"], str) and result["company_summary"]

    persona = result["ideal_buyer_persona"]
    for field in ("title", "department", "seniority", "description"):
        assert persona[field]

    assert len(result["pain_points"]) >= 1

    outreach = result["outreach"]
    assert outreach["cold_email"]["subject"]
    assert outreach["cold_email"]["body"]
    assert outreach["follow_up_email"]["subject"]
    assert outreach["follow_up_email"]["body"]
    assert outreach["linkedin_dm"]
    assert outreach["cold_call_opener"]

    assert result["crm_notes"]
    assert result["recommended_next_action"]


def test_run_without_api_key_falls_back_to_mock(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    result = run("Acme Robotics", "https://acme-robotics.example.com")

    assert result["mode"] == "mock"


def test_run_requires_company_name():
    with pytest.raises(ValueError):
        run("", "https://acme-robotics.example.com")


def test_run_requires_website():
    with pytest.raises(ValueError):
        run("Acme Robotics", "")


def test_run_strips_whitespace_from_inputs():
    result = run("  Acme Robotics  ", "  https://acme-robotics.example.com  ", force_mock=True)

    assert result["company_name"] == "Acme Robotics"
    assert result["website"] == "https://acme-robotics.example.com"
