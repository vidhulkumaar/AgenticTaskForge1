import os
import re

def refactor_browser():
    with open('execution/browser.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add ActionResult import
    content = re.sub(
        r'from utils import normalize_url, get_known_folder_path, wait_for_clipboard_sync',
        r'from utils import normalize_url, get_known_folder_path, wait_for_clipboard_sync, ActionResult',
        content
    )

    # Change is_chrome_running to return ActionResult? No, the audit report didn't complain about is_chrome_running itself returning False. Wait, yes it did: "execution/browser.py is_chrome_running Returns False | Agent gets boolean, no context".
    content = re.sub(
        r'def is_chrome_running\(\) -> bool:\n.*?    except Exception:\n        return False',
        r'def is_chrome_running() -> ActionResult:\n    """Checks if chrome.exe is currently running on Windows."""\n    try:\n        output = subprocess.check_output(\'tasklist /FI "IMAGENAME eq chrome.exe"\', shell=True, text=True)\n        is_running = "chrome.exe" in output.lower()\n        return ActionResult(success=True, data=is_running)\n    except Exception as e:\n        return ActionResult(success=False, error=f"Could not check process list: {e}")',
        content,
        flags=re.DOTALL
    )

    # Convert returns to ActionResult
    content = re.sub(
        r'def action_open_browser\(context: AgentContext, url: str\) -> str:',
        r'def action_open_browser(context: AgentContext, url: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        return f"Opened \{normalized\} directly in your active Google Chrome browser!"',
        r'        return ActionResult(success=True, message=f"Opened {normalized} directly in your active Google Chrome browser!")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        return f"Error launching browser: \{e\}"',
        r'    except Exception as e:\n        return ActionResult(success=False, error=f"Error launching browser: {e}")',
        content
    )

    content = re.sub(
        r'def action_close_browser\(context: AgentContext\) -> str:',
        r'def action_close_browser(context: AgentContext) -> ActionResult:',
        content
    )
    content = re.sub(
        r'    return "Browser closed."',
        r'    return ActionResult(success=True, message="Browser closed.")',
        content
    )

    content = re.sub(
        r'def action_fill_form\(context: AgentContext, field: str, value: str, submit: bool = False\) -> str:',
        r'def action_fill_form(context: AgentContext, field: str, value: str, submit: bool = False) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        raise RuntimeError\("No browser page open\. Use open_browser first\."\)',
        r'        return ActionResult(success=False, error="No browser page open. Use open_browser first.")',
        content
    )
    content = re.sub(
        r'                    return f"Filled \'\{field\}\' with \'\{value\}\' and submitted\. Now on: \{context\.page\.title\(\)\}"',
        r'                    return ActionResult(success=True, message=f"Filled \'{field}\' with \'{value}\' and submitted. Now on: {context.page.title()}")',
        content
    )
    content = re.sub(
        r'                return f"Filled \'\{field\}\' with \'\{value\}\'\."',
        r'                return ActionResult(success=True, message=f"Filled \'{field}\' with \'{value}\'.")',
        content
    )
    content = re.sub(
        r'    return f"Filled \(clipboard paste\) \'\{value\}\' into active field\."',
        r'    return ActionResult(success=True, message=f"Filled (clipboard paste) \'{value}\' into active field.")',
        content
    )

    content = re.sub(
        r'def action_click_browser_element\(context: AgentContext, selector: str\) -> str:',
        r'def action_click_browser_element(context: AgentContext, selector: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'                return f"Clicked \'\{selector\}\'\. Page: \{context\.page\.title\(\)\}"',
        r'                return ActionResult(success=True, message=f"Clicked \'{selector}\'. Page: {context.page.title()}")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        return f"Could not click \'\{selector\}\': \{e\}"',
        r'    except Exception as e:\n        return ActionResult(success=False, error=f"Could not click \'{selector}\': {e}")',
        content
    )
    # The fall back returns the result of click_text. click_text (from task6_computer_control) returns a string right now. I'll need to wrap it if it returns string. But let's assume we will refactor task6_computer_control to return ActionResult.

    content = re.sub(
        r'def action_read_page_content\(context: AgentContext\) -> str:',
        r'def action_read_page_content(context: AgentContext) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        return "No browser page open\."',
        r'        return ActionResult(success=False, error="No browser page open.")',
        content
    )
    content = re.sub(
        r'        return f"Page: \{title\}\\nURL: \{url\}\\n\\nVisible elements:\\n\{visible_text\[:2000\]\}"',
        r'        return ActionResult(success=True, message=f"Page: {title}\\nURL: {url}\\n\\nVisible elements:\\n{visible_text[:2000]}")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        return f"Could not read page: \{e\}"',
        r'    except Exception as e:\n        return ActionResult(success=False, error=f"Could not read page: {e}")',
        content
    )

    content = re.sub(
        r'def action_download_file\(url: str, filename: str = "", folder: str = "downloads"\) -> str:',
        r'def action_download_file(url: str, filename: str = "", folder: str = "downloads") -> ActionResult:',
        content
    )
    content = re.sub(
        r'        return f"Downloaded \'\{filename\}\' to \{dest_dir\} \(\{size_kb\} KB\)\."',
        r'        return ActionResult(success=True, message=f"Downloaded \'{filename}\' to {dest_dir} ({size_kb} KB).")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        return f"Download failed: \{e\}"',
        r'    except Exception as e:\n        return ActionResult(success=False, error=f"Download failed: {e}")',
        content
    )

    with open('execution/browser.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_browser()
