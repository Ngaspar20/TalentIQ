# core/styles.py — Shared TalentIQ UI theme

LOGO_SVG = """
<svg width="52" height="52" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
  <!-- connector lines -->
  <line x1="13" y1="13" x2="23" y2="23" stroke="#93c5fd" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="39" y1="13" x2="29" y2="23" stroke="#93c5fd" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="13" y1="39" x2="23" y2="29" stroke="#93c5fd" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="39" y1="39" x2="29" y2="29" stroke="#93c5fd" stroke-width="1.5" stroke-linecap="round"/>
  <!-- satellite nodes -->
  <circle cx="12" cy="12" r="9" fill="#bfdbfe" stroke="#93c5fd" stroke-width="1"/>
  <circle cx="40" cy="12" r="9" fill="#bfdbfe" stroke="#93c5fd" stroke-width="1"/>
  <circle cx="12" cy="40" r="9" fill="#bfdbfe" stroke="#93c5fd" stroke-width="1"/>
  <circle cx="40" cy="40" r="9" fill="#bfdbfe" stroke="#93c5fd" stroke-width="1"/>
  <!-- person silhouettes in satellite nodes -->
  <circle cx="12" cy="9"  r="3"   fill="#3b82f6"/>
  <path   d="M6,16 Q12,20 18,16"  fill="#60a5fa"/>
  <circle cx="40" cy="9"  r="3"   fill="#3b82f6"/>
  <path   d="M34,16 Q40,20 46,16" fill="#60a5fa"/>
  <circle cx="12" cy="37" r="3"   fill="#3b82f6"/>
  <path   d="M6,44 Q12,48 18,44"  fill="#60a5fa"/>
  <circle cx="40" cy="37" r="3"   fill="#3b82f6"/>
  <path   d="M34,44 Q40,48 46,44" fill="#60a5fa"/>
  <!-- centre badge -->
  <circle cx="26" cy="26" r="12" fill="#1d4ed8"/>
  <text x="26" y="31" font-family="Inter,Arial,sans-serif" font-size="10" font-weight="800"
        fill="white" text-anchor="middle" letter-spacing="-0.3">IQ</text>
  <!-- orange accent dot -->
  <circle cx="35" cy="17" r="4.5" fill="#f97316"/>
  <circle cx="35" cy="17" r="2"   fill="#fed7aa"/>
</svg>
"""

LOGO_SVG_DARK = """
<svg width="52" height="52" viewBox="0 0 52 52" xmlns="http://www.w3.org/2000/svg">
  <line x1="13" y1="13" x2="23" y2="23" stroke="#1d4ed8" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="39" y1="13" x2="29" y2="23" stroke="#1d4ed8" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="13" y1="39" x2="23" y2="29" stroke="#1d4ed8" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="39" y1="39" x2="29" y2="29" stroke="#1d4ed8" stroke-width="1.5" stroke-linecap="round"/>
  <circle cx="12" cy="12" r="9" fill="#1e3a6e" stroke="#1d4ed8" stroke-width="1.2"/>
  <circle cx="40" cy="12" r="9" fill="#1e3a6e" stroke="#1d4ed8" stroke-width="1.2"/>
  <circle cx="12" cy="40" r="9" fill="#1e3a6e" stroke="#1d4ed8" stroke-width="1.2"/>
  <circle cx="40" cy="40" r="9" fill="#1e3a6e" stroke="#1d4ed8" stroke-width="1.2"/>
  <circle cx="12" cy="9"  r="3"   fill="#3b82f6"/>
  <path   d="M6,16 Q12,20 18,16"  fill="#2563eb"/>
  <circle cx="40" cy="9"  r="3"   fill="#3b82f6"/>
  <path   d="M34,16 Q40,20 46,16" fill="#2563eb"/>
  <circle cx="12" cy="37" r="3"   fill="#3b82f6"/>
  <path   d="M6,44 Q12,48 18,44"  fill="#2563eb"/>
  <circle cx="40" cy="37" r="3"   fill="#3b82f6"/>
  <path   d="M34,44 Q40,48 46,44" fill="#2563eb"/>
  <circle cx="26" cy="26" r="12" fill="#1d4ed8"/>
  <text x="26" y="31" font-family="Inter,Arial,sans-serif" font-size="10" font-weight="800"
        fill="white" text-anchor="middle" letter-spacing="-0.3">IQ</text>
  <circle cx="35" cy="17" r="4.5" fill="#f97316"/>
  <circle cx="35" cy="17" r="2"   fill="#fed7aa"/>
</svg>
"""

