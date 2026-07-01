"""ApexGTM MVP workflow: Company Research -> Personalized Outreach -> CRM-ready Output."""

from .pipeline import WorkflowError, run

__all__ = ["run", "WorkflowError"]
