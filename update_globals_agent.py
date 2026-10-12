import sys
import re

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # Add import
    if "from agent_context import AgentContext" not in text:
        text = re.sub(
            r'^(import os\n)', 
            r'\1from agent_context import AgentContext\n', 
            text, count=1
        )

    # Remove global vars block
    text = re.sub(
        r'# Global state shared by browser and file actions\n(?:_[a-z_]+\s*=\s*None\n)+',
        '', text
    )

    # Change function definitions to accept context
    action_functions = [
        "action_open_app", "action_type_text", "action_save_file", 
        "action_close_notepad", "action_open_browser", "action_navigate",
        "action_click_text", "action_type_in_browser", "action_close_browser",
        "action_open_explorer", "action_create_folder", "action_rename_file",
        "action_move_file", "_list_files_in_explorer", "action_read_screen",
        "action_download_file", "execute_pipeline"
    ]
    
    for fn in action_functions:
        text = re.sub(fr'def {fn}\((.*?)\)', fr'def {fn}(context: AgentContext, \1)', text)
        text = re.sub(fr'def {fn}\(context: AgentContext, \)', fr'def {fn}(context: AgentContext)', text)

    # Replace `global _app, _main_window` etc. with nothing
    text = re.sub(r'^\s*global _[a-z_]+(?:,\s*_[a-z_]+)*\n', '', text, flags=re.MULTILINE)

    # Replace _var with context.var
    var_map = {
        "_app": "context.app",
        "_main_window": "context.main_window",
        "_document": "context.document",
        "_explorer_window": "context.explorer_window",
        "_current_folder_path": "context.current_folder_path",
        "_playwright": "context.playwright",
        "_browser": "context.browser",
        "_browser_context": "context.browser_context",
        "_page": "context.page"
    }

    # Replace usages but be careful about kwargs or strings. Word boundaries:
    for k, v in var_map.items():
        text = re.sub(fr'\b{k}\b', v, text)
        
    # Fix action_ functions taking context inside dispatch_action
    # In agent_orchestrator, dispatch_action needs context
    text = re.sub(r'def dispatch_action\(action: dict\) -> str:', r'def dispatch_action(context: AgentContext, action: dict) -> str:', text)
    
    # Inside dispatch_action calls to action_xxx
    for fn in action_functions:
        # e.g. return action_open_app() -> return action_open_app(context)
        # e.g. return action_type_text(action.get('value')) -> return action_type_text(context, action.get('value'))
        text = re.sub(fr'\b{fn}\(\)', fr'{fn}(context)', text)
        text = re.sub(fr'\b{fn}\(([^c][^o][^n][^t][^e][^x][^t].*?)\)', fr'{fn}(context, \1)', text)
        text = re.sub(fr'\b{fn}\((?!context)(.*?)\)', fr'{fn}(context, \1)', text) # more general regex
        
    # But wait, action_download_file is also called, maybe in execute_pipeline
    # In agent_orchestrator.py, execute_pipeline and evaluate_task don't take context
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

update_file('agent_orchestrator.py')
