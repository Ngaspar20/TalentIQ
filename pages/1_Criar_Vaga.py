# pages/1_Criar_Vaga.py — Job Creation via ToR Upload

import streamlit as st
import json
import os
import uuid
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.parser import extract_text_from_file, parse_tor
from core.styles import inject_css, page_header, skill_tags, footer, LOGO_SVG
from qa_agent import QAAgent

st.set_page_config(page_title="Criar Vaga · TalentIQ", page_icon="📋", layout="wide")
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

if "tor_extraido" not in st.session_state:
    st.session_state["tor_extraido"] = None

# ── Helper functions for selectbox indices ────────
def _dept_index(val: str) -> int:
    opts = ["Recursos Humanos", "Tecnologia de Informação", "Finanças",
            "Operações", "Saúde Pública", "Marketing", "Vendas", "Outro"]
    val_lower = val.lower()
    for i, o in enumerate(opts):
        if o.lower() in val_lower or val_lower in o.lower():
            return i
    return 7

def _nivel_index(val: str) -> int:
    opts = ["", "curso técnico", "licenciatura", "mestrado", "doutoramento"]
    val_lower = val.lower()
    for i, o in enumerate(opts):
        if o and o in val_lower:
            return i
    return 0

def _contrato_index(val: str) -> int:
    opts = ["tempo inteiro", "tempo parcial", "consultoria", "estágio"]
    val_lower = val.lower()
    for i, o in enumerate(opts):
        if o in val_lower:
            return i
    return 0

qa = QAAgent(config.APP_NAME, config.APP_VERSION)
qa.display_qa_dashboard(qa.run_full_qa_suite())

_sb_logo = LOGO_SVG.replace("\n", "").replace("  ", " ")
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:4px 0 12px;">'
        '<div style="display:inline-block;filter:drop-shadow(0 0 10px rgba(29,78,216,0.5));">'
        + _sb_logo +
        '</div><div style="font-size:1.5rem;font-weight:800;color:#ffffff;margin-top:6px;">'
        'Talent<span style="color:#3b82f6;">IQ</span></div></div>',
        unsafe_allow_html=True,
    )

page_header(
    "📋", "Criar Nova Vaga",
    f"Carregue o Termo de Referência — a IA extrai automaticamente todos os elementos da posição · Motor: {config.LLM_ENGINE.upper()}"
)

# ── Step 1: Upload ToR ────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
    <div style="background:#1d4ed8; color:white; border-radius:50%; width:32px; height:32px;
                display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">1</div>
    <div style="font-size:1.05rem; font-weight:600; color:#1e3a8a;">Carregar Termo de Referência</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)

uploaded_tor = st.file_uploader(
    "Arraste o ToR aqui ou clique para seleccionar (PDF ou DOCX)",
    type=["pdf", "docx"],
    help="O TalentIQ lê o documento e extrai título, competências, requisitos e descrição automaticamente.",
    key="tor_uploader",
)

