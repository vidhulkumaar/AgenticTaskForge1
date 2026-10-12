import sys
import re

with open('agent_orchestrator.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'(?m)^OLLAMA_URL\s*=\s*\".*?\"$', 
    'import os\nimport sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nfrom config import Config\n\n# Configuration moved to config.py', 
    text
)
text = re.sub(r'(?m)^OLLAMA_TAGS_URL\s*=\s*\".*?\"$\n', '', text)
text = re.sub(r'(?m)^OLLAMA_CHAT_URL\s*=\s*\".*?\"$\n', '', text)
text = re.sub(r'(?m)^ROUTER_MODEL\s*=\s*\".*?\"$\n', '', text)
text = re.sub(r'(?m)^MODEL_NAME\s*=\s*\".*?\"$\n', '', text)
text = re.sub(r'(?m)^LLM_TIMEOUT\s*=\s*.*?$\n', '', text)

text = text.replace('OLLAMA_URL', 'Config.OLLAMA_GENERATE_URL')
text = text.replace('OLLAMA_TAGS_URL', 'Config.OLLAMA_TAGS_URL')
text = text.replace('OLLAMA_CHAT_URL', 'Config.OLLAMA_CHAT_URL')
text = text.replace('MODEL_NAME', 'Config.OLLAMA_MODEL')
text = text.replace('ROUTER_MODEL', 'Config.OLLAMA_MODEL')
text = text.replace('LLM_TIMEOUT', 'Config.LLM_TIMEOUT')

with open('agent_orchestrator.py', 'w', encoding='utf-8') as f:
    f.write(text)
