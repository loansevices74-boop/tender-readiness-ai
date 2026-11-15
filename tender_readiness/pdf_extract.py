"""Page-aware PDF text extraction."""

from dataclasses import dataclass
from io import BytesIO

from pypdf import PdfReader


@dataclass(frozen=True)
class PageText:
    page_number: int
    text: str


def extract_pdf_pages(pdf_bytes: bytes) -> list[PageText]:
    """Extract text while preserving 1-based PDF page references."""
    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
    except Exception as exc:
        raise ValueError("The uploaded file is not a readable PDF.") from exc
    return [
        PageText(page_number=number, text=(page.extract_text() or "").strip())
        for number, page in enumerate(reader.pages, start=1)
    ]
