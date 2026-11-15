from tender_readiness.checklist import build_checklist
from tender_readiness.extractor import classify_requirement, extract_requirements
from tender_readiness.models import RequirementCategory


SAMPLE_TEXT = """
The bidder must submit a valid tax certificate.
Applicants must demonstrate technical experience in public works.
The financial turnover requirement is 10 million.
Submission deadline: 31 December 2026.
"""


def test_classify_requirement():
    assert classify_requirement("The bidder must submit a valid tax certificate.") == RequirementCategory.DOCUMENT
    assert classify_requirement("Submission deadline: 31 December 2026.") == RequirementCategory.DEADLINE


def test_extract_requirements_is_deterministic():
    first = extract_requirements(SAMPLE_TEXT)
    second = extract_requirements(SAMPLE_TEXT)
    assert first == second
    assert len(first) == 4
    assert first[0].id == "REQ-001"


def test_build_checklist_defaults_to_review():
    items = build_checklist(extract_requirements(SAMPLE_TEXT))
    assert items[0]["status"] == "needs_review"
    assert items[0]["review"] == "Required"
