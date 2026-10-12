import os
import re

def refactor_module5():
    filepath = 'module5_orchestrator.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove ACTION_FUNCTIONS import
    content = content.replace("from tools.pipeline_registry import ACTION_FUNCTIONS", "from tools.registry import TOOL_REGISTRY")
    
    # In run_command, we need to validate and execute using TOOL_REGISTRY
    target = """    if not validate_plan(plan):
        print("\\nPlan was rejected for safety reasons. Aborting.")
        return

    print("\\nExecuting plan step by step...\\n")
    for i, step in enumerate(plan, start=1):
        print(f"--- Step {i}/{len(plan)} ---")
        ACTION_FUNCTIONS[step["action"]](context, step)"""
        
    repl = """    from security.schemas import validate_tool_args
    # Let's validate the whole plan first to fail fast
    validated_plan = []
    for step in plan:
        action = step.get("action")
        is_valid, err, validated = validate_tool_args(action, step)
        if not is_valid:
            print(f"\\nPlan was rejected for safety reasons ({err}). Aborting.")
            return
        validated_plan.append((action, validated))

    print("\\nExecuting plan step by step...\\n")
    for i, (action, validated_params) in enumerate(validated_plan, start=1):
        print(f"--- Step {i}/{len(plan)} ---")
        TOOL_REGISTRY[action]["executor"](context, validated_params)"""
        
    content = content.replace(target, repl)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_module5()
    print("Module 5 refactored.")