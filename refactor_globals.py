import sys
import re

def refactor_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Inject import
    if "from agent_context import AgentContext" not in text:
        text = re.sub(r'^(import os\n)', r'\1from agent_context import AgentContext\n', text, count=1)

    # 2. Delete module-level global variables
    text = re.sub(
        r'(?m)^_app\s*=\s*None\n^_main_window\s*=\s*None\n^_document\s*=\s*None\n^_explorer_window\s*=\s*None\n^_current_folder_path\s*=\s*None\n^_browser\s*=\s*None\n^_browser_context\s*=\s*None\n^_page\s*=\s*None\n^_playwright\s*=\s*None\n',
        '', text
    )
    # Also delete the comment
    text = re.sub(r'# Global state shared by browser and file actions\n', '', text)

    # 3. List of functions that use global state
    state_functions = [
        "action_open_app", "action_type_text", "action_save_file", "action_close_notepad",
        "action_open_browser", "action_close_browser", "action_browser_go_back", 
        "action_browser_go_forward", "action_fill_form", "action_open_explorer", 
        "action_create_folder", "action_rename_file", "action_move_file", 
        "_list_files_in_explorer", "action_delete_file", "close_existing_explorer_windows",
        "get_observation"
    ]
    
    # 4. For each function, add `context: AgentContext` to its signature
    for fn in state_functions:
        # e.g., def action_open_app() -> str:
        text = re.sub(fr'(?m)^def {fn}\(([^)]*)\)(.*?):', lambda m: f"def {fn}(context: AgentContext, {m.group(1)}){m.group(2)}:" if m.group(1) else f"def {fn}(context: AgentContext){m.group(2)}:", text)

    # 5. Remove `global _app, _main_window, ...` statements
    text = re.sub(r'(?m)^\s*global\s+_[a-zA-Z_,\s]+\n', '', text)

    # 6. Replace references to globals with context fields
    mapping = {
        "_app": "context.app",
        "_main_window": "context.main_window",
        "_document": "context.document",
        "_explorer_window": "context.explorer_window",
        "_current_folder_path": "context.current_folder_path",
        "_playwright": "context.playwright",
        "_browser": "context.browser",
        "_browser_context": "context.browser_context",
        "_page": "context.page",
    }
    for old, new in mapping.items():
        text = re.sub(fr'\b{old}\b', new, text)

    # 7. Fix callers
    # In module5_orchestrator, ACTION_FUNCTIONS = { ... }
    # e.g., "open_app": lambda step: action_open_app() -> "open_app": lambda ctx, step: action_open_app(ctx)
    if "ACTION_FUNCTIONS = {" in text:
        text = re.sub(r'(?m)^\s*"([^"]+)":\s*lambda\s+step:\s*([a-zA-Z_]+)\(', r'    "\1": lambda ctx, step: \2(ctx, ', text)
        # Now update run_command to take context
        text = re.sub(r'def run_command\(user_request: str\):', r'def run_command(context: AgentContext, user_request: str):', text)
        text = re.sub(r'ACTION_FUNCTIONS\[step\["action"\]\]\(step\)', r'ACTION_FUNCTIONS[step["action"]](context, step)', text)
        # Add context creation in __main__
        text = re.sub(
            r'(?m)(^\s*while True:)',
            r'    context = AgentContext()\n\1', text
        )
        # Fix exit branch
        text = re.sub(r'if context\.browser is not None:\n\s*action_close_browser\(\)', r'if context.browser is not None:\n                    action_close_browser(context)', text)
        text = re.sub(r'run_command\(user_input\)', r'run_command(context, user_input)', text)

    # In agent_orchestrator, TOOL_REGISTRY = { ... }
    # e.g., "executor": lambda p: action_open_app() -> "executor": lambda ctx, p: action_open_app(ctx)
    if "TOOL_REGISTRY = {" in text:
        text = re.sub(r'(?m)^\s*"executor":\s*lambda\s+p:\s*([a-zA-Z_]+)\(', r'        "executor": lambda ctx, p: \1(ctx, ', text)
        
        # In agent_orchestrator, dispatch_action needs context
        text = re.sub(r'def dispatch_action\(action: dict\) -> str:', r'def dispatch_action(context: AgentContext, action: dict) -> str:', text)
        text = re.sub(r'TOOL_REGISTRY\[tool_name\]\["executor"\]\(params\)', r'TOOL_REGISTRY[tool_name]["executor"](context, params)', text)
        
        # update evaluate_task
        text = re.sub(r'def evaluate_task\(goal: str, obs: dict, execution_history: list\) -> tuple:', r'def evaluate_task(context: AgentContext, goal: str, obs: dict, execution_history: list) -> tuple:', text)
        text = re.sub(r'action_read_screen\((.*?)\)', r'action_read_screen(context, \1)', text)
        
        # update run_agent_loop
        text = re.sub(r'def run_agent_loop\(goal: str, max_steps: int = MAX_STEPS\) -> str:', r'def run_agent_loop(context: AgentContext, goal: str, max_steps: int = MAX_STEPS) -> str:', text)
        text = re.sub(r'obs = get_observation\(\)', r'obs = get_observation(context)', text)
        text = re.sub(r'evaluate_task\(goal, obs, history\)', r'evaluate_task(context, goal, obs, history)', text)

        # In __main__, create context
        text = re.sub(
            r'(?m)(^\s*while True:)',
            r'    context = AgentContext()\n\1', text
        )
        text = re.sub(r'run_agent_loop\(goal\)', r'run_agent_loop(context, goal)', text)

    # _list_files_in_explorer caller
    text = re.sub(r'_list_files_in_explorer\(\)', r'_list_files_in_explorer(context)', text)
    
    # Internal callers in agent_orchestrator / module5
    text = re.sub(r'action_close_notepad\(\)', r'action_close_notepad(context)', text)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

refactor_file('module5_orchestrator.py')
refactor_file('agent_orchestrator.py')
