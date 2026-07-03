# app.py — TalentIQ Entry Point

import streamlit as st
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config
from core.llm import engine_label
from core.styles import inject_dark_css, footer, LOGO_SVG_DARK
from qa_agent import QAAgent

st.set_page_config(
    page_title="TalentIQ — Recrutamento Inteligente",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_dark_css()

# ── Session state ─────────────────────────────────
def _load_data() -> dict:
    path = os.path.join(os.path.dirname(__file__), "data", "jobs.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"vagas": [], "candidatos": []}

if "dados" not in st.session_state:
    st.session_state["dados"] = _load_data()

# ── QA ────────────────────────────────────────────
qa = QAAgent(config.APP_NAME, config.APP_VERSION)
qa_report = qa.run_full_qa_suite(
    data=st.session_state["dados"],
    code_snippet=open(__file__).read(),
)
qa.display_qa_dashboard(qa_report)

# ── Sidebar ───────────────────────────────────────
_logo_sb = LOGO_SVG_DARK.replace("\n", "").replace("  ", " ")
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:20px 0 10px;">'
        '<div style="display:inline-block;filter:drop-shadow(0 0 14px rgba(29,78,216,0.7));">'
        + _logo_sb +
        '</div>'
        '<div style="font-size:1.5rem;font-weight:800;color:#ffffff;margin-top:8px;letter-spacing:1px;">'
        'Talent<span style="color:#3b82f6;">IQ</span></div>'
        '<div style="font-size:0.85rem;color:#64b5f6;margin-top:4px;letter-spacing:2px;text-transform:uppercase;">'
        'Recrutamento Inteligente</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    dados = _load_data()
    n_vagas      = len(dados.get("vagas", []))
    n_candidatos = len(dados.get("candidatos", []))
    st.metric("📋 Vagas", n_vagas)
    st.metric("👤 Candidatos", n_candidatos)
    st.markdown("---")
    st.markdown(f"**Motor IA:** `{engine_label()}`")
    st.markdown(f"**Versão:** `{config.APP_VERSION}`")

# ── Hero ──────────────────────────────────────────
_logo_hero = LOGO_SVG_DARK.replace('width="52"', 'width="80"').replace('height="52"', 'height="80"')
# Logo — separate call so the multi-line SVG doesn't corrupt surrounding HTML as a markdown code block
st.markdown(
    '<div style="text-align:center;padding-top:52px;padding-bottom:8px;">'
    '<div style="display:inline-block;filter:drop-shadow(0 0 24px rgba(29,78,216,0.6));">'
    + _logo_hero.replace("\n", "")
    + '</div></div>',
    unsafe_allow_html=True,
)
# Wordmark + badge — plain one-liners, no indentation
_eng = engine_label()
st.markdown(
    f'<div style="text-align:center;padding-bottom:24px;">'
    f'<span class="hero-title">TalentIQ</span>'
    f'<div class="hero-sub">Plataforma Inteligente de Recrutamento com IA</div>'
    f'<div class="hero-badge">&#9889; Motor: {_eng} &nbsp;&middot;&nbsp; Mercado: PT / BR / AO / MZ</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Stats row ─────────────────────────────────────
dados      = _load_data()
vagas      = dados.get("vagas", [])
candidatos = dados.get("candidatos", [])
scores     = [c["score_fit"] for c in candidatos if c.get("score_fit") is not None]
contratados = len([c for c in candidatos if c.get("etapa") == "Contratado"])

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("📋 Vagas Activas",  len(vagas))
col2.metric("👥 Candidatos",     len(candidatos))
col3.metric("✅ Contratados",    contratados)
col4.metric("🎯 Score Médio",    f"{round(sum(scores)/len(scores))}%" if scores else "—")

# ── Nav cards ─────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"{r},{g},{b}"

# Professional SVG icons (Heroicons outline style, 40x40 viewBox)
_ICON_VAGA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="40" height="40"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 4v-1a1 1 0 011-1h6a1 1 0 011 1v1"/><path d="M8 11h8M8 15h5"/></svg>'
_ICON_CV   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="40" height="40"><circle cx="12" cy="7" r="3"/><path d="M5 20a7 7 0 0114 0"/><path d="M19 10l2 2-6 6-3-3 6-5z" stroke-width="1.3"/></svg>'
_ICON_FIT  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="40" height="40"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6z"/></svg>'
_ICON_PIPE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="40" height="40"><path d="M3 4h18M6 8h12M9 12h6M11 16h2"/></svg>'
_ICON_SCORE= '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="40" height="40"><path d="M3 20h18M5 20V12M9 20V8M13 20V4M17 20v-6"/></svg>'

NAV = [
    {
        "icon": _ICON_VAGA,
        "title": "Criar Vaga",
        "desc": "Carregue o Termo de Referência e a IA extrai automaticamente todos os requisitos",
        "btn": "Abrir",
        "key": "btn_vagas",
        "page": "pages/1_Criar_Vaga.py",
        "glow": "#1e88e5",
        "accent": "#f97316",
    },
    {
        "icon": _ICON_CV,
        "title": "Carregar CV",
        "desc": "IA analisa o CV e extrai competências, experiência e formação em segundos",
        "btn": "Carregar",
        "key": "btn_cv",
        "page": "pages/2_Carregar_CV.py",
        "glow": "#7c3aed",
        "accent": "#a78bfa",
    },
    {
        "icon": _ICON_FIT,
        "title": "Pontuação Fit",
        "desc": "Ranking automático de candidatos por alinhamento com a vaga (0–100)",
        "btn": "Ver Scores",
        "key": "btn_fit",
        "page": "pages/3_Pontuacao_Fit.py",
        "glow": "#0891b2",
        "accent": "#22d3ee",
    },
    {
        "icon": _ICON_PIPE,
        "title": "Pipeline",
        "desc": "Funil de recrutamento visual — mova candidatos entre etapas",
        "btn": "Pipeline",
        "key": "btn_pipe",
        "page": "pages/4_Pipeline.py",
        "glow": "#059669",
        "accent": "#34d399",
    },
    {
        "icon": _ICON_SCORE,
        "title": "Scoring Geral",
        "desc": "Vista consolidada, exportação Excel e relatório Word de todos os candidatos",
        "btn": "Scoring",
        "key": "btn_scoring",
        "page": "pages/5_Scoring_Geral.py",
        "glow": "#f97316",
        "accent": "#fb923c",
    },
]

cols = st.columns(len(NAV))
for col, nav in zip(cols, NAV):
    with col:
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 28px 20px 22px;
            text-align: center;
            backdrop-filter: blur(12px);
            box-shadow:
                0 0 0 1px rgba({_hex_to_rgb(nav['glow'])},0.2),
                0 8px 32px rgba(0,0,0,0.4),
                inset 0 1px 0 rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        ">
            <!-- top glow bar -->
            <div style="
                position:absolute; top:0; left:0; right:0; height:2px;
                background: linear-gradient(90deg, transparent, {nav['glow']}, {nav['accent']}, transparent);
                border-radius:20px 20px 0 0;
            "></div>
            <!-- icon -->
            <div style="
                color: {nav['glow']};
                margin-bottom: 16px;
                filter: drop-shadow(0 0 10px {nav['glow']});
                display:flex; justify-content:center;
            ">{nav['icon']}</div>
            <!-- title -->
            <div style="
                font-size: 1rem;
                font-weight: 700;
                color: #f1f5f9;
                margin-bottom: 10px;
                letter-spacing: 0.3px;
            ">{nav['title']}</div>
            <!-- desc -->
            <div style="
                font-size: 0.78rem;
                color: #94a3b8;
                line-height: 1.55;
                min-height: 52px;
            ">{nav['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        if st.button(nav["btn"], key=nav["key"], use_container_width=True):
            st.switch_page(nav["page"])


# ── How it works ──────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="font-size:0.7rem; color:#64b5f6; text-transform:uppercase;
            letter-spacing:2px; margin-bottom:16px; text-align:center;">
    Como Funciona
</div>
""", unsafe_allow_html=True)

_STEPS = [
    ("#1565c0", "#1e88e5", "rgba(30,136,229,0.4)", "1",
     "Carregue o ToR",
     "Faça upload do Termo de Referência — a IA extrai título, competências e requisitos."),
    ("#6d28d9", "#7c3aed", "rgba(124,58,237,0.4)", "2",
     "Carregue os CVs",
     "IA analisa cada CV e extrai o perfil completo do candidato automaticamente."),
    ("#0e7490", "#0891b2", "rgba(8,145,178,0.4)", "3",
     "Veja o Ranking",
     "Score automático 0–100 por candidato com explicação detalhada das lacunas."),
    ("#065f46", "#059669", "rgba(5,150,105,0.4)", "4",
     "Exporte os Resultados",
     "Gere relatório Word ou Excel com todo o scoring para partilhar com a equipa."),
]

_hw_cols = st.columns(4)
for col, (c1, c2, glow, num, title, desc) in zip(_hw_cols, _STEPS):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding:20px 12px 24px;
                    background:rgba(255,255,255,0.03); border-radius:16px;
                    border:1px solid rgba(255,255,255,0.07);">
            <div style="width:44px; height:44px; border-radius:50%;
                        background:linear-gradient(135deg,{c1},{c2});
                        box-shadow:0 0 20px {glow};
                        font-weight:800; color:white; font-size:1rem;
                        line-height:44px; margin:0 auto 14px;">{num}</div>
            <div style="font-weight:600; color:#e2e8f0; font-size:.9rem; margin-bottom:8px;">{title}</div>
            <div style="color:#64748b; font-size:.78rem; line-height:1.55;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; color:#334155; font-size:.75rem; margin-top:40px; padding:16px 0;
            border-top:1px solid rgba(255,255,255,0.05);">
    TalentIQ v{config.APP_VERSION} &nbsp;·&nbsp; Motor IA: {engine_label()} &nbsp;·&nbsp;
    PT / BR / AO / MZ &nbsp;·&nbsp; © 2026
</div>
""", unsafe_allow_html=True)


