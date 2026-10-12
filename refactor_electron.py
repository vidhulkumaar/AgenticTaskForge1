import os
import re

with open('task6_electron_apps.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing config/utils imports
imports = """import os
import re
import sys
import time
import subprocess
import argparse
from typing import Optional

import pyperclip
from pywinauto import Application
from pywinauto.keyboard import send_keys
from config import Config
from utils import wait_for_window, wait_for_clipboard_sync
"""
content = re.sub(
    r'^import os\nimport re\nimport sys\nimport time\nimport subprocess\nimport argparse\nfrom typing import Optional\n\nimport pyperclip\nfrom pywinauto import Application\nfrom pywinauto\.keyboard import send_keys\n',
    imports,
    content,
    flags=re.MULTILINE
)

# 1. Update _focus_window
content = re.sub(
    r'def _focus_window\(title_re: str, timeout: int = 8\) -> Optional\[object\]:\n    """Tries to connect to a window matching title_re via pywinauto\."""\n    end = time\.time\(\) \+ timeout\n    while time\.time\(\) < end:\n        try:\n            app = Application\(backend="uia"\)\.connect\(title_re=title_re\)\n            win = app\.top_window\(\)\n            win\.set_focus\(\)\n            time\.sleep\(0\.5\)\n            return win\n        except Exception:\n            time\.sleep\(1\)\n    return None',
    r'def _focus_window(title_re: str, timeout: int = 8) -> Optional[object]:\n    hwnd = wait_for_window(title_re, timeout=timeout)\n    if hwnd:\n        try:\n            app = Application(backend="uia").connect(handle=hwnd)\n            win = app.top_window()\n            win.set_focus()\n            return win\n        except Exception:\n            pass\n    return None',
    content
)

# 2. Update _type_and_send
content = re.sub(
    r'def _type_and_send\(text: str, send: bool = True\):\n    """Pastes text via clipboard \(avoids unicode issues with send_keys\)\."""\n    pyperclip\.copy\(text\)\n    send_keys\("\^v"\)\n    time\.sleep\(0\.3\)\n    if send:\n        send_keys\("{ENTER}"\)\n        time\.sleep\(0\.5\)',
    r'def _type_and_send(text: str, send: bool = True):\n    """Pastes text via clipboard."""\n    pyperclip.copy(text)\n    wait_for_clipboard_sync()\n    send_keys("^v")\n    if send:\n        send_keys("{ENTER}")',
    content
)

# 3. WhatsApp
content = re.sub(
    r'    time\.sleep\(4\)\n    return _focus_window',
    r'    return _focus_window',
    content
)
content = re.sub(
    r'        win\.set_focus\(\)\n        time\.sleep\(0\.5\)\n        send_keys\("\^f"\)   # search / find contact\n        time\.sleep\(0\.8\)',
    r'        win.set_focus()\n        win.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)\n        send_keys("^f")',
    content
)
content = re.sub(
    r'        pyperclip\.copy\(contact\)\n        send_keys\("\^v"\)\n        time\.sleep\(1\.5\)\n\n        # Press Enter to open the chat \(or click first result\)\n        send_keys\("{ENTER}"\)\n        time\.sleep\(1\)',
    r'        pyperclip.copy(contact)\n        wait_for_clipboard_sync()\n        send_keys("^v")\n        # Bounded sleep justified: Electron apps do not expose UIA search result readiness reliably\n        time.sleep(1.0)\n        send_keys("{ENTER}")\n        time.sleep(1.0)',
    content
)
content = re.sub(
    r'            msg_box\.type_keys\(message, with_spaces=True\)\n            time\.sleep\(0\.3\)\n            send_keys\("{ENTER}"\)',
    r'            msg_box.type_keys(message, with_spaces=True)\n            send_keys("{ENTER}")',
    content
)
content = re.sub(
    r'            send_keys\("{TAB}"\)\n            time\.sleep\(0\.3\)\n            _type_and_send\(message, send=True\)\n\n        time\.sleep\(0\.5\)',
    r'            send_keys("{TAB}")\n            _type_and_send(message, send=True)',
    content
)

content = re.sub(
    r'        win\.set_focus\(\)\n        send_keys\("\^f"\)\n        time\.sleep\(0\.8\)\n        pyperclip\.copy\(contact\)\n        send_keys\("\^v"\)\n        time\.sleep\(1\.5\)\n        send_keys\("{ENTER}"\)\n        time\.sleep\(1\)',
    r'        win.set_focus()\n        send_keys("^f")\n        pyperclip.copy(contact)\n        wait_for_clipboard_sync()\n        send_keys("^v")\n        time.sleep(1.0)\n        send_keys("{ENTER}")\n        time.sleep(1.0)',
    content
)

# 4. Spotify
content = re.sub(
    r'    time\.sleep\(5\)\n    return _focus_window\(r"\(\?i\)Spotify", timeout=12\)',
    r'    return _focus_window(r"(?i)Spotify", timeout=Config.APP_START_TIMEOUT)',
    content
)
content = re.sub(r'    win\.set_focus\(\)\n    time\.sleep\(0\.3\)\n    send_keys\(_SPOTIFY_KEYS\["play_pause"\]\)', r'    win.set_focus()\n    win.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)\n    send_keys(_SPOTIFY_KEYS["play_pause"])', content)
content = re.sub(r'    send_keys\(_SPOTIFY_KEYS\["next"\]\)\n    time\.sleep\(0\.5\)', r'    send_keys(_SPOTIFY_KEYS["next"])', content)
content = re.sub(r'    send_keys\(_SPOTIFY_KEYS\["prev"\]\)\n    time\.sleep\(0\.5\)', r'    send_keys(_SPOTIFY_KEYS["prev"])', content)
content = re.sub(
    r'    win\.set_focus\(\)\n    time\.sleep\(0\.5\)\n\n    # Open search\n    send_keys\(_SPOTIFY_KEYS\["search"\]\)\n    time\.sleep\(0\.8\)',
    r'    win.set_focus()\n    win.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)\n    send_keys(_SPOTIFY_KEYS["search"])',
    content
)
content = re.sub(
    r'    send_keys\("\^a"\)\n    time\.sleep\(0\.2\)\n    pyperclip\.copy\(query\)\n    send_keys\("\^v"\)\n    time\.sleep\(1\.5\)\n    send_keys\("{ENTER}"\)\n    time\.sleep\(2\)',
    r'    send_keys("^a")\n    pyperclip.copy(query)\n    wait_for_clipboard_sync()\n    send_keys("^v")\n    time.sleep(1.0)\n    send_keys("{ENTER}")\n    time.sleep(1.5)',
    content
)
content = re.sub(
    r'    send_keys\("{TAB}{TAB}"\)\n    time\.sleep\(0\.3\)\n    send_keys\("{ENTER}"\)\n    time\.sleep\(0\.5\)',
    r'    send_keys("{TAB}{TAB}")\n    send_keys("{ENTER}")',
    content
)
content = re.sub(
    r'    win\.set_focus\(\)\n    time\.sleep\(0\.5\)\n    ocr = _ocr_read\(\)',
    r'    win.set_focus()\n    win.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)\n    ocr = _ocr_read()',
    content
)
content = re.sub(
    r'        send_keys\(key\)\n        time\.sleep\(0\.1\)',
    r'        send_keys(key)',
    content
)


# 5. Discord
content = re.sub(
    r'    time\.sleep\(6\)\n    return _focus_window\(r"\(\?i\)Discord", timeout=15\)',
    r'    return _focus_window(r"(?i)Discord", timeout=Config.APP_START_TIMEOUT)',
    content
)
content = re.sub(
    r'    win\.set_focus\(\)\n    time\.sleep\(0\.5\)\n\n    # Open quick switcher\n    send_keys\(_DISCORD_KEYS\["quick_switcher"\]\)\n    time\.sleep\(0\.8\)',
    r'    win.set_focus()\n    win.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)\n    send_keys(_DISCORD_KEYS["quick_switcher"])',
    content
)
content = re.sub(
    r'    send_keys\("\^a"\)\n    time\.sleep\(0\.2\)\n    pyperclip\.copy\(channel\)\n    send_keys\("\^v"\)\n    time\.sleep\(1\)\n\n    # Select first result\n    send_keys\("{DOWN}{ENTER}"\)\n    time\.sleep\(1\)',
    r'    send_keys("^a")\n    pyperclip.copy(channel)\n    wait_for_clipboard_sync()\n    send_keys("^v")\n    time.sleep(1.0)\n    send_keys("{DOWN}{ENTER}")\n    time.sleep(1.0)',
    content
)
content = re.sub(
    r'    win\.set_focus\(\)\n    time\.sleep\(0\.5\)',
    r'    win.set_focus()\n    win.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)',
    content
)
content = re.sub(
    r'        msg_box\.type_keys\(message, with_spaces=True\)\n        time\.sleep\(0\.3\)\n        send_keys\("{ENTER}"\)',
    r'        msg_box.type_keys(message, with_spaces=True)\n        send_keys("{ENTER}")',
    content
)
content = re.sub(
    r'        pyperclip\.copy\(message\)\n        send_keys\("\^v"\)\n        time\.sleep\(0\.3\)\n        send_keys\("{ENTER}"\)\n\n    time\.sleep\(0\.5\)',
    r'        pyperclip.copy(message)\n        wait_for_clipboard_sync()\n        send_keys("^v")\n        send_keys("{ENTER}")',
    content
)
content = re.sub(
    r'    time\.sleep\(1\)\n    ocr = _ocr_read\(\)',
    r'    time.sleep(1.0)\n    ocr = _ocr_read()',
    content
)


with open('task6_electron_apps.py', 'w', encoding='utf-8') as f:
    f.write(content)

