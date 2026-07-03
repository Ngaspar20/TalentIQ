# core/scorer.py — Candidate fit scoring engine for TalentIQ

import json
import logging
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from core.llm import get_llm_response

logger = logging.getLogger(__name__)


def calcular_fit(candidato: Dict[str, Any], vaga: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate fit score between a candidate and a job.
    Returns score (0-100), breakdown, and explanation.
    """
    if config.LLM_ENGINE != "deterministic":
        resultado = _score_with_llm(candidato, vaga)
        if resultado:
            resultado["metodo"] = f"LLM ({config.LLM_ENGINE})"
            return resultado

    resultado = _score_deterministic(candidato, vaga)
    resultado["metodo"] = "Determinístico"
    return resultado


def _score_deterministic(candidato: Dict, vaga: Dict) -> Dict[str, Any]:
    """
    Deterministic scoring across 3 dimensions:
    - Competências (50%)
    - Experiência em anos (30%)
    - Formação (20%)
    """
    pontos = {}
    explicacao = []

    # --- Competências (50 points) ---
    competencias_vaga = [c.lower() for c in vaga.get("competencias_requeridas", [])]
    competencias_candidato = [c.lower() for c in candidato.get("competencias", [])]

    if competencias_vaga:
        matches = [c for c in competencias_vaga if c in competencias_candidato]
        score_comp = round((len(matches) / len(competencias_vaga)) * 50)
        pontos["competencias"] = score_comp
        explicacao.append(
            f"✅ Competências: {len(matches)}/{len(competencias_vaga)} correspondências "
            f"({score_comp}/50 pts)"
        )
        gaps = [c for c in competencias_vaga if c not in competencias_candidato]
        if gaps:
            explicacao.append(f"⚠️ Competências em falta: {', '.join(gaps)}")
    else:
        pontos["competencias"] = 25
        explicacao.append("ℹ️ Nenhuma competência específica definida para a vaga (25/50 pts)")

    # --- Experiência (30 points) ---
    anos_requeridos = vaga.get("anos_experiencia_min", 0)
    anos_candidato = candidato.get("experiencia_anos", 0)

    if anos_requeridos == 0:
        score_exp = 30
        explicacao.append("ℹ️ Experiência mínima não definida (30/30 pts)")
    elif anos_candidato >= anos_requeridos:
        score_exp = 30
        explicacao.append(
            f"✅ Experiência: {anos_candidato} anos (mínimo: {anos_requeridos}) (30/30 pts)"
        )
    else:
        ratio = anos_candidato / anos_requeridos
        score_exp = round(ratio * 30)
        explicacao.append(
            f"⚠️ Experiência insuficiente: {anos_candidato} anos (mínimo: {anos_requeridos}) "
            f"({score_exp}/30 pts)"
        )
    pontos["experiencia"] = score_exp

    # --- Formação (20 points) ---
    nivel_requerido = vaga.get("nivel_formacao", "").lower()
    formacao_candidato = " ".join(candidato.get("formacao", [])).lower()

    nivel_map = {
        "licenciatura": ["licenciatura", "bacharel", "bachelor"],
        "mestrado": ["mestrado", "master", "mba"],
        "doutoramento": ["doutoramento", "phd", "doutor"],
        "curso técnico": ["técnico", "certificate", "certificação"],
    }

    score_form = 0
    if not nivel_requerido:
        score_form = 10
        explicacao.append("ℹ️ Formação mínima não definida (10/20 pts)")
    else:
        keywords = nivel_map.get(nivel_requerido, [nivel_requerido])
        if any(kw in formacao_candidato for kw in keywords):
            score_form = 20
            explicacao.append(f"✅ Formação adequada: {nivel_requerido} (20/20 pts)")
        else:
            score_form = 5
            explicacao.append(
                f"⚠️ Formação não confirmada para: {nivel_requerido} (5/20 pts)"
            )
    pontos["formacao"] = score_form

    # --- Total ---
    total = pontos["competencias"] + pontos["experiencia"] + pontos["formacao"]

    # Classify
    if total >= config.SCORE_ALTO:
        nivel = "Alto Alinhamento"
        cor = "green"
    elif total >= config.SCORE_MEDIO:
        nivel = "Alinhamento Médio"
        cor = "orange"
    else:
        nivel = "Baixo Alinhamento"
        cor = "red"

    return {
        "score_total": total,
        "pontuacao_detalhada": pontos,
        "nivel_alinhamento": nivel,
        "cor": cor,
        "explicacao": explicacao,
    }


def _score_with_llm(candidato: Dict, vaga: Dict) -> Dict[str, Any]:
    system = (
        "Você é um especialista em recrutamento e seleção. "
        "Avalie o alinhamento entre candidato e vaga. "
        "Responda APENAS com JSON válido."
    )
    prompt = f"""
Avalie o alinhamento entre este candidato e esta vaga. Responda em JSON:
{{
  "score_total": número de 0 a 100,
  "pontuacao_detalhada": {{
    "competencias": número de 0 a 50,
    "experiencia": número de 0 a 30,
    "formacao": número de 0 a 20
  }},
  "nivel_alinhamento": "Alto Alinhamento" | "Alinhamento Médio" | "Baixo Alinhamento",
  "cor": "green" | "orange" | "red",
  "explicacao": ["lista de frases explicando os pontos fortes e lacunas"]
}}

CANDIDATO:
{json.dumps(candidato, ensure_ascii=False, indent=2)}

VAGA:
{json.dumps(vaga, ensure_ascii=False, indent=2)}
"""
    try:
        response = get_llm_response(prompt, system)
        if response:
            clean = response.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
    except Exception as e:
        logger.warning(f"LLM scoring falhou, usando fallback: {e}")
    return {}
