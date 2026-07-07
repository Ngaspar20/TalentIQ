# launcher.py — TalentIQ Desktop Launcher
# Entry point for the packaged .exe (pywebview + Streamlit in a background thread).
# Also works in development: `python launcher.py`

import os
import sys
import json
import socket
import subprocess
import time
import urllib.request
import webbrowser
import shutil
from pathlib import Path


def _find_free_port(start: int = 8501) -> int:
    for port in range(start, start + 100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    return start


def _setup_user_data() -> str:
    """
    Create the user-data directory in %APPDATA%\\TalentIQ and return the
    full path to jobs.json.  Sets TALENTIQ_DATA_PATH so config.py picks it up.
    Also loads settings.json (if present) to inject the Grok API key.
    """
    appdata = os.environ.get("APPDATA") or str(Path.home())
    talentiq_dir = Path(appdata) / "TalentIQ"
    data_dir = talentiq_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # jobs.json — user data store
    data_file = data_dir / "jobs.json"
    if not data_file.exists():
        data_file.write_text(
            json.dumps({"vagas": [], "candidatos": []}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    os.environ["TALENTIQ_DATA_PATH"] = str(data_file)

    # settings.json — optional config (API keys, etc.)
    # Format: {"GROK_API_KEY": "xai-...", "LLM_ENGINE": "grok"}
    settings_file = talentiq_dir / "settings.json"
    if not settings_file.exists():
        settings_file.write_text(
            json.dumps(
                {"GROK_API_KEY": "", "_comment": "Cole aqui a sua chave Grok xAI"},
                ensure_ascii=False, indent=2,
            ),
            encoding="utf-8",
        )
    try:
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
        for key, val in settings.items():
            if not key.startswith("_") and val:
                os.environ.setdefault(key, str(val))
    except Exception:
        pass

    return str(data_file)


def _app_dir() -> str:
    if getattr(sys, "frozen", False):
        # Running inside a PyInstaller bundle
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _start_streamlit(port: int) -> subprocess.Popen:
    """Launch Streamlit as a child process and return the Popen handle."""
    app_dir = _app_dir()

    if getattr(sys, "frozen", False):
        # When packaged: re-run the exe itself with --worker flag.
        # The worker branch (below) runs Streamlit on the main thread,
        # which is required for signal-handler registration.
        cmd = [sys.executable, "--worker", str(port)]
    else:
        # Development: run via python -m streamlit
        app_path = os.path.join(app_dir, "app.py")
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_path,
            f"--server.port={port}",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false",
            "--browser.gatherUsageStats=false",
            "--browser.serverAddress=localhost",
        ]

    return subprocess.Popen(
        cmd,
        cwd=app_dir,
        env=os.environ.copy(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _run_worker(port: int) -> None:
    """Worker mode: called when the frozen exe is relaunched with --worker <port>.
    Runs Streamlit on the main thread (required for signal handlers)."""
    app_dir = _app_dir()
    app_path = os.path.join(app_dir, "app.py")
    os.chdir(app_dir)
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)

    from streamlit.web import bootstrap  # type: ignore
    bootstrap.run(
        app_path,
        command_line="",
        args=[],
        flag_options={
            "server.port": port,
            "server.headless": True,
            "server.enableCORS": False,
            "server.enableXsrfProtection": False,
            "browser.gatherUsageStats": False,
        },
    )


def _wait_for_server(port: int, timeout: int = 30) -> bool:
    url = f"http://localhost:{port}/_stcore/health"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def _open_app_window(url: str) -> subprocess.Popen | None:
    """
    Open a browser in --app mode (no address bar, looks native).
    Tries Edge then Chrome; falls back to the default browser.
    Returns the browser Popen handle, or None if fallback was used.
    """
    candidates = [
        # Edge — built into every Windows 11 machine
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        # Chrome
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return subprocess.Popen([
                path,
                f"--app={url}",
                "--window-size=1440,900",
                "--no-first-run",
                "--no-default-browser-check",
            ])
    # Last resort: system default browser
    webbrowser.open(url)
    return None


def main() -> None:
    # Worker mode: frozen exe relaunched by the GUI launcher to run Streamlit
    if "--worker" in sys.argv:
        _setup_user_data()
        port = int(sys.argv[sys.argv.index("--worker") + 1])
        _run_worker(port)
        return

    _setup_user_data()
    port = _find_free_port(8501)
    app_url = f"http://localhost:{port}"

    print(f"[TalentIQ] A iniciar servidor na porta {port}...")
    proc = _start_streamlit(port)

    print("[TalentIQ] A aguardar servidor...")
    if not _wait_for_server(port, timeout=45):
        print("[TalentIQ] ERRO: servidor nao iniciou a tempo.")
        proc.terminate()
        return

    print(f"[TalentIQ] Servidor pronto. A abrir app em {app_url}")
    browser_proc = _open_app_window(app_url)

    try:
        # Keep running until Streamlit exits (user closed the terminal / Ctrl+C)
        proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        if browser_proc:
            try:
                browser_proc.terminate()
            except Exception:
                pass


if __name__ == "__main__":
    main()
