import json
import re
import os

transcript_path = r"C:\Users\VIDHUL\.gemini\antigravity-ide\brain\777613d5-47b1-4273-a8c8-3d7d4dcc757c\.system_generated\logs\transcript_full.jsonl"

def run_in_order():
    executed = []
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except:
                continue
            if data.get('type') == 'PLANNER_RESPONSE':
                for tc in data.get('tool_calls', []):
                    name = tc.get('name', '')
                    if name in ['default_api:run_command', 'run_command']:
                        args = tc.get('args', {})
                        cmd = args.get('CommandLine', '')
                        if cmd.startswith('python refactor_') or cmd.startswith('python append_') or cmd.startswith('python update_') or cmd.startswith('python extract_') or cmd.startswith('python rewrite_') or cmd.startswith('python fix_'):
                            script = cmd.split(' ')[1]
                            if script.endswith('.py'):
                                executed.append(script)
    
    import subprocess
    idx = 0
    for i, s in enumerate(executed):
        if s == 'rewrite_orchestrators.py':
            idx = i + 1
            break
            
    for script in executed[idx:]:
        print(f"Running {script}...")
        res = subprocess.run(['python', script], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error in {script}:\n{res.stderr}")
        else:
            print(f"Success: {script}")

if __name__ == "__main__":
    run_in_order()
