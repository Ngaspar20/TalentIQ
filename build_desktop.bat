@echo off
setlocal EnableDelayedExpansion

echo ============================================================
echo   TalentIQ — Build Desktop App (.exe)
echo ============================================================
echo.

REM ── Activate conda env ────────────────────────────────────────
call conda activate ml_env 2>nul
if errorlevel 1 (
    echo [AVISO] Nao foi possivel activar ml_env — usando ambiente Python actual.
)

REM ── Install build dependencies ────────────────────────────────
echo [1/4] A instalar dependencias de build...
pip install pywebview bottle pyinstaller --quiet
if errorlevel 1 (
    echo [ERRO] Falhou a instalar dependencias. Abortando.
    pause & exit /b 1
)
echo       OK

REM ── Clean previous build ──────────────────────────────────────
echo [2/4] A limpar build anterior...
if exist dist\TalentIQ rmdir /s /q dist\TalentIQ
if exist build\launcher  rmdir /s /q build\launcher
echo       OK

REM ── Run PyInstaller ───────────────────────────────────────────
echo [3/4] A compilar com PyInstaller (pode demorar 3-5 minutos)...

pyinstaller ^
    --name "TalentIQ" ^
    --onedir ^
    --windowed ^
    --noconfirm ^
    --clean ^
    --add-data "app.py;." ^
    --add-data "config.py;." ^
    --add-data "pages;pages" ^
    --add-data "core;core" ^
    --add-data "data;data" ^
    --collect-all streamlit ^
    --collect-all altair ^
    --collect-all pydantic ^
    --collect-all pydantic_core ^
    --collect-all plotly ^
    --collect-all pandas ^
    --collect-all openpyxl ^
    --collect-all docx ^
    --collect-all pdfplumber ^
    --collect-all openai ^
    --hidden-import "streamlit.web.cli" ^
    --hidden-import "streamlit.web.bootstrap" ^
    --hidden-import "streamlit.runtime" ^
    --hidden-import "streamlit.runtime.scriptrunner" ^
    --hidden-import "streamlit.runtime.state" ^
    --hidden-import "streamlit.components.v1" ^
    --hidden-import "unicodedata" ^
    --hidden-import "pkg_resources.py2_warn" ^
    launcher.py

if errorlevel 1 (
    echo.
    echo [ERRO] PyInstaller falhou. Veja os erros acima.
    pause & exit /b 1
)

REM ── Copy qa_agent.py if not auto-collected ────────────────────
if exist qa_agent.py (
    copy /y qa_agent.py dist\TalentIQ\ >nul
)

echo       OK

REM ── Done ──────────────────────────────────────────────────────
echo [4/4] Build concluido!
echo.
echo   Pasta:       dist\TalentIQ\
echo   Executavel:  dist\TalentIQ\TalentIQ.exe
echo.
echo   NOTA: Antes de distribuir, defina a chave Grok:
echo     - Coloque um ficheiro .env em %%APPDATA%%\TalentIQ\
echo     - Ou defina a variavel de ambiente GROK_API_KEY
echo.
echo ============================================================
pause
