import ast
import re

def rewrite_file(filename, functions_to_remove, extra_imports):
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = ast.parse(source)
    source_lines = source.split('\n')
    
    # Sort nodes by start line descending so deleting lines doesn't affect previous offsets
    nodes_to_delete = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if node.name in functions_to_remove:
                start_line = node.lineno - 1
                if hasattr(node, "decorator_list") and node.decorator_list:
                    start_line = node.decorator_list[0].lineno - 1
                end_line = node.end_lineno
                nodes_to_delete.append((start_line, end_line))
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in functions_to_remove:
                    nodes_to_delete.append((node.lineno - 1, node.end_lineno))
                    break

    nodes_to_delete.sort(key=lambda x: x[0], reverse=True)
    
    for start, end in nodes_to_delete:
        del source_lines[start:end]
        
    # Now write the file back
    new_source = "\n".join(source_lines)
    
    # Add extra imports at the top, just after the docstring or first imports
    # A simple way is to insert them after `import os`
    new_source = re.sub(r'^(import os\n)', r'\1' + extra_imports + '\n', new_source, count=1, flags=re.MULTILINE)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_source)

# Shared removals
removed_agent = [
    "get_known_folder_path", "get_known_folders_dict", "normalize_url",
    "ask_llm", "check_and_preload_ollama", "warm_up_llm", "parse_json_from",
    "observe_desktop", "observation_summary", "_electron", "_dashboard_status", "action_read_screen",
    "action_open_app", "action_type_text", "action_save_file", "_ctrl_focus_app", "_ctrl_press_key", "_ctrl_type_anywhere", "_ctrl_click_text",
    "get_chrome_profile_dir", "is_chrome_running", "clear_chrome_crash_bubble", 
    "action_open_browser", "action_close_browser", "action_browser_go_back", 
    "action_browser_go_forward", "action_fill_form", "action_click_browser_element", 
    "action_read_page_content", "action_download_file",
    "action_open_folder", "_get_file_list_control", "_list_files_in_explorer", 
    "action_rename_file", "action_move_file", "action_delete_file",
    "action_run_calculator", "action_run_system_settings",
    "AGENT_PROMPT", "ROUTER_SYSTEM_PROMPT", "GENERIC_ROUTER_TOOLS", "check_completion", 
    "_router_exec_open_app", "_router_exec_open_url", "_router_exec_web_search_play", 
    "_router_exec_type_text", "_router_exec_click", "try_single_pass_router",
    "TOOL_REGISTRY", "tool_catalog_text"
]

extra_imports_agent = """
from utils import get_known_folder_path, normalize_url
from planning.llm_client import ask_llm, check_and_preload_ollama, warm_up_llm, parse_json_from
from perception.desktop import observe_desktop, observation_summary, _dashboard_status, action_read_screen
from planning.agentic import check_completion, try_single_pass_router
from tools.registry import TOOL_REGISTRY, tool_catalog_text
"""

rewrite_file('agent_orchestrator.py', removed_agent, extra_imports_agent)

removed_mod5 = [
    "get_known_folder_path", "get_known_folders_dict", "normalize_url",
    "CONTENT_PROMPT", "FILENAME_PROMPT", "EXPLICIT_PATH_PATTERN", "extract_explicit_path", 
    "detect_target_folder", "ECHO_TRIGGER_PHRASES", "clean_meta_commentary", 
    "looks_like_echoed_instruction", "looks_too_vague", "TASK_TYPE_PROMPT", 
    "RENAME_EXTRACTION_PROMPT", "MOVE_EXTRACTION_PROMPT", "DELETE_EXTRACTION_PROMPT", 
    "BROWSER_NAVIGATE_EXTRACTION_PROMPT", "FORM_FILL_EXTRACTION_PROMPT", "_SYSTEM_SETTINGS_RE",
    "classify_task_type", "extract_rename_details", "extract_move_details", 
    "extract_delete_details", "extract_browser_navigate_details", "build_rename_plan", 
    "build_move_plan", "build_delete_plan", "build_browser_navigate_plan", "build_search_url", 
    "extract_form_fill_details", "build_form_fill_plan", "build_calculator_plan", 
    "build_system_settings_plan", "extract_bare_creative_request", "get_plan_from_ai", 
    "validate_plan", "ask_ai",
    "action_open_app", "action_type_text", "action_save_file",
    "action_open_folder", "_get_file_list_control", "_list_files_in_explorer", 
    "action_rename_file", "action_move_file", "action_delete_file",
    "get_chrome_profile_dir", "is_chrome_running", "clear_chrome_crash_bubble", 
    "action_open_browser", "action_close_browser", "action_browser_go_back", 
    "action_browser_go_forward", "action_fill_form", "action_run_calculator", 
    "action_run_system_settings", "ACTION_FUNCTIONS"
]

extra_imports_mod5 = """
from utils import get_known_folder_path, normalize_url
from planning.pipeline import get_plan_from_ai, validate_plan
from execution.browser import action_close_browser
from tools.pipeline_registry import ACTION_FUNCTIONS
"""

rewrite_file('module5_orchestrator.py', removed_mod5, extra_imports_mod5)
