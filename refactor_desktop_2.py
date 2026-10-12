import os
import re

def refactor_desktop():
    with open('execution/desktop.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add ActionResult import
    content = re.sub(
        r'from utils import get_known_folder_path, wait_for_clipboard_sync, wait_for_file_exists, wait_for_window',
        r'from utils import get_known_folder_path, wait_for_clipboard_sync, wait_for_file_exists, wait_for_window, ActionResult',
        content
    )

    # Change return types of action_* to ActionResult
    content = re.sub(
        r'def action_open_app\(context: AgentContext\) -> str:',
        r'def action_open_app(context: AgentContext) -> ActionResult:',
        content
    )
    content = re.sub(
        r'    if app is None:\n        raise RuntimeError\("Could not connect to Notepad after launch."\)',
        r'    if app is None:\n        return ActionResult(success=False, error="Could not connect to Notepad after launch.")',
        content
    )
    content = re.sub(
        r'    return "Notepad is open and focused."',
        r'    return ActionResult(success=True, message="Notepad is open and focused.")',
        content
    )

    content = re.sub(
        r'def action_type_text\(context: AgentContext, value: str\) -> str:',
        r'def action_type_text(context: AgentContext, value: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        return f"Typed {len\(value\)} characters into Notepad."',
        r'        return ActionResult(success=True, message=f"Typed {len(value)} characters into Notepad.")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        raise RuntimeError\(f"type_text failed: \{e\}"\)',
        r'    except Exception as e:\n        return ActionResult(success=False, error=f"type_text failed: {e}")',
        content
    )

    content = re.sub(
        r'def action_save_file\(context: AgentContext, filename: str\) -> str:',
        r'def action_save_file(context: AgentContext, filename: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        raise RuntimeError\("No Notepad window open to save."\)',
        r'        return ActionResult(success=False, error="No Notepad window open to save.")',
        content
    )
    
    # Fix exception passes in action_save_file
    save_replace = r'''
    try:
        dlg = context.app.window(title_re=".*Save.*")
        dlg.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)
        dlg.set_focus()
        name_box = dlg.child_window(auto_id="1001")
        name_box.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT)
        name_box.set_text(full_path)
        send_keys("{ENTER}")
        try:
            dlg.wait_not("visible", timeout=Config.UI_ELEMENT_TIMEOUT)
        except Exception:
            pass # might already be closed or waiting for overwrite dialog
            
        # Handle overwrite dialog
        try:
            overwrite = context.app.window(title_re=".*Confirm Save As.*|.*Notepad.*")
            if overwrite.exists(timeout=2):
                yes_btn = overwrite.child_window(title="Yes")
                if yes_btn.exists(timeout=1):
                    yes_btn.wait("ready", timeout=Config.UI_ELEMENT_TIMEOUT).click()
                    overwrite.wait_not("visible", timeout=Config.UI_ELEMENT_TIMEOUT)
        except Exception as e:
            return ActionResult(success=False, error=f"Failed to handle overwrite dialog: {e}")
    except Exception as e:
        return ActionResult(success=False, error=f"Failed to interact with Save dialog: {e}")

    if wait_for_file_exists(full_path):
        return ActionResult(success=True, message=f"File saved: {full_path}")
    return ActionResult(success=False, error=f"Save attempted for: {full_path} but file was not created.")
'''

    content = re.sub(
        r'    try:\n        dlg = context\.app\.window\(title_re=".*Save.*"\)\n.*?    return f"Save attempted for: \{full_path\} \(could not confirm file exists\)"',
        save_replace.strip(),
        content,
        flags=re.DOTALL
    )


    with open('execution/desktop.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_desktop()
