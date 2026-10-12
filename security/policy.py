import os
import urllib.parse
from utils import get_known_folder_path
from typing import Tuple

def safe_path_join(folder: str, filename: str) -> str:
    """
    Safely resolves a path and ensures it does not escape the intended folder.
    Raises ValueError if path traversal is detected.
    """
    # Reject raw absolute paths in filename
    if os.path.isabs(filename) or filename.startswith("\\") or filename.startswith("/"):
        raise ValueError("Absolute paths in filenames are not permitted by security policy.")

    # 1. Resolve base directory
    known = {k: get_known_folder_path(k) for k in ["downloads", "desktop", "documents"]}
    
    # If folder matches a known keyword, use it.
    if folder.lower() in known:
        base_dir = known[folder.lower()]
    else:
        # Prevent absolute paths or C:\ as arbitrary base directories unless they are known
        # For security, we force it to Downloads if it's not a known directory.
        base_dir = known.get("downloads")
        
    base_dir = os.path.abspath(base_dir)
    
    # 2. Resolve target file
    target_path = os.path.abspath(os.path.join(base_dir, filename))
    
    # 3. Check containment
    if not target_path.startswith(base_dir):
        raise ValueError(f"Path traversal detected. Target path escapes safe directory: {base_dir}")
        
    return target_path


def is_safe_url(url: str) -> Tuple[bool, str]:
    """
    Validates URL scheme to prevent arbitrary code execution (javascript:)
    or local file reading (file:).
    Returns (is_safe, error_reason)
    """
    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme.lower()
    
    if not scheme:
        # Could be "google.com", normalize_url usually fixes this but let's be safe
        return True, ""
        
    if scheme not in ("http", "https"):
        return False, f"URL scheme '{scheme}' is not allowed by security policy."
        
    if parsed.hostname:
        host = parsed.hostname.lower()
        if host in ("localhost", "127.0.0.1", "::1"):
            # Depending on use case, this might be forbidden. We'll allow it for local testing if needed,
            # but generally SSRF is a risk. We'll permit localhost for now unless requested otherwise.
            pass
            
    return True, ""


def is_safe_executable(executable: str) -> bool:
    """
    Ensures that an application name provided by LLM resolves to a known, 
    safe application or a simple alphanumeric string, preventing injection of 
    shell metacharacters (e.g., `calc && del *`).
    """
    # Only allow alphanumeric and basic separators
    import re
    if not re.match(r"^[a-zA-Z0-9_\-\.\ ]+$", executable):
        return False
    return True
