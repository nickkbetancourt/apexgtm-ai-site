"""Environment configuration for the company research & outreach workflow."""

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str | None
    anthropic_model: str
    request_timeout_seconds: float
    force_mock: bool

    @property
    def use_mock(self) -> bool:
        return self.force_mock or not self.anthropic_api_key


def get_settings() -> Settings:
    """Build a fresh Settings object from the current environment.

    Read at call time (not import time) so tests can monkeypatch env vars
    and callers can force mock mode without mutating process state.
    """
    return Settings(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") or None,
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5"),
        request_timeout_seconds=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10")),
        force_mock=os.getenv("APEX_FORCE_MOCK", "false").strip().lower() == "true",
    )
