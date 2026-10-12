import os
import re

def refactor_llm_config():
    with open('config.py', 'r', encoding='utf-8') as f:
        config_content = f.read()

    config_content = re.sub(
        r'    MAX_RETRIES = int\(os\.getenv\("MAX_RETRIES", "10"\)\)',
        r'    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "10"))\n    LLM_RETRIES = int(os.getenv("LLM_RETRIES", "2"))',
        config_content
    )

    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)

    with open('planning/llm_client.py', 'r', encoding='utf-8') as f:
        llm_content = f.read()

    llm_content = re.sub(
        r'LLM_RETRIES',
        r'Config.LLM_RETRIES',
        llm_content
    )

    with open('planning/llm_client.py', 'w', encoding='utf-8') as f:
        f.write(llm_content)

    # Also check agent_orchestrator.py, it still has LLM_RETRIES = 2 defined but not used?
    with open('agent_orchestrator.py', 'r', encoding='utf-8') as f:
        orch = f.read()
    orch = re.sub(r'LLM_RETRIES\s*=\s*2.*?\n', '', orch)
    with open('agent_orchestrator.py', 'w', encoding='utf-8') as f:
        f.write(orch)

if __name__ == "__main__":
    refactor_llm_config()
