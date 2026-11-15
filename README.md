# Tender Readiness AI

A Streamlit-based tender-readiness and document-analysis MVP. It extracts likely requirements from pasted tender or grant text, organizes them into a compliance checklist, and generates a Markdown report.

## Status

This is an early deterministic MVP. It does **not** provide legal advice, guarantee bid eligibility, or replace review of the official tender documents.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Run tests and lint:

```bash
pytest
ruff check .
```

## MVP behavior

- Paste tender or grant text into the Streamlit app.
- Extract requirement-like lines using deterministic rules.
- Categorize requirements.
- Keep every result in `needs_review` status by default.
- Generate a Markdown report with source references and review warnings.

## Planned next steps

1. Add safe PDF text extraction.
2. Add page-level source references.
3. Add applicant-document comparison.
4. Add administrator authentication and review workflow.
5. Add optional, explicitly configured open-source model assistance.

## License

MIT
