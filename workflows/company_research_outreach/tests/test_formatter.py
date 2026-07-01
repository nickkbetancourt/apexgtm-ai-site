from workflows.company_research_outreach.formatter import to_human_readable
from workflows.company_research_outreach.pipeline import run


def test_to_human_readable_contains_key_sections():
    result = run("Acme Robotics", "https://acme-robotics.example.com", force_mock=True)

    text = to_human_readable(result)

    assert "Acme Robotics" in text
    assert "Ideal Buyer Persona" in text
    assert "Pain Points ApexGTM Can Solve" in text
    assert "Cold Email" in text
    assert "Follow-Up Email" in text
    assert "LinkedIn DM" in text
    assert "Cold Call Opener" in text
    assert "CRM Notes" in text
    assert "Recommended Next Action" in text
