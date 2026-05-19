"""
biomed_explorer.py
==================
Streamlit frontend — Biomedical Corpus Explorer
Backend : FastAPI @ http://localhost:8000
Run     : streamlit run biomed_explorer.py
"""
from __future__ import annotations
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime
from typing import Optional

st.set_page_config(page_title="Biomedical Corpus Explorer", layout="wide", initial_sidebar_state="expanded")

# ─── MOCK DATA ─────────────────────────────────────────────────────────────────
MOCK_ARTICLES = [
    {"pmid":"1001","title":"CRISPR-Cas9 Gene Editing in Cancer Therapy","authors":["Smith J.","Ali K."],"abstract":"This study explores the use of CRISPR-Cas9 for targeted cancer gene therapy. Results show significant tumor reduction in mouse models with minimal off-target effects.","journal":"Nature","year":2020,"domain":"Cancer","doi":"10.1000/xyz001"},
    {"pmid":"1002","title":"COVID-19 mRNA Vaccine Efficacy Study","authors":["Chen L.","Park S."],"abstract":"Analysis of mRNA vaccine efficacy against COVID-19 variants including Delta and Omicron. The study covers 50,000 participants over 18 months.","journal":"Lancet","year":2021,"domain":"COVID","doi":"10.1000/xyz002"},
    {"pmid":"1003","title":"Deep Learning for MRI Brain Tumor Segmentation","authors":["Duval M.","Lopez R."],"abstract":"Deep neural networks applied to MRI image segmentation achieve 94% accuracy in brain tumor delineation across three public datasets.","journal":"NEJM","year":2021,"domain":"Cancer","doi":"10.1000/xyz003"},
    {"pmid":"1004","title":"PD-1 Inhibitor Therapy in Stage III Lung Cancer","authors":["Lopez R.","Wang Y."],"abstract":"PD-1 inhibitor therapy outcomes in stage III lung cancer patients. Median overall survival improved by 8.4 months compared to chemotherapy alone.","journal":"Cell","year":2022,"domain":"Cancer","doi":"10.1000/xyz004"},
    {"pmid":"1005","title":"Novel CSF Biomarkers for Early Alzheimer Detection","authors":["Kim J.","Tanaka H."],"abstract":"Novel cerebrospinal fluid biomarkers for early Alzheimer detection with 91% sensitivity. Longitudinal study over 5 years with 1200 participants.","journal":"Brain","year":2022,"domain":"Genomics","doi":"10.1000/xyz005"},
    {"pmid":"1006","title":"Universal mRNA Therapeutic Delivery Platform","authors":["Jones A.","Nour B."],"abstract":"Development of a universal mRNA therapeutic delivery platform using lipid nanoparticles. Platform tested across 6 disease models with consistent efficacy.","journal":"Nature","year":2022,"domain":"COVID","doi":"10.1000/xyz006"},
    {"pmid":"1007","title":"GWAS Identifies 15 Novel Loci for Type 2 Diabetes","authors":["Yao C.","Smith J."],"abstract":"Genome-wide association study identifying 15 novel loci associated with type 2 diabetes risk across diverse ethnic populations.","journal":"Diabetes","year":2023,"domain":"Genomics","doi":"10.1000/xyz007"},
    {"pmid":"1008","title":"AI-Powered CT Scan for Early Lung Cancer Detection","authors":["Tanaka H.","Smith J."],"abstract":"AI-powered CT scan analysis for early-stage lung cancer detection achieves 96% sensitivity at 89% specificity in a multicenter validation study.","journal":"Lancet","year":2023,"domain":"Cancer","doi":"10.1000/xyz008"},
    {"pmid":"1009","title":"AlphaFold2 for Rare Disease Protein Structure Prediction","authors":["Ali K.","Chen L."],"abstract":"Using AlphaFold2 for novel protein structure prediction in rare diseases. Successfully modeled 340 previously uncharacterized proteins.","journal":"Science","year":2023,"domain":"Genomics","doi":"10.1000/xyz009"},
    {"pmid":"1010","title":"Machine Learning for 30-Day Heart Failure Readmission","authors":["Park S.","Duval M."],"abstract":"Machine learning model predicting 30-day readmission in heart failure patients with AUC of 0.87. Validated in 4 independent hospital cohorts.","journal":"JACC","year":2024,"domain":"Cancer","doi":"10.1000/xyz010"},
    {"pmid":"1011","title":"Beta-Lactamase Mechanisms Driving Antibiotic Resistance","authors":["Lopez R.","Kim J."],"abstract":"Comprehensive review of beta-lactamase mechanisms driving antibiotic resistance globally. Analysis of 2800 clinical isolates from 45 countries.","journal":"Lancet","year":2024,"domain":"COVID","doi":"10.1000/xyz011"},
    {"pmid":"1012","title":"AAV Gene Therapy Targeting Alpha-Synuclein in Parkinson","authors":["Wang Y.","Kim J."],"abstract":"AAV-based gene therapy targeting alpha-synuclein in Parkinson disease shows neuroprotective effect in primate model over 24-month follow-up.","journal":"Brain","year":2024,"domain":"Genomics","doi":"10.1000/xyz012"},
    {"pmid":"1013","title":"CNN for Early Breast Cancer Detection in Mammograms","authors":["Smith J.","Yao C."],"abstract":"Convolutional neural network for early breast cancer detection in mammograms achieves radiologist-level performance in retrospective study of 28,000 images.","journal":"Nature","year":2023,"domain":"Cancer","doi":"10.1000/xyz013"},
    {"pmid":"1014","title":"Gut Microbiome Composition Linked to Obesity","authors":["Chen L.","Park S."],"abstract":"Gut microbiome composition linked to obesity and metabolic disorders. Specific bacterial ratios predict metabolic syndrome with 85% accuracy.","journal":"Science","year":2022,"domain":"COVID","doi":"10.1000/xyz014"},
    {"pmid":"1015","title":"CRISPR-Cas9 Gene Correction in Sickle Cell Disease","authors":["Ali K.","Jones A."],"abstract":"Gene correction using CRISPR-Cas9 achieves functional cure in 11 of 12 sickle cell disease patients after 24 months of follow-up.","journal":"NEJM","year":2024,"domain":"Genomics","doi":"10.1000/xyz015"},
    {"pmid":"1016","title":"Long COVID Neurological Manifestations","authors":["Nour B.","Lopez R."],"abstract":"Systematic review of neurological manifestations in long COVID across 42 studies. Cognitive impairment reported in 22-32% of post-COVID patients.","journal":"Lancet","year":2022,"domain":"COVID","doi":"10.1000/xyz016"},
    {"pmid":"1017","title":"Single-Cell RNA Sequencing in Tumor Microenvironment","authors":["Tanaka H.","Ali K."],"abstract":"Single-cell RNA sequencing reveals heterogeneity in tumor microenvironment. Identifies 8 novel cell subpopulations with prognostic significance.","journal":"Cell","year":2023,"domain":"Cancer","doi":"10.1000/xyz017"},
    {"pmid":"1018","title":"Omicron Variant Immune Evasion Mechanisms","authors":["Chen L.","Wang Y."],"abstract":"Structural analysis of Omicron variant spike protein reveals key mutations responsible for immune evasion and reduced vaccine neutralization.","journal":"Nature","year":2022,"domain":"COVID","doi":"10.1000/xyz018"},
    {"pmid":"1019","title":"Polygenic Risk Score for Coronary Artery Disease","authors":["Park S.","Smith J."],"abstract":"Polygenic risk score for coronary artery disease integrating 6 million variants predicts lifetime risk with C-statistic of 0.81.","journal":"NEJM","year":2023,"domain":"Genomics","doi":"10.1000/xyz019"},
    {"pmid":"1020","title":"Liquid Biopsy ctDNA for Colorectal Cancer Monitoring","authors":["Yao C.","Duval M."],"abstract":"Circulating tumor DNA in liquid biopsy detects colorectal cancer recurrence 8 months earlier than conventional imaging in prospective cohort.","journal":"Science","year":2024,"domain":"Cancer","doi":"10.1000/xyz020"},
]
MOCK_STATS_DOMAIN = [{"_id":"Cancer","count":8,"avg_year":2022.5},{"_id":"COVID","count":7,"avg_year":2022.1},{"_id":"Genomics","count":5,"avg_year":2022.8}]
MOCK_STATS_YEAR   = [{"_id":y,"count":c} for y,c in [(2020,1),(2021,2),(2022,5),(2023,6),(2024,6)]]
MOCK_HEALTH       = {"status":"ok","database":"connected"}

