import os
import re

def refactor_task2_1():
    with open('task2_1_browser_navigation.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add ActionResult import
    content = re.sub(
        r'from urllib\.parse import quote_plus',
        r'from urllib.parse import quote_plus\nfrom utils import ActionResult',
        content
    )

    # Change open_in_active_system_chrome to return ActionResult
    content = re.sub(
        r'def open_in_active_system_chrome\(url: str\) -> bool:',
        r'def open_in_active_system_chrome(url: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'        return True',
        r'        return ActionResult(success=True, message="Opened in active Chrome window")',
        content
    )
    content = re.sub(
        r'    except Exception as e:\n        print\(f"Could not dispatch directly to active Chrome: \{e\}"\)\n        return False',
        r'    except Exception as e:\n        print(f"Could not dispatch directly to active Chrome: {e}")\n        return ActionResult(success=False, error=str(e))',
        content
    )

    # In open_via_playwright, remove bare pass blocks or return ActionResult
    content = re.sub(
        r'def open_via_playwright\(url: str, headless: bool = False\):',
        r'def open_via_playwright(url: str, headless: bool = False) -> ActionResult:',
        content
    )
    content = re.sub(
        r'            print\(f"Successfully opened via active Chrome CDP: \'\{page\.title\(\)\}\'"\)\n            return',
        r'            print(f"Successfully opened via active Chrome CDP: \'{page.title()}\'")\n            return ActionResult(success=True, message=f"Opened via CDP: {page.title()}")',
        content
    )
    content = re.sub(
        r'        except Exception:\n            pass',
        r'        except Exception as e:\n            print(f"CDP connection failed, falling back to local context: {e}")',
        content
    )
    content = re.sub(
        r'        print\(f"Opened URL: \'\{page\.title\(\)\}\' \| \{page\.url\}"\)',
        r'        print(f"Opened URL: \'{page.title()}\' | {page.url}")\n        return ActionResult(success=True, message=f"Opened via Playwright: {page.title()}")',
        content
    )
    
    # In run_task_2_1, handle ActionResult
    content = re.sub(
        r'    success = open_in_active_system_chrome\(url\)\n    if not success:',
        r'    result = open_in_active_system_chrome(url)\n    if not result.success:',
        content
    )

    with open('task2_1_browser_navigation.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_task2_1()