if uploaded_tor:
    with st.spinner("🔍 A analisar o Termo de Referência com IA..."):
        texto_tor = extract_text_from_file(uploaded_tor)
        if not texto_tor.strip():
            st.error("❌ Não foi possível extrair texto. Verifique se o ficheiro não é uma imagem digitalizada.")
            st.stop()
        extraido = parse_tor(texto_tor)
        st.session_state["tor_extraido"] = extraido

    st.markdown(f"""
    <div style="background:#dcfce7; border:1px solid #86efac; border-radius:10px; padding:12px 16px; margin-top:8px;">
        ✅ <strong style="color:#15803d;">ToR analisado via {extraido.get('metodo_extracao', '—')}</strong>
        &nbsp;·&nbsp; <span style="color:#64748b; font-size:0.85rem;">{uploaded_tor.name}</span>
    </div>
    """, unsafe_allow_html=True)

    # Show raw text preview
    with st.expander("📃 Ver texto extraído do documento"):
        st.text_area("", texto_tor[:3000], height=250, disabled=True, label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# ── Step 2: Review & edit extracted fields ────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
    <div style="background:#1d4ed8; color:white; border-radius:50%; width:32px; height:32px;
                display:flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0;">2</div>
    <div style="font-size:1.05rem; font-weight:600; color:#1e3a8a;">Rever e Confirmar Dados Extraídos</div>
</div>
""", unsafe_allow_html=True)

tor = st.session_state.get("tor_extraido") or {}

st.markdown('<div class="section-card">', unsafe_allow_html=True)

with st.form("form_vaga"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📌 Informação Básica")
        titulo = st.text_input(
            "Título da Vaga *",
            value=tor.get("titulo", ""),
            placeholder="Ex: Analista de Dados Sénior"
        )
        organizacao = st.text_input(
            "🏛️ Organização",
            value=tor.get("organizacao", ""),
            placeholder="Ex: Ministério da Saúde"
        )
        departamento = st.selectbox(
            "Departamento",
            ["Recursos Humanos", "Tecnologia de Informação", "Finanças",
             "Operações", "Saúde Pública", "Marketing", "Vendas", "Outro"],
            index=_dept_index(tor.get("departamento", "")),
        )
        local = st.text_input(
            "📍 Localização",
            value=tor.get("local", ""),
            placeholder="Ex: Maputo, Moçambique"
        )
        modalidade = st.selectbox(
            "🏢 Modalidade",
            ["Presencial", "Remoto", "Híbrido"],
            index=["presencial", "remoto", "híbrido"].index(
                tor.get("modalidade", "Presencial").lower()
            ) if tor.get("modalidade", "").lower() in ["presencial", "remoto", "híbrido"] else 0
        )

    with col2:
        st.markdown("#### 🎓 Requisitos")
        nivel_formacao = st.selectbox(
            "Nível de Formação Mínimo",
            ["", "Curso Técnico", "Licenciatura", "Mestrado", "Doutoramento"],
            index=_nivel_index(tor.get("nivel_formacao", "")),
        )
        anos_experiencia = st.number_input(
            "⏳ Anos de Experiência Mínimos",
            min_value=0, max_value=30,
            value=int(tor.get("anos_experiencia_min", 0) or 0)
        )
        tipo_contrato = st.selectbox(
            "📄 Tipo de Contrato",
            ["Tempo Inteiro", "Tempo Parcial", "Consultoria", "Estágio"],
            index=_contrato_index(tor.get("tipo_contrato", "")),
        )
        salario = st.text_input(
            "💰 Faixa Salarial (opcional)",
            value=tor.get("salario") or "",
            placeholder="Ex: 50.000 - 80.000 MZN"
        )
        prazo = st.text_input(
            "📅 Prazo de Candidatura",
            value=tor.get("prazo_candidatura") or "",
            placeholder="Ex: 31 de Julho de 2026"
        )

    st.markdown("#### 🧠 Competências Requeridas")
    st.caption("Edite se necessário — separadas por vírgula")
    competencias_extraidas = ", ".join(tor.get("competencias_requeridas", []))
    competencias_input = st.text_area(
        "Competências *",
        value=competencias_extraidas,
        placeholder="Ex: Python, SQL, Power BI, Gestão de Projetos",
        height=90,
    )

    if tor.get("responsabilidades"):
        st.markdown("#### 📋 Responsabilidades Extraídas")
        resp_text = "\n".join(f"• {r}" for r in tor["responsabilidades"])
        responsabilidades_input = st.text_area(
            "Responsabilidades",
            value=resp_text,
            height=120,
        )
    else:
        responsabilidades_input = ""

    st.markdown("#### 📝 Descrição da Vaga")
    descricao = st.text_area(
        "Descrição",
        value=tor.get("descricao", ""),
        placeholder="Contexto e objectivo da posição...",
        height=120,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        submitted = st.form_submit_button(
            "💾  Guardar Vaga", use_container_width=True, type="primary"
        )
    with col_btn2:
        limpar = st.form_submit_button(
            "🔄  Limpar", use_container_width=True
        )

st.markdown('</div>', unsafe_allow_html=True)

if limpar:
    st.session_state["tor_extraido"] = None
    st.rerun()

if submitted:
    erros = []
    if not titulo.strip():
        erros.append("O título da vaga é obrigatório.")
    if not competencias_input.strip():
        erros.append("Adicione pelo menos uma competência requerida.")

    if erros:
        for e in erros:
            st.error(f"❌ {e}")
    else:
        competencias_lista = [c.strip().lower() for c in competencias_input.split(",") if c.strip()]
        vaga = {
            "id": str(uuid.uuid4())[:8],
            "titulo": titulo.strip(),
            "organizacao": organizacao.strip(),
            "departamento": departamento,
            "local": local,
            "modalidade": modalidade,
            "nivel_formacao": nivel_formacao.lower(),
            "anos_experiencia_min": int(anos_experiencia),
            "tipo_contrato": tipo_contrato,
            "salario": salario,
            "prazo_candidatura": prazo,
            "competencias_requeridas": competencias_lista,
            "responsabilidades": [
                r.strip().lstrip("•").strip()
                for r in responsabilidades_input.split("\n") if r.strip()
            ],
            "descricao": descricao,
            "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "estado": "Aberta",
            "origem": f"ToR · {tor.get('metodo_extracao', '—')}",
        }

        qa.validate_data_integrity(
            vaga,
            required_fields=["titulo", "competencias_requeridas"],
            data_type="dict"
        )

        dados = _load_data()
        dados["vagas"].append(vaga)
        _save_data(dados)
        st.session_state["dados"] = dados
        st.session_state["tor_extraido"] = None

        st.markdown(f"""
        <div style="background:#dcfce7; border:1px solid #86efac; border-radius:12px; padding:16px 20px; margin:16px 0;">
            ✅ <strong style="color:#15803d;">Vaga <em>{titulo}</em> criada com sucesso!</strong>
            <span style="color:#64748b; font-size:0.85rem; margin-left:12px;">ID: {vaga['id']} · Origem: {vaga['origem']}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Competências registadas:**")
        skill_tags(competencias_lista)

# ── Existing jobs ─────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📌 Vagas Existentes")

dados = _load_data()
vagas = dados.get("vagas", [])

if not vagas:
    st.markdown("""
    <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:12px;
                padding:20px; text-align:center; color:#1d4ed8;">
        ℹ️ Nenhuma vaga criada ainda. Carregue um ToR acima para começar.
    </div>
    """, unsafe_allow_html=True)
else:
    for v in reversed(vagas):
        with st.expander(f"📌  {v['titulo']}  ·  {v.get('organizacao','') or v['departamento']}  ·  {v.get('estado','Aberta')}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("⏳ Experiência", f"{v['anos_experiencia_min']} anos")
            col2.metric("🎓 Formação", v['nivel_formacao'].title() or "—")
            col3.metric("🏢 Modalidade", v['modalidade'])
            col4.metric("📄 Contrato", v['tipo_contrato'])

            st.markdown("**🧠 Competências Requeridas:**")
            skill_tags(v['competencias_requeridas'])

            if v.get("responsabilidades"):
                st.markdown("**📋 Responsabilidades:**")
                for r in v["responsabilidades"][:5]:
                    st.markdown(f"<div style='color:#374151; padding:2px 0;'>• {r}</div>",
                                unsafe_allow_html=True)

            if v.get("descricao"):
                st.markdown(f"**📝 Descrição:** {v['descricao'][:300]}{'...' if len(v.get('descricao',''))>300 else ''}")

            colA, colB = st.columns([4, 1])
            origem = v.get("origem", "—")
            colA.caption(f"ID: `{v['id']}` · Criada em: {v['data_criacao']} · Origem: {origem}")
            with colB:
                if st.button("🗑️ Remover", key=f"del_{v['id']}"):
                    dados["vagas"] = [x for x in dados["vagas"] if x["id"] != v["id"]]
                    _save_data(dados)
                    st.session_state["dados"] = dados
                    st.rerun()

footer(config.APP_VERSION, config.LLM_ENGINE)
