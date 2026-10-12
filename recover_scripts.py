import json
import os

transcript_path = r"C:\Users\VIDHUL\.gemini\antigravity-ide\brain\777613d5-47b1-4273-a8c8-3d7d4dcc757c\.system_generated\logs\transcript_full.jsonl"

def recover_all_scripts():
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except:
                continue
                
            if data.get('type') == 'PLANNER_RESPONSE':
                for tc in data.get('tool_calls', []):
                    name = tc.get('name', '')
                    if name in ['default_api:write_to_file', 'write_to_file']:
                        args = tc.get('args', {})
                        target = args.get('TargetFile', '')
                        content = args.get('CodeContent', '')
                        if target and content and target.endswith('.py'):
                            target_norm = os.path.normpath(os.path.abspath(target))
                            # Avoid recovering over things that shouldn't be recovered from old transcript
                            if os.path.basename(target) not in ['verify_imports.py', 'recover_scripts.py', 'rerun_refactors.py', 'e2e_test.py']:
                                print(f"Recovering {target_norm}")
                                os.makedirs(os.path.dirname(target_norm), exist_ok=True)
                                with open(target_norm, 'w', encoding='utf-8') as out:
                                    out.write(content)

if __name__ == "__main__":
    recover_all_scripts()
