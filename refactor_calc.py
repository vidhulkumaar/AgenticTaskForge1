import os
import re

with open('task3_1_calculator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Imports
content = re.sub(
    r'from config import Config',
    r'from config import Config\nfrom utils import wait_for_window',
    content
)

content = re.sub(
    r'    subprocess\.Popen\(\["calc\.exe"\]\)\n\n    for attempt in range\(15\):\n        time\.sleep\(1\)\n        hwnd = find_calc_hwnd\(\)\n        if hwnd:\n            break',
    r'    subprocess.Popen(["calc.exe"])\n    end_t = time.time() + Config.APP_START_TIMEOUT\n    while time.time() < end_t:\n        hwnd = find_calc_hwnd()\n        if hwnd:\n            break\n        time.sleep(0.2)',
    content
)

content = re.sub(
    r'    app = Application\(backend="uia"\)\.connect\(handle=hwnd\)\n    time\.sleep\(0\.5\)\n    return app',
    r'    app = Application(backend="uia").connect(handle=hwnd)\n    # UIA takes a moment to become accessible in Calculator\n    app.wait_cpu_usage_lower(threshold=5, timeout=Config.UI_ELEMENT_TIMEOUT)\n    return app',
    content
)

content = re.sub(
    r'        window\.set_focus\(\)\n        time\.sleep\(0\.5\)',
    r'        window.set_focus()\n        window.wait("visible", timeout=Config.UI_ELEMENT_TIMEOUT)',
    content
)

with open('task3_1_calculator.py', 'w', encoding='utf-8') as f:
    f.write(content)
