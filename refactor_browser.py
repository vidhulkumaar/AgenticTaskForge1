import os
import re

with open('execution/browser.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add missing imports
imports = """import os
import time
import re
import subprocess
import webbrowser
import requests
import pyperclip
from pywinauto.keyboard import send_keys
from agent_context import AgentContext
from utils import normalize_url, get_known_folder_path, wait_for_clipboard_sync
from config import Config
"""
content = re.sub(
    r'^import os\nimport time\nimport re\nimport subprocess\nimport webbrowser\nimport requests\nfrom agent_context import AgentContext\nfrom utils import normalize_url, get_known_folder_path\n',
    imports,
    content
)

# Fix action_browser_go_back
content = re.sub(
    r'    context\.page\.go_back\(\)\n    time\.sleep\(1\)',
    r'    context.page.go_back(wait_until="domcontentloaded", timeout=Config.BROWSER_TIMEOUT * 1000)',
    content
)

# Fix action_browser_go_forward
content = re.sub(
    r'    context\.page\.go_forward\(\)\n    time\.sleep\(1\)',
    r'    context.page.go_forward(wait_until="domcontentloaded", timeout=Config.BROWSER_TIMEOUT * 1000)',
    content
)

# Fix action_fill_form sleeps
content = re.sub(
    r'                loc\.first\.fill\(value\)\n                time\.sleep\(0\.4\)\n                if submit:\n                    loc\.first\.press\("Enter"\)\n                    time\.sleep\(1\.5\)',
    r'                loc.first.fill(value)\n                if submit:\n                    loc.first.press("Enter")\n                    context.page.wait_for_load_state("domcontentloaded", timeout=Config.BROWSER_TIMEOUT * 1000)',
    content
)
content = re.sub(
    r'    pyperclip\.copy\(value\)\n    time\.sleep\(0\.3\)\n    send_keys\("\^v"\)\n    if submit:\n        send_keys\("{ENTER}"\)\n        time\.sleep\(1\)',
    r'    pyperclip.copy(value)\n    wait_for_clipboard_sync()\n    send_keys("^v")\n    if submit:\n        send_keys("{ENTER}")',
    content
)

# Fix action_click_browser_element missing context arg and sleeps
content = re.sub(
    r'def action_click_browser_element\(selector: str\) -> str:',
    r'def action_click_browser_element(context: AgentContext, selector: str) -> str:',
    content
)
content = re.sub(
    r'                fn\(\)\n                time\.sleep\(0\.8\)',
    r'                fn()\n                context.page.wait_for_load_state("domcontentloaded", timeout=Config.BROWSER_TIMEOUT * 1000)',
    content
)

# Fix action_read_page_content missing context arg
content = re.sub(
    r'def action_read_page_content\(\) -> str:',
    r'def action_read_page_content(context: AgentContext) -> str:',
    content
)


with open('execution/browser.py', 'w', encoding='utf-8') as f:
    f.write(content)

