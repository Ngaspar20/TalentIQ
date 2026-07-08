# pages/3_Pontuacao_Fit.py — Fit Scoring

import streamlit as st
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.scorer import calcular_fit
from core.styles import inject_css, page_header, skill_tags, score_badge, footer, LOGO_SVG
from core.security import esc, atomic_save
from qa_agent import QAAgent

st.set_page_config(page_title="Pontuação Fit &middot; TalentIQ", page_icon="&#127919;", layout="wide")
inject_css()

def _load_data():
    try:
        with open(config.DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"vagas": [], "candidatos": []}

def _save_data(dados):
    atomic_save(config.DATA_PATH, dados)

if config.DEV_MODE:
    qa = QAAgent(config.APP_NAME, config.APP_VERSION)
    qa.display_qa_dashboard(qa.run_full_qa_suite())

_sb_logo = LOGO_SVG.replace("\n", "").replace("  ", " ")
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:4px 0 12px;">'
        '<div style="display:inline-block;filter:drop-shadow(0 0 10px rgba(29,78,216,0.5));">'
        + _sb_logo +
        '</div>'
        '<div style="font-size:1.5rem;font-weight:800;color:#ffffff;margin-top:6px;">'
        'Talent<span style="color:#3b82f6;">IQ</span></div>'
        '</div>',
        unsafe_allow_html=True,
    )

page_header("&#127919;", "Pontuação de Alinhamento",
            "Ranking automático de candidatos por score de fit 0&ndash;100 &middot; Competências &middot; Experiência &middot; Formação")

dados = _load_data()
vagas = dados.get("vagas", [])
candidatos = dados.get("candidatos", [])

if not vagas:
    st.warning("Nenhuma vaga criada. Vá a **&#128203; Criar Vaga** primeiro.")
    st.stop()
if not candidatos:
    st.warning("Nenhum candidato registado. Vá a **&#128196; Carregar CV** primeiro.")
    st.stop()

# Vaga selector
st.markdown('<div class="section-card">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    vaga_opcoes = {}
    for v in vagas:
        label = v["titulo"]
        if label in vaga_opcoes:
            label = f"{v['titulo']} ({v['id'][:6]})"
        vaga_opcoes[label] = v
    vaga_key = st.selectbox("&#128204; Selecionar Vaga", list(vaga_opcoes.keys()))
    vaga = vaga_opcoes[vaga_key]
    st.markdown("**Competências requeridas:**")
    skill_tags(vaga.get("competencias_requeridas", []))
with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    calcular_btn = st.button("🚀  Calcular Scores", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

candidatos_vaga = [c for c in candidatos if c["vaga_id"] == vaga["id"]]

if not candidatos_vaga:
    st.markdown(f"""
    <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:18px; text-align:center; color:#1d4ed8;">
        &#8505; Nenhum candidato associado à vaga <strong>{vaga['titulo']}</strong>.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if calcular_btn:
    with st.spinner("&#128269; A calcular alinhamento..."):
        for i, c in enumerate(dados["candidatos"]):
            if c["vaga_id"] == vaga["id"]:
                resultado = calcular_fit(c["perfil"], vaga)
                dados["candidatos"][i]["score_fit"] = resultado["score_total"]
                dados["candidatos"][i]["fit_resultado"] = resultado
                dados["candidatos"][i]["score_calculado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        _save_data(dados)
        st.session_state["dados"] = dados
    st.success("&#9989; Scores calculados com sucesso!")
    st.rerun()

# Stale score alert — warn if vaga was modified after scores were calculated
candidatos_vaga = [c for c in dados.get("candidatos", []) if c["vaga_id"] == vaga["id"]]
vaga_modificada = vaga.get("data_modificacao") or vaga.get("data_criacao", "")
scores_desactualizados = [
    c for c in candidatos_vaga
    if c.get("score_fit") is not None
    and c.get("score_calculado_em", "") < vaga_modificada
]
if scores_desactualizados:
    st.warning(
        f"⚠️ A vaga foi editada após o cálculo de scores de "
        f"**{len(scores_desactualizados)}** candidato(s). "
        f"Clique em **Calcular Scores** para recalcular com os critérios actuais."
    )

candidatos_sorted = sorted(candidatos_vaga, key=lambda x: x.get("score_fit") or 0, reverse=True)

scores_calc = [c["score_fit"] for c in candidatos_vaga if c.get("score_fit") is not None]
altos = len([s for s in scores_calc if s >= 75])
medios = len([s for s in scores_calc if 50 <= s < 75])
baixos = len([s for s in scores_calc if s < 50])

st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("&#128101; Candidatos", len(candidatos_vaga))
col2.metric("🟢 Alto Alinhamento", altos)
col3.metric("🟡 Alinhamento Médio", medios)
col4.metric("🔴 Baixo Alinhamento", baixos)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### &#127942; Ranking de Candidatos")

# â"€â"€ Candidate cards â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
for rank, c in enumerate(candidatos_sorted, 1):
    score = c.get("score_fit")
    fit = c.get("fit_resultado", {})
    nivel = fit.get("nivel_alinhamento", "Não calculado")
    detalhes = fit.get("pontuacao_detalhada", {})

    badge = score_badge(score)
    rank_icon = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")

    comps_cand = c["perfil"].get("competencias", [])
    comps_vaga = vaga.get("competencias_requeridas", [])
    matches = [x for x in comps_cand if x.lower() in [v.lower() for v in comps_vaga]]
    gaps = [x for x in comps_vaga if x.lower() not in [c.lower() for c in comps_cand]]

    with st.expander(f"{rank_icon}  {c['nome']}  &middot;  {nivel}"):
        # Score row
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:20px; margin-bottom:16px;">
            {badge}
            <div>
                <div style="font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">
                    Alinhamento Geral
                </div>
                <div style="font-weight:700; color:#1e3a8a;">{nivel}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Score breakdown
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("&#127919; Score Total", f"{score}/100" if score is not None else "—")
        col2.metric("&#129504; Competências", f"{detalhes.get('competencias', '—')}/50")
        col3.metric("&#9203; Experiência", f"{detalhes.get('experiencia', '—')}/30")
        col4.metric("&#127891; Formação", f"{detalhes.get('formacao', '—')}/20")

        # Analysis
        if fit.get("explicacao"):
            st.markdown("**&#128203; Análise Detalhada:**")
            for linha in fit["explicacao"]:
                st.markdown(f"<div style='padding:4px 0; color:#374151;'>{esc(linha)}</div>",
                            unsafe_allow_html=True)

        # Skills comparison
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**&#129504; Competências do Candidato:**")
            if comps_cand:
                skill_tags(comps_cand, matches=matches)
            else:
                st.caption("_Nenhuma identificada_")
        with col_b:
            st.markdown("**&#10060; Lacunas em Relação à Vaga:**")
            if gaps:
                skill_tags(gaps, gaps=gaps)
            else:
                st.markdown('<span class="skill-tag-match">&#10003; Sem lacunas</span>', unsafe_allow_html=True)

        metodo = fit.get("metodo", "—")
        st.caption(f"Motor: {metodo} &middot; Etapa: {c['etapa']} &middot; ID: {c['id']}")

footer(config.APP_VERSION, config.LLM_ENGINE)


