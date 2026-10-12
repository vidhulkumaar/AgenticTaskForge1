import os
import re

def refactor_registry_desktop():
    # 1. Update execution/desktop.py
    with open('execution/desktop.py', 'r', encoding='utf-8') as f:
        desktop_content = f.read()

    ctrl_block = """
def _ctrl_focus_app(ctx, app_name: str) -> ActionResult:
    from task6_computer_control import focus_app
    return focus_app(app_name)

def _ctrl_press_key(ctx, key: str) -> ActionResult:
    from task6_computer_control import press_key
    return press_key(key)

def _ctrl_type_anywhere(ctx, text: str) -> ActionResult:
    from task6_computer_control import type_anywhere
    return type_anywhere(text)

def _ctrl_click_text(ctx, text: str, occurrence: int = 1) -> ActionResult:
    from task6_computer_control import click_text
    return click_text(text, occurrence)

def _ctrl_clear_input(ctx) -> ActionResult:
    from task6_computer_control import clear_input
    return clear_input()
"""

    desktop_content = re.sub(
        r'def _ctrl_focus_app\(app_name: str\) -> str:.*?return click_text\(text, occurrence\)',
        ctrl_block.strip(),
        desktop_content,
        flags=re.DOTALL
    )

    with open('execution/desktop.py', 'w', encoding='utf-8') as f:
        f.write(desktop_content)

    # 2. Update tools/registry.py
    with open('tools/registry.py', 'r', encoding='utf-8') as f:
        registry_content = f.read()

    registry_content = re.sub(
        r'    "click_text": \{"desc": "Click text visible on screen via OCR\.", "executor": lambda ctx, p: _ctrl_click_text\(ctx, p\["text"\], int\(p\.get\("occurrence", 1\)\)\)\},',
        r'    "click_text": {"desc": "Click text visible on screen via OCR.", "executor": lambda ctx, p: _ctrl_click_text(ctx, p["text"], int(p.get("occurrence", 1)))},\n    "clear_input": {"desc": "Clear the currently focused text input field.", "executor": lambda ctx, p: _ctrl_clear_input(ctx)},',
        registry_content
    )

    with open('tools/registry.py', 'w', encoding='utf-8') as f:
        f.write(registry_content)

if __name__ == "__main__":
    refactor_registry_desktop()
