import os
import re

def patch_agent_orchestrator():
    filepath = 'agent_orchestrator.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update try_single_pass_router call
    content = content.replace(
        "def agent_loop(goal: str, max_steps: int = MAX_STEPS) -> str:",
        "def agent_loop(goal: str, context, max_steps: int = MAX_STEPS) -> str:"
    )
    content = content.replace(
        "success, result_text, timings = try_single_pass_router(goal)",
        "success, result_text, timings = try_single_pass_router(goal, context)"
    )
    content = content.replace(
        "result = agent_loop(goal, max_steps=args.max_steps)",
        "result = agent_loop(goal, context, max_steps=args.max_steps)"
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def patch_agentic_py():
    filepath = 'planning/agentic.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove GENERIC_ROUTER_TOOLS block
    content = re.sub(r'GENERIC_ROUTER_TOOLS = \{.*?\}\n', '', content, flags=re.DOTALL)
    
    # Update try_single_pass_router signature and implementation
    target = """def try_single_pass_router(command: str) -> tuple[bool, str, dict]:"""
    repl = """def try_single_pass_router(command: str, context) -> tuple[bool, str, dict]:"""
    content = content.replace(target, repl)

    router_exec_target = """    t_tool_start = time.perf_counter()
    try:
        executor = GENERIC_ROUTER_TOOLS[tool_name]
        result_text, browser_time = executor(args)
        t_tool_end = time.perf_counter()"""

    router_exec_repl = """    t_tool_start = time.perf_counter()
    try:
        from tools.registry import TOOL_REGISTRY
        from security.schemas import validate_tool_args
        
        # 1. Map generic aliases to TOOL_REGISTRY names
        mapped_tool_name = tool_name
        if tool_name in ["open_url", "web_search", "web_search_play"]:
            mapped_tool_name = "open_browser"
        elif tool_name == "click":
            mapped_tool_name = "click_text"
            
        # 2. Schema Validation
        is_valid, err_msg, validated_params = validate_tool_args(mapped_tool_name, args)
        if not is_valid:
            return False, f"Validation failed: {err_msg}", timings
            
        # 3. Execute
        result = TOOL_REGISTRY[mapped_tool_name]["executor"](context, validated_params)
        result_text = str(result) if result else "Done."
        browser_time = 0.0 # simplified
        t_tool_end = time.perf_counter()"""

    content = content.replace(router_exec_target, router_exec_repl)
    
    # Also fix unknown tool check
    content = content.replace("not in GENERIC_ROUTER_TOOLS:", "not in ['open_app', 'focus_app', 'open_url', 'open_browser', 'web_search_play', 'web_search', 'type_text', 'type_anywhere', 'click', 'click_text']:")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def patch_task6_computer_control():
    filepath = 'task6_computer_control.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove cmd and powershell from _APP_LAUNCH
    content = re.sub(r'\s*"cmd":\s*"cmd\.exe",\n', '\n', content)
    content = re.sub(r'\s*"powershell":\s*"powershell\.exe",\n', '\n', content)

    # Patch the shell=True fallbacks in focus_app (around line 225)
    fallback_target = """        if exe.startswith("ms-") or ":" in exe and not exe[1] == ":":
            subprocess.Popen(["start", exe], shell=True)
        elif os.path.exists(exe):
            args = ["--processStart", "Discord.exe"] if "Discord" in exe and "Update" in exe else []
            subprocess.Popen([exe] + args)
        else:
            subprocess.Popen(exe, shell=True)"""
    fallback_repl = """        if exe.startswith("ms-") or (":" in exe and not exe[1] == ":"):
            import os
            os.startfile(exe)  # Safe way to open default handler without shell=True
        elif os.path.exists(exe):
            args = ["--processStart", "Discord.exe"] if "Discord" in exe and "Update" in exe else []
            subprocess.Popen([exe] + args)
        else:
            return ActionResult(success=False, error=f"Application path not found and shell execution is disabled: {exe}")"""
    content = content.replace(fallback_target, fallback_repl)
    
    start_target = """    # 3. Try via 'start' command with the name directly
    try:
        if not is_safe_executable(app_name):
            return ActionResult(success=False, error=f"Application name '{app_name}' contains unsafe characters.")
        subprocess.Popen(["start", "", app_name], shell=True) # start requires shell=True on windows but we validated app_name"""
    
    start_repl = """    # 3. Try via 'startfile' command with the name directly
    try:
        if not is_safe_executable(app_name):
            return ActionResult(success=False, error=f"Application name '{app_name}' contains unsafe characters.")
        if app_name.lower() in ["cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe"]:
            return ActionResult(success=False, error="Shell execution is strictly prohibited by security policy.")
        import os
        os.startfile(app_name) # startfile is safer than Popen with shell=True"""
    content = content.replace(start_target, start_repl)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def patch_browser_prompt_injection():
    filepath = 'execution/browser.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sanitize observation tags in read_page_content
    # The output format is: `[tag#id] text`
    target = """return `[${tag}${name ? '#'+name : ''}] ${text}`;"""
    repl = """return `[${tag}${name ? '#'+name : ''}] ${text.replace(/</g, "&lt;").replace(/>/g, "&gt;")}`;"""
    content = content.replace(target, repl)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def patch_desktop_prompt_injection():
    filepath = 'perception/desktop.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    target = """    # 3. Return the text lines found
    return "\\n".join(texts)"""
    repl = """    # 3. Return the text lines found (sanitized for prompt injection)
    sanitized = "\\n".join(texts).replace("<", "&lt;").replace(">", "&gt;")
    return sanitized"""
    content = content.replace(target, repl)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def patch_pipeline_orchestrator():
    filepath = 'planning/pipeline.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    target = """    allowed_actions = {
        "open_app", "type_text", "save_file", "open_folder", "rename_file",
        "move_file", "delete_file", "open_browser", "close_browser",
        "browser_go_back", "browser_go_forward", "fill_form", "run_calculator",
        "run_system_settings"
    }

    for step in plan:
        action = step.get("action")
        if action not in allowed_actions:
            print(f"Rejected plan: unknown action '{action}'")
            return False
        if action == "type_text" and "value" not in step:
            print("Rejected plan: type_text step missing 'value' field")
            return False
        if action == "save_file" and "filename" not in step:
            print("Rejected plan: save_file step missing 'filename' field")
            return False
        if action == "open_folder" and "folder" not in step:
            print("Rejected plan: open_folder step missing 'folder' field")
            return False
        if action == "rename_file" and ("old_name" not in step or "new_name" not in step):
            print("Rejected plan: rename_file step missing 'old_name' or 'new_name' field")
            return False
        if action == "move_file" and ("filename" not in step or "dest_folder" not in step):
            print("Rejected plan: move_file step missing 'filename' or 'dest_folder' field")
            return False
        if action == "delete_file" and "filename" not in step:
            print("Rejected plan: delete_file step missing 'filename' field")
            return False
        if action == "open_browser" and "url" not in step:
            print("Rejected plan: open_browser step missing 'url' field")
            return False
        if action == "fill_form" and "value" not in step:
            print("Rejected plan: fill_form step missing 'value' field")
            return False

    return True"""
    
    repl = """    from security.schemas import validate_tool_args
    for step in plan:
        action = step.get("action")
        if not action:
            print("Rejected plan: missing action")
            return False
        
        # Pydantic schemas use slightly different arg names sometimes, let's map them or validate them
        is_valid, err, validated = validate_tool_args(action, step)
        if not is_valid:
            print(f"Rejected plan: {err}")
            return False
            
    return True"""
    
    content = content.replace(target, repl)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
def delete_electron_apps():
    import os
    if os.path.exists("task6_electron_apps.py"):
        os.remove("task6_electron_apps.py")
        
    filepath = 'perception/desktop.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove _electron helper
    content = re.sub(r'def _electron.*?return result\.get\("message", "done"\)\n', '', content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    patch_agent_orchestrator()
    patch_agentic_py()
    patch_task6_computer_control()
    patch_browser_prompt_injection()
    patch_desktop_prompt_injection()
    patch_pipeline_orchestrator()
    delete_electron_apps()
    print("Refactoring complete.")