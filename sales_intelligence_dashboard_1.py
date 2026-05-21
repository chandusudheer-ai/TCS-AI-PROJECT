"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   DataForge Sales Intelligence Dashboard — CIO Executive Suite (Light)      ║
║   H1 2024 vs H1 2025 · White Theme · Tab Navigation · OpenAI GPT-4         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Requirements:
    pip install streamlit plotly pandas openai python-dotenv

Run:
    streamlit run sales_intelligence_dashboard.py

Set your OpenAI API key in a .env file:
    OPENAI_API_KEY=sk-...
Or enter it in the Settings widget in the sidebar.
"""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Intelligence · CIO Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — Executive White / Light Theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700;800&family=Roboto+Mono:wght@400;500&display=swap');

:root {
    --white:        #FFFFFF;
    --bg-app:       #F0F4F8;
    --bg-sidebar:   #1E293B;
    --bg-card:      #FFFFFF;
    --bg-card-alt:  #F8FAFC;
    --bg-header:    #1E3A5F;
    --border:       #E2E8F0;
    --border-mid:   #CBD5E1;
    --blue:         #1D4ED8;
    --blue-lt:      #EFF6FF;
    --blue-mid:     #3B82F6;
    --cyan:         #0891B2;
    --cyan-lt:      #ECFEFF;
    --green:        #059669;
    --green-lt:     #ECFDF5;
    --amber:        #D97706;
    --amber-lt:     #FFFBEB;
    --rose:         #E11D48;
    --rose-lt:      #FFF1F2;
    --purple:       #7C3AED;
    --purple-lt:    #F5F3FF;
    --text-dark:    #0F172A;
    --text-body:    #334155;
    --text-muted:   #64748B;
    --text-light:   #94A3B8;
    --shadow-sm:    0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md:    0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
    --shadow-lg:    0 10px 28px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.05);
    --radius:       12px;
    --font-head:    'Poppins', sans-serif;
    --font-body:    'Inter', sans-serif;
    --font-mono:    'Roboto Mono', monospace;
}

/* ── App Background ── */
html, body { background: var(--bg-app) !important; }
.stApp     { background: var(--bg-app) !important; }
.main .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1400px; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: none;
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F1F5F9 !important;
    font-family: var(--font-head) !important;
}
[data-testid="stSidebar"] label { color: #94A3B8 !important; font-size: 0.78rem !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #0F172A !important;
    border: 1px solid #334155 !important;
    color: #E2E8F0 !important;
    border-radius: 8px !important;
}

/* ── Metric Cards ── */
[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 20px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s, transform 0.15s;
}
[data-testid="metric-container"]:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}
[data-testid="stMetricLabel"] p {
    font-family: var(--font-body) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-head) !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
    color: var(--text-dark) !important;
}
[data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
}

/* ── Tabs — TOP LEVEL navigation ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--white);
    border-bottom: 2px solid var(--border);
    gap: 2px;
    padding: 0 4px;
    border-radius: var(--radius) var(--radius) 0 0;
    box-shadow: var(--shadow-sm);
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-body) !important;
    font-weight: 500;
    font-size: 0.82rem;
    color: var(--text-muted) !important;
    padding: 11px 18px;
    border-radius: 8px 8px 0 0;
    letter-spacing: 0.01em;
    transition: color 0.15s, background 0.15s;
}
.stTabs [data-baseweb="tab"]:hover {
    background: var(--bg-card-alt) !important;
    color: var(--blue) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--white) !important;
    color: var(--blue) !important;
    border-bottom: 3px solid var(--blue) !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--white);
    border: 1px solid var(--border);
    border-top: none;
    border-radius: 0 0 var(--radius) var(--radius);
    padding: 24px 20px;
    box-shadow: var(--shadow-sm);
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-mid) 100%);
    color: white !important;
    border: none;
    border-radius: 8px;
    font-family: var(--font-body) !important;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 10px 24px;
    box-shadow: 0 2px 8px rgba(29,78,216,0.3);
    transition: all 0.2s;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    box-shadow: 0 4px 16px rgba(29,78,216,0.4);
    transform: translateY(-1px);
}

/* ── Selectbox / Inputs ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTextArea textarea {
    background: var(--white) !important;
    border: 1px solid var(--border-mid) !important;
    color: var(--text-dark) !important;
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
    font-size: 0.875rem !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus {
    border-color: var(--blue-mid) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card-alt) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    color: var(--text-dark) !important;
}
.streamlit-expanderContent {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* ── Custom Components ── */
.page-header {
    background: linear-gradient(135deg, #1E3A5F 0%, #1D4ED8 60%, #0891B2 100%);
    border-radius: var(--radius);
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}
.page-header::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.page-header-title {
    font-family: var(--font-head);
    font-size: 1.9rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin: 0 0 6px 0;
}
.page-header-sub {
    font-family: var(--font-body);
    font-size: 0.85rem;
    color: rgba(255,255,255,0.65);
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-family: var(--font-mono);
    font-weight: 500;
    letter-spacing: 0.05em;
    margin-top: 14px;
    margin-right: 6px;
}

.section-title {
    font-family: var(--font-head);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-dark);
    margin: 0 0 2px 0;
}
.section-sub {
    font-family: var(--font-body);
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.divider {
    height: 1px;
    background: var(--border);
    margin: 16px 0 20px 0;
}

.stat-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px 20px;
    box-shadow: var(--shadow-sm);
}
.stat-card-accent { border-top: 3px solid var(--blue); }
.stat-card-green  { border-top: 3px solid var(--green); }
.stat-card-amber  { border-top: 3px solid var(--amber); }
.stat-card-rose   { border-top: 3px solid var(--rose); }
.stat-card-purple { border-top: 3px solid var(--purple); }
.stat-card-cyan   { border-top: 3px solid var(--cyan); }

.kpi-value {
    font-family: var(--font-head);
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-dark);
    line-height: 1.2;
}
.kpi-label {
    font-family: var(--font-body);
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}
.kpi-delta-pos { color: var(--green); font-family: var(--font-mono); font-size: 0.75rem; font-weight: 500; }
.kpi-delta-neg { color: var(--rose);  font-family: var(--font-mono); font-size: 0.75rem; font-weight: 500; }
.kpi-delta-neu { color: var(--amber); font-family: var(--font-mono); font-size: 0.75rem; font-weight: 500; }

.insight-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s, transform 0.15s;
}
.insight-card:hover { box-shadow: var(--shadow-md); transform: translateX(2px); }
.insight-title {
    font-family: var(--font-body);
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 5px;
}
.insight-body {
    font-family: var(--font-body);
    font-size: 0.81rem;
    color: var(--text-body);
    line-height: 1.6;
}

.ai-card {
    background: linear-gradient(135deg, #EFF6FF, #ECFEFF);
    border: 1px solid #BFDBFE;
    border-left: 4px solid var(--blue);
    border-radius: var(--radius);
    padding: 22px 26px;
    margin: 14px 0;
    font-family: var(--font-body);
    font-size: 0.88rem;
    line-height: 1.75;
    color: var(--text-body);
    box-shadow: var(--shadow-sm);
}

.okr-kr {
    background: var(--bg-card-alt);
    border-left: 3px solid;
    padding: 10px 14px;
    margin: 6px 0;
    border-radius: 0 8px 8px 0;
    font-family: var(--font-body);
    font-size: 0.83rem;
    color: var(--text-body);
}
.sprint-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
    box-shadow: var(--shadow-sm);
    display: flex;
    gap: 14px;
    align-items: flex-start;
}
.sprint-period {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 4px;
    white-space: nowrap;
    border: 1px solid;
}
.sprint-title {
    font-family: var(--font-body);
    font-weight: 700;
    font-size: 0.88rem;
    color: var(--text-dark);
    margin-bottom: 3px;
}
.sprint-body {
    font-family: var(--font-body);
    font-size: 0.79rem;
    color: var(--text-muted);
    line-height: 1.55;
}

.info-widget {
    background: var(--blue-lt);
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
}
.info-widget-amber {
    background: var(--amber-lt);
    border: 1px solid #FDE68A;
}
.info-widget-green {
    background: var(--green-lt);
    border: 1px solid #A7F3D0;
}

/* ── Sidebar Widgets ── */
.sidebar-widget {
    background: #0F172A;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
}
.sidebar-widget-title {
    font-family: var(--font-head);
    font-size: 0.72rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
}
.sidebar-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid #1E293B;
}
.sidebar-stat:last-child { border-bottom: none; }
.sidebar-stat-label { font-size: 0.73rem; color: #64748B; font-family: var(--font-body); }
.sidebar-stat-val   { font-size: 0.78rem; color: #E2E8F0; font-family: var(--font-mono); font-weight: 500; }
.sidebar-progress-bg {
    background: #1E293B;
    border-radius: 4px;
    height: 5px;
    margin-top: 4px;
    overflow: hidden;
}
.sidebar-progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.4s;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

RAW_2024 = {
    "Jan": {"gross_revenue":88400,  "net_revenue":79560,  "units":590,  "txn":441,"aov":180.4,"quota":85000, "attainment":93.6,"wins":30,"losses":22,"pipeline":225000,"conv":21.4,"new_cust":62, "ret_cust":379,"cac":238,"churn":4.8,"forecast":82000, "cogs":44600,"gm":43.9,"sales_exp":14800,"refunds":3100,"disc":8.1,"cycle":36,"rep_rev":15912,"online_pct":22,"direct_pct":60,"partner_pct":18},
    "Feb": {"gross_revenue":92100,  "net_revenue":82890,  "units":615,  "txn":461,"aov":179.9,"quota":90000, "attainment":92.1,"wins":33,"losses":24,"pipeline":248000,"conv":22.8,"new_cust":68, "ret_cust":393,"cac":225,"churn":4.5,"forecast":88000, "cogs":46500,"gm":43.9,"sales_exp":15200,"refunds":2900,"disc":7.8,"cycle":35,"rep_rev":16578,"online_pct":24,"direct_pct":58,"partner_pct":18},
    "Mar": {"gross_revenue":110500, "net_revenue":99450,  "units":739,  "txn":553,"aov":179.8,"quota":100000,"attainment":99.5,"wins":44,"losses":20,"pipeline":290000,"conv":25.7,"new_cust":88, "ret_cust":465,"cac":208,"churn":4.1,"forecast":98000, "cogs":55800,"gm":43.9,"sales_exp":17100,"refunds":3700,"disc":7.2,"cycle":32,"rep_rev":19890,"online_pct":26,"direct_pct":56,"partner_pct":18},
    "Apr": {"gross_revenue":103200, "net_revenue":92880,  "units":691,  "txn":517,"aov":179.6,"quota":105000,"attainment":88.5,"wins":38,"losses":29,"pipeline":268000,"conv":22.3,"new_cust":79, "ret_cust":438,"cac":218,"churn":4.6,"forecast":106000,"cogs":52400,"gm":43.6,"sales_exp":16400,"refunds":4200,"disc":7.9,"cycle":38,"rep_rev":18576,"online_pct":27,"direct_pct":55,"partner_pct":18},
    "May": {"gross_revenue":118700, "net_revenue":106830, "units":793,  "txn":594,"aov":179.8,"quota":112000,"attainment":95.4,"wins":48,"losses":21,"pipeline":315000,"conv":27.6,"new_cust":102,"ret_cust":492,"cac":198,"churn":3.9,"forecast":110000,"cogs":60100,"gm":43.7,"sales_exp":17900,"refunds":3800,"disc":7.1,"cycle":33,"rep_rev":21366,"online_pct":29,"direct_pct":53,"partner_pct":18},
    "Jun": {"gross_revenue":128900, "net_revenue":116010, "units":861,  "txn":645,"aov":179.8,"quota":125000,"attainment":92.8,"wins":54,"losses":23,"pipeline":345000,"conv":28.9,"new_cust":118,"ret_cust":527,"cac":185,"churn":3.5,"forecast":122000,"cogs":65200,"gm":43.8,"sales_exp":19200,"refunds":4100,"disc":6.9,"cycle":30,"rep_rev":23202,"online_pct":31,"direct_pct":52,"partner_pct":17},
}

RAW_2025 = {
    "Jan": {"gross_revenue":124500, "net_revenue":112050, "units":830,  "txn":620,"aov":180.7,"quota":110000,"attainment":101.9,"wins":42,"losses":18,"pipeline":340000,"conv":28.5,"new_cust":95, "ret_cust":525,"cac":185,"churn":3.2,"forecast":115000,"cogs":61000,"gm":45.6,"sales_exp":18200,"refunds":3800,"disc":6.2,"cycle":28,"rep_rev":20750,"online_pct":32,"direct_pct":48,"partner_pct":20},
    "Feb": {"gross_revenue":138200, "net_revenue":124380, "units":921,  "txn":689,"aov":180.5,"quota":120000,"attainment":103.7,"wins":51,"losses":15,"pipeline":385000,"conv":31.2,"new_cust":112,"ret_cust":577,"cac":172,"churn":2.8,"forecast":122000,"cogs":67200,"gm":46.0,"sales_exp":19800,"refunds":4100,"disc":5.8,"cycle":26,"rep_rev":23033,"online_pct":38,"direct_pct":44,"partner_pct":18},
    "Mar": {"gross_revenue":165800, "net_revenue":149220, "units":1105, "txn":827,"aov":180.4,"quota":150000,"attainment":99.5,"wins":63,"losses":22,"pipeline":452000,"conv":33.8,"new_cust":148,"ret_cust":679,"cac":158,"churn":2.5,"forecast":155000,"cogs":80900,"gm":51.2,"sales_exp":22100,"refunds":5100,"disc":5.2,"cycle":24,"rep_rev":27633,"online_pct":35,"direct_pct":50,"partner_pct":15},
    "Apr": {"gross_revenue":152300, "net_revenue":137070, "units":1015, "txn":760,"aov":180.4,"quota":155000,"attainment":88.4,"wins":55,"losses":28,"pipeline":420000,"conv":29.7,"new_cust":130,"ret_cust":630,"cac":168,"churn":3.1,"forecast":160000,"cogs":74600,"gm":45.1,"sales_exp":21500,"refunds":6200,"disc":6.8,"cycle":30,"rep_rev":25383,"online_pct":35,"direct_pct":40,"partner_pct":25},
    "May": {"gross_revenue":178900, "net_revenue":161010, "units":1192, "txn":894,"aov":180.2,"quota":165000,"attainment":97.6,"wins":72,"losses":19,"pipeline":510000,"conv":36.4,"new_cust":165,"ret_cust":729,"cac":145,"churn":2.2,"forecast":170000,"cogs":87200,"gm":51.3,"sales_exp":24300,"refunds":4800,"disc":4.9,"cycle":22,"rep_rev":29817,"online_pct":41,"direct_pct":42,"partner_pct":17},
    "Jun": {"gross_revenue":195600, "net_revenue":176040, "units":1304, "txn":978,"aov":180.0,"quota":180000,"attainment":97.8,"wins":81,"losses":17,"pipeline":580000,"conv":38.9,"new_cust":188,"ret_cust":790,"cac":132,"churn":1.9,"forecast":185000,"cogs":95300,"gm":51.3,"sales_exp":26800,"refunds":5200,"disc":4.5,"cycle":20,"rep_rev":32600,"online_pct":45,"direct_pct":38,"partner_pct":17},
}

def build_df(raw, year):
    rows = []
    for m in MONTHS:
        d = dict(raw[m])
        d["month"] = m
        d["year"]  = year
        d["win_rate"]   = round(d["wins"]/(d["wins"]+d["losses"])*100, 1)
        d["net_margin"] = round((d["net_revenue"]-d["cogs"]-d["sales_exp"])/d["net_revenue"]*100, 1)
        rows.append(d)
    return pd.DataFrame(rows)

df24  = build_df(RAW_2024, 2024)
df25  = build_df(RAW_2025, 2025)

tot24 = {k: sum(RAW_2024[m][k] for m in MONTHS) for k in ["net_revenue","gross_revenue","units","new_cust","wins","losses","cogs","sales_exp"]}
tot25 = {k: sum(RAW_2025[m][k] for m in MONTHS) for k in ["net_revenue","gross_revenue","units","new_cust","wins","losses","cogs","sales_exp"]}
avg24 = {k: sum(RAW_2024[m][k] for m in MONTHS)/6 for k in ["attainment","gm","churn","cac","conv","cycle","disc"]}
avg25 = {k: sum(RAW_2025[m][k] for m in MONTHS)/6 for k in ["attainment","gm","churn","cac","conv","cycle","disc"]}

def yoy(v24, v25): return round((v25-v24)/v24*100, 1)
def ys(v24, v25):
    v = yoy(v24, v25)
    return f"+{v}%" if v > 0 else f"{v}%"

# ─────────────────────────────────────────────────────────────────────────────
# CHART HELPERS  (white background)
# ─────────────────────────────────────────────────────────────────────────────
GRID  = "rgba(0,0,0,0.05)"
TICK  = "#94A3B8"
C24   = "#F59E0B"   # amber  = 2024
C25   = "#1D4ED8"   # blue   = 2025
CGREEN= "#059669"
CROSE = "#E11D48"

def theme(fig, title="", h=320):
    fig.update_layout(
        height=h,
        title=dict(text=f"<b>{title}</b>",
                   font=dict(family="Poppins,sans-serif", size=13, color="#0F172A"), x=0.01),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FAFBFC",
        font=dict(family="Inter,sans-serif", color=TICK, size=11),
        legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#E2E8F0",
                    borderwidth=1, font=dict(size=10), orientation="h",
                    yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=8, r=8, t=54, b=8),
        xaxis=dict(gridcolor=GRID, linecolor="#E2E8F0", tickfont=dict(size=10), showgrid=False),
        yaxis=dict(gridcolor=GRID, linecolor="#E2E8F0", tickfont=dict(size=10)),
    )
    return fig

def dual_bar(metric, title, ylabel="", h=320):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=MONTHS, y=df24[metric], name="H1 2024",
                          marker_color=C24, opacity=0.85,
                          marker_line=dict(width=0)))
    fig.add_trace(go.Bar(x=MONTHS, y=df25[metric], name="H1 2025",
                          marker_color=C25, opacity=0.85,
                          marker_line=dict(width=0)))
    fig.update_layout(barmode="group", bargap=0.2, bargroupgap=0.06)
    theme(fig, title, h)
    return fig

def dual_line(metric, title, h=320, fmt=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=MONTHS, y=df24[metric], name="H1 2024",
                              mode="lines+markers",
                              line=dict(color=C24, width=2.5, dash="dot"),
                              marker=dict(size=7, color=C24)))
    fig.add_trace(go.Scatter(x=MONTHS, y=df25[metric], name="H1 2025",
                              mode="lines+markers",
                              line=dict(color=C25, width=2.5),
                              marker=dict(size=7, color=C25)))
    theme(fig, title, h)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# OPENAI
# ─────────────────────────────────────────────────────────────────────────────
def ask_openai(prompt, api_key, model="gpt-4o"):
    try:
        client = OpenAI(api_key=api_key)
        r = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": (
                    "You are an elite sales analytics consultant advising a CIO. "
                    "Use MEDDIC, OKR, SPIN and SaaS/IT benchmarks. "
                    "Be direct, data-driven and executive-level. "
                    "Use numbered lists and clear sections."
                )},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3, max_tokens=2000,
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ OpenAI Error: {e}\n\nPlease verify your API key."

DATA_CONTEXT = f"""
DataForge Analytics — H1 2024 vs H1 2025 Sales Data:

