# pages/4_Pipeline.py — Candidate Pipeline

import streamlit as st
import json
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.styles import inject_css, page_header, score_badge, footer, LOGO_SVG
from qa_agent import QAAgent

st.set_page_config(page_title="Pipeline &middot; TalentIQ", page_icon="&#128202;", layout="wide")
inject_css()

ETAPAS = [
    "Candidatura Recebida",
    "Em Triagem",
    "Entrevista",
    "Proposta",
    "Contratado",
    "Rejeitado",
]

ETAPA_ICONS = {
    "Candidatura Recebida": "&#128229;",
    "Em Triagem": "&#128269;",
    "Entrevista": "&#128172;",
    "Proposta": "&#128221;",
    "Contratado": "&#9989;",
    "Rejeitado": "&#10060;",
}

ETAPA_COLORS = {
    "Candidatura Recebida": "#3b82f6",
    "Em Triagem": "#8b5cf6",
    "Entrevista": "#f59e0b",
    "Proposta": "#06b6d4",
    "Contratado": "#10b981",
    "Rejeitado": "#ef4444",
}

def _load_data():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"vagas": [], "candidatos": []}

def _save_data(dados):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

qa = QAAgent(config.APP_NAME, config.APP_VERSION)

dados = _load_data()
vagas = dados.get("vagas", [])
candidatos = dados.get("candidatos", [])

if candidatos:
    df_qa = pd.DataFrame(candidatos)
    qa.display_qa_dashboard(qa.run_full_qa_suite(data=df_qa))
else:
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

page_header("&#128202;", "Pipeline de Candidatos",
            "Acompanhe o funil de recrutamento e mova candidatos entre etapas")

if not vagas:
    st.warning("Nenhuma vaga criada. Vá a **&#128203; Criar Vaga** primeiro.")
    st.stop()

# â”€â”€ Filter â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown('<div class="section-card">', unsafe_allow_html=True)
vaga_opcoes = {"&#128203; Todas as Vagas": None}
vaga_opcoes.update({f"{v['titulo']} ({v['id']})": v["id"] for v in vagas})
filtro_key = st.selectbox("&#128269; Filtrar por Vaga", list(vaga_opcoes.keys()))
filtro_vaga_id = vaga_opcoes[filtro_key]
st.markdown('</div>', unsafe_allow_html=True)

candidatos_filtrados = (
    candidatos if filtro_vaga_id is None
    else [c for c in candidatos if c["vaga_id"] == filtro_vaga_id]
)

