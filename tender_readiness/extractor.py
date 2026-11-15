"""Deterministic extraction of likely tender requirements from plain text."""

import re

from .models import Requirement, RequirementCategory

_CATEGORY_PATTERNS: list[tuple[RequirementCategory, tuple[str, ...]]] = [
    (RequirementCategory.DEADLINE, ("deadline", "closing date", "submission date", "due date")),
    (RequirementCategory.FINANCIAL, ("turnover", "revenue", "financial", "budget", "bank guarantee")),
    (RequirementCategory.DOCUMENT, ("document", "certificate", "declaration", "attachment")),
    (RequirementCategory.TECHNICAL, ("technical", "experience", "qualification", "specification")),
    (RequirementCategory.SUBMISSION, ("submit", "submission", "portal", "format")),
    (RequirementCategory.EVALUATION, ("evaluation", "scoring", "award criteria")),
    (RequirementCategory.ELIGIBILITY, ("eligible", "eligibility", "must be", "shall be")),
]


def classify_requirement(text: str) -> RequirementCategory:
    lowered = text.casefold()
    for category, keywords in _CATEGORY_PATTERNS:
        if any(keyword in lowered for keyword in keywords):
            return category
    return RequirementCategory.OTHER


def extract_requirements(text: str) -> list[Requirement]:
    """Extract requirement-like lines without pretending to interpret the tender."""
    requirements: list[Requirement] = []
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", raw_line).strip()
        if not line or len(line) < 12:
            continue
        lowered = line.casefold()
        looks_like_requirement = (
            any(token in lowered for _, tokens in _CATEGORY_PATTERNS for token in tokens)
            or any(token in lowered for token in ("required", "mandatory", "applicant", "bidder"))
        )
        if looks_like_requirement:
            requirements.append(
                Requirement(
                    id=f"REQ-{len(requirements) + 1:03d}",
                    text=line,
                    category=classify_requirement(line),
                    source_reference=f"Input line {line_number}",
                )
            )
    return requirements
