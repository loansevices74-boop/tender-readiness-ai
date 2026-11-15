"""Streamlit entry point for the tender-readiness MVP."""

import streamlit as st

from tender_readiness.extractor import extract_requirements, extract_requirements_from_pages
from tender_readiness.models import TenderAnalysis
from tender_readiness.pdf_extract import extract_pdf_pages
from tender_readiness.report import render_markdown_report

st.set_page_config(page_title="Tender Readiness AI", page_icon="✅", layout="wide")
st.title("Tender Readiness AI")
st.caption("Tender-readiness and document-analysis tool — not legal advice")

with st.sidebar:
    st.header("Administrator")
    st.info("All findings require administrator review before delivery.")
    title = st.text_input("Tender title", value="Untitled tender")

source_mode = st.radio("Input source", ["Paste text", "Upload PDF"], horizontal=True)
text = ""
page_pairs: list[tuple[int, str]] = []

if source_mode == "Paste text":
    text = st.text_area(
        "Paste tender or grant text",
        height=360,
        placeholder="Paste the tender notice or grant requirements here...",
    )
else:
    uploaded = st.file_uploader("Upload a text-based PDF", type=["pdf"])
    if uploaded is not None:
        try:
            pages = extract_pdf_pages(uploaded.getvalue())
            page_pairs = [(page.page_number, page.text) for page in pages]
            st.success(f"Read {len(pages)} PDF page(s).")
            empty_pages = [str(page.page_number) for page in pages if not page.text]
            if empty_pages:
                st.warning("No selectable text was found on page(s): " + ", ".join(empty_pages) + ". Scanned PDFs need OCR in a later version.")
        except ValueError as exc:
            st.error(str(exc))

if st.button("Analyze requirements", type="primary"):
    if source_mode == "Paste text" and not text.strip():
        st.warning("Paste tender text before analyzing.")
    elif source_mode == "Upload PDF" and not page_pairs:
        st.warning("Upload a readable, text-based PDF before analyzing.")
    else:
        requirements = (
            extract_requirements(text)
            if source_mode == "Paste text"
            else extract_requirements_from_pages(page_pairs)
        )
        st.session_state["analysis"] = TenderAnalysis(
            title=title.strip() or "Untitled tender",
            requirements=requirements,
            warnings=[
                "This tool extracts likely requirements; it does not determine legal eligibility.",
                "Every item must be checked against the official tender before submission.",
                "Page references identify extracted PDF pages; verify the quotation in the original document.",
            ],
        )

analysis = st.session_state.get("analysis")
if analysis:
    st.subheader("Analysis summary")
    col1, col2 = st.columns(2)
    col1.metric("Requirements identified", analysis.requirement_count)
    col2.metric("Human review required", sum(item.human_review_required for item in analysis.requirements))
    if analysis.requirements:
        st.dataframe(
            [{
                "ID": item.id,
                "Category": item.category.value,
                "Requirement": item.text,
                "Status": item.status,
                "Evidence reference": item.source_reference,
            } for item in analysis.requirements],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No requirement-like lines were identified. Review the input manually.")
    report = render_markdown_report(analysis)
    st.download_button("Download Markdown report", report, "tender-readiness-report.md", "text/markdown")
    with st.expander("Preview report"):
        st.markdown(report)
