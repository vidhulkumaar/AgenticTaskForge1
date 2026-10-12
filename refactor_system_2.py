import os
import sys

def refactor_sys():
    with open('execution/system.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = """import os
import sys
import time
from pywinauto import Application
from agent_context import AgentContext
from utils import ActionResult

def action_run_calculator(context: AgentContext, expression: str) -> ActionResult:
    print(f"  [tool] run_calculator: '{expression}'")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from task3_1_calculator import run_task_3_1
    try:
        result = run_task_3_1(expression)
        if isinstance(result, ActionResult):
            return result
        # fallback
        return ActionResult(success=True, data=result, message=f"Calculator result: {result}")
    except Exception as e:
        return ActionResult(success=False, error=f"Calculator failed: {e}")

def action_run_system_settings(context: AgentContext, command: str) -> ActionResult:
    print(f"  [tool] run_system_settings: '{command}'")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from task3_2_system_settings import run_task_3_2
    try:
        result = run_task_3_2(command)
        if isinstance(result, dict):
            return ActionResult(success=result.get("success", False), message=result.get("message", "done"), error=result.get("error"))
        return ActionResult(success=True, message=str(result))
    except Exception as e:
        return ActionResult(success=False, error=f"System settings failed: {e}")
"""
    with open('execution/system.py', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    refactor_sys()
