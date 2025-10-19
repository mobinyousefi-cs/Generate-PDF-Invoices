# Invoice Generator (Python, Tkinter, ReportLab)

Create professional PDF invoices with a clean Tkinter GUI, typed data models, and a battle‑tested PDF backend powered by ReportLab. Project is scaffolded with a modern `src/` layout, tests, linting, and CI so you can use it as a template across your portfolio.

---

## ✨ Features
- **GUI app (Tkinter)** for entering company, customer, and line‑item details
- **Typed dataclasses** for `Company`, `Customer`, `Item`, `Invoice`
- **Accurate totals** with tax/VAT (GST) handling and currency formatting
- **PDF generation** with ReportLab (A4, auto‑paginate, consistent typography)
- **Autosave** JSON invoice drafts; reopen and edit later
- **CLI** to render invoices from JSON (useful for CI/batch jobs)
- **Tests** with `pytest`; **lint/format** via Ruff + Black
- **GitHub Actions** CI workflow

---

## 🧱 Project Structure
```
invoice_generator/
├─ src/
│  └─ invoice_generator/
│     ├─ __init__.py
│     ├─ main.py          # Tkinter entry point
│     ├─ gui.py           # GUI widgets/forms
│     ├─ models.py        # Dataclasses for domain objects
│     ├─ pdf.py           # ReportLab PDF rendering
│     ├─ storage.py       # JSON persistence & paths
│     └─ utils.py         # Validation & helpers
├─ tests/
│  ├─ test_models.py
│  ├─ test_pdf.py
│  └─ test_utils.py
├─ scripts/
│  └─ cli.py              # CLI: render invoice JSON -> PDF
├─ pyproject.toml         # deps + tool configs (Black, Ruff, PyTest)
├─ requirements.txt       # pinned runtime dependencies
├─ .editorconfig
├─ .gitignore
├─ LICENSE (MIT)
└─ .github/workflows/ci.yml
```

---

## 🚀 Quickstart

### 1) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
Either use pip with requirements:
```bash
pip install -r requirements.txt
```
…or use `pyproject.toml` with pip >= 23 / uv / pipx:
```bash
pip install .
```

### 3) Run the GUI
```bash
python -m invoice_generator
```

### 4) Use the CLI (JSON → PDF)
```bash
python -m invoice_generator --sample-json   # writes sample JSON to ./invoices/sample.json
python scripts/cli.py invoices/sample.json  # renders PDF next to JSON
```

> PDFs are written by default into `./invoices/` with an ISO 8601 timestamp in the filename.

---

## 🧩 Data Model Overview
- **Company**: name, address, GST/VAT number, email/phone
- **Customer**: name, address, email/phone
- **Item**: description, quantity, unit price, tax rate (per‑line override)
- **Invoice**: header meta (number/date/due), currency, items, notes, signatures

All amounts are computed via `Decimal` for accuracy.

---

## 🖨 PDF Output
- Page size: **A4**
- Header with company branding and invoice meta
- Line‑items table with auto wraps and page breaks
- Subtotal, Tax, Grand Total
- Optional signature block & notes

---

## 🧪 Testing
```bash
pytest -q
```

---

## 🧹 Lint & Format
```bash
ruff check .
ruff format .     # or: black .
```

---

## 🔐 License
MIT — see [LICENSE](LICENSE).

---

## 🙌 Credits
Authored by **Mobin Yousefi** (GitHub: [mobinyousefi-cs](https://github.com/mobinyousefi-cs)).

This repository follows the user’s standard template (src layout, tests, CI, Ruff+Black) and is suitable for academic/portfolio use.

