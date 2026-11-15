"""Streamlit entry point for the deterministic MVP."""

import streamlit as st

from tender_readiness.extractor import extract_requirements
from tender_readiness.models import TenderAnalysis
from tender_readiness.report import render_markdown_report


st.set_page_config(page_title="Tender Readiness AI", page_icon="✅", layout="wide")
st.title("Tender Readiness AI")
st.caption("Tender-readiness and document-analysis tool — not legal advice")

with st.sidebar:
    st.header("Administrator")
    st.info("All findings require administrator review before delivery.")
    title = st.text_input("Tender title", value="Untitled tender")

text = st.text_area(
    "Paste tender or grant text",
    height=360,
    placeholder="Paste the relevant tender notice, eligibility section, or grant requirements here...",
)

if st.button("Analyze requirements", type="primary"):
    if not text.strip():
        st.warning("Paste tender text before analyzing.")
    else:
        requirements = extract_requirements(text)
        analysis = TenderAnalysis(
            title=title.strip() or "Untitled tender",
            requirements=requirements,
            warnings=[
                "This MVP extracts likely requirements from plain text; it does not yet parse uploaded PDFs.",
                "Every item must be checked against the official tender before submission.",
            ],
        )
        st.session_state["analysis"] = analysis

analysis = st.session_state.get("analysis")
if analysis:
    st.subheader("Analysis summary")
    col1, col2 = st.columns(2)
    col1.metric("Requirements identified", analysis.requirement_count)
    col2.metric("Human review required", sum(item.human_review_required for item in analysis.requirements))

    if analysis.requirements:
        st.dataframe(
            [
                {
                    "ID": item.id,
                    "Category": item.category.value,
                    "Requirement": item.text,
                    "Status": item.status,
                    "Source": item.source_reference,
                }
                for item in analysis.requirements
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No requirement-like lines were identified. Review the input manually.")

    report = render_markdown_report(analysis)
    st.download_button("Download Markdown report", report, "tender-readiness-report.md", "text/markdown")
    with st.expander("Preview report"):
        st.markdown(report)
