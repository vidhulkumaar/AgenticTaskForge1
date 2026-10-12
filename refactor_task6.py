import os
import re

def refactor_file():
    with open('task6_electron_apps.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add ActionResult import
    content = re.sub(
        r'from utils import wait_for_window, wait_for_clipboard_sync',
        r'from utils import wait_for_window, wait_for_clipboard_sync, ActionResult',
        content
    )

    # _ocr_read returning "" on exception
    content = re.sub(
        r'    except Exception:\n        return ""',
        r'    except Exception as e:\n        raise RuntimeError(f"OCR failed: {e}") from e',
        content
    )

    # Change _err and _ok to return ActionResult
    content = re.sub(
        r'def _err\(msg: str, context: str = ""\) -> str:\n    return f"ERROR: \[{context}\] {msg}"',
        r'def _err(msg: str, context: str = "") -> ActionResult:\n    return ActionResult(success=False, error=f"[{context}] {msg}")',
        content
    )
    content = re.sub(
        r'def _ok\(msg: str, context: str = ""\) -> str:\n    return f"\[{context}\] {msg}"',
        r'def _ok(msg: str, context: str = "") -> ActionResult:\n    return ActionResult(success=True, message=f"[{context}] {msg}")',
        content
    )
    
    # Change _type_and_send to return ActionResult or just raise
    # Currently _type_and_send does not return explicitly

    with open('task6_electron_apps.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_file()