if not candidatos_filtrados:
    st.markdown("""
    <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px;
                padding:20px; text-align:center; color:#1d4ed8;">
        &#8505; Nenhum candidato encontrado para este filtro.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# â”€â”€ KPI row â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("<br>", unsafe_allow_html=True)
scores = [c["score_fit"] for c in candidatos_filtrados if c.get("score_fit") is not None]
em_processo = len([c for c in candidatos_filtrados if c["etapa"] not in ["Contratado", "Rejeitado"]])
contratados = len([c for c in candidatos_filtrados if c["etapa"] == "Contratado"])
rejeitados = len([c for c in candidatos_filtrados if c["etapa"] == "Rejeitado"])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("&#128101; Total", len(candidatos_filtrados))
col2.metric("âš™ Em Processo", em_processo)
col3.metric("&#9989; Contratados", contratados)
col4.metric("&#10060; Rejeitados", rejeitados)
col5.metric("&#127919; Score Médio", f"{round(sum(scores)/len(scores))}%" if scores else "—")

# â”€â”€ Charts â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("<br>", unsafe_allow_html=True)
col_chart1, col_chart2 = st.columns([3, 2])

with col_chart1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### ðŸ“‰ Funil de Recrutamento")
    contagem_etapas = {e: 0 for e in ETAPAS}
    for c in candidatos_filtrados:
        etapa = c.get("etapa", "Candidatura Recebida")
        if etapa in contagem_etapas:
            contagem_etapas[etapa] += 1

    df_funil = pd.DataFrame({
        "Etapa": list(contagem_etapas.keys()),
        "Candidatos": list(contagem_etapas.values()),
    })
    fig_funil = px.funnel(
        df_funil, x="Candidatos", y="Etapa",
        color="Etapa",
        color_discrete_map={e: ETAPA_COLORS.get(e, "#3b82f6") for e in ETAPAS},
    )
    fig_funil.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#1e3a8a"),
    )
    st.plotly_chart(fig_funil, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### &#127919; Distribuição de Scores")
    if scores:
        altos = len([s for s in scores if s >= 75])
        medios = len([s for s in scores if 50 <= s < 75])
        baixos = len([s for s in scores if s < 50])
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Alto (â‰¥75)", "Médio (50-74)", "Baixo (<50)"],
            values=[altos, medios, baixos],
            hole=0.55,
            marker_colors=["#10b981", "#f59e0b", "#ef4444"],
        )])
        fig_pie.update_layout(
            showlegend=True,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#1e3a8a"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align:center; color:#94a3b8; padding:40px 0;">
            Calcule os scores em <strong>&#127919; Pontuação Fit</strong> para ver a distribuição.
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# â”€â”€ Kanban board â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### ðŸ—‚ Candidatos por Etapa")

etapas_ativas = [e for e in ETAPAS if e not in ["Contratado", "Rejeitado"]]
cols = st.columns(len(etapas_ativas))

for col, etapa in zip(cols, etapas_ativas):
    icon = ETAPA_ICONS.get(etapa, "")
    cor = ETAPA_COLORS.get(etapa, "#3b82f6")
    candidatos_etapa = [c for c in candidatos_filtrados if c.get("etapa") == etapa]

    with col:
        st.markdown(f"""
        <div class="kanban-col-header" style="background:{cor};">
            {icon} {etapa}<br>
            <span style="font-size:0.75rem; opacity:0.85;">{len(candidatos_etapa)} candidato(s)</span>
        </div>
        """, unsafe_allow_html=True)

        for c in sorted(candidatos_etapa, key=lambda x: x.get("score_fit") or 0, reverse=True):
            score = c.get("score_fit")
            score_html = f"<span style='color:#1d4ed8; font-weight:600;'>&#127919; {score}%</span>" \
                if score is not None else "<span style='color:#94a3b8;'>&#9898; Sem score</span>"
            st.markdown(f"""
            <div class="kanban-card" style="border-left-color:{cor};">
                <div class="kanban-card-name">{c['nome']}</div>
                <div class="kanban-card-sub">{c['vaga_titulo']}</div>
                <div style="margin-top:6px; font-size:0.82rem;">{score_html}</div>
            </div>
            """, unsafe_allow_html=True)

# â”€â”€ Move candidate â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("### &#128260; Mover Candidato de Etapa")

nomes = {f"{c['nome']} &middot; {c['vaga_titulo']} ({c['id']})": c["id"] for c in candidatos_filtrados}
if nomes:
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        candidato_key = st.selectbox("&#128100; Selecionar Candidato", list(nomes.keys()))
        candidato_id = nomes[candidato_key]
    with col2:
        nova_etapa = st.selectbox("ðŸ“ Nova Etapa", ETAPAS)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("&#9989;  Actualizar", type="primary", use_container_width=True):
            for i, c in enumerate(dados["candidatos"]):
                if c["id"] == candidato_id:
                    dados["candidatos"][i]["etapa"] = nova_etapa
            _save_data(dados)
            st.success(f"Candidato movido para **{nova_etapa}**!")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# â”€â”€ Full table â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### &#128203; Tabela Completa")

df = pd.DataFrame([{
    "Nome": c["nome"],
    "Vaga": c["vaga_titulo"],
    "Etapa": f"{ETAPA_ICONS.get(c.get('etapa',''), '')} {c.get('etapa', '—')}",
    "Score Fit": f"{c['score_fit']}%" if c.get("score_fit") is not None else "—",
    "Experiência": f"{c['perfil'].get('experiencia_anos', 0)} anos",
    "Candidatura": c.get("data_candidatura", "—"),
} for c in candidatos_filtrados])

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Score Fit": st.column_config.TextColumn("&#127919; Score Fit"),
        "Etapa": st.column_config.TextColumn("ðŸ“ Etapa"),
        "Nome": st.column_config.TextColumn("&#128100; Nome"),
    }
)

footer(config.APP_VERSION, config.LLM_ENGINE)


