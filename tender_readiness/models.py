"""Typed domain models for tender-readiness analysis."""

from enum import StrEnum

from pydantic import BaseModel, Field


class RequirementCategory(StrEnum):
    ELIGIBILITY = "eligibility"
    DOCUMENT = "document"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    DEADLINE = "deadline"
    SUBMISSION = "submission"
    EVALUATION = "evaluation"
    OTHER = "other"


class Requirement(BaseModel):
    id: str
    text: str = Field(min_length=1)
    category: RequirementCategory = RequirementCategory.OTHER
    source_reference: str | None = None
    evidence: str | None = None
    status: str = "needs_review"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    human_review_required: bool = True


class TenderAnalysis(BaseModel):
    title: str = "Untitled tender"
    requirements: list[Requirement] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    @property
    def requirement_count(self) -> int:
        return len(self.requirements)
