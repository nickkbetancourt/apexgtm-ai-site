"""Optional thin FastAPI wrapper around the workflow (not required to use the CLI).

Run with: uvicorn workflows.company_research_outreach.app:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .pipeline import WorkflowError, run

app = FastAPI(title="ApexGTM Company Research & Outreach")


class ResearchOutreachRequest(BaseModel):
    company_name: str
    website: str
    force_mock: bool = False


@app.post("/research-outreach")
def research_outreach(body: ResearchOutreachRequest) -> dict:
    try:
        return run(body.company_name, body.website, force_mock=body.force_mock)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except WorkflowError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
