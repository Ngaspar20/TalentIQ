# pages/2_Carregar_CV.py — CV Upload & Parsing

import streamlit as st
import json
import os
import uuid
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.parser import extract_text_from_file, parse_cv
from core.styles import inject_css, page_header, skill_tags, footer, LOGO_SVG
from qa_agent import QAAgent

st.set_page_config(page_title="Carregar CV &middot; TalentIQ", page_icon="&#128196;", layout="wide")
inject_css()

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

if "dados" not in st.session_state:
    st.session_state["dados"] = _load_data()

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

page_header("&#128196;", "Carregar e Analisar CV",
            f"Motor activo: {config.LLM_ENGINE.upper()} &middot; Suporta PDF e DOCX &middot; Extracção automática de competências e experiência")

dados = _load_data()
vagas = dados.get("vagas", [])

if not vagas:
    st.markdown("""
    <div style="background:#fefce8; border:1px solid #fde047; border-radius:12px; padding:18px 20px;">
        &#9888; <strong>Nenhuma vaga criada.</strong> Crie uma vaga primeiro em <strong>&#128203; Criar Vaga</strong>.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Job selector
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("#### &#128204; Associar Candidato a uma Vaga")
vaga_opcoes = {f"{v['titulo']} ({v['id']})": v for v in vagas}
vaga_selecionada_key = st.selectbox("Seleccionar Vaga", list(vaga_opcoes.keys()))
vaga_selecionada = vaga_opcoes[vaga_selecionada_key]
st.markdown(f"**Competências requeridas:**")
skill_tags(vaga_selecionada.get("competencias_requeridas", []))
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Upload area
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("#### &#128228; Carregar CV")
uploaded_file = st.file_uploader(
    "Arraste o CV aqui ou clique para seleccionar",
    type=["pdf", "docx"],
    help="O TalentIQ extrai automaticamente competências, experiência e formação.",
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    with st.spinner("&#128269; A analisar o CV com IA..."):
        texto = extract_text_from_file(uploaded_file)
        if not texto.strip():
            st.error("&#10060; Não foi possível extrair texto. Verifique se o PDF não é uma imagem digitalizada.")
            st.stop()
        perfil = parse_cv(texto)

    st.markdown(f"""
    <div style="background:#dcfce7; border:1px solid #86efac; border-radius:12px; padding:14px 18px; margin:12px 0;">
        &#9989; <strong style="color:#15803d;">CV analisado via {perfil.get('metodo_extracao', '—')}</strong>
    </div>
    """, unsafe_allow_html=True)

    qa.validate_data_integrity(perfil, required_fields=["nome", "competencias", "experiencia_anos"], data_type="dict")

    # Profile display
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### &#128100; Perfil Extraído")

        st.markdown(f"""
        <div style="background:#eff6ff; border-radius:10px; padding:16px; margin-bottom:16px;">
            <div style="font-size:1.1rem; font-weight:700; color:#1e3a8a;">
                {perfil.get('nome', '—')}
            </div>
            <div style="color:#64748b; font-size:0.85rem; margin-top:4px;">
                {perfil.get('email') or '—'} &nbsp;&middot;&nbsp; {perfil.get('telefone') or '—'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        col_a.metric("&#9203; Anos Experiência", perfil.get("experiencia_anos", 0))
        col_b.metric("&#129504; Competências", len(perfil.get("competencias", [])))

        # Highlight matches vs gaps
        comps_cand = perfil.get("competencias", [])
        comps_vaga = vaga_selecionada.get("competencias_requeridas", [])
        matches = [c for c in comps_cand if c.lower() in [v.lower() for v in comps_vaga]]
        outros = [c for c in comps_cand if c.lower() not in [v.lower() for v in comps_vaga]]

        if comps_cand:
            st.markdown("**&#129504; Competências:**")
            skill_tags(matches + outros, matches=matches)
        else:
            st.caption("_Nenhuma competência identificada_")

        if perfil.get("formacao"):
            st.markdown("**&#127891; Formação:**")
            skill_tags(perfil["formacao"])

        if perfil.get("idiomas"):
            st.markdown("**&#127757; Idiomas:**")
            skill_tags(perfil["idiomas"])

        if perfil.get("resumo"):
            st.markdown(f"**&#128221; Resumo:** _{perfil['resumo']}_")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### &#128195; Texto Extraído do CV")
        st.text_area("", texto[:3000], height=380, disabled=True, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    # Save form
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("#### &#128190; Guardar Candidato")

    with st.form("form_candidato"):
        col1, col2 = st.columns(2)
        with col1:
            nome_edit = st.text_input("&#128100; Nome do Candidato", value=perfil.get("nome", ""))
            email_edit = st.text_input("&#128231; Email", value=perfil.get("email") or "")
        with col2:
            etapa = st.selectbox("ðŸ“ Etapa no Pipeline", [
                "Candidatura Recebida", "Em Triagem", "Entrevista",
                "Proposta", "Contratado", "Rejeitado"
            ])
            notas = st.text_area("&#128221; Notas do Recrutador", placeholder="Observações sobre o candidato...", height=80)

        guardar = st.form_submit_button("&#128190;  Guardar Candidato", type="primary", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if guardar:
        candidato = {
            "id": str(uuid.uuid4())[:8],
            "vaga_id": vaga_selecionada["id"],
            "vaga_titulo": vaga_selecionada["titulo"],
            "nome": nome_edit.strip() or perfil.get("nome", "Desconhecido"),
            "email": email_edit.strip(),
            "perfil": perfil,
            "etapa": etapa,
            "notas": notas,
            "score_fit": None,
            "data_candidatura": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        dados = _load_data()
        dados["candidatos"].append(candidato)
        _save_data(dados)
        st.session_state["dados"] = dados
        st.success(f"&#9989; Candidato **{candidato['nome']}** guardado com sucesso!")

# â”€â”€ Existing candidates â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### &#128101; Candidatos Registados")

dados = _load_data()
candidatos = dados.get("candidatos", [])

if not candidatos:
    st.markdown("""
    <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px; padding:18px; text-align:center; color:#1d4ed8;">
        &#8505; Nenhum candidato registado ainda.
    </div>
    """, unsafe_allow_html=True)
else:
    for c in reversed(candidatos):
        score = c.get("score_fit")
        score_txt = f"&#127919; {score}%" if score is not None else "&#9898; Sem score"
        with st.expander(f"&#128100;  {c['nome']}  &middot;  {c['vaga_titulo']}  &middot;  {c['etapa']}  &middot;  {score_txt}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("&#9203; Experiência", f"{c['perfil'].get('experiencia_anos', 0)} anos")
            col2.metric("&#129504; Competências", len(c['perfil'].get('competencias', [])))
            col3.metric("&#127919; Score Fit", f"{score}%" if score is not None else "—")
            st.write(f"**&#128231; Email:** {c.get('email') or '—'}")
            if c['perfil'].get('competencias'):
                st.markdown("**&#129504; Competências:**")
                skill_tags(c['perfil']['competencias'])
            if c.get("notas"):
                st.write(f"**&#128221; Notas:** {c['notas']}")
            st.caption(f"ID: `{c['id']}` &middot; Candidatura: {c['data_candidatura']}")

footer(config.APP_VERSION, config.LLM_ENGINE)


