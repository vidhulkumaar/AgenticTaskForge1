import sys
import re

with open('task6_electron_apps.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(
    r'(?m)^WHATSAPP_EXE\s*=\s*os\.path\.join\([^)]+\)$', 
    'import sys\nimport os\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nfrom config import Config\n\nWHATSAPP_EXE = Config.WHATSAPP_EXE', 
    text
)

text = re.sub(
    r'(?m)^SPOTIFY_EXE\s*=\s*os\.path\.join\([^)]+\)$', 
    'SPOTIFY_EXE = Config.SPOTIFY_EXE', 
    text
)

text = re.sub(
    r'(?m)^DISCORD_EXE\s*=\s*os\.path\.join\([^)]+\)$', 
    'DISCORD_EXE = Config.DISCORD_EXE', 
    text
)

with open('task6_electron_apps.py', 'w', encoding='utf-8') as f:
    f.write(text)
