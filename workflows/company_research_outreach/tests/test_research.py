from workflows.company_research_outreach.research import fetch_website_text


def test_fetch_website_text_returns_none_for_empty_url():
    assert fetch_website_text("") is None
    assert fetch_website_text(None) is None


def test_fetch_website_text_returns_none_on_unreachable_host():
    assert fetch_website_text("http://this-domain-should-not-resolve.invalid", timeout=2) is None
