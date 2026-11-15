"""Markdown report rendering."""

from .checklist import build_checklist
from .models import TenderAnalysis


def render_markdown_report(analysis: TenderAnalysis) -> str:
    lines = [
        f"# Tender Readiness Report: {analysis.title}",
        "",
        "> This report is an analysis aid, not legal advice. Verify every item against the official tender and obtain qualified review where appropriate.",
        "",
        f"**Requirements identified:** {analysis.requirement_count}",
        "",
        "## Compliance checklist",
        "",
        "| ID | Category | Requirement | Status | Evidence | Source | Review |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in build_checklist(analysis.requirements):
        values = [item[key].replace("|", "\\|").replace("\n", " ") for key in ("id", "category", "requirement", "status", "evidence", "source", "review")]
        lines.append("| " + " | ".join(values) + " |")
    if analysis.warnings:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in analysis.warnings)
    return "\n".join(lines) + "\n"