# ─── MOCK FUNCTIONS ────────────────────────────────────────────────────────────
@st.cache_data
def mock_articles(domain=None, search=None, year_from=None, year_to=None, page=1, limit=100):
    data = MOCK_ARTICLES[:]
    if domain:    data = [a for a in data if a.get("domain") == domain]
    if year_from: data = [a for a in data if (a.get("year") or 0) >= year_from]
    if year_to:   data = [a for a in data if (a.get("year") or 0) <= year_to]
    if search:
        q = search.lower()
        data = [a for a in data if q in (a.get("title","") or "").lower()
                or q in (a.get("abstract","") or "").lower()
                or any(q in au.lower() for au in (a.get("authors") or []))]
    start = (page - 1) * limit
    return data[start:start + limit]

@st.cache_data
def mock_article_by_pmid(pmid): return next((a for a in MOCK_ARTICLES if a["pmid"]==pmid), None)

@st.cache_data
def mock_stats_year():   return MOCK_STATS_YEAR

@st.cache_data
def mock_stats_domain(): return MOCK_STATS_DOMAIN

@st.cache_data
def mock_health(): return True, MOCK_HEALTH

# ─── BACKEND API — connecté à FastAPI ─────────────────────────────────────────
import requests
API_BASE = "https://eidm-project6-54pd.onrender.com"

