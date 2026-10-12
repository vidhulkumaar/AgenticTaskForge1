import os
import re

with open('task6_computer_control.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
content = re.sub(
    r'from config import Config, get_app_path',
    r'from config import Config, get_app_path\nfrom utils import wait_for_clipboard_sync, wait_for_window',
    content
)

# 1. OS focus settling
content = re.sub(
    r'            win32gui\.SetForegroundWindow\(found_hwnd\)\n            time\.sleep\(0\.6\)\n            return f"Brought \'\{app_name\}\' to foreground\."',
    r'            win32gui.SetForegroundWindow(found_hwnd)\n            # Wait for OS focus to transition\n            end_t = time.time() + Config.APP_START_TIMEOUT\n            while time.time() < end_t:\n                if win32gui.GetForegroundWindow() == found_hwnd:\n                    break\n                time.sleep(0.1)\n            return f"Brought \'{app_name}\' to foreground."',
    content
)

# 2. Popen sleeps
content = re.sub(
    r'            subprocess\.Popen\(exe, shell=True\)\n        time\.sleep\(3\.5\)\n        return f"Launched \'\{app_name\}\' — waiting for it to open\."',
    r'            subprocess.Popen(exe, shell=True)\n        wait_for_window(name_lower, timeout=Config.APP_START_TIMEOUT)\n        return f"Launched \'{app_name}\' — waiting for it to open."',
    content
)

content = re.sub(
    r'        subprocess\.Popen\(\["start", app_name\], shell=True\)\n        time\.sleep\(3\)\n        return f"Attempted to launch \'\{app_name\}\' via system\."',
    r'        subprocess.Popen(["start", app_name], shell=True)\n        wait_for_window(name_lower, timeout=Config.APP_START_TIMEOUT)\n        return f"Attempted to launch \'{app_name}\' via system."',
    content
)

# 3. type_anywhere
content = re.sub(
    r'        pyperclip\.copy\(text\)\n        time\.sleep\(0\.2\)\n        pyautogui\.hotkey\("ctrl", "v"\)\n        time\.sleep\(0\.4\)',
    r'        pyperclip.copy(text)\n        wait_for_clipboard_sync()\n        pyautogui.hotkey("ctrl", "v")',
    content
)

# 4. click_text
content = re.sub(
    r'        pyautogui\.click\(x, y\)\n        time\.sleep\(0\.5\)',
    r'        pyautogui.click(x, y)',
    content
)

with open('task6_computer_control.py', 'w', encoding='utf-8') as f:
    f.write(content)

