import os
import shutil
import winreg

def _load_env():
    """Simple .env parser to avoid external dependencies like python-dotenv."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())

_load_env()

def _get_registry_app_path(exe_name: str) -> str:
    """Dynamically discover executable paths using Windows Registry."""
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\' + exe_name)
        path, _ = winreg.QueryValueEx(key, '')
        return path
    except Exception:
        pass
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\\' + exe_name)
        path, _ = winreg.QueryValueEx(key, '')
        return path
    except Exception:
        pass
    return ""

def get_app_path(exe_name: str, fallback: str = "") -> str:
    """Find application path via registry, PATH, or fallback."""
    path = _get_registry_app_path(exe_name)
    if path and os.path.exists(path):
        return path
    which_path = shutil.which(exe_name)
    if which_path:
        return which_path
    if fallback and os.path.exists(fallback):
        return fallback
    return exe_name

class Config:
    # ── LLM Settings ────────────────────────────────────────────────────────
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    
    # ── Derived Endpoints ───────────────────────────────────────────────────
    OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
    OLLAMA_CHAT_URL     = f"{OLLAMA_BASE_URL}/api/chat"
    OLLAMA_TAGS_URL     = f"{OLLAMA_BASE_URL}/api/tags"
    OLLAMA_EMBED_URL    = f"{OLLAMA_BASE_URL}/api/embeddings"
    
    # ── Timeouts & Retries ──────────────────────────────────────────────────
    LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "120"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "10"))
    LLM_RETRIES = int(os.getenv("LLM_RETRIES", "2"))
    LLM_RETRIES = int(os.getenv("LLM_RETRIES", "2"))
    
    # ── Paths & Executables ─────────────────────────────────────────────────
    @staticmethod
    def get_tesseract_path() -> str:
        tess_env = os.getenv("TESSERACT_CMD")
        if tess_env and os.path.exists(tess_env):
            return tess_env
        fallback_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
        ]
        for path in fallback_paths:
            if os.path.exists(path):
                return path
        return "tesseract"

    # App specific paths that can't reliably be found in PATH or Registry on all systems
    WHATSAPP_EXE = os.path.join(os.getenv("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe")
    SPOTIFY_EXE = os.path.join(os.getenv("APPDATA", ""), "Spotify", "Spotify.exe")
    DISCORD_EXE = os.path.join(os.getenv("LOCALAPPDATA", ""), "Discord", "Update.exe")
    TEAMS_EXE = os.path.join(os.getenv("LOCALAPPDATA", ""), "Microsoft", "Teams", "current", "Teams.exe")
    ZOOM_EXE = os.path.join(os.getenv("APPDATA", ""), "Zoom", "bin", "Zoom.exe")