@st.cache_data(ttl=60)
def api_articles(domain=None, search=None, year_from=None, year_to=None, page=1, limit=100):
    params = {"page": page, "limit": limit}
    if domain:    params["domain"]    = domain
    if search:    params["search"]    = search
    if year_from: params["year_from"] = year_from
    if year_to:   params["year_to"]   = year_to
    try:
        r = requests.get(f"{API_BASE}/articles", params=params, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception:
        return MOCK_ARTICLES  # fallback si backend lent au démarrage

@st.cache_data(ttl=60)
def api_article_by_pmid(pmid):
    try:
        r = requests.get(f"{API_BASE}/articles/{pmid}", timeout=60)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return next((a for a in MOCK_ARTICLES if a["pmid"] == pmid), None)

@st.cache_data(ttl=60)
def api_stats_year():
    try:
        return requests.get(f"{API_BASE}/stats/year", timeout=60).json()
    except Exception:
        return MOCK_STATS_YEAR

@st.cache_data(ttl=60)
def api_stats_domain():
    try:
        return requests.get(f"{API_BASE}/stats/domain", timeout=60).json()
    except Exception:
        return MOCK_STATS_DOMAIN

@st.cache_data(ttl=10)
def api_health():
    try:
        d = requests.get(f"{API_BASE}/health", timeout=30).json()
        return d.get("status") == "ok", d
    except Exception:
        return False, {"status":"unreachable","database":"disconnected"}

# ─── ACTIVE WRAPPERS ───────────────────────────────────────────────────────────
def get_articles(domain=None, search=None, year_from=None, year_to=None, page=1, limit=100):
    return api_articles(domain, search, year_from, year_to, page, limit)

def get_article_by_pmid(pmid):  return api_article_by_pmid(pmid)
def get_stats_year():            return api_stats_year()
def get_stats_domain():          return api_stats_domain()
def get_health():                return api_health()

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
for _k, _v in {"dark_mode": True, "page": "Dashboard", "search_query": ""}.items():
    if _k not in st.session_state: st.session_state[_k] = _v

D = st.session_state.dark_mode

# ─── DESIGN TOKENS ─────────────────────────────────────────────────────────────
T = {
    "bg":      "#0d1117" if D else "#f6f8fa",
    "surface": "#161b22" if D else "#ffffff",
    "surface2":"#1c2128" if D else "#eaeef2",
    "border":  "#30363d" if D else "#d0d7de",
    "t1":      "#e6edf3" if D else "#1f2328",
    "t2":      "#7d8590" if D else "#57606a",
    "t3":      "#484f58" if D else "#8c959f",
    "accent":  "#2f81f7",
    "green":   "#3fb950",
    "red":     "#f85149",
    "yellow":  "#d29922",
    "purple":  "#a371f7",
    "orange":  "#db6d28",
    "cyan":    "#39c5cf",
}
DOMAIN_COLORS = {
    "Cancer":"#f85149","Oncology":"#f85149","COVID":"#3fb950","Virology":"#3fb950",
    "Genomics":"#2f81f7","Neurology":"#d29922","Cardiology":"#58a6ff",
    "Radiology":"#a371f7","Endocrinology":"#bc8cff","Microbiology":"#39c5cf",
}
CHART_COLORS = ["#2f81f7","#f85149","#3fb950","#a371f7","#d29922","#39c5cf","#f0883e","#db61a2","#58a6ff","#56d364"]

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body,[class*="css"]{{font-family:'Inter',sans-serif!important;background:{T['bg']}!important;color:{T['t1']}!important}}
.stApp{{background:{T['bg']}!important}}
section[data-testid="stSidebar"]>div{{background:{T['surface']}!important;border-right:1px solid {T['border']}}}
.page-title{{font-size:17px;font-weight:700;color:{T['t1']};border-bottom:1px solid {T['border']};padding-bottom:14px;margin-bottom:22px}}
.section-label{{font-size:10px;font-weight:700;color:{T['t3']};text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px}}
.divider{{height:1px;background:{T['border']};margin:14px 0}}
.card{{background:{T['surface']};border:1px solid {T['border']};border-radius:6px;padding:18px 20px}}
.kpi-label{{font-size:10px;font-weight:700;color:{T['t3']};text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px}}
.kpi-value{{font-size:26px;font-weight:700;line-height:1;color:{T['t1']};letter-spacing:-.02em}}
.kpi-sub{{font-size:11px;color:{T['t3']};margin-top:7px;line-height:1.4}}
.art-row{{background:{T['surface']};border:1px solid {T['border']};border-radius:6px;padding:14px 16px;margin-bottom:8px}}
.art-row:hover{{border-color:{T['accent']}60}}
.art-title{{font-size:13px;font-weight:600;color:{T['t1']};margin-bottom:5px;line-height:1.45}}
.art-meta{{font-size:11px;color:{T['t2']};margin-bottom:6px;display:flex;align-items:center;gap:6px;flex-wrap:wrap}}
.art-abstract{{font-size:12px;color:{T['t3']};line-height:1.65;display:-webkit-box;-webkit-line-clamp:var(--clamp,2);-webkit-box-orient:vertical;overflow:hidden}}
.badge{{display:inline-block;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:700;letter-spacing:.04em;white-space:nowrap}}
.tag{{display:inline-block;padding:1px 6px;border-radius:3px;font-size:10px;color:{T['t2']};background:{T['surface2']};border:1px solid {T['border']}}}
.status-mock{{display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:99px;font-size:11px;font-weight:600;background:{T['yellow']}18;color:{T['yellow']};border:1px solid {T['yellow']}40}}
.ep-row{{display:flex;align-items:center;gap:10px;padding:8px 12px;background:{T['surface']};border:1px solid {T['border']};border-radius:6px;margin-bottom:6px}}
.ep-method{{font-size:10px;font-weight:700;color:{T['accent']};background:{T['accent']}18;padding:2px 7px;border-radius:4px;min-width:36px;text-align:center}}
.ep-path{{font-family:monospace;font-size:12px;color:{T['t1']}}}
.ep-desc{{font-size:11px;color:{T['t3']};margin-left:auto}}
div[data-testid="stButton"] button{{border-radius:6px!important;font-size:12px!important;font-weight:500!important}}
.stTextInput>div>input{{background:{T['surface']}!important;color:{T['t1']}!important;border:1px solid {T['border']}!important;border-radius:6px!important;font-size:13px!important}}
.stSelectbox>div>div{{background:{T['surface']}!important;border-color:{T['border']}!important;border-radius:6px!important}}
.stTabs [data-baseweb="tab"]{{font-size:12px!important;font-weight:500!important;color:{T['t2']}!important}}
.stTabs [aria-selected="true"]{{color:{T['t1']}!important;border-bottom-color:{T['accent']}!important}}
</style>""", unsafe_allow_html=True)

# ─── HELPERS ───────────────────────────────────────────────────────────────────
def normalize(raw):
    if not raw: return pd.DataFrame()
    if isinstance(raw, dict):
        raw = raw.get("results", [])
    if not raw: return pd.DataFrame()
    df = pd.DataFrame(raw)
    df.drop(columns=["_id"], inplace=True, errors="ignore")
    if "authors" in df.columns:
        df["authors"] = df["authors"].apply(lambda x: "; ".join(x) if isinstance(x, list) else str(x or ""))
    for col in ("pmid","title","authors","abstract","journal","year","domain","doi"):
        if col not in df.columns: df[col] = None
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    return df

# ✅ FIX : _layout ne contient PAS de clé 'legend' pour éviter le conflit
def _layout(**kw):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=T["t2"], size=11),
        title_font=dict(color=T["t1"], size=13),
        margin=dict(t=44, b=16, l=16, r=16),
        height=300,
    )
    base.update(kw)
    return base

# Légende par défaut réutilisable
_LEG_H = dict(font=dict(color=T["t2"], size=10), bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.22, x=0)
_LEG_V = dict(font=dict(color=T["t2"], size=10), bgcolor="rgba(0,0,0,0)", orientation="v")

def _ax(**kw):
    base = dict(color=T["t3"], gridcolor=T["surface2"], linecolor=T["border"],
                tickfont=dict(size=10, color=T["t3"]), zeroline=False, showgrid=True)
    base.update(kw); return base

def _badge(domain):
    c = DOMAIN_COLORS.get(domain, T["t3"])
    return f'<span class="badge" style="background:{c}1a;color:{c}">{domain}</span>'

def _tag(text): return f'<span class="tag">{text}</span>'

def _doi_link(val):
    if val and str(val).startswith("10."):
        return f'<a href="https://doi.org/{val}" target="_blank" style="color:{T["accent"]};font-size:10px;text-decoration:none;font-weight:500">DOI ↗</a>'
    return ""

def render_article(row, clamp=2):
    title    = str(row.get("title","") or "Untitled")
    authors  = str(row.get("authors","") or "")
    journal  = str(row.get("journal","") or "")
    year     = row.get("year")
    domain   = str(row.get("domain","") or "")
    abstract = str(row.get("abstract","") or "")
    doi      = str(row.get("doi","") or row.get("pmid","") or "")
    yr_str   = str(int(year)) if pd.notna(year) else ""
    auth_str = (authors[:90]+"...") if len(authors)>90 else authors
    st.markdown(f"""<div class="art-row">
      <div class="art-title">{title}</div>
      <div class="art-meta">{_badge(domain)}{_tag(yr_str) if yr_str else ""}{_tag(journal) if journal else ""}
        <span style="color:{T['t3']};font-size:11px">{auth_str}</span>{_doi_link(doi)}
      </div>
      <div class="art-abstract" style="--clamp:{clamp}">{abstract}</div>
    </div>""", unsafe_allow_html=True)

# ─── LOAD DATA ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""<div style="padding:20px 0 6px">
      <div style="font-size:14px;font-weight:700;color:{T['t1']}">Biomedical Corpus</div>
      <div style="font-size:11px;color:{T['t3']};margin-top:3px">FastAPI · MongoDB Atlas · PubMed</div>
    </div><div class="divider"></div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
    for label, pid in [("Dashboard","Dashboard"),("Search","Search"),("Analytics","Analytics"),("Publications","Publications"),("Data Table","Table")]:
        active = st.session_state.page == pid
        if st.button(label, key=f"nav_{pid}", use_container_width=True, type="primary" if active else "secondary"):
            st.session_state.page = pid; st.rerun()
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)
    _all_raw = get_articles(limit=100)
    _df_all  = normalize(_all_raw)
    _domains = sorted(_df_all["domain"].dropna().unique()) if not _df_all.empty else []
    _years_raw = _df_all["year"].dropna().astype(int).unique() if not _df_all.empty else []
    _years   = sorted([y for y in _years_raw if y > 0]) if len(_years_raw) > 0 else [2020, 2024]
    sel_domain = st.selectbox("Domain", ["All"] + list(_domains))
    year_range = st.slider("Year range", min_value=int(min(_years)), max_value=int(max(_years)),
                           value=(int(min(_years)), int(max(_years)))) if len(_years)>=2 else (2020,2024)

_dom_param = None if sel_domain == "All" else sel_domain
_raw = get_articles(domain=_dom_param, year_from=year_range[0], year_to=year_range[1], limit=100)
df   = normalize(_raw)
PAGE = st.session_state.page
now  = datetime.now()

# ─── Stats depuis /stats/year et /stats/domain ────────────────────────────────
_raw_stats_year   = get_stats_year()    # [{_id: year, count: N}]
_raw_stats_domain = get_stats_domain()  # [{_id: domain, count: N, avg_year: X}]
df_sy = pd.DataFrame(_raw_stats_year).rename(columns={"_id":"year","count":"count"}) if _raw_stats_year else pd.DataFrame(columns=["year","count"])
df_sd = pd.DataFrame(_raw_stats_domain).rename(columns={"_id":"domain"}) if _raw_stats_domain else pd.DataFrame(columns=["domain","count","avg_year"])
total_db = int(df_sd["count"].sum()) if not df_sd.empty else 0

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if PAGE == "Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    total      = len(df)
    n_domains  = int(df["domain"].nunique()) if not df.empty else 0
    n_journals = int(df["journal"].nunique()) if not df.empty else 0
    latest_yr  = int(df["year"].max()) if not df.empty and df["year"].notna().any() else now.year
    oldest_yr  = int(df["year"].min()) if not df.empty and df["year"].notna().any() else now.year
    _flat = []
    if not df.empty:
        for cell in df["authors"].dropna():
            _flat.extend(a.strip() for a in str(cell).replace(",",";").split(";") if a.strip())

    k1,k2,k3,k4,k5 = st.columns(5)
    for col,lbl,val,sub,color in [
        (k1,"Total Articles",f"{total:,}",f"Filtre: {sel_domain}",T["accent"]),
        (k2,"Domaines",f"{n_domains}",f"{year_range[0]}–{year_range[1]}",T["green"]),
        (k3,"Journaux",f"{n_journals}","Journaux uniques",T["purple"]),
        (k4,"Auteurs",f"{len(set(_flat)):,}","Auteurs uniques",T["yellow"]),
        (k5,"Span",f"{latest_yr-oldest_yr}y",f"{oldest_yr} → {latest_yr}",T["cyan"]),
    ]:
        with col:
            st.markdown(f'<div class="card"><div class="kpi-label">{lbl}</div><div class="kpi-value" style="color:{color}">{val}</div><div class="kpi-sub">{sub}</div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if df.empty:
        st.info("Aucune donnée.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            dc = df["domain"].value_counts().reset_index(); dc.columns = ["domain","count"]
            colors = [DOMAIN_COLORS.get(d, T["t3"]) for d in dc["domain"]]
            fig = go.Figure(go.Pie(
                labels=dc["domain"], values=dc["count"], hole=0.58,
                marker=dict(colors=colors, line=dict(color=T["bg"], width=2)),
                textinfo="label+percent", textfont=dict(size=10),
                hovertemplate="<b>%{label}</b><br>%{value} articles (%{percent})<extra></extra>",
            ))
            fig.add_annotation(text=f"<b>{total:,}</b><br>articles", x=0.5, y=0.5,
                               showarrow=False, font=dict(size=13, color=T["t1"]))
            fig.update_layout(title="Distribution par domaine", legend=_LEG_V, **_layout(height=300))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Utilise /stats/year (données agrégées MongoDB)
            yc = df_sy.copy() if not df_sy.empty else df.dropna(subset=["year"]).assign(year=lambda d:d["year"].astype(int)).groupby("year").size().reset_index(name="count")
            fig2 = go.Figure(go.Bar(
                x=yc["year"], y=yc["count"],
                marker=dict(color=yc["count"],
                            colorscale=[[0,"rgba(47,129,247,0.25)"],[1,"#2f81f7"]],  # ✅ rgba
                            line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>%{y} articles<extra></extra>",
            ))
            fig2.update_layout(title="Publications par an",
                               xaxis=dict(**_ax(title="", tickmode="linear")),
                               yaxis=dict(**_ax(title="")),
                               bargap=0.2, **_layout(height=300))
            st.plotly_chart(fig2, use_container_width=True)

        c3, c4 = st.columns([3, 2])
        with c3:
            yd = (df.dropna(subset=["year","domain"])
                    .assign(year=lambda d: d["year"].astype(int))
                    .groupby(["year","domain"]).size().reset_index(name="count"))
            fig3 = px.bar(yd, x="year", y="count", color="domain",
                          color_discrete_map=DOMAIN_COLORS,
                          title="Publications empilées par domaine", barmode="stack")
            fig3.update_traces(marker_line_width=0)
            # ✅ FIX : legend passé séparément, pas dans _layout
            fig3.update_layout(
                xaxis=dict(**_ax(title="", tickmode="linear")),
                yaxis=dict(**_ax(title="")),
                bargap=0.15,
                legend=dict(font=dict(size=10), orientation="h", y=-0.22, x=0, bgcolor="rgba(0,0,0,0)"),
                **_layout(height=320),
            )
            st.plotly_chart(fig3, use_container_width=True)

        with c4:
            jc = df["journal"].value_counts().head(10).reset_index(); jc.columns = ["journal","count"]
            fig4 = go.Figure(go.Bar(
                x=jc["count"], y=jc["journal"], orientation="h",
                marker=dict(color=jc["count"],
                            colorscale=[[0,"rgba(63,185,80,0.25)"],[1,"#3fb950"]],  # ✅ rgba
                            line=dict(width=0)),
                hovertemplate="<b>%{y}</b><br>%{x} articles<extra></extra>",
            ))
            fig4.update_layout(title="Top 10 Journaux",
                               xaxis=dict(**_ax(title="")),
                               yaxis=dict(**_ax(title="", categoryorder="total ascending")),
                               **_layout(height=320))
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown('<div class="section-label" style="margin-top:8px">Dernières publications</div>', unsafe_allow_html=True)
        for _, row in df.sort_values("year", ascending=False).head(10).iterrows():
            render_article(row, clamp=2)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : SEARCH  — /articles?domain=&search=&year_from=&year_to=&page=&limit=
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "Search":
    st.markdown('<div class="page-title">Search</div>', unsafe_allow_html=True)
    col_q, col_btn = st.columns([6, 1])
    with col_q:
        query = st.text_input("", placeholder="Titre, abstract, auteur, mot-clé...",
                              label_visibility="collapsed", value=st.session_state.search_query)
    with col_btn:
        if st.button("Rechercher", type="primary", use_container_width=True):
            st.session_state.search_query = query

    sc1, sc2, sc3 = st.columns(3)
    with sc1: sort_by  = st.selectbox("Trier par", ["Année (desc)","Année (asc)","Titre A-Z","Journal"], key="s_sort")
    with sc2: f_domain = st.selectbox("Domaine", ["All"] + list(_domains), key="s_dom")
    with sc3:
        _journals = sorted(_df_all["journal"].dropna().unique().tolist()) if not _df_all.empty else []
        f_journal = st.selectbox("Journal", ["All"] + _journals, key="s_jrn")

    PAGE_SIZE = 20
    cur_page  = st.number_input("Page", min_value=1, value=1, step=1, key="s_page")
    results   = normalize(get_articles(
        domain=None if f_domain=="All" else f_domain,
        search=query or None,
        year_from=year_range[0], year_to=year_range[1],
        page=cur_page, limit=PAGE_SIZE,
    ))
    if f_journal != "All" and not results.empty:
        results = results[results["journal"] == f_journal]
    if not results.empty:
        col_s, asc_s = {"Année (desc)":("year",False),"Année (asc)":("year",True),"Titre A-Z":("title",True),"Journal":("journal",True)}[sort_by]
        results = results.sort_values(col_s, ascending=asc_s)

    # Masquer les résultats tant qu'aucune recherche n'est lancée
    if not st.session_state.search_query and f_domain == "All" and f_journal == "All":
        st.markdown(f'<div style="text-align:center;padding:60px 0;color:{T["t3"]};font-size:14px">🔍 Entrez un mot-clé et cliquez sur Rechercher</div>', unsafe_allow_html=True)
    elif results.empty:
        st.info("Aucun résultat pour cette recherche.")
    else:
        st.markdown(f'<div style="font-size:11px;color:{T["t3"]};margin-bottom:14px">{len(results):,} résultat(s) — page {cur_page}</div>', unsafe_allow_html=True)
        for _, row in results.iterrows():
            title  = str(row.get("title","") or "Untitled")
            yr     = int(row["year"]) if pd.notna(row.get("year")) else ""
            domain = str(row.get("domain","") or "")
            label  = f"[{domain}]  {title[:80]}{'...' if len(title)>80 else ''}  ({yr})"
            with st.expander(label):
                render_article(row, clamp=20)
                pmid = str(row.get("pmid","") or "")
                doi  = str(row.get("doi","") or "")
                c1, c2, _ = st.columns([1,1,3])
                if pmid and pmid.isdigit():
                    with c1:
                        st.link_button("🔗 Voir sur PubMed", f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
                if doi and doi.startswith("10."):
                    with c2:
                        st.link_button("📄 Voir DOI", f"https://doi.org/{doi}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "Analytics":
    st.markdown('<div class="page-title">Analytics</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("Aucune donnée.")
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Distributions","Trends","Auteurs","Journaux","Cross"])

        with tab1:
            r1, r2 = st.columns(2)
            with r1:
                # Utilise /stats/domain
                src = df_sd if not df_sd.empty else df["domain"].value_counts().reset_index().rename(columns={"domain":"domain","count":"count"})
                fig = px.bar(src, x="count", y="domain", orientation="h",
                             color="domain", color_discrete_map=DOMAIN_COLORS, title="Articles par domaine")
                fig.update_traces(marker_line_width=0)
                fig.update_layout(showlegend=False,
                                  xaxis=dict(**_ax(title="Articles")),
                                  yaxis=dict(**_ax(title="", categoryorder="total ascending")),
                                  **_layout(height=300))
                st.plotly_chart(fig, use_container_width=True)
            with r2:
                jc = df["journal"].value_counts().head(10).reset_index(); jc.columns = ["journal","count"]
                fig2 = px.pie(jc, names="journal", values="count", title="Top 10 Journaux",
                              color_discrete_sequence=CHART_COLORS, hole=0.4)
                fig2.update_layout(legend=_LEG_V, **_layout(height=300))
                st.plotly_chart(fig2, use_container_width=True)
            # Utilise /stats/year
            yc = df_sy if not df_sy.empty else df.dropna(subset=["year"]).assign(year=lambda d:d["year"].astype(int)).groupby("year").size().reset_index(name="count")
            fig3 = px.area(yc, x="year", y="count", title="Volume publications dans le temps",
                           color_discrete_sequence=[T["accent"]])
            fig3.update_traces(fill="tozeroy", fillcolor="rgba(47,129,247,0.15)",
                               line=dict(color=T["accent"], width=2))
            fig3.update_layout(xaxis=dict(**_ax(title="", tickmode="linear")),
                               yaxis=dict(**_ax(title="Articles")), **_layout(height=240))
            st.plotly_chart(fig3, use_container_width=True)

        with tab2:
            yd = (df.dropna(subset=["year","domain"])
                    .assign(year=lambda d: d["year"].astype(int))
                    .groupby(["year","domain"]).size().reset_index(name="count"))
            fig_a = px.area(yd, x="year", y="count", color="domain",
                            color_discrete_map=DOMAIN_COLORS, title="Tendances cumulées par domaine")
            fig_a.update_layout(xaxis=dict(**_ax(title="", tickmode="linear")),
                                yaxis=dict(**_ax(title="Articles")),
                                legend=_LEG_H, **_layout(height=320))
            st.plotly_chart(fig_a, use_container_width=True)
            fig_b = px.line(yd, x="year", y="count", color="domain",
                            color_discrete_map=DOMAIN_COLORS,
                            title="Évolution YoY par domaine", markers=True)
            fig_b.update_layout(xaxis=dict(**_ax(title="", tickmode="linear")),
                                yaxis=dict(**_ax(title="Articles")),
                                legend=_LEG_H, **_layout(height=300))
            st.plotly_chart(fig_b, use_container_width=True)
            # avg_year depuis /stats/domain
            if "avg_year" in df_sd.columns:
                st.markdown('<div class="section-label">Année moyenne par domaine (/stats/domain)</div>', unsafe_allow_html=True)
                st.dataframe(df_sd[["domain","count","avg_year"]].sort_values("count", ascending=False), use_container_width=True)

        with tab3:
            raw_a = []
            for cell in df["authors"].dropna():
                raw_a.extend(a.strip() for a in str(cell).replace(",",";").split(";") if a.strip())
            ac = pd.Series(raw_a).value_counts().reset_index(); ac.columns = ["author","count"]
            top_n = st.slider("Top N auteurs", 5, 50, 20, key="an")
            fig_au = px.bar(ac.head(top_n), x="count", y="author", orientation="h",
                            title=f"Top {top_n} auteurs", color="count",
                            color_continuous_scale=[[0,"rgba(163,113,247,0.25)"],[1,"#a371f7"]])  # ✅ rgba
            fig_au.update_traces(marker_line_width=0)
            fig_au.update_layout(showlegend=False, coloraxis_showscale=False,
                                 xaxis=dict(**_ax(title="Articles")),
                                 yaxis=dict(**_ax(title="", categoryorder="total ascending")),
                                 **_layout(height=max(280, top_n*22)))
            st.plotly_chart(fig_au, use_container_width=True)

        with tab4:
            jc_full = df["journal"].value_counts().reset_index(); jc_full.columns = ["journal","count"]
            top_j = st.slider("Top N journaux", 5, 30, 15, key="jn")
            fig_j = px.bar(jc_full.head(top_j), x="count", y="journal", orientation="h",
                           title=f"Top {top_j} journaux", color="count",
                           color_continuous_scale=[[0,"rgba(63,185,80,0.25)"],[1,"#3fb950"]])  # ✅ rgba
            fig_j.update_traces(marker_line_width=0)
            fig_j.update_layout(showlegend=False, coloraxis_showscale=False,
                                xaxis=dict(**_ax(title="Articles")),
                                yaxis=dict(**_ax(title="", categoryorder="total ascending")),
                                **_layout(height=max(260, top_j*20)))
            st.plotly_chart(fig_j, use_container_width=True)

        with tab5:
            _top_j   = df["journal"].value_counts().head(12).index.tolist()
            _heat    = df[df["journal"].isin(_top_j)].groupby(["domain","journal"]).size().reset_index(name="count")
            heat_piv = _heat.pivot(index="domain", columns="journal", values="count").fillna(0)
            fig_h = go.Figure(go.Heatmap(
                z=heat_piv.values, x=heat_piv.columns.tolist(), y=heat_piv.index.tolist(),
                colorscale=[[0,T["bg"]],[0.5,"rgba(47,129,247,0.55)"],[1,T["accent"]]],
                hovertemplate="Domaine: <b>%{y}</b><br>Journal: <b>%{x}</b><br>Count: <b>%{z}</b><extra></extra>",
            ))
            fig_h.update_layout(title="Heatmap Domaine × Journal",
                                xaxis=dict(tickfont=dict(size=10), color=T["t2"], tickangle=-30),
                                yaxis=dict(tickfont=dict(size=10), color=T["t2"]),
                                **_layout(height=340))
            st.plotly_chart(fig_h, use_container_width=True)
            yd2 = (df.dropna(subset=["year","domain"])
                     .assign(year=lambda d: d["year"].astype(int))
                     .groupby(["year","domain"]).size().reset_index(name="count"))
            fig_sc = px.scatter(yd2, x="year", y="count", color="domain", size="count",
                                size_max=28, color_discrete_map=DOMAIN_COLORS,
                                title="Bubble: volume par an et domaine")
            fig_sc.update_layout(xaxis=dict(**_ax(title="", tickmode="linear")),
                                 yaxis=dict(**_ax(title="Articles")),
                                 legend=_LEG_H, **_layout(height=320))
            st.plotly_chart(fig_sc, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : PUBLICATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "Publications":
    st.markdown('<div class="page-title">Publications</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("Aucune donnée.")
    else:
        _avail_years = sorted(df["year"].dropna().astype(int).unique(), reverse=True)
        sel_year = st.selectbox("Année", ["Toutes"] + [str(y) for y in _avail_years])
        view_df  = df[df["year"] == int(sel_year)] if sel_year != "Toutes" else df.copy()
        _view_domains = sorted(view_df["domain"].dropna().unique())
        dtabs = st.tabs(["Tous"] + list(_view_domains))
        for i, dtab in enumerate(dtabs):
            with dtab:
                sub = (view_df.sort_values("year", ascending=False) if i == 0
                       else view_df[view_df["domain"] == _view_domains[i-1]].sort_values("year", ascending=False))
                st.markdown(f'<div style="font-size:11px;color:{T["t3"]};margin-bottom:12px">{len(sub):,} article(s)</div>', unsafe_allow_html=True)
                for _, row in sub.head(50).iterrows():
                    title  = str(row.get("title","") or "Untitled")
                    yr     = int(row["year"]) if pd.notna(row.get("year")) else ""
                    domain = str(row.get("domain","") or "")
                    label  = f"[{domain}]  {title[:80]}{'...' if len(title)>80 else ''}  ({yr})"
                    with st.expander(label):
                        render_article(row, clamp=20)
                        pmid = str(row.get("pmid","") or "")
                        doi  = str(row.get("doi","") or "")
                        c1, c2, _ = st.columns([1,1,3])
                        if pmid and pmid.isdigit():
                            with c1:
                                st.link_button("🔗 Voir sur PubMed", f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
                        if doi and doi.startswith("10."):
                            with c2:
                                st.link_button("📄 Voir DOI", f"https://doi.org/{doi}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : TABLE
# ══════════════════════════════════════════════════════════════════════════════
elif PAGE == "Table":
    st.markdown('<div class="page-title">Data Table</div>', unsafe_allow_html=True)
    if df.empty:
        st.info("Aucune donnée.")
    else:
        COLS = [c for c in ("pmid","title","authors","year","journal","domain","doi") if c in df.columns]
        display = df[COLS].copy()
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1: f_dom = st.selectbox("Domaine", ["All"]+sorted(df["domain"].dropna().unique()), key="t_dom")
        with fc2: f_jrn = st.selectbox("Journal", ["All"]+sorted(df["journal"].dropna().unique()), key="t_jrn")
        with fc3: f_yr  = st.selectbox("Année", ["All"]+[str(y) for y in sorted(df["year"].dropna().astype(int).unique(), reverse=True)], key="t_yr")
        with fc4: f_txt = st.text_input("Titre", placeholder="mot-clé...", key="t_txt")
        mask = pd.Series([True]*len(display), index=display.index)
        if f_dom != "All": mask &= df["domain"] == f_dom
        if f_jrn != "All": mask &= df["journal"] == f_jrn
        if f_yr  != "All": mask &= df["year"] == int(f_yr)
        if f_txt: mask &= display["title"].str.contains(f_txt, case=False, na=False)
        filtered = display[mask]
        st.markdown(f'<div style="font-size:11px;color:{T["t3"]};margin-bottom:8px">{len(filtered):,} ligne(s)</div>', unsafe_allow_html=True)
        st.dataframe(filtered, use_container_width=True, height=520)
        dl, _ = st.columns([1, 5])
        with dl:
            st.download_button("⬇ CSV", data=filtered.to_csv(index=False).encode("utf-8"),
                               file_name=f"biomed_{now.strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")

