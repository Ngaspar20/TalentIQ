import html as _html
import json
import os
import tempfile

MAX_UPLOAD_MB = 10
_ALLOWED_EXTENSIONS = {".pdf", ".docx"}
_MAGIC_BYTES = {
    b"%PDF": ".pdf",
    b"PK\x03\x04": ".docx",
}


def esc(value) -> str:
    """Escape HTML special characters to prevent XSS injection."""
    if value is None:
        return ""
    return _html.escape(str(value))


def validate_upload(uploaded_file, max_mb: int = MAX_UPLOAD_MB) -> tuple:
    """
    Check file size and magic bytes.
    Returns (ok: bool, error_message: str).
    """
    ext = os.path.splitext(uploaded_file.name.lower())[1]
    if ext not in _ALLOWED_EXTENSIONS:
        return False, f"Tipo de ficheiro não suportado: {ext}. Apenas PDF e DOCX."

    size = getattr(uploaded_file, "size", None)
    if size is None:
        data = uploaded_file.read()
        uploaded_file.seek(0)
    else:
        data = None

    file_size = size if size is not None else len(data)
    if file_size > max_mb * 1024 * 1024:
        mb = file_size // (1024 * 1024)
        return False, f"Ficheiro demasiado grande ({mb} MB). Máximo permitido: {max_mb} MB."

    if data is None:
        header = uploaded_file.read(8)
        uploaded_file.seek(0)
    else:
        header = data[:8]

    detected = next((ext_ for magic, ext_ in _MAGIC_BYTES.items() if header.startswith(magic)), None)
    if detected and detected != ext:
        return False, "O conteúdo do ficheiro não corresponde à extensão declarada."

    return True, ""


def atomic_save(path: str, data: dict) -> None:
    """Write JSON atomically: write to temp file then rename to target."""
    dir_path = os.path.dirname(path)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=dir_path, delete=False, suffix=".tmp"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        tmp_path = f.name
    os.replace(tmp_path, path)
