from typing import Optional, List, Dict, Any, Tuple

def wait_for_window(title_re: str, timeout: float = None) -> int:
    """Wait for a window matching the regex to appear. Returns HWND."""
    if timeout is None:
        timeout = Config.APP_START_TIMEOUT
    end_time = time.time() + timeout
    while time.time() < end_time:
        hwnd = 0
        def callback(h, extra):
            nonlocal hwnd
            if win32gui.IsWindowVisible(h):
                title = win32gui.GetWindowText(h)
                if re.search(title_re, title):
                    hwnd = h
        win32gui.EnumWindows(callback, None)
        if hwnd:
            return hwnd
        time.sleep(0.1)
    return 0

def wait_for_file_exists(path: str, timeout: float = None) -> bool:
    """Wait until a file exists on disk."""
    if timeout is None:
        timeout = Config.FILE_OPERATION_TIMEOUT
    end_time = time.time() + timeout
    while time.time() < end_time:
        if os.path.exists(path):
            return True
        time.sleep(0.1)
    return False

def wait_for_clipboard_sync(timeout: float = None) -> str:
    """Wait for clipboard to become available and not empty, returns content."""
    if timeout is None:
        timeout = Config.CLIPBOARD_TIMEOUT
    import pyperclip
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            val = pyperclip.paste()
            if val is not None:
                return val
        except Exception:
            pass
        time.sleep(0.05)
    return ""

from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ActionResult:
    success: bool
    message: str = ""
    error: Optional[str] = None
    data: Optional[Any] = None

    def __str__(self):
        if self.success:
            return self.message if self.message else "Success."
        return f"ERROR: {self.error or self.message}"

def wait_for_window(title_re: str, timeout: float = None) -> int:
    """Wait for a window matching the regex to appear. Returns HWND."""
    if timeout is None:
        timeout = Config.APP_START_TIMEOUT
    end_time = time.time() + timeout
    while time.time() < end_time:
        hwnd = 0
        def callback(h, extra):
            nonlocal hwnd
            if win32gui.IsWindowVisible(h):
                title = win32gui.GetWindowText(h)
                if re.search(title_re, title):
                    hwnd = h
        win32gui.EnumWindows(callback, None)
        if hwnd:
            return hwnd
        time.sleep(0.1)
    return 0

def wait_for_file_exists(path: str, timeout: float = None) -> bool:
    """Wait until a file exists on disk."""
    if timeout is None:
        timeout = Config.FILE_OPERATION_TIMEOUT
    end_time = time.time() + timeout
    while time.time() < end_time:
        if os.path.exists(path):
            return True
        time.sleep(0.1)
    return False

def wait_for_clipboard_sync(timeout: float = None) -> str:
    """Wait for clipboard to become available and not empty, returns content."""
    if timeout is None:
        timeout = Config.CLIPBOARD_TIMEOUT
    import pyperclip
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            val = pyperclip.paste()
            if val is not None:
                return val
        except Exception:
            pass
        time.sleep(0.05)
    return ""

from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ActionResult:
    success: bool
    message: str = ""
    error: Optional[str] = None
    data: Optional[Any] = None

    def __str__(self):
        if self.success:
            return self.message if self.message else "Success."
        return f"ERROR: {self.error or self.message}"
