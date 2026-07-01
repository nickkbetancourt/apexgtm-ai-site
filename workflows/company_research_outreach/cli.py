"""Command-line entry point for the Company Research & Outreach workflow.

Usage:
    python -m workflows.company_research_outreach --company "Acme Robotics" --website "acme.com"
"""

import argparse
import json
import sys

from .formatter import to_human_readable
from .pipeline import WorkflowError, run


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="ApexGTM: Company Research -> Personalized Outreach -> CRM-ready Output"
    )
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--website", required=True, help="Company website URL")
    parser.add_argument(
        "--mock", action="store_true", help="Force mock mode (no API calls, no API key required)"
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Also print a human-readable summary after the JSON"
    )
    parser.add_argument("--output", help="Write the JSON output to this file path")
    args = parser.parse_args(argv)

    try:
        result = run(args.company, args.website, force_mock=args.mock)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except WorkflowError as exc:
        print(f"Workflow error: {exc}", file=sys.stderr)
        return 1

    output_json = json.dumps(result, indent=2, ensure_ascii=False)
    print(output_json)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)

    if args.pretty:
        print("\n" + to_human_readable(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