def inject_css(dark: bool = False):
    import streamlit as st
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Main background (light pages) ── */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8eeff 100%);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1628 0%, #0f2044 60%, #1a1a2e 100%);
        border-right: 1px solid rgba(99,179,237,0.15);
    }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; font-size: 1rem !important; }
    section[data-testid="stSidebar"] .stMetric label { color: #93c5fd !important; font-size: 0.85rem !important; }
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #ffffff !important; font-weight: 700; font-size: 1.8rem !important;
    }
    section[data-testid="stSidebar"] a { font-size: 1.05rem !important; font-weight: 500 !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
    section[data-testid="stSidebar"] code {
        background: rgba(255,255,255,0.1) !important;
        color: #93c5fd !important; border-radius: 4px; padding: 2px 6px; font-size: 0.9rem !important;
    }

    /* ── Page header ── */
    .talentiq-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%);
        border-radius: 16px; padding: 32px 40px; margin-bottom: 28px;
        color: white; box-shadow: 0 8px 32px rgba(29,78,216,0.25);
    }
    .talentiq-header h1 { margin:0; font-size:2rem; font-weight:700; color:white !important; }
    .talentiq-header p  { margin:6px 0 0; color:#bfdbfe; font-size:1rem; }

    /* ── KPI metric cards ── */
    [data-testid="stMetric"] {
        background: white; border-radius: 12px; padding: 16px 20px;
        border: 1px solid #e0e7ff; box-shadow: 0 2px 8px rgba(29,78,216,0.07);
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important; font-size: 0.8rem !important;
        font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        color: #1e3a8a !important; font-weight: 700 !important; font-size: 1.8rem !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        color: white !important; border: none; border-radius: 10px;
        padding: 10px 24px; font-weight: 600; font-size: 0.9rem;
        transition: all 0.2s ease; box-shadow: 0 4px 12px rgba(29,78,216,0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(29,78,216,0.4); transform: translateY(-1px);
    }

    /* ── Form inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        border: 2px solid #e0e7ff !important; border-radius: 10px !important;
        background: white !important; transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
    }

    /* ── Section cards ── */
    .section-card {
        background: white; border-radius: 14px; padding: 24px 28px;
        border: 1px solid #e0e7ff; margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(29,78,216,0.06);
    }

    /* ── Score badges ── */
    .score-high {
        background: linear-gradient(135deg,#059669,#10b981); color:white;
        padding:6px 16px; border-radius:20px; font-weight:700; display:inline-block;
    }
    .score-mid {
        background: linear-gradient(135deg,#d97706,#f59e0b); color:white;
        padding:6px 16px; border-radius:20px; font-weight:700; display:inline-block;
    }
    .score-low {
        background: linear-gradient(135deg,#dc2626,#ef4444); color:white;
        padding:6px 16px; border-radius:20px; font-weight:700; display:inline-block;
    }

    /* ── Skill tags ── */
    .skill-tag       { background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; padding:3px 10px; border-radius:20px; font-size:.78rem; font-weight:500; display:inline-block; margin:2px 3px; }
    .skill-tag-match { background:#dcfce7; color:#15803d; border:1px solid #86efac; padding:3px 10px; border-radius:20px; font-size:.78rem; font-weight:500; display:inline-block; margin:2px 3px; }
    .skill-tag-gap   { background:#fef2f2; color:#b91c1c; border:1px solid #fca5a5; padding:3px 10px; border-radius:20px; font-size:.78rem; font-weight:500; display:inline-block; margin:2px 3px; }

    /* ── Kanban ── */
    .kanban-col-header {
        color:white; padding:10px 14px; border-radius:10px 10px 0 0;
        font-weight:600; font-size:.85rem; text-align:center;
    }
    .kanban-card {
        background:white; border-left:4px solid #3b82f6; border-radius:8px;
        padding:12px 14px; margin:8px 0; box-shadow:0 2px 6px rgba(0,0,0,0.08);
    }
    .kanban-card-name { font-weight:600; color:#1e3a8a; font-size:.9rem; }
    .kanban-card-sub  { color:#64748b; font-size:.75rem; margin-top:2px; }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background:white !important; border:1px solid #e0e7ff !important;
        border-radius:10px !important; font-weight:500 !important; color:#1e3a8a !important;
    }
    .streamlit-expanderContent {
        border:1px solid #e0e7ff !important; border-top:none !important;
        border-radius:0 0 10px 10px !important; background:#fafbff !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background:white; border:2px dashed #93c5fd; border-radius:12px; padding:8px;
    }

    hr { border:none; border-top:2px solid #e0e7ff; margin:24px 0; }

    [data-testid="stDataFrame"] {
        border-radius:12px; overflow:hidden; border:1px solid #e0e7ff;
    }

    .talentiq-footer {
        text-align:center; color:#94a3b8; font-size:.78rem;
        margin-top:40px; padding:20px 0; border-top:1px solid #e0e7ff;
    }
    </style>
    """, unsafe_allow_html=True)


def inject_dark_css():
    """Dark premium theme for the home page."""
    import streamlit as st
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Dark background ── */
    .stApp {
        background: radial-gradient(ellipse at 20% 20%, #0d1f3c 0%, #080d1a 50%, #0a0a0f 100%);
        min-height: 100vh;
    }

    /* ── Hide default streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Sidebar dark ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080d1a 0%, #0d1f3c 100%);
        border-right: 1px solid rgba(99,179,237,0.1);
    }
    section[data-testid="stSidebar"] * { color: #cbd5e1 !important; font-size: 1rem !important; }
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #ffffff !important; font-weight:700; font-size: 1.8rem !important;
    }
    section[data-testid="stSidebar"] .stMetric label { color: #64b5f6 !important; font-size: 0.85rem !important; }
    section[data-testid="stSidebar"] a { font-size: 1.05rem !important; font-weight: 500 !important; }
    section[data-testid="stSidebar"] p { font-size: 1rem !important; }
    section[data-testid="stSidebar"] code {
        background: rgba(255,255,255,0.08) !important; color:#90caf9 !important;
        border-radius:4px; padding:2px 6px; font-size: 0.9rem !important;
    }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }

    /* ── Metric cards (dark) ── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px; padding: 16px 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #64b5f6 !important; font-size:.78rem !important;
        font-weight:500 !important; text-transform:uppercase; letter-spacing:0.8px;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important; font-weight:800 !important; font-size:2rem !important;
    }

    /* ── Buttons (dark) ── */
    .stButton > button {
        background: linear-gradient(135deg, #1565c0 0%, #1e88e5 100%);
        color: white !important; border: 1px solid rgba(100,180,255,0.3) !important;
        border-radius: 12px; padding: 10px 28px;
        font-weight: 600; font-size: 0.9rem; letter-spacing: 0.3px;
        box-shadow: 0 0 20px rgba(30,136,229,0.4), 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.25s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2 0%, #42a5f5 100%);
        box-shadow: 0 0 32px rgba(66,165,245,0.6), 0 6px 20px rgba(0,0,0,0.4);
        transform: translateY(-2px);
    }

    /* ── Tabs (dark) ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.04);
        border-radius: 12px; padding: 4px; border: 1px solid rgba(255,255,255,0.08);
    }
    .stTabs [data-baseweb="tab"] { color: #94a3b8 !important; border-radius: 8px; }
    .stTabs [aria-selected="true"] {
        background: rgba(30,136,229,0.2) !important; color: #90caf9 !important;
    }

    /* ── Dataframe (dark) ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px; overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #080d1a; }
    ::-webkit-scrollbar-thumb { background: #1e88e5; border-radius: 3px; }

    /* ── Hero title gradient ── */
    .hero-title {
        display: inline-block;
        background: linear-gradient(135deg, #1e88e5, #42a5f5, #f97316);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.6rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 12px;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(30,136,229,0.12);
        border: 1px solid rgba(30,136,229,0.3);
        border-radius: 20px;
        padding: 5px 16px;
        color: #64b5f6;
        font-size: 0.78rem;
        margin-top: 12px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    import streamlit as st
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="talentiq-header">
        <h1>{icon} {title}</h1>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def skill_tags(skills: list, matches: list = None, gaps: list = None):
    html = ""
    for s in skills:
        s_lower = s.lower()
        if matches and s_lower in [m.lower() for m in matches]:
            html += f'<span class="skill-tag-match">&#10003; {s}</span>'
        elif gaps and s_lower in [g.lower() for g in gaps]:
            html += f'<span class="skill-tag-gap">&#10007; {s}</span>'
        else:
            html += f'<span class="skill-tag">{s}</span>'
    import streamlit as st
    st.markdown(html, unsafe_allow_html=True)


def score_badge(score: int) -> str:
    if score is None:
        return '<span class="skill-tag">Sem score</span>'
    if score >= 75:
        return f'<span class="score-high">&#127942; {score}/100</span>'
    if score >= 50:
        return f'<span class="score-mid">&#9889; {score}/100</span>'
    return f'<span class="score-low">&#9888; {score}/100</span>'


def footer(version: str, engine: str):
    import streamlit as st
    st.markdown(f"""
    <div class="talentiq-footer">
        TalentIQ v{version} &nbsp;&middot;&nbsp; Motor IA: {engine} &nbsp;&middot;&nbsp;
        Mercado: PT/BR/AO/MZ &nbsp;&middot;&nbsp; &copy; 2026
    </div>
    """, unsafe_allow_html=True)