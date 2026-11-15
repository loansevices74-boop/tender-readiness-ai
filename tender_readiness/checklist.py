"""Checklist generation with conservative, administrator-review defaults."""

from .models import Requirement


def build_checklist(requirements: list[Requirement]) -> list[dict[str, str]]:
    return [
        {
            "id": requirement.id,
            "category": requirement.category.value,
            "requirement": requirement.text,
            "status": requirement.status,
            "evidence": requirement.evidence or "Not provided",
            "source": requirement.source_reference or "Not provided",
            "review": "Required" if requirement.human_review_required else "Not required",
        }
        for requirement in requirements
    ]
