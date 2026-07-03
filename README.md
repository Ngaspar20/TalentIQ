# TalentIQ — Plataforma Inteligente de Recrutamento com IA

> Automatize a triagem de candidatos com Inteligência Artificial. Carregue o Termo de Referência, analise os CVs e obtenha um ranking automático em segundos.

---

## Experimente a aplicação

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talentiq-9aoi2fndbxbijqgubjozkx.streamlit.app/)

**[→ Abrir TalentIQ](https://talentiq-9aoi2fndbxbijqgubjozkx.streamlit.app/)**

---

## O que o TalentIQ faz

| Funcionalidade | Descrição |
|---|---|
| **Criar Vaga** | Carregue um Termo de Referência (PDF/DOCX) — a IA extrai título, competências e requisitos automaticamente |
| **Carregar CV** | Analise CVs individuais — extracção automática de competências, experiência e formação |
| **Pontuação Fit** | Ranking 0–100 de todos os candidatos por alinhamento com a vaga |
| **Pipeline** | Funil visual de recrutamento — mova candidatos entre etapas (Triagem → Entrevista → Proposta → Contratado) |
| **Scoring Geral** | Vista consolidada + exportação Excel e relatório Word |

---

## Como testar — guia passo a passo

A pasta `documentos_teste/` contém ficheiros de exemplo prontos a usar.

### Passo 1 — Criar uma Vaga

1. Clique em **Criar Vaga** no menu lateral
2. Clique em **Browse files** e carregue um dos ToRs de exemplo:
   - `ToR_Analista_Dados_Senior.docx` — Analista de Dados Sénior, Programa de Saúde Pública
   - `ToR_Especialista_RH.docx` — Especialista em Recursos Humanos
3. A IA extrai automaticamente: título, competências, nível de formação, anos de experiência
4. Reveja os campos e clique **Guardar Vaga**

### Passo 2 — Carregar CVs

1. Clique em **Carregar CV** no menu lateral
2. Seleccione a vaga criada no passo anterior
3. Carregue um CV de cada vez — use os 4 exemplos disponíveis:
   - `CV_Ana_Macie_Analista_Senior.docx` — perfil sénior, forte match com a vaga de dados
   - `CV_Carlos_Sitoe_Gestor_TI.docx` — perfil de TI, match parcial
   - `CV_Joao_Nhantumbo_RH_Senior.docx` — especialista em RH, bom match para a vaga de RH
   - `CV_Fatima_Cumbe_Professora.docx` — perfil de educação, match baixo (cenário de rejeição)
4. Após cada upload, clique **Guardar Candidato**

### Passo 3 — Ver o Ranking

1. Clique em **Pontuação Fit**
2. Seleccione a vaga — a IA calcula o score de cada candidato (0–100) com base no alinhamento de competências
3. Veja quais competências fazem match e quais são lacunas

### Passo 4 — Gerir o Pipeline

1. Clique em **Pipeline**
2. Mova os candidatos entre etapas: arraste ou use o selector de etapa
3. Acompanhe o funil: Candidatura → Triagem → Entrevista → Proposta → Contratado

### Passo 5 — Exportar Resultados

1. Clique em **Scoring Geral**
2. Exporte para **Excel** (tabela completa com scores) ou **Word** (relatório formatado)
3. Partilhe com a equipa de decisão

---

## Resultados esperados nos ficheiros de teste

| Candidato | Vaga | Score esperado | Motivo |
|---|---|---|---|
| Ana Macie | Analista de Dados Sénior | 75–90% | Python, SQL, Power BI, saúde pública |
| Carlos Sitoe | Analista de Dados Sénior | 50–65% | TI sólida, falta epidemiologia |
| Joao Nhantumbo | Especialista RH | 70–85% | RH, recrutamento, gestão de pessoas |
| Fatima Cumbe | Analista de Dados Sénior | 20–35% | Perfil de educação, poucas competências técnicas |

---

## Motor de IA

O TalentIQ suporta três motores intercambiáveis — configurável em `config.py`:

| Motor | Descrição |
|---|---|
| `deterministic` | Algoritmo de matching por palavras-chave (sem API, gratuito, funciona offline) |
| `openai` | GPT-4o via OpenAI API (requer chave API) |
| `grok` | Grok via xAI API (requer chave API) |

Por defeito usa o motor **determinístico** — não requer nenhuma chave API.

---

## Deploy no Streamlit Cloud (gratuito)

1. Aceda a [share.streamlit.io](https://share.streamlit.io)
2. Clique em **New app**
3. Seleccione o repositório `Ngaspar20/TalentIQ`
4. Main file path: `app.py`
5. Clique **Deploy** — o URL fica disponível em ~2 minutos

---

## Executar localmente

```bash
# Requisitos: Python 3.9+, pip
pip install -r requirements.txt
streamlit run app.py
```

---

## Stack técnico

- **Frontend:** Streamlit + HTML/CSS customizado (dark theme)
- **Backend:** Python 3.9+
- **Parsing:** python-docx, PyMuPDF (PDFs)
- **LLM:** OpenAI / xAI Grok / motor determinístico (intercambiável)
- **Export:** openpyxl (Excel), python-docx (Word)
- **QA:** Módulo interno de validação de dados

---

## Mercados-alvo

Portugal · Brasil · Angola · Moçambique

---

*TalentIQ v1.0 · Desenvolvido por Nuno Gaspar · 2026*
