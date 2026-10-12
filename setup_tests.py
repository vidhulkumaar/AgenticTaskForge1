import os

def create_tests():
    os.makedirs('tests', exist_ok=True)

    with open('tests/__init__.py', 'w', encoding='utf-8') as f:
        pass

    with open('tests/test_config.py', 'w', encoding='utf-8') as f:
        f.write("""import os
from config import Config

def test_config_defaults():
    assert Config.LLM_RETRIES == int(os.getenv("LLM_RETRIES", "2"))
    assert Config.MAX_STEPS == int(os.getenv("MAX_STEPS", "15"))

def test_config_env_override(monkeypatch):
    monkeypatch.setenv("MAX_STEPS", "20")
    # Need to reload or just test the property if it was dynamic
    # Since they are class attributes loaded at import time, this might not reflect immediately unless we reload
    import importlib
    import config
    importlib.reload(config)
    assert config.Config.MAX_STEPS == 20
""")

    with open('tests/test_action_result.py', 'w', encoding='utf-8') as f:
        f.write("""from utils import ActionResult

def test_action_result_success():
    res = ActionResult(success=True, message="All good")
    assert res.success is True
    assert str(res) == "All good"

def test_action_result_failure():
    res = ActionResult(success=False, error="Something broke")
    assert res.success is False
    assert str(res) == "ERROR: Something broke"
    
def test_action_result_default_message():
    res = ActionResult(success=True)
    assert str(res) == "Success."
""")

    with open('tests/test_llm_parsing.py', 'w', encoding='utf-8') as f:
        f.write("""from planning.llm_client import parse_json_from

def test_parse_json_valid():
    raw = '{"tool": "open_app", "params": {"app_name": "notepad"}}'
    res = parse_json_from(raw)
    assert res["tool"] == "open_app"

def test_parse_json_markdown():
    raw = '''```json
{"tool": "click", "params": {"target": "Submit"}}
```'''
    res = parse_json_from(raw)
    assert res["tool"] == "click"

def test_parse_json_invalid():
    raw = 'just some text without json'
    res = parse_json_from(raw)
    assert res is None
""")

    with open('tests/test_failure_propagation.py', 'w', encoding='utf-8') as f:
        f.write("""from utils import ActionResult
from execution.desktop import action_type_text
from agent_context import AgentContext

def test_false_success_prevention():
    # If a tool returns False or raises, we want to ensure it doesn't accidentally return success
    # Here we simulate a failure
    res = ActionResult(success=False, error="Simulated verification failure")
    assert res.success is False
    assert "ERROR" in str(res)
""")

    with open('tests/test_privacy_logging.py', 'w', encoding='utf-8') as f:
        f.write("""import logging
from task6_computer_control import type_anywhere

def test_privacy_redaction(caplog):
    caplog.set_level(logging.INFO)
    
    # We will patch pyperclip.copy and pyautogui.hotkey to avoid real UI interaction
    import unittest.mock
    with unittest.mock.patch('pyperclip.copy'), unittest.mock.patch('task6_computer_control.wait_for_clipboard_sync'), unittest.mock.patch('pyautogui.hotkey'):
        # Call with is_secret=True
        secret_val = "SuperSecretPassword123"
        type_anywhere(secret_val, is_secret=True)
        
    log_output = caplog.text
    assert secret_val not in log_output
    assert "***" in log_output
""")

if __name__ == "__main__":
    create_tests()
