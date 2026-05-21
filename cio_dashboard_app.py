"""
CIO Intelligence Dashboard - Multi-Agent Document Analysis Platform
=====================================================================
Executive-grade Streamlit application with colorful widgets and AI agents
that process PDF, DOC, XLS, and TXT documents to generate CIO-level reports.

Requirements:
    pip install streamlit openai PyPDF2 python-docx openpyxl pandas plotly
"""

import streamlit as st
import openai
import os
import glob
import json
import time
from datetime import datetime
from pathlib import Path
import traceback

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CIO Intelligence Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — Dark executive theme with vivid accent colours
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1528 50%, #0a0e1a 100%);
    color: #e8eaf6;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1a2235 100%);
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #60a5fa;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent;
    border-bottom: 2px solid #1e3a5f;
    padding-bottom: 0;
}
.stTabs [data-baseweb="tab"] {
    background: #111827;
    color: #94a3b8;
    border-radius: 10px 10px 0 0;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 14px;
    border: 1px solid #1e3a5f;
    border-bottom: none;
    transition: all 0.25s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed) !important;
    color: white !important;
    border-color: #3b82f6 !important;
}
.stTabs [data-baseweb="tab"]:hover {
    background: #1e3a5f;
    color: white;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, #111827, #1a2235);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    margin-bottom: 12px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(59,130,246,0.25);
}
.metric-number {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 4px;
}

/* ── Section cards ── */
.section-card {
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #60a5fa;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e3a5f;
}

/* ── Folder input boxes ── */
.folder-box {
    background: #0f172a;
    border: 1.5px solid #1e3a5f;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
    transition: border-color 0.2s;
}
.folder-box:hover { border-color: #3b82f6; }
.folder-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}

