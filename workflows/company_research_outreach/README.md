# Company Research -> Personalized Outreach -> CRM-ready Output

The first production-ready ApexGTM module. Input a company name and website;
get back structured, CRM-ready research and personalized outreach content.

This is intentionally a single, simple pipeline — not a multi-agent system.
It does one job well: turn a company name + website into everything a rep
needs to start a sequence.

## What it produces

Given `company_name` and `website`, the workflow returns one JSON object with:

1. Company summary
2. Ideal buyer/persona
3. Pain points ApexGTM can solve
4. Personalized cold email
5. Follow-up email
6. LinkedIn DM
7. Cold call opener
8. CRM-ready notes
9. Recommended next action

See [`samples/sample_input.json`](samples/sample_input.json) and
[`samples/sample_output.json`](samples/sample_output.json) for a full example.

## How it works

```
company_name, website
        |
        v
research.py       -- best-effort fetch of the company's homepage text
        |
        v
generator.py       -- builds a prompt, calls the LLM (or mock_data.py if no
        |              API key / on failure), returns one JSON object
        v
pipeline.py        -- validates the JSON against models.py, stamps metadata
        |              (generated_at, mode), falls back to mock on bad output
        v
cli.py / app.py     -- CLI prints JSON (+ optional human-readable summary);
                        FastAPI wrapper exposes the same thing over HTTP
```

Folder structure:

```
workflows/company_research_outreach/
  __init__.py         # exposes run()
  __main__.py         # `python -m workflows.company_research_outreach`
  config.py           # env var loading
  models.py           # pydantic schema for the output
  research.py         # website text fetch (best-effort, no hard dependency)
  mock_data.py         # deterministic offline content
  llm_client.py         # Anthropic API call + JSON extraction
  generator.py         # prompt building + live/mock switch
  pipeline.py         # orchestration, validation, fallback
  formatter.py         # JSON -> human-readable text
  cli.py             # command-line interface
  app.py             # optional FastAPI wrapper (one endpoint)
  requirements.txt / requirements-dev.txt
  .env.example
  samples/           # sample input/output
  tests/             # pytest suite (runs fully offline in mock mode)
```

## Setup

From the repo root:

```bash
pip install -r workflows/company_research_outreach/requirements.txt
cp workflows/company_research_outreach/.env.example workflows/company_research_outreach/.env
# then edit .env and add your ANTHROPIC_API_KEY
```

If `ANTHROPIC_API_KEY` is not set, the workflow automatically runs in **mock
mode** and returns realistic placeholder content — no API key required to
try it out or run the tests.

## Running it

CLI (from the repo root):

```bash
python -m workflows.company_research_outreach \
  --company "Acme Robotics" \
  --website "https://acme-robotics.example.com"
```

Flags:

- `--mock` - force mock mode even if an API key is configured
- `--pretty` - also print a human-readable summary after the JSON
- `--output path.json` - write the JSON result to a file

Example with the human-readable summary:

```bash
python -m workflows.company_research_outreach \
  --company "Acme Robotics" \
  --website "acme-robotics.example.com" \
  --mock --pretty
```

As an HTTP API (optional):

```bash
pip install uvicorn
uvicorn workflows.company_research_outreach.app:app --reload
curl -X POST http://127.0.0.1:8000/research-outreach \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Acme Robotics", "website": "acme-robotics.example.com"}'
```

As a Python import:

```python
from workflows.company_research_outreach import run

result = run("Acme Robotics", "https://acme-robotics.example.com")
```

## Sample input / output

Input ([`samples/sample_input.json`](samples/sample_input.json)):

```json
{
  "company_name": "Acme Robotics",
  "website": "https://acme-robotics.example.com"
}
```

Output (mock mode; see [`samples/sample_output.json`](samples/sample_output.json)
for the full file):

```json
{
  "company_name": "Acme Robotics",
  "website": "https://acme-robotics.example.com",
  "generated_at": "2026-07-01T11:56:50.063907+00:00",
  "mode": "mock",
  "company_summary": "...",
  "ideal_buyer_persona": { "title": "VP of Sales", "...": "..." },
  "pain_points": ["...", "...", "..."],
  "outreach": {
    "cold_email": { "subject": "...", "body": "..." },
    "follow_up_email": { "subject": "...", "body": "..." },
    "linkedin_dm": "...",
    "cold_call_opener": "..."
  },
  "crm_notes": "...",
  "recommended_next_action": "..."
}
```

## Environment variables

See [`.env.example`](.env.example):

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | No | unset | Enables live generation. Falls back to mock data if unset. |
| `ANTHROPIC_MODEL` | No | `claude-sonnet-5` | Model used for generation. |
| `APEX_FORCE_MOCK` | No | `false` | Force mock mode regardless of API key. |
| `REQUEST_TIMEOUT_SECONDS` | No | `10` | Timeout for fetching the prospect's website. |

## Error handling

- Missing `company_name` or `website` raises `ValueError` before any API call.
- Website fetch failures (timeout, DNS, non-200, etc.) are swallowed and just
  result in less context for the prompt - never a hard failure.
- LLM call failures or malformed LLM JSON are caught, logged as a warning,
  and the workflow falls back to mock content instead of crashing.
- LLM output that doesn't match the expected schema is also caught and
  replaced with mock content, so the CLI/API always returns a valid,
  fully-shaped result.

## Testing

```bash
pip install -r workflows/company_research_outreach/requirements-dev.txt
python -m pytest workflows/company_research_outreach/tests -v
```

All tests run in mock mode, so no API key or network access is required.

## What's next (not built yet)

- Wire the CRM notes / recommended next action into an actual HubSpot object
  (currently returns text only, no CRM write).
- Add a lightweight caching layer so re-running the same company doesn't
  re-fetch the website or re-call the LLM.
- Add richer company research (e.g. news, funding, tech stack) once basic
  usage validates the outreach quality is good enough to act on.
- Add auth to `app.py` before exposing it beyond local use.

## Known limitations

- Website research is a single best-effort homepage fetch with basic HTML
  stripping - no JS rendering, no crawling beyond the homepage.
- Live mode depends on the LLM returning valid JSON; malformed output falls
  back to mock content rather than retrying the call.
- No persistence - every run is stateless; nothing is saved unless you pass
  `--output` or wire it into a CRM yourself.
