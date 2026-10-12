import os
import ast

def extract_node_source(source_lines, node):
    # Extract decorators if they exist (though not heavily used here)
    start_line = node.lineno - 1
    if hasattr(node, "decorator_list") and node.decorator_list:
        start_line = node.decorator_list[0].lineno - 1
    
    end_line = node.end_lineno
    return "\n".join(source_lines[start_line:end_line]) + "\n\n"

def analyze_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    source_lines = source.split('\n')
    tree = ast.parse(source)
    
    nodes = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            nodes[node.name] = {
                "source": extract_node_source(source_lines, node),
                "start": node.lineno if not hasattr(node, "decorator_list") or not node.decorator_list else node.decorator_list[0].lineno,
                "end": node.end_lineno
            }
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    nodes[target.id] = {
                        "source": extract_node_source(source_lines, node),
                        "start": node.lineno,
                        "end": node.end_lineno
                    }
    return source_lines, nodes

agent_lines, agent_nodes = analyze_file('agent_orchestrator.py')
mod5_lines, mod5_nodes = analyze_file('module5_orchestrator.py')

# Ensure directories exist
for d in ['execution', 'perception', 'planning', 'tools']:
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, '__init__.py'), 'w', encoding='utf-8') as f:
        pass

# Group functions by module
MODULES = {
    "utils.py": {
        "funcs": ["get_known_folder_path", "get_known_folders_dict", "normalize_url"],
        "imports": "import os\nfrom pathlib import Path\nimport urllib.parse\n"
    },
    "planning/llm_client.py": {
        "funcs": ["ask_llm", "ask_ai", "check_and_preload_ollama", "warm_up_llm", "parse_json_from"],
        "imports": "import json\nimport re\nimport requests\nfrom config import Config\n"
    },
    "perception/desktop.py": {
        "funcs": ["observe_desktop", "observation_summary", "_electron", "_dashboard_status", "action_read_screen"],
        "imports": "import win32gui\nimport re\nfrom agent_context import AgentContext\n"
    },
    "execution/desktop.py": {
        "funcs": ["action_open_app", "action_type_text", "action_save_file", "_ctrl_focus_app", "_ctrl_press_key", "_ctrl_type_anywhere", "_ctrl_click_text"],
        "imports": "import time\nimport subprocess\nfrom pywinauto import Application\nfrom agent_context import AgentContext\n"
    },
    "execution/browser.py": {
        "funcs": ["get_chrome_profile_dir", "is_chrome_running", "clear_chrome_crash_bubble", 
                  "action_open_browser", "action_close_browser", "action_browser_go_back", 
                  "action_browser_go_forward", "action_fill_form", "action_click_browser_element", 
                  "action_read_page_content", "action_download_file"],
        "imports": "import os\nimport time\nimport re\nimport subprocess\nimport webbrowser\nimport requests\nfrom agent_context import AgentContext\nfrom utils import normalize_url, get_known_folder_path\n"
    },
    "execution/filesystem.py": {
        "funcs": ["action_open_folder", "_get_file_list_control", "_list_files_in_explorer", 
                  "action_rename_file", "action_move_file", "action_delete_file"],
        "imports": "import time\nimport win32gui\nfrom pywinauto import Application\nfrom agent_context import AgentContext\n"
    },
    "execution/system.py": {
        "funcs": ["action_run_calculator", "action_run_system_settings"],
        "imports": "import time\nfrom pywinauto import Application\nfrom agent_context import AgentContext\n"
    },
    "planning/pipeline.py": {
        "funcs": ["CONTENT_PROMPT", "FILENAME_PROMPT", "EXPLICIT_PATH_PATTERN", "extract_explicit_path", 
                  "detect_target_folder", "ECHO_TRIGGER_PHRASES", "clean_meta_commentary", 
                  "looks_like_echoed_instruction", "looks_too_vague", "TASK_TYPE_PROMPT", 
                  "RENAME_EXTRACTION_PROMPT", "MOVE_EXTRACTION_PROMPT", "DELETE_EXTRACTION_PROMPT", 
                  "BROWSER_NAVIGATE_EXTRACTION_PROMPT", "FORM_FILL_EXTRACTION_PROMPT", "_SYSTEM_SETTINGS_RE",
                  "classify_task_type", "extract_rename_details", "extract_move_details", 
                  "extract_delete_details", "extract_browser_navigate_details", "build_rename_plan", 
                  "build_move_plan", "build_delete_plan", "build_browser_navigate_plan", "build_search_url", 
                  "extract_form_fill_details", "build_form_fill_plan", "build_calculator_plan", 
                  "build_system_settings_plan", "extract_bare_creative_request", "get_plan_from_ai", 
                  "validate_plan"],
        "imports": "import re\nimport json\nimport urllib.parse\nfrom planning.llm_client import ask_ai\nfrom utils import extract_explicit_path, detect_target_folder\n"
    },
    "planning/agentic.py": {
        "funcs": ["AGENT_PROMPT", "ROUTER_SYSTEM_PROMPT", "GENERIC_ROUTER_TOOLS", "check_completion", 
                  "_router_exec_open_app", "_router_exec_open_url", "_router_exec_web_search_play", 
                  "_router_exec_type_text", "_router_exec_click", "try_single_pass_router"],
        "imports": "import json\nfrom planning.llm_client import ask_llm\nfrom agent_context import AgentContext\n"
    }
}

# We need to construct the files
for filepath, data in MODULES.items():
    content = data["imports"] + "\n\n"
    for func in data["funcs"]:
        # Try to get from agent_orchestrator first, then module5
        source = None
        if func in agent_nodes:
            source = agent_nodes[func]["source"]
        elif func in mod5_nodes:
            source = mod5_nodes[func]["source"]
        
        if source:
            content += source
        else:
            print(f"WARNING: {func} not found in either file!")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {filepath}")