/* ── Agent status items ── */
.agent-item {
    display: flex;
    align-items: center;
    gap: 14px;
    background: #0f172a;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 10px;
    font-size: 0.9rem;
}
.agent-idle    { border-left: 4px solid #475569; }
.agent-running { border-left: 4px solid #f59e0b; background: #1a140a; }
.agent-done    { border-left: 4px solid #22c55e; background: #0a1a0f; }
.agent-error   { border-left: 4px solid #ef4444; background: #1a0a0a; }

/* ── Buttons ── */
div.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 0.4px;
    transition: all 0.25s;
    border: none;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.4);
}

/* ── Primary CTA button ── */
.cta-btn div.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    padding: 16px 32px;
    font-size: 17px;
}

/* ── Text inputs ── */
div[data-testid="stTextInput"] input {
    background: #0f172a;
    border: 1.5px solid #1e3a5f;
    border-radius: 8px;
    color: #e2e8f0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
}

/* ── Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #2563eb, #7c3aed, #ec4899);
    border-radius: 4px;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 10px;
    border: none;
}

/* ── Report container ── */
.report-container {
    background: #0a0e1a;
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 32px 40px;
    line-height: 1.75;
    font-size: 15px;
    color: #cbd5e1;
}
.report-container h1 { color: #60a5fa; font-size: 1.8rem; border-bottom: 2px solid #1e3a5f; padding-bottom: 12px; }
.report-container h2 { color: #a78bfa; font-size: 1.3rem; margin-top: 28px; }
.report-container h3 { color: #34d399; font-size: 1.1rem; margin-top: 20px; }
.report-container ul  { padding-left: 20px; }
.report-container li  { margin-bottom: 6px; }
.report-container strong { color: #f1f5f9; }
.report-container em { color: #94a3b8; }
.report-container blockquote {
    border-left: 3px solid #3b82f6;
    margin: 16px 0;
    padding: 10px 20px;
    background: #111827;
    border-radius: 0 8px 8px 0;
    color: #93c5fd;
    font-style: italic;
}
.report-container table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
}
.report-container th {
    background: #1e3a5f;
    color: #93c5fd;
    padding: 10px 14px;
    text-align: left;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.report-container td {
    padding: 9px 14px;
    border-bottom: 1px solid #1e2d4a;
    color: #cbd5e1;
    font-size: 0.9rem;
}
.report-container tr:hover td { background: #111827; }

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #111827, #1a2235);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.header-icon {
    font-size: 3.5rem;
    filter: drop-shadow(0 0 12px rgba(99,102,241,0.6));
}
.header-title { font-size: 2rem; font-weight: 700; color: #f1f5f9; }
.header-sub   { color: #64748b; font-size: 0.95rem; margin-top: 4px; }

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.badge-blue   { background: rgba(37,99,235,0.2); color: #93c5fd; border: 1px solid #1d4ed8; }
.badge-purple { background: rgba(124,58,237,0.2); color: #c4b5fd; border: 1px solid #7c3aed; }
.badge-green  { background: rgba(34,197,94,0.2);  color: #86efac; border: 1px solid #16a34a; }
.badge-amber  { background: rgba(245,158,11,0.2); color: #fcd34d; border: 1px solid #d97706; }
.badge-red    { background: rgba(239,68,68,0.2);  color: #fca5a5; border: 1px solid #dc2626; }

/* ── Divider ── */
hr { border-color: #1e3a5f; margin: 20px 0; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3b82f6; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DOCUMENT READER HELPERS
# ─────────────────────────────────────────────────────────────
def read_pdf_files(folder: str) -> list[dict]:
    """Extract text from all PDF files in a folder."""
    results = []
    try:
        import PyPDF2
    except ImportError:
        return [{"file": "PyPDF2 not installed", "content": "pip install PyPDF2", "error": True}]

    for path in glob.glob(os.path.join(folder, "**/*.pdf"), recursive=True) + \
                glob.glob(os.path.join(folder, "*.pdf")):
        try:
            text = []
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text() or "")
            results.append({"file": os.path.basename(path), "content": "\n".join(text)[:8000]})
        except Exception as e:
            results.append({"file": os.path.basename(path), "content": f"Error: {e}", "error": True})
    return results


def read_doc_files(folder: str) -> list[dict]:
    """Extract text from all DOC/DOCX files in a folder."""
    results = []
    try:
        from docx import Document
    except ImportError:
        return [{"file": "python-docx not installed", "content": "pip install python-docx", "error": True}]

    patterns = ["*.doc", "*.docx"]
    for pat in patterns:
        for path in glob.glob(os.path.join(folder, pat)) + \
                    glob.glob(os.path.join(folder, "**/" + pat), recursive=True):
            try:
                doc = Document(path)
                text = "\n".join(p.text for p in doc.paragraphs)
                results.append({"file": os.path.basename(path), "content": text[:8000]})
            except Exception as e:
                results.append({"file": os.path.basename(path), "content": f"Error: {e}", "error": True})
    return results


def read_xls_files(folder: str) -> list[dict]:
    """Extract data from all XLS/XLSX files in a folder."""
    results = []
    try:
        import pandas as pd
    except ImportError:
        return [{"file": "pandas not installed", "content": "pip install pandas openpyxl", "error": True}]

    patterns = ["*.xls", "*.xlsx", "*.csv"]
    for pat in patterns:
        for path in glob.glob(os.path.join(folder, pat)) + \
                    glob.glob(os.path.join(folder, "**/" + pat), recursive=True):
            try:
                if path.endswith(".csv"):
                    df = pd.read_csv(path)
                else:
                    df = pd.read_excel(path)
                summary = f"Shape: {df.shape[0]} rows × {df.shape[1]} cols\nColumns: {list(df.columns)}\n\n"
                summary += df.head(30).to_string()
                results.append({"file": os.path.basename(path), "content": summary[:8000]})
            except Exception as e:
                results.append({"file": os.path.basename(path), "content": f"Error: {e}", "error": True})
    return results


def read_txt_files(folder: str) -> list[dict]:
    """Read all TXT/MD/LOG files in a folder."""
    results = []
    patterns = ["*.txt", "*.md", "*.log", "*.json"]
    for pat in patterns:
        for path in glob.glob(os.path.join(folder, pat)) + \
                    glob.glob(os.path.join(folder, "**/" + pat), recursive=True):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(8000)
                results.append({"file": os.path.basename(path), "content": content})
            except Exception as e:
                results.append({"file": os.path.basename(path), "content": f"Error: {e}", "error": True})
    return results


# ─────────────────────────────────────────────────────────────
# OPENAI AGENT CALLS
# ─────────────────────────────────────────────────────────────
def call_openai(client, system_prompt: str, user_prompt: str, model: str = "gpt-4o") -> str:
    """Thin wrapper around OpenAI chat completions."""
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=3000,
    )
    return resp.choices[0].message.content.strip()


def pdf_agent(client, documents: list[dict]) -> str:
    if not documents:
        return "No PDF documents found."
    system = (
        "You are the PDF Document Intelligence Agent. "
        "Analyse the provided PDF content and extract key business insights, "
        "risks, strategic themes, and actionable findings relevant to a CIO. "
        "Structure your output with: Summary, Key Findings, Risks, Opportunities, "
        "and Recommended Actions."
    )
    combined = "\n\n---\n\n".join(
        f"[FILE: {d['file']}]\n{d['content']}" for d in documents[:5]
    )
    return call_openai(client, system, f"Analyse these PDF documents:\n\n{combined}")


def doc_agent(client, documents: list[dict]) -> str:
    if not documents:
        return "No DOC/DOCX documents found."
    system = (
        "You are the Word Document Intelligence Agent. "
        "Analyse the provided document content and extract governance decisions, "
        "project statuses, compliance items, and executive communications. "
        "Structure your output with: Summary, Key Decisions, Action Items, "
        "Compliance Notes, and Strategic Implications."
    )
    combined = "\n\n---\n\n".join(
        f"[FILE: {d['file']}]\n{d['content']}" for d in documents[:5]
    )
    return call_openai(client, system, f"Analyse these Word documents:\n\n{combined}")


def xls_agent(client, documents: list[dict]) -> str:
    if not documents:
        return "No spreadsheet documents found."
    system = (
        "You are the Spreadsheet & Data Intelligence Agent. "
        "Analyse the provided tabular data and extract KPIs, financial metrics, "
        "performance trends, anomalies, and data-driven insights. "
        "Structure your output with: Summary, Key Metrics, Trends, Anomalies, "
        "and Forecast Indicators."
    )
    combined = "\n\n---\n\n".join(
        f"[FILE: {d['file']}]\n{d['content']}" for d in documents[:5]
    )
    return call_openai(client, system, f"Analyse these spreadsheet files:\n\n{combined}")


def txt_agent(client, documents: list[dict]) -> str:
    if not documents:
        return "No text documents found."
    system = (
        "You are the Text & Log Intelligence Agent. "
        "Analyse the provided text files, logs, and markdown documents. "
        "Extract technical findings, system health indicators, incident reports, "
        "and any strategic communications. "
        "Structure your output with: Summary, Technical Highlights, Incidents, "
        "System Health, and Notable Patterns."
    )
    combined = "\n\n---\n\n".join(
        f"[FILE: {d['file']}]\n{d['content']}" for d in documents[:5]
    )
    return call_openai(client, system, f"Analyse these text documents:\n\n{combined}")


def cio_report_agent(
    client,
    pdf_insights:  str,
    doc_insights:  str,
    xls_insights:  str,
    txt_insights:  str,
) -> str:
    today = datetime.now().strftime("%B %d, %Y")
    system = """You are the Chief Intelligence Officer Report Synthesiser Agent — 
an elite AI that consolidates multi-source intelligence into an impeccable one-page CIO Dashboard Report.

Your report MUST follow this exact Markdown structure:

---
# 🏢 CIO Intelligence Dashboard
**Report Date:** {DATE} | **Classification:** EXECUTIVE CONFIDENTIAL

---

## 📊 Executive Summary
[3–4 sentence strategic overview suitable for a board audience]

---

## 🎯 Strategic KPIs at a Glance
| KPI | Status | Trend | Priority |
|-----|--------|-------|----------|
[4–6 rows with emojis in Status/Trend columns]

---

## 🔴 Critical Issues & Risks
[Bullet list of top 3–5 critical issues with impact assessment]

---

## 🟢 Wins & Opportunities
[Bullet list of top 3–5 positive findings and opportunities]

---

## 📋 Key Decisions Required
[Numbered list of 3–5 decisions the CIO must make]

---

## 🔄 Technology & Operations Pulse
[2–3 sentences on IT health, system performance, and operational status]

---

## 💰 Financial & Resource Overview
[2–3 sentences on budgets, headcount, and spend patterns extracted from data]

---

## 🗓️ Recommended Next Actions (30-day horizon)
1. [Action 1 — Owner — Deadline]
2. [Action 2 — Owner — Deadline]
3. [Action 3 — Owner — Deadline]
4. [Action 4 — Owner — Deadline]
5. [Action 5 — Owner — Deadline]

---

> **Prepared by:** CIO Intelligence Platform  |  **AI Agents:** PDF · DOC · XLS · TXT · Synthesis
---

Use clear, executive-level language. Be concise, data-driven, and actionable.
Replace {DATE} with today's date."""

    user_prompt = f"""Synthesise the following agent intelligence outputs into a CIO Dashboard Report.
Today's date: {today}

═══ PDF AGENT FINDINGS ═══
{pdf_insights}

═══ DOC AGENT FINDINGS ═══
{doc_insights}

═══ SPREADSHEET AGENT FINDINGS ═══
{xls_insights}

═══ TEXT AGENT FINDINGS ═══
{txt_insights}

Generate the complete CIO Dashboard Report now."""

    return call_openai(client, system, user_prompt)


# ─────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────
defaults = {
    "api_key": "",
    "pdf_folder": "",
    "doc_folder": "",
    "xls_folder": "",
    "txt_folder": "",
    "agent_statuses": {
        "PDF Agent":         {"status": "idle", "message": "Waiting…"},
        "DOC Agent":         {"status": "idle", "message": "Waiting…"},
        "XLS Agent":         {"status": "idle", "message": "Waiting…"},
        "TXT Agent":         {"status": "idle", "message": "Waiting…"},
        "CIO Report Agent":  {"status": "idle", "message": "Waiting…"},
    },
    "pdf_insights":  "",
    "doc_insights":  "",
    "xls_insights":  "",
    "txt_insights":  "",
    "final_report":  "",
    "processing":    False,
    "progress":      0,
    "doc_counts":    {"pdf": 0, "doc": 0, "xls": 0, "txt": 0},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────────────────────
# SIDEBAR — API KEY + HELP
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px;'>
        <div style='font-size:2.8rem;filter:drop-shadow(0 0 10px rgba(99,102,241,0.7));'>🏢</div>
        <div style='font-size:1.1rem;font-weight:700;color:#f1f5f9;margin-top:6px;'>CIO Intelligence</div>
        <div style='font-size:0.75rem;color:#475569;letter-spacing:1px;text-transform:uppercase;'>Platform v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔑 API Configuration")
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-…",
        help="Your OpenAI API key. Never stored on disk.",
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    model_choice = st.selectbox(
        "Model",
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0,
        help="GPT-4o recommended for best executive-quality output.",
    )

    st.markdown("---")
    st.markdown("### 🤖 Active Agents")
    agent_icons = {
        "PDF Agent":         ("📄", "#ef4444"),
        "DOC Agent":         ("📝", "#f59e0b"),
        "XLS Agent":         ("📊", "#22c55e"),
        "TXT Agent":         ("📃", "#3b82f6"),
        "CIO Report Agent":  ("🏆", "#a78bfa"),
    }
    for agent_name, (icon, color) in agent_icons.items():
        s = st.session_state.agent_statuses[agent_name]
        status_emoji = {"idle": "⚪", "running": "🟡", "done": "🟢", "error": "🔴"}.get(s["status"], "⚪")
        st.markdown(
            f"""<div style='display:flex;align-items:center;gap:10px;padding:8px 12px;
            background:#0f172a;border-radius:8px;margin-bottom:6px;border:1px solid #1e3a5f;'>
            <span style='font-size:1.1rem;'>{icon}</span>
            <div style='flex:1;'>
                <div style='font-size:0.78rem;font-weight:600;color:{color};'>{agent_name}</div>
                <div style='font-size:0.7rem;color:#64748b;'>{s['message']}</div>
            </div>
            <span>{status_emoji}</span></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.72rem;color:#334155;text-align:center;line-height:1.8;'>
    Documents are read locally.<br>Only extracted text is sent to OpenAI.<br>
    <span style='color:#1e3a5f;'>──────────────────────</span><br>
    Built for CIO / Executive use.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='app-header'>
    <div class='header-icon'>🏢</div>
    <div>
        <div class='header-title'>CIO Intelligence Dashboard</div>
        <div class='header-sub'>Multi-Agent Document Analysis Platform &nbsp;·&nbsp;
            <span class='badge badge-blue'>AI Powered</span> &nbsp;
            <span class='badge badge-purple'>Executive Grade</span> &nbsp;
            <span class='badge badge-green'>Real-time Synthesis</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "⚙️  Configuration & Run",
    "📡  Agent Intelligence",
    "🏆  CIO Dashboard",
])


# ═══════════════════════════════════════════════════════════════
# TAB 1 — CONFIGURATION
# ═══════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([3, 2], gap="large")

    # ── Folder inputs ──────────────────────────────────────────
    with col_left:
        st.markdown("<div class='section-title'>📁 Document Source Configuration</div>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#64748b;font-size:0.88rem;margin-bottom:20px;'>"
            "Enter the full folder path for each document type. "
            "You may use different folders for each type. Leave empty to skip that type.</p>",
            unsafe_allow_html=True,
        )

        folder_configs = [
            ("pdf_folder", "📄", "PDF Documents", "#ef4444",
             "e.g. /reports/quarterly_pdfs", "PyPDF2"),
            ("doc_folder", "📝", "Word Documents (DOC / DOCX)", "#f59e0b",
             "e.g. /reports/word_docs", "python-docx"),
            ("xls_folder", "📊", "Spreadsheets (XLS / XLSX / CSV)", "#22c55e",
             "e.g. /reports/financial_data", "pandas + openpyxl"),
            ("txt_folder", "📃", "Text Files (TXT / MD / LOG / JSON)", "#3b82f6",
             "e.g. /reports/logs_and_notes", "built-in"),
        ]

        for key, icon, label, color, placeholder, dep in folder_configs:
            st.markdown(f"""
            <div class='folder-box'>
                <div class='folder-label'>
                    <span style='font-size:1.2rem'>{icon}</span>
                    <span style='color:{color};'>{label}</span>
                    <span class='badge badge-blue' style='margin-left:auto;font-size:0.65rem;'>{dep}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state[key] = st.text_input(
                label,
                value=st.session_state[key],
                placeholder=placeholder,
                label_visibility="collapsed",
                key=f"input_{key}",
            )

    # ── Quick stats + CTA ─────────────────────────────────────
    with col_right:
        st.markdown("<div class='section-title'>📊 Document Inventory</div>", unsafe_allow_html=True)

        # Count files
        def count_files(folder, patterns):
            if not folder or not os.path.isdir(folder):
                return 0
            total = 0
            for p in patterns:
                total += len(glob.glob(os.path.join(folder, p)))
                total += len(glob.glob(os.path.join(folder, "**/" + p), recursive=True))
            return total

        counts = {
            "PDF":  count_files(st.session_state.pdf_folder, ["*.pdf"]),
            "DOC":  count_files(st.session_state.doc_folder, ["*.doc", "*.docx"]),
            "XLS":  count_files(st.session_state.xls_folder, ["*.xls", "*.xlsx", "*.csv"]),
            "TXT":  count_files(st.session_state.txt_folder, ["*.txt", "*.md", "*.log", "*.json"]),
        }
        total = sum(counts.values())
        st.session_state.doc_counts = {k.lower(): v for k, v in counts.items()}

        c1, c2 = st.columns(2)
        for (dtype, cnt), col in zip(counts.items(), [c1, c2, c1, c2]):
            icons_map = {"PDF": "📄", "DOC": "📝", "XLS": "📊", "TXT": "📃"}
            col.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1.8rem;'>{icons_map[dtype]}</div>
                <div class='metric-number'>{cnt}</div>
                <div class='metric-label'>{dtype} Files</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='metric-card' style='background:linear-gradient(135deg,#1d1040,#1a2235);
             border:2px solid #7c3aed;'>
            <div class='metric-number' style='font-size:3rem;'>{total}</div>
            <div class='metric-label'>Total Documents</div>
        </div>
        """, unsafe_allow_html=True)

        # Validation
        has_key = bool(st.session_state.api_key)
        has_docs = total > 0
        has_folder = any([
            st.session_state.pdf_folder,
            st.session_state.doc_folder,
            st.session_state.xls_folder,
            st.session_state.txt_folder,
        ])

        if not has_key:
            st.warning("⚠️ Enter your OpenAI API key in the sidebar.")
        elif not has_folder:
            st.info("ℹ️ Enter at least one folder path above.")
        else:
            if not has_docs:
                st.warning("⚠️ No supported files found in the specified folders.")
            else:
                st.success(f"✅ Ready — {total} document(s) detected.")

    # ── CTA ───────────────────────────────────────────────────
    st.markdown("---")
    cta_col, _, info_col = st.columns([2, 1, 3])

    with cta_col:
        generate_clicked = st.button(
            "🚀  Generate CIO Dashboard",
            use_container_width=True,
            disabled=st.session_state.processing,
            help="Run all agents and generate the consolidated CIO report.",
        )

    with info_col:
        if not st.session_state.processing:
            st.markdown("""
            <div style='background:#0f172a;border:1px solid #1e3a5f;border-radius:10px;
                 padding:12px 18px;font-size:0.82rem;color:#64748b;'>
            🤖 <b style='color:#94a3b8'>Pipeline:</b>
            PDF Agent → DOC Agent → XLS Agent → TXT Agent → CIO Synthesis Agent
            </div>
            """, unsafe_allow_html=True)

    # ── Progress bar ──────────────────────────────────────────
    progress_slot = st.empty()
    status_slot   = st.empty()

    if st.session_state.processing:
        progress_slot.progress(st.session_state.progress)


# ═══════════════════════════════════════════════════════════════
# TAB 2 — AGENT INTELLIGENCE
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>🤖 Agent Output & Intelligence Feed</div>", unsafe_allow_html=True)

    agent_output_map = {
        "📄 PDF Agent":         ("pdf_insights",  "#ef4444"),
        "📝 DOC Agent":         ("doc_insights",  "#f59e0b"),
        "📊 XLS Agent":         ("xls_insights",  "#22c55e"),
        "📃 TXT Agent":         ("txt_insights",  "#3b82f6"),
    }

    for title, (key, color) in agent_output_map.items():
        content = st.session_state.get(key, "")
        with st.expander(f"{title}  {'✅' if content else '⚪'}", expanded=False):
            if content:
                st.markdown(
                    f"<div class='report-container'>{content}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<p style='color:#475569;font-style:italic;'>No output yet — run the pipeline first.</p>",
                    unsafe_allow_html=True,
                )


# ═══════════════════════════════════════════════════════════════
# TAB 3 — CIO DASHBOARD
# ═══════════════════════════════════════════════════════════════
with tab3:
    report = st.session_state.final_report

    if report:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.markdown(f"""
        <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;'>
            <div>
                <span class='badge badge-green'>● LIVE REPORT</span>
                <span style='color:#475569;font-size:0.8rem;margin-left:12px;'>Generated: {ts}</span>
            </div>
            <div>
                <span class='badge badge-blue'>AI Synthesised</span>
                &nbsp;
                <span class='badge badge-purple'>Executive Confidential</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<div class='report-container'>{report}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")
        dl_col1, dl_col2, _ = st.columns([1, 1, 3])
        with dl_col1:
            st.download_button(
                "⬇️  Download Report (.md)",
                data=report,
                file_name=f"CIO_Dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with dl_col2:
            st.download_button(
                "⬇️  Download Raw Text (.txt)",
                data=report,
                file_name=f"CIO_Dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.markdown("""
        <div style='text-align:center;padding:80px 40px;'>
            <div style='font-size:5rem;margin-bottom:20px;
                 filter:drop-shadow(0 0 20px rgba(99,102,241,0.4));'>📊</div>
            <div style='font-size:1.4rem;font-weight:700;color:#475569;margin-bottom:12px;'>
                No Report Generated Yet
            </div>
            <div style='color:#334155;font-size:0.95rem;max-width:420px;margin:0 auto;'>
                Configure your document folders in the
                <strong style='color:#60a5fa;'>Configuration</strong> tab,
                then click <strong style='color:#a78bfa;'>Generate CIO Dashboard</strong>
                to run the multi-agent pipeline.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PIPELINE EXECUTION (fires when button clicked)
# ─────────────────────────────────────────────────────────────
if generate_clicked:
    if not st.session_state.api_key:
        st.error("❌ Please enter your OpenAI API key in the sidebar.")
        st.stop()

    # Reset state
    st.session_state.processing   = True
    st.session_state.final_report = ""
    st.session_state.pdf_insights = ""
    st.session_state.doc_insights = ""
    st.session_state.xls_insights = ""
    st.session_state.txt_insights = ""
    for k in st.session_state.agent_statuses:
        st.session_state.agent_statuses[k] = {"status": "idle", "message": "Queued…"}

    try:
        client = openai.OpenAI(api_key=st.session_state.api_key)

        total_steps   = 5
        current_step  = 0

        def update_progress(msg):
            global current_step
            current_step += 1
            pct = int((current_step / total_steps) * 100)
            st.session_state.progress = pct / 100
            progress_slot.progress(pct)
            status_slot.info(f"⚙️ {msg}")

        # ── Agent 1 — PDF ──────────────────────────────────────
        st.session_state.agent_statuses["PDF Agent"] = {"status": "running", "message": "Reading PDF files…"}
        update_progress("PDF Agent: reading and analysing documents…")
        pdf_docs = read_pdf_files(st.session_state.pdf_folder) if st.session_state.pdf_folder else []
        pdf_ins  = pdf_agent(client, pdf_docs) if pdf_docs else "No PDF folder configured."
        st.session_state.pdf_insights = pdf_ins
        st.session_state.agent_statuses["PDF Agent"] = {"status": "done", "message": f"Processed {len(pdf_docs)} file(s)"}

        # ── Agent 2 — DOC ──────────────────────────────────────
        st.session_state.agent_statuses["DOC Agent"] = {"status": "running", "message": "Reading Word documents…"}
        update_progress("DOC Agent: extracting governance & decision content…")
        doc_docs = read_doc_files(st.session_state.doc_folder) if st.session_state.doc_folder else []
        doc_ins  = doc_agent(client, doc_docs) if doc_docs else "No DOC folder configured."
        st.session_state.doc_insights = doc_ins
        st.session_state.agent_statuses["DOC Agent"] = {"status": "done", "message": f"Processed {len(doc_docs)} file(s)"}

        # ── Agent 3 — XLS ──────────────────────────────────────
        st.session_state.agent_statuses["XLS Agent"] = {"status": "running", "message": "Reading spreadsheets…"}
        update_progress("XLS Agent: analysing KPIs and financial data…")
        xls_docs = read_xls_files(st.session_state.xls_folder) if st.session_state.xls_folder else []
        xls_ins  = xls_agent(client, xls_docs) if xls_docs else "No XLS folder configured."
        st.session_state.xls_insights = xls_ins
        st.session_state.agent_statuses["XLS Agent"] = {"status": "done", "message": f"Processed {len(xls_docs)} file(s)"}

        # ── Agent 4 — TXT ──────────────────────────────────────
        st.session_state.agent_statuses["TXT Agent"] = {"status": "running", "message": "Reading text files…"}
        update_progress("TXT Agent: processing logs, notes, and text data…")
        txt_docs = read_txt_files(st.session_state.txt_folder) if st.session_state.txt_folder else []
        txt_ins  = txt_agent(client, txt_docs) if txt_docs else "No TXT folder configured."
        st.session_state.txt_insights = txt_ins
        st.session_state.agent_statuses["TXT Agent"] = {"status": "done", "message": f"Processed {len(txt_docs)} file(s)"}

        # ── Agent 5 — CIO Report ───────────────────────────────
        st.session_state.agent_statuses["CIO Report Agent"] = {"status": "running", "message": "Synthesising CIO report…"}
        update_progress("CIO Report Agent: synthesising executive dashboard…")
        final = cio_report_agent(client, pdf_ins, doc_ins, xls_ins, txt_ins)
        st.session_state.final_report = final
        st.session_state.agent_statuses["CIO Report Agent"] = {"status": "done", "message": "Report generated ✅"}

        progress_slot.progress(100)
        status_slot.success("✅ CIO Dashboard generated! Switch to the **🏆 CIO Dashboard** tab to view the report.")

    except openai.AuthenticationError:
        status_slot.error("❌ Invalid OpenAI API key. Please check your key in the sidebar.")
        for k in st.session_state.agent_statuses:
            if st.session_state.agent_statuses[k]["status"] == "running":
                st.session_state.agent_statuses[k] = {"status": "error", "message": "Auth failed"}
    except Exception as e:
        status_slot.error(f"❌ Pipeline error: {str(e)}")
        for k in st.session_state.agent_statuses:
            if st.session_state.agent_statuses[k]["status"] == "running":
                st.session_state.agent_statuses[k] = {"status": "error", "message": str(e)[:60]}
    finally:
        st.session_state.processing = False
        st.rerun()