H1 2024: Net Revenue=${tot24['net_revenue']:,} | Units={tot24['units']:,} | New Customers={tot24['new_cust']:,}
  Avg Attainment={avg24['attainment']:.1f}% | Avg Gross Margin={avg24['gm']:.1f}%
  Avg CAC=${avg24['cac']:.0f} | Avg Churn={avg24['churn']:.1f}%/mo | Avg Cycle={avg24['cycle']:.0f}d
  Total Wins={tot24['wins']} | Avg Conversion={avg24['conv']:.1f}%

H1 2025: Net Revenue=${tot25['net_revenue']:,} | Units={tot25['units']:,} | New Customers={tot25['new_cust']:,}
  Avg Attainment={avg25['attainment']:.1f}% | Avg Gross Margin={avg25['gm']:.1f}%
  Avg CAC=${avg25['cac']:.0f} | Avg Churn={avg25['churn']:.1f}%/mo | Avg Cycle={avg25['cycle']:.0f}d
  Total Wins={tot25['wins']} | Avg Conversion={avg25['conv']:.1f}%

Key highlights: Revenue +48.9% YoY | Gross margin broke 50% in Mar/May/Jun 2025 |
CAC dropped 29% | Churn down from 4.2% to 2.6% avg | Online channel grew 22%→45% |
April recurring attainment dip (88.4-88.5%) in both years |
Sales cycle shortened from 34d to 25d avg.
"""

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR  — settings + live KPI widgets
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:18px 0 10px 0;text-align:center'>
        <div style='font-size:2rem;margin-bottom:4px'>📊</div>
        <div style='font-family:Poppins,sans-serif;font-size:1rem;font-weight:700;
                    color:#F1F5F9;letter-spacing:-0.01em;'>Sales Intelligence</div>
        <div style='font-size:0.65rem;color:#475569;letter-spacing:0.08em;
                    text-transform:uppercase;margin-top:1px'>CIO Executive Suite</div>
    </div>
    <hr style='border:none;border-top:1px solid #1E293B;margin:8px 0 16px 0'>
    """, unsafe_allow_html=True)

    # ── Widget 1: API Settings ──────────────────────────────────────────────
    with st.expander("🔑  OpenAI Settings", expanded=True):
        api_key = st.text_input("API Key", value=os.getenv("OPENAI_API_KEY",""),
                                 type="password", placeholder="sk-...")
        model_choice = st.selectbox("Model", ["gpt-4o","gpt-4-turbo","gpt-3.5-turbo"])
        if api_key:
            st.markdown('<div style="color:#34D399;font-size:0.72rem;font-family:monospace;'
                        'margin-top:4px">✓ API key configured</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#FB923C;font-size:0.72rem;font-family:monospace;'
                        'margin-top:4px">○ No API key — AI tab disabled</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Widget 2: H1 2025 Live KPIs ────────────────────────────────────────
    st.markdown("""
    <div class="sidebar-widget">
        <div class="sidebar-widget-title">H1 2025 Snapshot</div>
    """, unsafe_allow_html=True)
    kpis_sidebar = [
        ("Net Revenue",  f"${tot25['net_revenue']/1000:.0f}K",  ys(tot24['net_revenue'],  tot25['net_revenue'])),
        ("New Customers",f"{tot25['new_cust']:,}",               ys(tot24['new_cust'],      tot25['new_cust'])),
        ("Avg Attainment",f"{avg25['attainment']:.1f}%",         f"{avg25['attainment']-avg24['attainment']:+.1f}pp"),
        ("Avg CAC",      f"${avg25['cac']:.0f}",                 f"${avg25['cac']-avg24['cac']:+.0f}"),
        ("Avg Churn",    f"{avg25['churn']:.1f}%/mo",            f"{avg25['churn']-avg24['churn']:+.1f}pp"),
        ("Sales Cycle",  f"{avg25['cycle']:.0f} days",           f"{avg25['cycle']-avg24['cycle']:+.0f}d"),
    ]
    for lbl, val, delta in kpis_sidebar:
        color = "#34D399" if delta.startswith("+") and lbl not in ("Avg CAC","Avg Churn","Sales Cycle") \
                else "#34D399" if lbl in ("Avg CAC","Avg Churn","Sales Cycle") and delta.startswith("-") \
                else "#FB923C"
        st.markdown(f"""
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">{lbl}</span>
            <span style="display:flex;flex-direction:column;align-items:flex-end;gap:1px">
                <span class="sidebar-stat-val">{val}</span>
                <span style="font-size:0.62rem;color:{color};font-family:monospace">{delta}</span>
            </span>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Widget 3: Benchmark Gauge ───────────────────────────────────────────
    st.markdown("""
    <div class="sidebar-widget">
        <div class="sidebar-widget-title">IT Benchmark Progress</div>
    """, unsafe_allow_html=True)
    benchmarks = [
        ("Gross Margin",    avg25['gm'],    65,  "#3B82F6"),
        ("Quota Attainment",avg25['attainment'], 100, "#10B981"),
        ("Win Rate",        tot25['wins']/(tot25['wins']+tot25['losses'])*100, 50, "#8B5CF6"),
        ("Churn Control",   (5-avg25['churn'])/5*100, 100, "#F59E0B"),
    ]
    for label, current, target, color in benchmarks:
        pct = min(int(current/target*100), 100)
        st.markdown(f"""
        <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                <span style="font-size:0.7rem;color:#64748B">{label}</span>
                <span style="font-size:0.7rem;color:#94A3B8;font-family:monospace">{current:.1f}% / {target}%</span>
            </div>
            <div class="sidebar-progress-bg">
                <div class="sidebar-progress-fill" style="width:{pct}%;background:{color}"></div>
            </div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Widget 4: Report Info ───────────────────────────────────────────────
    st.markdown("""
    <div class="sidebar-widget">
        <div class="sidebar-widget-title">Report Info</div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">Period</span>
            <span class="sidebar-stat-val">Jan–Jun 2024/25</span>
        </div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">Company</span>
            <span class="sidebar-stat-val">DataForge</span>
        </div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">Framework</span>
            <span class="sidebar-stat-val">MEDDIC+OKR</span>
        </div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">Industry</span>
            <span class="sidebar-stat-val">IT / SaaS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;margin-top:8px;font-size:0.62rem;color:#1E293B'>
        DataForge Analytics · Hackathon 2025<br>AI by OpenAI GPT-4
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px">
    <div>
      <div class="page-header-title">Sales Performance Dashboard</div>
      <div class="page-header-sub">H1 2024 vs H1 2025 · Year-over-Year Analysis · CIO Review</div>
      <div>
        <span class="header-badge">⚡ LIVE DATA</span>
        <span class="header-badge">📈 YoY BENCHMARKING</span>
        <span class="header-badge">🤖 GPT-4 INSIGHTS</span>
        <span class="header-badge">🎯 H2 ROADMAP</span>
      </div>
    </div>
    <div style="text-align:right">
      <div style="font-family:'Roboto Mono',monospace;font-size:0.68rem;color:rgba(255,255,255,0.45)">REPORT SCOPE</div>
      <div style="font-family:Poppins,sans-serif;font-size:1.1rem;font-weight:700;color:white">Jan – Jun 2025</div>
      <div style="font-family:'Roboto Mono',monospace;font-size:0.68rem;color:rgba(255,255,255,0.35);margin-top:2px">DataForge Analytics Team</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TOP-LEVEL KPI ROW (always visible)
# ─────────────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("Net Revenue H1 2025",  f"${tot25['net_revenue']/1000:.0f}K",  ys(tot24['net_revenue'],tot25['net_revenue']))
k2.metric("Units Sold H1 2025",   f"{tot25['units']:,}",                  ys(tot24['units'],tot25['units']))
k3.metric("New Customers",         f"{tot25['new_cust']:,}",               ys(tot24['new_cust'],tot25['new_cust']))
k4.metric("Avg Gross Margin",      f"{avg25['gm']:.1f}%",                  f"{avg25['gm']-avg24['gm']:+.1f}pp")
k5.metric("Avg Quota Attainment",  f"{avg25['attainment']:.1f}%",          f"{avg25['attainment']-avg24['attainment']:+.1f}pp")
k6.metric("Avg Sales Cycle",       f"{avg25['cycle']:.0f} days",           f"{avg25['cycle']-avg24['cycle']:+.0f}d")

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏠  Overview",
    "💰  Revenue & Volume",
    "🎯  Sales Performance",
    "👥  Customer Intel",
    "📈  Profitability",
    "📡  Channel Strategy",
    "🤖  AI Analysis",
    "🚀  H2 Action Plan",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Side-by-side scorecard · H1 2024 vs H1 2025</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2], gap="large")
    with col_l:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=MONTHS, y=df24["net_revenue"]/1000, name="H1 2024",
                              marker_color=C24, opacity=0.85, marker_line_width=0))
        fig.add_trace(go.Bar(x=MONTHS, y=df25["net_revenue"]/1000, name="H1 2025",
                              marker_color=C25, opacity=0.85, marker_line_width=0))
        fig.update_layout(barmode="group", bargap=0.18, bargroupgap=0.06)
        theme(fig, "Net Revenue Comparison (USD thousands)", 330)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        cats = ["Revenue Growth","Quota Attainment","Gross Margin","Win Rate","Cust. Acq.","Conversion"]
        v24r = [round(tot24['net_revenue']/tot25['net_revenue']*100),
                round(avg24['attainment']),
                round(avg24['gm']*2),
                round(tot24['wins']/(tot24['wins']+tot24['losses'])*100),
                round(tot24['new_cust']/tot25['new_cust']*100),
                round(avg24['conv']*2.5)]
        v25r = [100, round(avg25['attainment']),
                round(avg25['gm']*2),
                round(tot25['wins']/(tot25['wins']+tot25['losses'])*100),
                100,
                round(avg25['conv']*2.5)]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(r=v24r+[v24r[0]], theta=cats+[cats[0]],
                                         fill='toself', name='H1 2024',
                                         line_color=C24, fillcolor="rgba(245,158,11,0.10)"))
        fig_r.add_trace(go.Scatterpolar(r=v25r+[v25r[0]], theta=cats+[cats[0]],
                                         fill='toself', name='H1 2025',
                                         line_color=C25, fillcolor="rgba(29,78,216,0.10)"))
        fig_r.update_layout(
            polar=dict(
                bgcolor="#FAFBFC",
                radialaxis=dict(visible=True, range=[0,115], tickfont=dict(size=8), gridcolor=GRID),
                angularaxis=dict(tickfont=dict(size=9), gridcolor=GRID),
            ),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
            legend=dict(bgcolor="rgba(255,255,255,0.9)", bordercolor="#E2E8F0", borderwidth=1,
                        font=dict(size=10), orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            margin=dict(l=10,r=10,t=44,b=10), height=330,
            title=dict(text="<b>Performance Radar: 2024 vs 2025</b>",
                       font=dict(family="Poppins,sans-serif",size=13,color="#0F172A"), x=0.01),
        )
        st.plotly_chart(fig_r, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Head-to-head scorecard</div>', unsafe_allow_html=True)

    score = {
        "Metric":         ["Net Revenue (H1 Total)","Total Units","New Customers","Avg Quota Attainment",
                           "Avg Gross Margin","Avg CAC","Avg Churn Rate","Avg Sales Cycle",
                           "Total Wins","Avg Win Rate"],
        "H1 2024":        [f"${tot24['net_revenue']:,}", f"{tot24['units']:,}", f"{tot24['new_cust']:,}",
                           f"{avg24['attainment']:.1f}%", f"{avg24['gm']:.1f}%", f"${avg24['cac']:.0f}",
                           f"{avg24['churn']:.1f}%/mo", f"{avg24['cycle']:.0f} days",
                           str(tot24['wins']),
                           f"{tot24['wins']/(tot24['wins']+tot24['losses'])*100:.1f}%"],
        "H1 2025":        [f"${tot25['net_revenue']:,}", f"{tot25['units']:,}", f"{tot25['new_cust']:,}",
                           f"{avg25['attainment']:.1f}%", f"{avg25['gm']:.1f}%", f"${avg25['cac']:.0f}",
                           f"{avg25['churn']:.1f}%/mo", f"{avg25['cycle']:.0f} days",
                           str(tot25['wins']),
                           f"{tot25['wins']/(tot25['wins']+tot25['losses'])*100:.1f}%"],
        "YoY Change":     [ys(tot24['net_revenue'],tot25['net_revenue']),
                           ys(tot24['units'],tot25['units']),
                           ys(tot24['new_cust'],tot25['new_cust']),
                           f"{avg25['attainment']-avg24['attainment']:+.1f}pp",
                           f"{avg25['gm']-avg24['gm']:+.1f}pp",
                           ys(avg24['cac'],avg25['cac']),
                           f"{avg25['churn']-avg24['churn']:+.1f}pp",
                           f"{avg25['cycle']-avg24['cycle']:+.0f}d",
                           ys(tot24['wins'],tot25['wins']),
                           f"{(tot25['wins']/(tot25['wins']+tot25['losses'])-tot24['wins']/(tot24['wins']+tot24['losses']))*100:+.1f}pp"],
    }
    st.dataframe(pd.DataFrame(score), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REVENUE & VOLUME
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-title">Revenue & Volume</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Gross/Net Revenue · Units Sold · AOV · MoM Growth</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=MONTHS, y=df24["net_revenue"]/1000, name="H1 2024",
                                  mode="lines+markers",
                                  line=dict(color=C24, width=2.5, dash="dot"),
                                  fill='tozeroy', fillcolor="rgba(245,158,11,0.05)",
                                  marker=dict(size=7)))
        fig.add_trace(go.Scatter(x=MONTHS, y=df25["net_revenue"]/1000, name="H1 2025",
                                  mode="lines+markers",
                                  line=dict(color=C25, width=2.5),
                                  fill='tozeroy', fillcolor="rgba(29,78,216,0.05)",
                                  marker=dict(size=7)))
        theme(fig, "Net Revenue Trend ($K)", 300)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.plotly_chart(dual_bar("units", "Units Sold per Month", h=300), use_container_width=True)

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        mom24 = [None]+[round((df24["net_revenue"].iloc[i]-df24["net_revenue"].iloc[i-1])/df24["net_revenue"].iloc[i-1]*100,1) for i in range(1,6)]
        mom25 = [None]+[round((df25["net_revenue"].iloc[i]-df25["net_revenue"].iloc[i-1])/df25["net_revenue"].iloc[i-1]*100,1) for i in range(1,6)]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=MONTHS[1:], y=mom24[1:], name="H1 2024 MoM%",
                               marker_color=C24, opacity=0.85, marker_line_width=0))
        fig3.add_trace(go.Bar(x=MONTHS[1:], y=mom25[1:], name="H1 2025 MoM%",
                               marker_color=C25, opacity=0.85, marker_line_width=0))
        fig3.add_hline(y=0, line_color="rgba(0,0,0,0.15)")
        fig3.update_layout(barmode="group")
        theme(fig3, "Month-over-Month Revenue Growth (%)", 300)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.plotly_chart(dual_line("aov", "Average Order Value ($)", 300), use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    rev_tbl = pd.DataFrame({
        "Month":          MONTHS,
        "Gross Rev 2024": [f"${RAW_2024[m]['gross_revenue']:,}" for m in MONTHS],
        "Net Rev 2024":   [f"${RAW_2024[m]['net_revenue']:,}"   for m in MONTHS],
        "Gross Rev 2025": [f"${RAW_2025[m]['gross_revenue']:,}" for m in MONTHS],
        "Net Rev 2025":   [f"${RAW_2025[m]['net_revenue']:,}"   for m in MONTHS],
        "YoY Rev%":       [ys(RAW_2024[m]['net_revenue'],RAW_2025[m]['net_revenue']) for m in MONTHS],
        "Units 2024":     [RAW_2024[m]['units'] for m in MONTHS],
        "Units 2025":     [RAW_2025[m]['units'] for m in MONTHS],
        "Units YoY%":     [ys(RAW_2024[m]['units'],RAW_2025[m]['units']) for m in MONTHS],
    })
    st.dataframe(rev_tbl, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SALES PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title">Sales Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Quota Attainment · Win/Loss · Pipeline · Conversion Rate</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=MONTHS, y=df24["attainment"], name="H1 2024",
                                  mode="lines+markers+text",
                                  line=dict(color=C24, width=2.5, dash="dot"),
                                  marker=dict(size=8),
                                  text=[f"{v:.0f}%" for v in df24["attainment"]],
                                  textposition="top right", textfont=dict(size=9, color=C24)))
        fig.add_trace(go.Scatter(x=MONTHS, y=df25["attainment"], name="H1 2025",
                                  mode="lines+markers+text",
                                  line=dict(color=C25, width=2.5),
                                  marker=dict(size=8),
                                  text=[f"{v:.0f}%" for v in df25["attainment"]],
                                  textposition="top left", textfont=dict(size=9, color=C25)))
        fig.add_hline(y=100, line_dash="dash", line_color="#059669",
                      annotation_text="100% Target", annotation_font_color="#059669",
                      annotation_font_size=9)
        fig.add_hline(y=90,  line_dash="dot",  line_color="#E11D48",
                      annotation_text="90% Danger", annotation_font_color="#E11D48",
                      annotation_font_size=9)
        theme(fig, "Quota Attainment % — 2024 vs 2025", 320)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.plotly_chart(dual_bar("win_rate", "Win Rate % per Month", h=320), use_container_width=True)

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=MONTHS, y=df24["pipeline"]/1000, name="H1 2024",
                                   mode="lines+markers", line=dict(color=C24,width=2,dash="dot"),
                                   fill='tozeroy', fillcolor="rgba(245,158,11,0.05)"))
        fig3.add_trace(go.Scatter(x=MONTHS, y=df25["pipeline"]/1000, name="H1 2025",
                                   mode="lines+markers", line=dict(color=C25,width=2),
                                   fill='tozeroy', fillcolor="rgba(29,78,216,0.05)"))
        theme(fig3, "Pipeline Value ($K)", 300)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.plotly_chart(dual_line("conv", "Pipeline Conversion Rate (%)", 300), use_container_width=True)

    # Wins vs Losses waterfall
    labels_wl = [f"{m} '24" for m in MONTHS] + [f"{m} '25" for m in MONTHS]
    wins_all   = [RAW_2024[m]["wins"] for m in MONTHS] + [RAW_2025[m]["wins"] for m in MONTHS]
    losses_all = [-RAW_2024[m]["losses"] for m in MONTHS] + [-RAW_2025[m]["losses"] for m in MONTHS]
    colors_wl  = [C24]*6 + [C25]*6

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=labels_wl, y=wins_all,   name="Wins",
                           marker_color=colors_wl, opacity=0.85, marker_line_width=0))
    fig5.add_trace(go.Bar(x=labels_wl, y=losses_all, name="Losses",
                           marker_color=colors_wl, opacity=0.35, marker_line_width=0))
    fig5.add_hline(y=0, line_color="rgba(0,0,0,0.15)")
    fig5.update_layout(barmode="relative")
    theme(fig5, "Wins (+) vs Losses (−) Waterfall — All Months", 300)
    st.plotly_chart(fig5, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — CUSTOMER INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title">Customer Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Acquisition · CAC · Churn · Retention · LTV Signals</div>', unsafe_allow_html=True)

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Total New Customers 2025", f"{tot25['new_cust']:,}",    f"+{tot25['new_cust']-tot24['new_cust']:,} vs 2024")
    m2.metric("Avg CAC 2025",             f"${avg25['cac']:.0f}",      f"${avg25['cac']-avg24['cac']:+.0f} vs 2024")
    m3.metric("Avg Monthly Churn 2025",   f"{avg25['churn']:.1f}%",    f"{avg25['churn']-avg24['churn']:+.1f}pp")
    m4.metric("Jun 2025 Churn",           "1.9%",                      "−1.6pp vs Jun 2024")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.plotly_chart(dual_bar("new_cust", "New Customer Acquisition per Month", h=295), use_container_width=True)
    with c2:
        fig_cac = go.Figure()
        fig_cac.add_trace(go.Scatter(x=MONTHS, y=df24["cac"], name="CAC 2024",
                                      mode="lines+markers", line=dict(color=C24,width=2.5,dash="dot"),
                                      marker=dict(size=8, symbol="diamond")))
        fig_cac.add_trace(go.Scatter(x=MONTHS, y=df25["cac"], name="CAC 2025",
                                      mode="lines+markers", line=dict(color=C25,width=2.5),
                                      marker=dict(size=8, symbol="diamond")))
        theme(fig_cac, "Customer Acquisition Cost ($) Trend", 295)
        st.plotly_chart(fig_cac, use_container_width=True)

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        fig_ch = go.Figure()
        fig_ch.add_trace(go.Scatter(x=MONTHS, y=df24["churn"], name="Churn 2024",
                                     mode="lines+markers",
                                     line=dict(color=CROSE, width=2.5, dash="dot"),
                                     marker=dict(size=7)))
        fig_ch.add_trace(go.Scatter(x=MONTHS, y=df25["churn"], name="Churn 2025",
                                     mode="lines+markers",
                                     line=dict(color=CGREEN, width=2.5),
                                     marker=dict(size=7)))
        fig_ch.add_hline(y=2.0, line_dash="dash", line_color="#059669",
                         annotation_text="2% IT Target", annotation_font_size=9,
                         annotation_font_color="#059669")
        theme(fig_ch, "Monthly Churn Rate % — Lower is Better", 295)
        st.plotly_chart(fig_ch, use_container_width=True)

    with c4:
        fig_mix = go.Figure()
        fig_mix.add_trace(go.Bar(x=[f"{m} '25" for m in MONTHS], y=df25["new_cust"],
                                  name="New", marker_color=C25, opacity=0.9, marker_line_width=0))
        fig_mix.add_trace(go.Bar(x=[f"{m} '25" for m in MONTHS], y=df25["ret_cust"],
                                  name="Returning", marker_color="#06B6D4", opacity=0.75, marker_line_width=0))
        fig_mix.update_layout(barmode="stack")
        theme(fig_mix, "2025: New vs Returning Customer Mix", 295)
        st.plotly_chart(fig_mix, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">CAC Efficiency & LTV Signals — IT Industry Benchmarks</div>', unsafe_allow_html=True)
    bench_tbl = pd.DataFrame({
        "Metric":         ["Avg CAC H1 2024","Avg CAC H1 2025","CAC Improvement",
                           "Avg Churn H1 2024","Avg Churn H1 2025","Churn Improvement",
                           "Est. LTV:CAC 2024","Est. LTV:CAC 2025","IT SaaS Target"],
        "Value":          [f"${avg24['cac']:.0f}", f"${avg25['cac']:.0f}",
                           f"-{yoy(avg24['cac'],avg25['cac'])*-1:.1f}%",
                           f"{avg24['churn']:.1f}%/mo", f"{avg25['churn']:.1f}%/mo",
                           f"-{avg24['churn']-avg25['churn']:.1f}pp",
                           f"~{180/avg24['cac']*12:.1f}x", f"~{180/avg25['cac']*14:.1f}x",
                           "LTV:CAC ≥ 3x · Churn < 2%/mo"],
        "Status":         ["Baseline","✅ Improved","✅ 29% reduction",
                           "⚠️ Above target","✅ Near target","✅ Trending down",
                           "⚠️ Below 3x","✅ Approaching 3x","Industry Standard"],
    })
    st.dataframe(bench_tbl, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PROFITABILITY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-title">Profitability Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Gross Margin · Net Margin · COGS · Sales Efficiency · Rep Productivity</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        fig_gm = go.Figure()
        fig_gm.add_trace(go.Scatter(x=MONTHS, y=df24["gm"], name="Gross Margin 2024",
                                     mode="lines+markers",
                                     line=dict(color=C24,width=2.5,dash="dot"),
                                     fill='tozeroy', fillcolor="rgba(245,158,11,0.05)"))
        fig_gm.add_trace(go.Scatter(x=MONTHS, y=df25["gm"], name="Gross Margin 2025",
                                     mode="lines+markers",
                                     line=dict(color=C25,width=2.5),
                                     fill='tozeroy', fillcolor="rgba(29,78,216,0.05)"))
        fig_gm.add_hrect(y0=50, y1=56, fillcolor="rgba(5,150,105,0.06)", line_width=0,
                         annotation_text="50%+ Milestone", annotation_font_size=9,
                         annotation_font_color="#059669")
        theme(fig_gm, "Gross Margin % Trend", 310)
        st.plotly_chart(fig_gm, use_container_width=True)

    with c2:
        st.plotly_chart(dual_line("net_margin", "Net Margin % (after Sales Expenses)", 310), use_container_width=True)

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        fig_cogs = go.Figure()
        fig_cogs.add_trace(go.Bar(x=MONTHS, y=df25["net_revenue"]/1000, name="Net Revenue",
                                   marker_color=C25, opacity=0.85, marker_line_width=0))
        fig_cogs.add_trace(go.Bar(x=MONTHS, y=df25["cogs"]/1000, name="COGS",
                                   marker_color=CROSE, opacity=0.7, marker_line_width=0))
        fig_cogs.add_trace(go.Bar(x=MONTHS, y=df25["sales_exp"]/1000, name="Sales Exp",
                                   marker_color=C24, opacity=0.7, marker_line_width=0))
        fig_cogs.update_layout(barmode="overlay")
        theme(fig_cogs, "2025: Revenue vs COGS vs Sales Expenses ($K)", 300)
        st.plotly_chart(fig_cogs, use_container_width=True)

    with c4:
        fig_disc = go.Figure()
        fig_disc.add_trace(go.Scatter(x=MONTHS, y=df24["disc"], name="Discount% 2024",
                                       mode="lines+markers", line=dict(color=C24,width=2.5,dash="dot"),
                                       marker=dict(size=7)))
        fig_disc.add_trace(go.Scatter(x=MONTHS, y=df25["disc"], name="Discount% 2025",
                                       mode="lines+markers", line=dict(color=C25,width=2.5),
                                       marker=dict(size=7)))
        fig_disc.add_hline(y=5.0, line_dash="dash", line_color="#059669",
                           annotation_text="5% Target", annotation_font_size=9,
                           annotation_font_color="#059669")
        theme(fig_disc, "Discount Rate % — Pricing Power Signal", 300)
        st.plotly_chart(fig_disc, use_container_width=True)

    st.plotly_chart(dual_bar("rep_rev", "Revenue per Sales Rep ($) — Productivity", h=290),
                    use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — CHANNEL STRATEGY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-title">Channel Strategy</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Direct vs Online vs Partner · Digital Shift · Sales Velocity</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        fig_ch = go.Figure()
        fig_ch.add_trace(go.Scatter(x=MONTHS, y=df24["online_pct"], name="Online 2024",
                                     mode="lines+markers", line=dict(color=C24,width=2,dash="dot"),
                                     marker=dict(size=6)))
        fig_ch.add_trace(go.Scatter(x=MONTHS, y=df25["online_pct"], name="Online 2025",
                                     mode="lines+markers", line=dict(color=C25,width=2.5),
                                     marker=dict(size=7)))
        fig_ch.add_trace(go.Scatter(x=MONTHS, y=df25["direct_pct"], name="Direct 2025",
                                     mode="lines+markers", line=dict(color="#0891B2",width=2,dash="dash"),
                                     marker=dict(size=6)))
        theme(fig_ch, "Online vs Direct Channel Share % (2024→2025)", 320)
        st.plotly_chart(fig_ch, use_container_width=True)

    with c2:
        fig_pie = make_subplots(rows=1, cols=2, specs=[[{"type":"pie"},{"type":"pie"}]],
                                 subplot_titles=["Jun 2024 Mix","Jun 2025 Mix"])
        fig_pie.add_trace(go.Pie(
            labels=["Direct","Online","Partner"],
            values=[RAW_2024["Jun"]["direct_pct"],RAW_2024["Jun"]["online_pct"],RAW_2024["Jun"]["partner_pct"]],
            marker_colors=[C24,"#FB923C","#FCD34D"], hole=0.52,
            textfont_size=10, showlegend=True), 1,1)
        fig_pie.add_trace(go.Pie(
            labels=["Direct","Online","Partner"],
            values=[RAW_2025["Jun"]["direct_pct"],RAW_2025["Jun"]["online_pct"],RAW_2025["Jun"]["partner_pct"]],
            marker_colors=[C25,"#0891B2","#7C3AED"], hole=0.52,
            textfont_size=10, showlegend=False), 1,2)
        fig_pie.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                               font=dict(color="#334155",size=10), height=320,
                               margin=dict(l=8,r=8,t=44,b=8),
                               legend=dict(bgcolor="rgba(255,255,255,0.9)",bordercolor="#E2E8F0",
                                           borderwidth=1,font=dict(size=10)),
                               title=dict(text="<b>Channel Mix: Jun 2024 vs Jun 2025</b>",
                                          font=dict(family="Poppins,sans-serif",size=13,color="#0F172A"),x=0.01))
        st.plotly_chart(fig_pie, use_container_width=True)

    c3, c4 = st.columns(2, gap="medium")
    with c3:
        fig_cyc = go.Figure()
        fig_cyc.add_trace(go.Bar(x=MONTHS, y=df24["cycle"], name="H1 2024",
                                  marker_color=C24, opacity=0.85, marker_line_width=0))
        fig_cyc.add_trace(go.Bar(x=MONTHS, y=df25["cycle"], name="H1 2025",
                                  marker_color=C25, opacity=0.85, marker_line_width=0))
        fig_cyc.add_hline(y=30, line_dash="dash", line_color="#059669",
                          annotation_text="30-day benchmark", annotation_font_size=9,
                          annotation_font_color="#059669")
        fig_cyc.update_layout(barmode="group")
        theme(fig_cyc, "Sales Cycle Days — Velocity Improvement", 295)
        st.plotly_chart(fig_cyc, use_container_width=True)

    with c4:
        fig_stk = go.Figure()
        fig_stk.add_trace(go.Scatter(x=MONTHS, y=df25["direct_pct"], name="Direct",
                                      stackgroup="one", fillcolor="rgba(29,78,216,0.55)",
                                      line=dict(color="rgba(29,78,216,0.7)",width=1)))
        fig_stk.add_trace(go.Scatter(x=MONTHS, y=df25["online_pct"], name="Online",
                                      stackgroup="one", fillcolor="rgba(8,145,178,0.55)",
                                      line=dict(color="rgba(8,145,178,0.7)",width=1)))
        fig_stk.add_trace(go.Scatter(x=MONTHS, y=df25["partner_pct"], name="Partner",
                                      stackgroup="one", fillcolor="rgba(124,58,237,0.45)",
                                      line=dict(color="rgba(124,58,237,0.7)",width=1)))
        theme(fig_stk, "2025 Channel Composition (Stacked %)", 295)
        st.plotly_chart(fig_stk, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — AI ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-title">AI-Powered Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">GPT-4 · MEDDIC · OKR · IT Industry Benchmarks · Strategic Insights</div>', unsafe_allow_html=True)

    if not api_key:
        st.markdown("""
        <div class="info-widget">
            <b>⚠️ OpenAI API Key Required</b><br>
            Enter your API key in the <b>OpenAI Settings</b> widget in the left sidebar to enable AI analysis.
        </div>
        """, unsafe_allow_html=True)
    else:
        analysis_opts = [
            "Executive Summary & YoY Assessment",
            "MEDDIC Framework Analysis",
            "IT Industry Benchmark Comparison",
            "Root Cause Analysis: April Dip",
            "Channel Strategy Assessment",
            "Customer Health & Retention Analysis",
            "Competitive Positioning & Pricing Power",
            "Custom Question",
        ]

        sel_col, btn_col = st.columns([3, 1], gap="medium")
        with sel_col:
            analysis_type = st.selectbox("Select Analysis Mode", analysis_opts, label_visibility="collapsed")
        with btn_col:
            run_btn = st.button("🤖 Analyse", use_container_width=True)

        PROMPTS = {
            "Executive Summary & YoY Assessment":
                f"{DATA_CONTEXT}\n\nProvide a 400-word executive summary for the CIO covering: "
                "1) Top 5 YoY highlights with specific numbers, 2) Key concerns, "
                "3) Overall scorecard rating (A/B/C/D) with IT-industry justification.",
            "MEDDIC Framework Analysis":
                f"{DATA_CONTEXT}\n\nAnalyse this sales team using MEDDIC "
                "(Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion). "
                "For each, rate maturity 1-5 and cite specific evidence from the data.",
            "IT Industry Benchmark Comparison":
                f"{DATA_CONTEXT}\n\nCompare results against IT/SaaS benchmarks (Gartner, Forrester, "
                "SaaS metrics): win rates, CAC ratios, churn, gross margins, sales cycles, quota attainment. "
                "Score each area Red/Amber/Green.",
            "Root Cause Analysis: April Dip":
                f"{DATA_CONTEXT}\n\nConduct a 5-Why root cause analysis of the April dip "
                "(both 2024: 88.5% and 2025: 88.4%). What structural/seasonal factors? "
                "What preventative measures?",
            "Channel Strategy Assessment":
                f"{DATA_CONTEXT}\n\nAnalyse the Direct→Online channel transformation using "
                "SiriusDecisions Demand Waterfall. Revenue implications? "
                "Risks with Partner stuck at 17%?",
            "Customer Health & Retention Analysis":
                f"{DATA_CONTEXT}\n\nCalculate estimated LTV, payback period, NRR implications. "
                "Compare against IT benchmarks (churn <2%/mo, LTV:CAC >3x). "
                "Which retention programs should be prioritised?",
            "Competitive Positioning & Pricing Power":
                f"{DATA_CONTEXT}\n\nAssess competitive positioning: discount rate 8.1%→4.5%, "
                "AOV stability $179-180, gross margin 43.8%→51.3%. "
                "What does this tell us about pricing power? H2 2025 pricing strategy?",
            "Custom Question": None,
        }

        custom_q = ""
        if analysis_type == "Custom Question":
            custom_q = st.text_area("Enter your question:",
                                     placeholder="e.g. What sales methodology should we adopt for H2 2025?",
                                     height=90)

        if run_btn:
            with st.spinner("GPT-4 is analysing your data..."):
                prompt = f"{DATA_CONTEXT}\n\n{custom_q}" if analysis_type == "Custom Question" and custom_q \
                         else PROMPTS.get(analysis_type, DATA_CONTEXT + "\n\nSummarise the data.")
                result = ask_openai(prompt, api_key, model_choice)

            st.markdown(f'<div class="ai-card">{result.replace(chr(10),"<br>")}</div>',
                        unsafe_allow_html=True)
            st.download_button("📥 Download Analysis",
                                result,
                                file_name=f"ai_{analysis_type[:25].replace(' ','_')}.txt",
                                mime="text/plain")

        # Quick insight cards
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Quick Data Highlights</div>', unsafe_allow_html=True)
        insights = [
            ("#1D4ED8","Revenue Surge",
             f"Net revenue grew +48.9% YoY from ${tot24['net_revenue']/1000:.0f}K to ${tot25['net_revenue']/1000:.0f}K. "
             f"Jun 2025 alone delivered ${RAW_2025['Jun']['net_revenue']/1000:.0f}K — the single best month on record."),
            ("#059669","Margin Breakthrough",
             "Gross margin crossed the 50% threshold for the first time in Mar 2025 (51.2%) and held above 51% "
             "in May and June. The 2024 margin was flatlined at 43.8% all half-year."),
            ("#0891B2","Digital Channel Takeover",
             "Online channel share surged from 22% (Jan 2024) to 45% (Jun 2025), overtaking Direct for the "
             "first time in May 2025. This structural shift lowers CAC and shortens sales cycles."),
            ("#E11D48","April Anomaly — Recurring Risk",
             "April dipped to 88.5% attainment in 2024 and 88.4% in 2025 — the only sub-90% months in both years. "
             "Coincides with longest sales cycle (38d→30d) and highest churn. Structural, not random."),
            ("#7C3AED","CAC Efficiency",
             f"Customer Acquisition Cost fell from avg ${avg24['cac']:.0f} in 2024 to ${avg25['cac']:.0f} in 2025 "
             f"(-29%). New customer acquisition grew 62% (517→838) while spending less per acquisition."),
        ]
        c1, c2 = st.columns(2, gap="medium")
        for i, (clr, title, body) in enumerate(insights):
            col = c1 if i % 2 == 0 else c2
            with col:
                st.markdown(f"""
                <div class="insight-card" style="border-left:4px solid {clr}">
                    <div class="insight-title" style="color:{clr}">{title}</div>
                    <div class="insight-body">{body}</div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — H2 ACTION PLAN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-title">H2 2025 Action Plan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">OKRs · 90-Day Sprint · IT Benchmark Scorecard · AI Roadmap</div>', unsafe_allow_html=True)

    # Projections
    st.markdown("#### 📊 H2 2025 Revenue Projections")
    p1,p2,p3,p4 = st.columns(4)
    p1.metric("H1 2025 Actual",       "$859,770",   "Baseline")
    p2.metric("H2 Conservative",      "$980,000",   "+14% vs H1")
    p3.metric("H2 Target",            "$1,120,000", "+30% vs H1")
    p4.metric("H2 Stretch",           "$1,280,000", "+49% vs H1")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # OKRs in sub-tabs
    st.markdown("#### 🎯 H2 2025 OKRs")
    okr_tabs = st.tabs(["O1: Revenue","O2: Digital","O3: Customer","O4: Margin","O5: April Risk"])
    okrs = [
        ("#1D4ED8",[
            "KR1: Achieve $1.1M+ net revenue in H2 2025 (28% above H1)",
            "KR2: Reach 100%+ quota attainment every month in H2",
            "KR3: Grow pipeline to $700K+ by Dec 2025",
        ]),
        ("#0891B2",[
            "KR1: Grow online channel to 55%+ share by Dec 2025",
            "KR2: Reduce average sales cycle to ≤18 days by Q4",
            "KR3: Launch 2 new digital demand-gen campaigns by Aug 2025",
        ]),
        ("#059669",[
            "KR1: Reduce monthly churn to <1.5% by Dec 2025",
            "KR2: Achieve LTV:CAC ratio of 3.0x+ across all segments",
            "KR3: Increase net revenue retention (NRR) to 115%+",
        ]),
        ("#D97706",[
            "KR1: Maintain gross margin above 52% every month in H2",
            "KR2: Reduce average discount rate to below 4% by Dec 2025",
            "KR3: Improve net margin to 35%+ by Q4 2025",
        ]),
        ("#7C3AED",[
            "KR1: Pre-load 40% of Jul pipeline before Jun 30",
            "KR2: Implement seasonal quota adjustment model by Jul 1",
            "KR3: Deploy early-warning attainment dashboard by Jul 15",
        ]),
    ]
    for tab, (clr, krs) in zip(okr_tabs, okrs):
        with tab:
            for kr in krs:
                st.markdown(f"""
                <div class="okr-kr" style="border-left-color:{clr};margin:8px 0">
                    <span style="color:{clr};font-weight:700">{kr[:3]}</span>
                    <span style="color:#334155">{kr[3:]}</span>
                </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # 90-Day Sprint
    st.markdown("#### 🚀 90-Day Execution Sprint (Jul–Sep 2025)")
    sprints = [
        ("Jul Wk 1–2","Pre-load Pipeline","#1D4ED8",
         "Sales ops to qualify $420K+ in Jul–Aug pipeline before Jul 1. Assign top reps to enterprise accounts."),
        ("Jul Wk 3–4","Digital Channel Blitz","#0891B2",
         "Launch LinkedIn + intent-data campaigns. Target 50% online share by Jul end. Enable self-serve demos."),
        ("Aug Wk 1–2","Churn Intervention","#059669",
         "Identify customers 90d+ without engagement. Assign CSMs to top-50 at-risk accounts. Target 1.5% churn."),
        ("Aug Wk 3–4","Pricing Power Initiative","#D97706",
         "Eliminate discretionary discounts >5% without VP approval. Roll out value-based pricing playbook."),
        ("Sep Wk 1–2","Partner Channel Revamp","#7C3AED",
         "Audit Partner at 17%. Recruit 3 new strategic partners in underserved verticals. Target 22% by Q4."),
        ("Sep Wk 3–4","Q4 Planning & Lock","#E11D48",
         "Lock Q4 quotas with seasonal adjustment. Run pipeline health check. Forecast $600K+ Q4 pipeline."),
    ]
    sc1, sc2 = st.columns(2, gap="medium")
    for i, (period, title, clr, detail) in enumerate(sprints):
        col = sc1 if i % 2 == 0 else sc2
        with col:
            st.markdown(f"""
            <div class="sprint-card">
                <div>
                    <span class="sprint-period" style="color:{clr};border-color:{clr};
                                background:{clr}18">{period}</span>
                </div>
                <div>
                    <div class="sprint-title">{title}</div>
                    <div class="sprint-body">{detail}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Benchmark Scorecard
    st.markdown("#### 📋 IT Industry Benchmark Scorecard")
    bench_df = pd.DataFrame({
        "Metric":        ["Gross Margin","Quota Attainment","Win Rate","Sales Cycle",
                          "Churn Rate","CAC Payback","Discount Rate","Pipeline Coverage"],
        "IT Benchmark":  ["≥ 65% SaaS","≥ 100%","≥ 50%","≤ 30 days",
                          "< 2%/mo","< 12 months","< 5%","≥ 3x quota"],
        "H1 2024":       ["43.8% ❌","93.6% ❌","62.3% ✅","34 days ❌",
                          "4.2% ❌","~14 mo ❌","7.5% ❌","~2.5x ❌"],
        "H1 2025":       ["48.4% ⚠️","98.1% ⚠️","75.4% ✅","25 days ✅",
                          "2.6% ⚠️","~10 mo ⚠️","5.5% ⚠️","~3.0x ✅"],
        "H2 2025 Target":["52%+","100%+","78%+","≤18 days",
                          "<1.5%","<9 months","<4%","3.5x+"],
        "Priority":      ["HIGH","CRITICAL","MEDIUM","HIGH",
                          "CRITICAL","HIGH","MEDIUM","HIGH"],
    })
    st.dataframe(bench_df, use_container_width=True, hide_index=True)

    # AI Roadmap
    if api_key:
        st.markdown("#### 🤖 AI-Generated H2 Roadmap")
        if st.button("✨ Generate Full AI H2 Action Plan", use_container_width=True):
            with st.spinner("GPT-4 is crafting your H2 roadmap..."):
                prompt = f"""{DATA_CONTEXT}

As an elite sales strategy consultant reporting to the CIO, produce a comprehensive H2 2025 action plan:
1. Top 5 strategic priorities ranked by revenue impact
2. Specific 30/60/90-day milestones for each
3. KPIs to track each initiative
4. Preventative measures for the recurring April dip pattern
5. Team enablement (training, tools, compensation structure)
6. Technology/CRM investments to accelerate growth
7. Expected H2 revenue outcome if fully executed (with confidence interval)

Be specific, quantitative, and actionable. Reference IT industry best practices and SaaS benchmarks."""
                result = ask_openai(prompt, api_key, model_choice)
            st.markdown(f'<div class="ai-card">{result.replace(chr(10),"<br>")}</div>',
                        unsafe_allow_html=True)
            st.download_button("📥 Download H2 Action Plan", result,
                                file_name="H2_2025_action_plan.txt", mime="text/plain")
    else:
        st.markdown("""
        <div class="info-widget info-widget-amber">
            💡 Enter your OpenAI API key in the sidebar settings widget to generate an AI-powered H2 roadmap.
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-top:36px;padding:16px 20px;background:#F8FAFC;
            border:1px solid #E2E8F0;border-radius:10px;
            display:flex;justify-content:space-between;align-items:center;
            flex-wrap:wrap;gap:8px'>
    <div style='font-family:"Roboto Mono",monospace;font-size:0.68rem;color:#94A3B8'>
        DataForge Analytics · Sales Intelligence Platform · Hackathon 2025
    </div>
    <div style='font-family:Inter,sans-serif;font-size:0.72rem;color:#94A3B8'>
        Data: H1 2024–2025 Simulated · Framework: MEDDIC + OKR · Powered by OpenAI GPT-4
    </div>
</div>
""", unsafe_allow_html=True)