# Generate tools/registry.py separately since TOOL_REGISTRY might have lambda scope issues if moved blindly
registry_code = """
from execution.desktop import *
from execution.browser import *
from execution.filesystem import *
from execution.system import *

TOOL_REGISTRY = {
    "open_app": {"desc": "Launch an app like Notepad.", "executor": lambda ctx, p: action_open_app(ctx)},
    "type_text": {"desc": "Type text into focused edit control.", "executor": lambda ctx, p: action_type_text(ctx, p.get("value", ""))},
    "save_file": {"desc": "Save text content to a file. Specify folder as prefix (e.g. 'documents/notes.txt').", "executor": lambda ctx, p: action_save_file(ctx, p["filename"])},
    "open_folder": {"desc": "Open File Explorer to a specific folder.", "executor": lambda ctx, p: action_open_folder(ctx, p["folder"])},
    "rename_file": {"desc": "Rename a file in the currently open File Explorer window.", "executor": lambda ctx, p: action_rename_file(ctx, p["old_name"], p["new_name"])},
    "move_file": {"desc": "Move a file from source folder to destination folder.", "executor": lambda ctx, p: action_move_file(ctx, p["filename"], p["dest_folder"], p.get("source_folder"))},
    "delete_file": {"desc": "Delete a file.", "executor": lambda ctx, p: action_delete_file(ctx, p["filename"], p.get("folder"))},
    "open_browser": {"desc": "Open browser and navigate to a URL.", "executor": lambda ctx, p: action_open_browser(ctx, p["url"])},
    "close_browser": {"desc": "Close the active Playwright browser.", "executor": lambda ctx, p: action_close_browser(ctx)},
    "fill_form": {"desc": "Fill an input field on a web page.", "executor": lambda ctx, p: action_fill_form(ctx, p.get("field", "search"), p["value"], p.get("submit", True))},
    "click_browser_element": {"desc": "Click an element by text/role.", "executor": lambda ctx, p: action_click_browser_element(ctx, p.get("text"), p.get("role"))},
    "read_page_content": {"desc": "Read visible text from current web page.", "executor": lambda ctx, p: action_read_page_content(ctx)},
    "run_calculator": {"desc": "Calculate a math expression using Windows Calculator.", "executor": lambda ctx, p: action_run_calculator(ctx, p["expression"])},
    "run_system_settings": {"desc": "Toggle system settings like Wi-Fi or Bluetooth.", "executor": lambda ctx, p: action_run_system_settings(ctx, p["command"])},
    "read_screen": {"desc": "Extract visible text from screen using OCR.", "executor": lambda ctx, p: action_read_screen(ctx, p.get("find", ""))},
    "download_file": {"desc": "Download a file from URL.", "executor": lambda ctx, p: action_download_file(ctx, p["url"], p.get("filename", ""), p.get("folder", "downloads"))},
    "focus_app": {"desc": "Focus an application window.", "executor": lambda ctx, p: _ctrl_focus_app(ctx, p["app_name"])},
    "press_key": {"desc": "Send a key press to focused window.", "executor": lambda ctx, p: _ctrl_press_key(ctx, p["key"])},
    "type_anywhere": {"desc": "Type text anywhere.", "executor": lambda ctx, p: _ctrl_type_anywhere(ctx, p["text"])},
    "click_text": {"desc": "Click text visible on screen via OCR.", "executor": lambda ctx, p: _ctrl_click_text(ctx, p["text"], int(p.get("occurrence", 1)))},
}

def tool_catalog_text() -> str:
    lines = []
    for tname, tinfo in TOOL_REGISTRY.items():
        if "params" in tinfo:
            p_str = ", ".join(f"{k} ({v})" for k, v in tinfo["params"].items())
            lines.append(f"- {tname}: {tinfo['description']}\\n  Args: {p_str}")
        else:
            lines.append(f"- {tname}: {tinfo.get('description', tinfo.get('desc'))}")
    return "\\n".join(lines)
"""
with open('tools/registry.py', 'w', encoding='utf-8') as f:
    f.write(registry_code)
print("Created tools/registry.py")

action_funcs_code = """
from execution.desktop import *
from execution.browser import *
from execution.filesystem import *
from execution.system import *

ACTION_FUNCTIONS = {
    "open_app": lambda ctx, step: action_open_app(ctx),
    "type_text": lambda ctx, step: action_type_text(ctx, step["value"]),
    "save_file": lambda ctx, step: action_save_file(ctx, step["filename"]),
    "open_folder": lambda ctx, step: action_open_folder(ctx, step["folder"]),
    "rename_file": lambda ctx, step: action_rename_file(ctx, step["old_name"], step["new_name"]),
    "move_file": lambda ctx, step: action_move_file(ctx, step["filename"], step["dest_folder"], step.get("source_folder")),
    "delete_file": lambda ctx, step: action_delete_file(ctx, step["filename"], step.get("folder")),
    "open_browser": lambda ctx, step: action_open_browser(ctx, step["url"]),
    "close_browser": lambda ctx, step: action_close_browser(ctx),
    "browser_go_back": lambda ctx, step: action_browser_go_back(ctx),
    "browser_go_forward": lambda ctx, step: action_browser_go_forward(ctx),
    "fill_form": lambda ctx, step: action_fill_form(ctx, step.get("field", "search"), step["value"], step.get("submit", True)),
    "run_calculator": lambda ctx, step: action_run_calculator(ctx, step["expression"]),
    "run_system_settings": lambda ctx, step: action_run_system_settings(ctx, step["command"]),
}
"""
with open('tools/pipeline_registry.py', 'w', encoding='utf-8') as f:
    f.write(action_funcs_code)
print("Created tools/pipeline_registry.py")

