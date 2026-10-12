import os
import re

def refactor_llm_log():
    with open('planning/llm_client.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add get_logger
    content = re.sub(
        r'from typing import Optional, Any, Dict, List, Tuple',
        r'from typing import Optional, Any, Dict, List, Tuple\nfrom utils import get_logger\n\nlogger = get_logger(__name__)',
        content
    )

    content = re.sub(
        r'print\(f"  \[LLM\] \{last_err\} — retrying\.\.\."\)',
        r'logger.warning(f"[LLM] {last_err} — retrying...")',
        content
    )

    content = re.sub(
        r'print\(f"  \[Startup\] Checking Ollama server at \{Config\.OLLAMA_TAGS_URL\}\.\.\."\)',
        r'logger.info(f"[Startup] Checking Ollama server at {Config.OLLAMA_TAGS_URL}...")',
        content
    )

    content = re.sub(
        r'print\(f"\\n  \[ERROR\] Ollama server returned HTTP status (.*?)"\)',
        r'logger.error(f"Ollama server returned HTTP status \1")',
        content
    )

    content = re.sub(
        r'print\("  Please make sure Ollama server is running \(\'ollama serve\'\)\.\\n"\)',
        r'logger.error("Please make sure Ollama server is running (\'ollama serve\').")',
        content
    )

    content = re.sub(
        r'print\(f"\\n  \[ERROR\] Ollama server is NOT reachable at (.*?)"\)',
        r'logger.error(f"Ollama server is NOT reachable at \1")',
        content
    )

    content = re.sub(
        r'print\(f"  \[Startup\] Preloading router model (.*?)"\)',
        r'logger.info(f"[Startup] Preloading router model \1")',
        content
    )

    content = re.sub(
        r'print\(f"  \[Startup\] Model (.*?) preloaded and ready \((.*?)\)\."\)',
        r'logger.info(f"[Startup] Model \1 preloaded and ready (\2).")',
        content
    )

    content = re.sub(
        r'print\(f"  \[WARNING\] Preloading (.*?) returned HTTP (.*?)"\)',
        r'logger.warning(f"Preloading \1 returned HTTP \2")',
        content
    )

    content = re.sub(
        r'print\(f"  \[WARNING\] Could not preload model (.*?): \{exc\}"\)',
        r'logger.warning(f"Could not preload model \1: {exc}")',
        content
    )

    with open('planning/llm_client.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_llm_log()
