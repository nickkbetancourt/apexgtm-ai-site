"""Deterministic mock content used when no API key is configured (or on LLM failure).

Keeps the workflow fully testable and runnable offline.
"""


def build_mock_content(company_name: str, website: str) -> dict:
    return {
        "company_summary": (
            f"{company_name} ({website}) is a growing software company. "
            "[MOCK DATA] This summary is a placeholder — configure ANTHROPIC_API_KEY "
            "to generate a real, research-backed summary."
        ),
        "ideal_buyer_persona": {
            "title": "VP of Sales",
            "department": "Sales",
            "seniority": "VP",
            "description": (
                f"Owns revenue growth at {company_name} and is evaluating ways to "
                "scale outbound pipeline without growing headcount."
            ),
        },
        "pain_points": [
            "Manual prospecting is slow and inconsistent across reps",
            "Outbound volume doesn't scale with current headcount",
            "Personalizing outreach at scale is hard to maintain",
        ],
        "outreach": {
            "cold_email": {
                "subject": f"Quick idea for {company_name}'s pipeline",
                "body": (
                    f"Hi {{first_name}},\n\n"
                    f"Noticed {company_name} is scaling its go-to-market motion. "
                    "ApexGTM helps AI software companies generate qualified pipeline "
                    "through AI-powered outbound, without adding headcount.\n\n"
                    "Worth a quick chat this week?\n\nBest,\n{sender_name}"
                ),
            },
            "follow_up_email": {
                "subject": f"Re: Quick idea for {company_name}'s pipeline",
                "body": (
                    "Hi {first_name},\n\n"
                    "Following up in case this got buried. Happy to share a couple "
                    "of examples of how we've helped similar teams generate pipeline "
                    "faster.\n\nBest,\n{sender_name}"
                ),
            },
            "linkedin_dm": (
                f"Hi {{first_name}}, saw {company_name} is growing fast — curious if "
                "scaling outbound pipeline is on your radar this quarter?"
            ),
            "cold_call_opener": (
                f"Hi {{first_name}}, this is {{sender_name}} from ApexGTM — I'll be quick. "
                f"We help GTM teams at AI companies like {company_name} generate qualified "
                "pipeline without adding headcount. Is that worth 15 minutes on your calendar?"
            ),
        },
        "crm_notes": (
            f"[MOCK DATA] Researched {company_name} ({website}). "
            "Persona: VP of Sales. Primary pain point: scaling outbound without "
            "more headcount. Draft outreach sequence generated and ready for review."
        ),
        "recommended_next_action": (
            "Send the cold email, wait 3 business days, then follow up via LinkedIn DM."
        ),
    }
