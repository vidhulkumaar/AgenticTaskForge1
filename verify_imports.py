import importlib

modules_to_test = [
    "agent_orchestrator",
    "module5_orchestrator",
    "agent_context",
    "config",
    "utils",
    "security.schemas",
    "security.policy",
    "planning.llm_client",
    "planning.agentic",
    "planning.pipeline",
    "execution.desktop",
    "execution.browser",
    "execution.filesystem",
    "execution.system",
    "perception.desktop",
    "tools.registry",
    "tools.pipeline_registry"
]

failed = False
for mod in modules_to_test:
    try:
        importlib.import_module(mod)
        print(f"PASS: {mod}")
    except Exception as e:
        print(f"FAIL: {mod} -> {e}")
        failed = True

if failed:
    exit(1)
print("ALL IMPORTS PASSED.")
