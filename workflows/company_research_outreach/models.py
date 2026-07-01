"""Structured schema for the Company Research -> Outreach -> CRM workflow output."""

from typing import List

from pydantic import BaseModel


class ResearchInput(BaseModel):
    company_name: str
    website: str


class BuyerPersona(BaseModel):
    title: str
    department: str
    seniority: str
    description: str


class EmailContent(BaseModel):
    subject: str
    body: str


class OutreachContent(BaseModel):
    cold_email: EmailContent
    follow_up_email: EmailContent
    linkedin_dm: str
    cold_call_opener: str


class WorkflowOutput(BaseModel):
    company_name: str
    website: str
    generated_at: str
    mode: str  # "live" or "mock"
    company_summary: str
    ideal_buyer_persona: BuyerPersona
    pain_points: List[str]
    outreach: OutreachContent
    crm_notes: str
    recommended_next_action: str
