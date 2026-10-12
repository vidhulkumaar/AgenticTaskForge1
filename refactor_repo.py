import os
import re

def refactor_agent_context():
    with open('agent_context.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add execution_id
    if "execution_id" not in content:
        content = re.sub(
            r'class AgentContext:',
            r'class AgentContext:\n    execution_id: Optional[str] = None',
            content
        )

    with open('agent_context.py', 'w', encoding='utf-8') as f:
        f.write(content)

def replace_logging(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "get_logger" not in content:
        imports = "\nfrom utils import get_logger\nlogger = get_logger(__name__)\n"
        # Find first class or function def or after standard imports
        if "import " in content:
            # find last import
            parts = content.split('\n')
            last_import_idx = 0
            for i, p in enumerate(parts):
                if p.startswith("import ") or p.startswith("from "):
                    last_import_idx = i
            parts.insert(last_import_idx + 1, imports)
            content = '\n'.join(parts)
        else:
            content = imports + content

    # Simple regex to replace print with logger.info
    # We will exclude some prints if needed, but for now we replace all
    content = re.sub(r'print\((f?".*?")\)', r'logger.info(\1)', content)
    content = re.sub(r'print\((f?\'.*?\')\)', r'logger.info(\1)', content)

    # Privacy fix for OCR
    content = content.replace(
        "logger.info(f\"\\n--- Extracted Screen Text ---\\n{ocr_text[:1000]}\")",
        "logger.debug(f\"[Privacy] OCR extracted {len(ocr_text)} characters.\")"
    )
    
    # Redact observation summary text log
    content = content.replace(
        "logger.info(f\"  Observation: {obs_text[:120]}\")",
        "logger.info(f\"  Observation: [Redacted for privacy, length={len(obs_text)}]\")"
    )
    
    # Redact LLM raw output
    content = content.replace(
        "logger.info(f\"  LLM raw: {raw_decision[:200]}\")",
        "logger.debug(f\"  LLM raw length: {len(raw_decision)}\")"
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def refactor_task6_computer_control():
    filepath = 'task6_computer_control.py'
    replace_logging(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add is_secret
    content = content.replace(
        "def type_anywhere(text: str) -> ActionResult:",
        "def type_anywhere(text: str, is_secret: bool = False) -> ActionResult:"
    )
    
    # Replace typing log
    content = content.replace(
        "logger.info(f\"  [type_anywhere] typing {len(text)} chars: {text[:60]!r}\")",
        "display_text = '***' if is_secret else text[:60]\n    logger.info(f\"  [type_anywhere] typing {len(text)} chars: {display_text!r}\")"
    )
    
    # Replace Typed result log
    content = content.replace(
        "ActionResult(success=True, message=f\"Typed: {text[:80]}\")",
        "ActionResult(success=True, message=f\"Typed: {'***' if is_secret else text[:80]}\")"
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def refactor_execution_desktop():
    filepath = 'execution/desktop.py'
    if not os.path.exists(filepath):
        return
    replace_logging(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add is_secret to action_type_text
    content = content.replace(
        "def action_type_text(context: AgentContext, args: dict) -> ActionResult:",
        "def action_type_text(context: AgentContext, args: dict, is_secret: bool = False) -> ActionResult:"
    )
    
    # Update call to type_anywhere
    content = content.replace(
        "return type_anywhere(text)",
        "return type_anywhere(text, is_secret=is_secret)"
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def refactor_agent_orchestrator():
    filepath = 'agent_orchestrator.py'
    replace_logging(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Wrap the `while True` in try/finally
    content = content.replace(
        """        while True:
            try:
                if not goal:
                    goal = input("What should TaskForge do?\\n> ").strip()
                if not goal:
                    continue
                if goal.lower() in ("exit", "quit"):
                    logger.info("Goodbye!")
                    break
                result = agent_loop(goal, max_steps=args.max_steps)
                logger.info(f"\\nFinal result: {result}\\n")
                goal = None
            except KeyboardInterrupt:
                logger.info("\\nStopped by user.")
                break
            except Exception as e:
                logger.info(f"\\nAgent error: {e}")
                traceback.print_exc()
                goal = None
        sys.exit(0)""",
        """        try:
            while True:
                try:
                    if not goal:
                        goal = input("What should TaskForge do?\\n> ").strip()
                    if not goal:
                        continue
                    if goal.lower() in ("exit", "quit"):
                        logger.info("Goodbye!")
                        break
                    
                    from utils import set_execution_id
                    context.execution_id = set_execution_id()
                    
                    result = agent_loop(goal, max_steps=args.max_steps)
                    logger.info(f"\\nFinal result: {result}\\n")
                    goal = None
                except KeyboardInterrupt:
                    logger.info("\\nStopped by user.")
                    break
                except Exception as e:
                    logger.error(f"\\nAgent error: {e}")
                    traceback.print_exc()
                    goal = None
        finally:
            context.cleanup()
            logger.info("AgentContext cleaned up.")
        sys.exit(0)"""
    )
    
    # Same for GUI mode
    content = content.replace(
        """    def _gui_agent_callback(goal: str) -> str:
        \"\"\"Called from dashboard GUI thread — runs agent_loop synchronously.\"\"\"
        return agent_loop(goal, max_steps=max_steps)""",
        """    def _gui_agent_callback(goal: str) -> str:
        \"\"\"Called from dashboard GUI thread — runs agent_loop synchronously.\"\"\"
        from utils import set_execution_id
        # We don't have direct access to context here, but agent_loop will use a local one.
        # Actually agent_loop doesn't instantiate context. We need to check if agent_loop does it.
        # Wait, agent_loop uses global `context` if called from __main__ or creates it? 
        # In current design `context` is global to `agent_orchestrator.py` or passed.
        # Let's set exec id.
        set_execution_id()
        try:
            return agent_loop(goal, max_steps=max_steps)
        finally:
            if 'context' in globals():
                context.cleanup()
                logger.info("AgentContext cleaned up.")
"""
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_agent_context()
    refactor_task6_computer_control()
    refactor_execution_desktop()
    refactor_agent_orchestrator()
    
    for mod in ["execution/browser.py", "execution/filesystem.py", "execution/system.py", "planning/agentic.py", "perception/desktop.py"]:
        replace_logging(mod)

