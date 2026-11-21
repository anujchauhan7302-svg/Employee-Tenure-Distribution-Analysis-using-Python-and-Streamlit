from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dataset" / "employees.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    required = {"employee_id", "name", "department", "joining_date", "exit_date"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError("Dataset is missing columns: " + ", ".join(sorted(missing)))
    df["joining_date"] = pd.to_datetime(df["joining_date"], errors="coerce")
    df["exit_date"] = pd.to_datetime(df["exit_date"], errors="coerce")
    df = df.dropna(subset=["joining_date"]).copy()
    today = pd.Timestamp.today().normalize()
    df["end_date"] = df["exit_date"].fillna(today)
    df["tenure"] = ((df["end_date"] - df["joining_date"]).dt.days / 365.25).clip(lower=0)
    df["status"] = np.where(df["exit_date"].isna(), "Currently Working", "Left Company")
    df["tenure_category"] = pd.cut(
        df["tenure"], bins=[-0.001, 1, 3, 5, float("inf")],
        labels=["New Employee", "Junior Employee", "Experienced Employee", "Senior Employee"]
    )
    df["joining_year"] = df["joining_date"].dt.year
    df["joining_month"] = df["joining_date"].dt.to_period("M").astype(str)
    return df

def page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)
    st.divider()

def metric_row(df):
    cols = st.columns(4)
    values = [
        ("Total Employees", f"{len(df):,}"),
        ("Average Tenure", f"{df['tenure'].mean():.2f} yrs" if len(df) else "0"),
        ("Currently Working", f"{(df['status']=='Currently Working').sum():,}"),
        ("Left Company", f"{(df['status']=='Left Company').sum():,}")
    ]
    for col, (label, value) in zip(cols, values):
        col.metric(label, value)

def filtered_data(df, key="filter"):
    a,b,c = st.columns(3)
    departments = ["All"] + sorted(df["department"].dropna().astype(str).unique())
    statuses = ["All"] + sorted(df["status"].unique())
    with a: dep = st.selectbox("Department", departments, key=f"{key}_dep")
    with b: status = st.selectbox("Employee status", statuses, key=f"{key}_status")
    with c: query = st.text_input("Search employee", key=f"{key}_search", placeholder="Enter a name or ID")
    result=df.copy()
    if dep!="All": result=result[result["department"].astype(str)==dep]
    if status!="All": result=result[result["status"]==status]
    if query.strip():
        q=query.strip()
        result=result[result["name"].astype(str).str.contains(q,case=False,na=False) |
                      result["employee_id"].astype(str).str.contains(q,case=False,na=False)]
    return result

def chart_note():
    st.caption("Charts are calculated from the employee dataset included with this project.")

def apply_css():
    """Apply a shared, responsive visual theme to every Streamlit page."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
    :root { --ink:#172554; --muted:#64748b; --brand:#4f46e5; --brand2:#7c3aed; --line:#e2e8f0; }
    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
    .stApp { background:linear-gradient(135deg,#f7f8ff 0%,#f8fbff 48%,#f5f7ff 100%); color:var(--ink); }
    [data-testid="stHeader"] { background:rgba(248,250,255,.82); }
    .block-container { max-width:1500px; padding-top:2rem; padding-bottom:3rem; }
    h1,h2,h3 { font-family:'Manrope','DM Sans',sans-serif !important; color:#172554 !important; letter-spacing:-.035em; }
    h1 { font-weight:800 !important; font-size:2.15rem !important; }
    h2 { font-weight:750 !important; font-size:1.4rem !important; }
    h3 { font-weight:700 !important; font-size:1.08rem !important; }
    [data-testid="stCaptionContainer"] { color:#64748b; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#111a3b 0%,#202b59 100%); border-right:1px solid #26345f; }
    [data-testid="stSidebar"] * { color:#edf2ff !important; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#cbd5f5 !important; }
    [data-testid="stSidebarNav"] { padding-top:1rem; }
    [data-testid="stSidebarNav"] a { border-radius:10px; margin:3px 8px; padding:9px 12px; transition:all .2s ease; }
    [data-testid="stSidebarNav"] a:hover { background:#344477; }
    [data-testid="stSidebarNav"] a[aria-current="page"] { background:linear-gradient(90deg,#625cf2,#8b5cf6); font-weight:700; }
    [data-testid="stMetric"] { background:linear-gradient(145deg,#ffffff,#f5f7ff); border:1px solid #e1e7f5; border-radius:16px; padding:18px 20px; box-shadow:0 7px 22px rgba(38,54,112,.07); transition:transform .2s,box-shadow .2s; }
    [data-testid="stMetric"]:hover { transform:translateY(-2px); box-shadow:0 12px 26px rgba(38,54,112,.11); }
    [data-testid="stMetricLabel"] { color:#64748b !important; font-weight:600; }
    [data-testid="stMetricValue"] { color:#312e81 !important; font-family:'Manrope',sans-serif; font-weight:800; }
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] { gap:1rem; }
    [data-testid="stPlotlyChart"], [data-testid="stImage"] { border-radius:16px; }
    [data-testid="stDataFrame"] { border:1px solid #e2e8f0; border-radius:14px; overflow:hidden; box-shadow:0 5px 18px rgba(38,54,112,.05); }
    .stButton>button, .stDownloadButton>button { border:0; border-radius:10px; padding:.58rem 1rem; font-weight:700; color:white; background:linear-gradient(100deg,#4f46e5,#7c3aed); box-shadow:0 5px 13px rgba(79,70,229,.2); transition:all .2s ease; }
    .stButton>button:hover, .stDownloadButton>button:hover { color:white; transform:translateY(-1px); box-shadow:0 8px 18px rgba(79,70,229,.28); }
    .stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] > div { border-radius:10px; border-color:#dbe3f0; background:#fff; }
    [data-testid="stExpander"] { background:#fff; border:1px solid #e2e8f0; border-radius:13px; }
    [data-testid="stAlert"] { border-radius:12px; }
    hr { border-color:#e2e8f0; }
    @media (max-width: 768px) { .block-container { padding:1.2rem 1rem 2rem; } h1 { font-size:1.65rem !important; } [data-testid="stMetric"] { padding:13px; } }
    </style>
    """, unsafe_allow_html=True)
