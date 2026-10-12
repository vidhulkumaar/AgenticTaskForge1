import os
import re

def refactor_comp_ctrl():
    with open('task6_computer_control.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add ActionResult import
    content = re.sub(
        r'from utils import wait_for_clipboard_sync, wait_for_window',
        r'from utils import wait_for_clipboard_sync, wait_for_window, ActionResult',
        content
    )

    # Change return types
    content = re.sub(
        r'def focus_app\(app_name: str\) -> str:',
        r'def focus_app(app_name: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'            return f"Brought \\\'\{app_name\}\\\' to foreground\."',
        r'            return ActionResult(success=True, message=f"Brought \'{app_name}\' to foreground.")',
        content
    )
    content = re.sub(
        r'        return f"Launched \\\'\{app_name\}\\\' — waiting for it to open\."',
        r'        return ActionResult(success=True, message=f"Launched \'{app_name}\' — waiting for it to open.")',
        content
    )
    content = re.sub(
        r'        return f"Attempted to launch \\\'\{app_name\}\\\' via system\."',
        r'        return ActionResult(success=True, message=f"Attempted to launch \'{app_name}\' via system.")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        return f"Could not find or launch \'\{app_name\}\': \{e\}"',
        r'    except Exception as e:\n        return ActionResult(success=False, error=f"Could not find or launch \'{app_name}\': {e}")',
        content
    )

    content = re.sub(
        r'def press_key\(key: str\) -> str:',
        r'def press_key(key: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        return f"Pressed key: \{key\}"',
        r'        return ActionResult(success=True, message=f"Pressed key: {key}")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        return f"Key press failed: \{e\}"',
        r'    except Exception as e:\n        return ActionResult(success=False, error=f"Key press failed: {e}")',
        content
    )

    content = re.sub(
        r'def type_anywhere\(text: str\) -> str:',
        r'def type_anywhere(text: str) -> ActionResult:',
        content
    )
    
    # Fix duplication in type_anywhere and wrap return
    type_anywhere_block = r'''
    except Exception as e:
        return f"Typing failed: {e}"

        return f"Typed: {text[:80]}"
    except Exception as e:
        return f"Typing failed: {e}"
'''
    content = content.replace(type_anywhere_block.strip(), 
        '    except Exception as e:\n        return ActionResult(success=False, error=f"Typing failed: {e}")'
    )
    content = re.sub(
        r'        return f"Typed: \{text\[:80\]\}"',
        r'        return ActionResult(success=True, message=f"Typed: {text[:80]}")',
        content
    )

    content = re.sub(
        r'def click_text\(text: str, occurrence: int = 1\) -> str:',
        r'def click_text(text: str, occurrence: int = 1) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        return \(f"click_text requires: mss, pytesseract, pyautogui\. "\n                f"Install: pip install mss pytesseract pyautogui pillow"\)',
        r'        return ActionResult(success=False, error="click_text requires: mss, pytesseract, pyautogui. Install: pip install mss pytesseract pyautogui pillow")',
        content
    )
    content = re.sub(
        r'            return \(f"Text \'\{text\}\' not found on screen\. "\n                    f"Use read_screen\(\) to see what\'s currently visible\."\)',
        r'            return ActionResult(success=False, error=f"Text \'{text}\' not found on screen. Use read_screen() to see what\'s currently visible.")',
        content
    )
    content = re.sub(
        r'        return f"Clicked \'\{found_word\}\' at \(\{x\}, \{y\}\)\."',
        r'        return ActionResult(success=True, message=f"Clicked \'{found_word}\' at ({x}, {y}).")',
        content
    )
    content = re.sub(
        r'        if "tesseract" in str\(e\)\.lower\(\):\n            return "click_text unavailable.*?type_anywhere instead\."\n        return f"click_text failed: \{e\}"',
        r'        if "tesseract" in str(e).lower():\n            return ActionResult(success=False, error="click_text unavailable (Tesseract OCR engine not installed in PATH). Use press_key (e.g. \'ctrl+f\' to search, \'enter\' to confirm) or type_anywhere instead.")\n        return ActionResult(success=False, error=f"click_text failed: {e}")',
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'def clear_input\(\) -> str:',
        r'def clear_input() -> ActionResult:',
        content
    )
    content = re.sub(
        r'    return "Cleared input field\."',
        r'    return ActionResult(success=True, message="Cleared input field.")',
        content
    )

    with open('task6_computer_control.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_comp_ctrl()
