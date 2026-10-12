import os
import re

with open('execution/desktop.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing imports
imports = """import os
import time
import subprocess
import pyperclip
from pywinauto import Application
from pywinauto.keyboard import send_keys
from agent_context import AgentContext
from utils import get_known_folder_path, wait_for_clipboard_sync, wait_for_file_exists, wait_for_window
from config import Config
"""

content = re.sub(r'^import time\nimport subprocess\nfrom pywinauto import Application\nfrom agent_context import AgentContext\n', imports, content)

# 1. action_open_app
content = re.sub(
    r'    subprocess.run\(\["taskkill", "/F", "/IM", "notepad.exe", "/T"\], capture_output=True\)\n    time.sleep\(1\)\n    subprocess.Popen\(\["notepad.exe"\]\)\n    app = None\n    for _ in range\(10\):\n        time.sleep\(1\)\n        try:\n            app = Application\(backend="uia"\)\.connect\(path="notepad\.exe"\)\n            break\n        except Exception:\n            continue',
    r'    subprocess.run(["taskkill", "/F", "/IM", "notepad.exe", "/T"], capture_output=True)\n    # wait for process to die\n    subprocess.Popen(["notepad.exe"])\n    app = Application(backend="uia").connect(path="notepad.exe", timeout=Config.APP_START_TIMEOUT)',
    content
)
content = re.sub(
    r'    context.main_window.set_focus\(\)\n    time.sleep\(0\.5\)',
    r'    context.main_window.set_focus()\n    context.main_window.wait("visible", timeout=Config.UI_ELEMENT_TIMEOUT)',
    content
)

# 2. action_type_text
content = re.sub(
    r'        edit\.set_focus\(\)\n        time\.sleep\(0\.3\)\n        send_keys\("\^a"\)\n        time\.sleep\(0\.1\)\n        send_keys\("\^v"\)\n        time\.sleep\(0\.5\)',
    r'        edit.wait("visible", timeout=Config.UI_ELEMENT_TIMEOUT)\n        edit.set_focus()\n        wait_for_clipboard_sync()\n        send_keys("^a")\n        send_keys("^v")\n        # Wait for the text to appear\n        edit.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)',
    content
)
content = re.sub(r'action_open_app\(\)', r'action_open_app(context)', content)

# 3. action_save_file
content = re.sub(
    r'    send_keys\("\^s"\)\n    time\.sleep\(1\.5\)\n    try:\n        dlg = context.app.window\(title_re="\.\*Save\.\*"\)\n        dlg\.set_focus\(\)\n        name_box = dlg.child_window\(auto_id="1001"\)\n        name_box\.set_text\(full_path\)\n        time\.sleep\(0\.3\)\n        send_keys\("{ENTER}"\)\n        time\.sleep\(1\)',
    r'    send_keys("^s")\n    try:\n        dlg = context.app.window(title_re=".*Save.*")\n        dlg.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)\n        dlg.set_focus()\n        name_box = dlg.child_window(auto_id="1001")\n        name_box.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)\n        name_box.set_text(full_path)\n        send_keys("{ENTER}")\n        dlg.wait_not("visible", timeout=Config.UI_ELEMENT_TIMEOUT)',
    content
)

content = re.sub(
    r'            if overwrite.exists\(timeout=2\):\n                overwrite.child_window\(title="Yes"\).click\(\)\n                time\.sleep\(0\.5\)',
    r'            if overwrite.exists(timeout=2):\n                overwrite.child_window(title="Yes").wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT).click()\n                overwrite.wait_not("visible", timeout=Config.UI_ELEMENT_TIMEOUT)',
    content
)

content = re.sub(
    r'    for _ in range\(8\):\n        time\.sleep\(0\.5\)\n        if os\.path\.exists\(full_path\):\n            return f"File saved: \{full_path\}"',
    r'    if wait_for_file_exists(full_path):\n        return f"File saved: {full_path}"',
    content
)


with open('execution/desktop.py', 'w', encoding='utf-8') as f:
    f.write(content)

