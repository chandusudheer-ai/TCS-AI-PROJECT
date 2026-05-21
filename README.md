# 🏢 CIO Intelligence Dashboard

A multi-agent AI platform that reads PDF, DOC, XLS, and TXT documents and synthesises
an executive-grade CIO one-page dashboard report using OpenAI GPT-4o.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run cio_dashboard_app.py
```

---

## 🤖 Agent Architecture

| Agent | Input | Task |
|-------|-------|------|
| **PDF Agent** | `.pdf` files | Extracts findings, risks, strategic themes |
| **DOC Agent** | `.doc / .docx` files | Extracts decisions, action items, compliance |
| **XLS Agent** | `.xls / .xlsx / .csv` | Extracts KPIs, metrics, financial trends |
| **TXT Agent** | `.txt / .md / .log / .json` | Extracts logs, incidents, technical notes |
| **CIO Report Agent** | All agent outputs | Synthesises final one-page CIO Dashboard |

---

## 📁 Folder Configuration

You can point each agent to a **different folder**:

- **PDF folder:** `/path/to/your/pdf_reports`
- **DOC folder:** `/path/to/your/word_docs`
- **XLS folder:** `/path/to/your/spreadsheets`
- **TXT folder:** `/path/to/your/text_logs`

Leave a folder blank to skip that document type.

---

## 🔑 OpenAI API Key

Enter your key in the sidebar. It is used only in-session and never written to disk.
Get a key at: https://platform.openai.com/api-keys

Recommended model: **gpt-4o** (best quality for executive reports)

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | UI framework |
| `openai` | GPT-4o API calls |
| `PyPDF2` | PDF text extraction |
| `python-docx` | DOC/DOCX parsing |
| `pandas` + `openpyxl` | Excel/CSV reading |

---

## 🎨 Features

- **Dark executive theme** with gradient accents
- **Real-time agent status** updates in sidebar
- **3-tab interface:** Config → Agent Outputs → CIO Dashboard
- **Download report** as `.md` or `.txt`
- **Document inventory counter** — shows file counts before running
- **Per-agent expandable outputs** in the Agent Intelligence tab
