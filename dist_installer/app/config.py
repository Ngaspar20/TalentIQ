# config.py — TalentIQ LLM Engine Configuration
# Change LLM_ENGINE to switch between providers without touching any other file.
# Options: "grok" | "openai" | "deterministic"

LLM_ENGINE = "grok"  # Options: "grok" | "openai" | "deterministic"

# API Keys — set via environment variables or replace here for local testing
# Never commit real keys to version control
import os

GROK_API_KEY = os.environ.get("GROK_API_KEY", "")
GROK_BASE_URL = "https://api.x.ai/v1"
GROK_MODEL = "grok-3"

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"

# Dev / production flag — set TALENTIQ_DEV=true to show QA dashboard
DEV_MODE = os.environ.get("TALENTIQ_DEV", "false").lower() == "true"

# Data file path — overridden by launcher.py when running as a packaged .exe
# so user data lives in %APPDATA%\TalentIQ rather than inside the read-only bundle
DATA_PATH = os.environ.get("TALENTIQ_DATA_PATH") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "jobs.json"
)

# App settings
APP_NAME = "TalentIQ"
APP_VERSION = "0.1.0-prototype"
APP_LANGUAGE = "pt-BR"

# Scoring thresholds
SCORE_ALTO = 75       # >= 75% → Alto Alinhamento
SCORE_MEDIO = 50      # >= 50% → Alinhamento Médio
                      # <  50% → Baixo Alinhamento

# CV parsing — deterministic keyword lists (PT/EN bilingual)
SKILLS_KEYWORDS = [
    # Tecnologia
    "python", "java", "javascript", "sql", "excel", "power bi", "tableau",
    "r", "machine learning", "inteligência artificial", "data science",
    "gestão de projetos", "project management", "scrum", "agile",
    # Saúde
    "saúde pública", "epidemiologia", "monitoria", "avaliação", "m&a",
    "hiv", "ats", "smaj", "sisma", "dhis2",
    # Soft skills
    "liderança", "comunicação", "trabalho em equipa", "resolução de problemas",
    "negociação", "gestão de equipa", "formação", "treinamento",
    # Línguas
    "inglês", "português", "francês", "espanhol", "english", "french",
    # Finanças / Gestão
    "contabilidade", "finanças", "orçamento", "recursos humanos", "rh",
    "recrutamento", "seleção", "marketing", "vendas", "logística",
]

EDUCATION_KEYWORDS = [
    "licenciatura", "mestrado", "doutoramento", "mba", "bacharel",
    "pós-graduação", "curso técnico", "certificação", "diploma",
    "bachelor", "master", "phd", "degree", "certificate",
    "universidade", "faculdade", "instituto", "university", "college",
]

JOB_TITLE_KEYWORDS = [
    "gestor", "gerente", "diretor", "coordenador", "analista", "técnico",
    "consultor", "especialista", "supervisor", "assistente", "oficial",
    "manager", "director", "coordinator", "analyst", "consultant",
    "specialist", "supervisor", "assistant", "officer", "engineer",
]
