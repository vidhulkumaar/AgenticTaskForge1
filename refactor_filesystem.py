import os
import re

with open('execution/filesystem.py', 'r', encoding='utf-8') as f:
    content = f.read()

imports = """import os
import re
import time
import subprocess
import shutil
import win32gui
from pywinauto import Application
from agent_context import AgentContext
from utils import get_known_folder_path, wait_for_window
from config import Config
"""
content = re.sub(
    r'^import time\nimport win32gui\nfrom pywinauto import Application\nfrom agent_context import AgentContext\n',
    imports,
    content
)

# Fix action_open_folder missing context and sleep loop
content = re.sub(
    r'def action_open_folder\(folder: str\) -> str:',
    r'def action_open_folder(context: AgentContext, folder: str) -> str:',
    content
)

content = re.sub(
    r'    subprocess\.Popen\(\["explorer\.exe", folder_path\]\)\n    for _ in range\(10\):\n        time\.sleep\(1\)\n        try:\n            app = Application\(backend="uia"\)\.connect\(title_re=f"\.\*\{folder_display\}\.\*"\)\n            context\.explorer_window = app\.top_window\(\)\n            return f"Opened File Explorer at: \{folder_path\}"\n        except Exception:\n            continue\n    return f"Opened File Explorer at \{folder_path\} \(could not connect to UIA\)\."',
    r'    subprocess.Popen(["explorer.exe", folder_path])\n    hwnd = wait_for_window(f".*{folder_display}.*", timeout=Config.APP_START_TIMEOUT)\n    if hwnd:\n        try:\n            app = Application(backend="uia").connect(handle=hwnd)\n            context.explorer_window = app.top_window()\n            return f"Opened File Explorer at: {folder_path}"\n        except Exception:\n            pass\n    return f"Opened File Explorer at {folder_path} (could not connect to UIA)."',
    content
)

# Fix _get_file_list_control missing context arg
content = re.sub(
    r'def _get_file_list_control\(\):',
    r'def _get_file_list_control(context: AgentContext):',
    content
)
content = re.sub(
    r'    file_list_control = _get_file_list_control\(\)',
    r'    file_list_control = _get_file_list_control(context)',
    content
)


with open('execution/filesystem.py', 'w', encoding='utf-8') as f:
    f.write(content)
