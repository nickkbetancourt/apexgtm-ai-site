"""Converts the structured workflow JSON output into a human-readable summary."""


def to_human_readable(result: dict) -> str:
    persona = result["ideal_buyer_persona"]
    outreach = result["outreach"]
    pain_points = "\n".join(f"  - {p}" for p in result["pain_points"])

    return f"""ApexGTM Research & Outreach Summary
=====================================
Company: {result['company_name']} ({result['website']})
Mode: {result['mode']}
Generated: {result['generated_at']}

Company Summary:
  {result['company_summary']}

Ideal Buyer Persona:
  {persona['title']} - {persona['department']} ({persona['seniority']})
  {persona['description']}

Pain Points ApexGTM Can Solve:
{pain_points}

Cold Email:
  Subject: {outreach['cold_email']['subject']}
  {outreach['cold_email']['body']}

Follow-Up Email:
  Subject: {outreach['follow_up_email']['subject']}
  {outreach['follow_up_email']['body']}

LinkedIn DM:
  {outreach['linkedin_dm']}

Cold Call Opener:
  {outreach['cold_call_opener']}

CRM Notes:
  {result['crm_notes']}

Recommended Next Action:
  {result['recommended_next_action']}
"""
