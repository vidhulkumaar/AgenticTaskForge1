import json
import os

transcript_path = r"C:\Users\VIDHUL\.gemini\antigravity-ide\brain\777613d5-47b1-4273-a8c8-3d7d4dcc757c\.system_generated\logs\transcript_full.jsonl"

def replay_edits():
    # First, restore to clean git state again to ensure a clean slate
    os.system("git restore .")
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except:
                continue
            
            if data.get('type') == 'PLANNER_RESPONSE':
                for tc in data.get('tool_calls', []):
                    name = tc.get('name', '')
                    args = tc.get('args', {})
                    
                    if name in ['default_api:write_to_file', 'write_to_file']:
                        target = args.get('TargetFile', '')
                        content = args.get('CodeContent', '')
                        if target and content:
                            target_norm = os.path.normpath(os.path.abspath(target))
                            os.makedirs(os.path.dirname(target_norm), exist_ok=True)
                            with open(target_norm, 'w', encoding='utf-8') as out:
                                out.write(content)
                                
                    elif name in ['default_api:replace_file_content', 'replace_file_content']:
                        target = args.get('TargetFile', '')
                        t_content = args.get('TargetContent', '')
                        r_content = args.get('ReplacementContent', '')
                        if target and t_content and r_content:
                            target_norm = os.path.normpath(os.path.abspath(target))
                            if os.path.exists(target_norm):
                                with open(target_norm, 'r', encoding='utf-8') as tf:
                                    text = tf.read()
                                if t_content in text:
                                    text = text.replace(t_content, r_content)
                                    with open(target_norm, 'w', encoding='utf-8') as tf:
                                        tf.write(text)
                                else:
                                    print(f"Warning: TargetContent not found in {target}")
                                    
                    elif name in ['default_api:multi_replace_file_content', 'multi_replace_file_content']:
                        target = args.get('TargetFile', '')
                        chunks = args.get('ReplacementChunks', [])
                        if target and chunks:
                            target_norm = os.path.normpath(os.path.abspath(target))
                            if os.path.exists(target_norm):
                                with open(target_norm, 'r', encoding='utf-8') as tf:
                                    text = tf.read()
                                for chunk in chunks:
                                    t_content = chunk.get('TargetContent', '')
                                    r_content = chunk.get('ReplacementContent', '')
                                    if t_content in text:
                                        text = text.replace(t_content, r_content)
                                    else:
                                        print(f"Warning: Chunk TargetContent not found in {target}")
                                with open(target_norm, 'w', encoding='utf-8') as tf:
                                    tf.write(text)
                                    
                    elif name in ['default_api:run_command', 'run_command']:
                        cmd = args.get('CommandLine', '')
                        # only execute our refactoring scripts!
                        if cmd.startswith('python refactor_') or cmd.startswith('python append_') or cmd.startswith('python update_') or cmd.startswith('python extract_') or cmd.startswith('python rewrite_') or cmd.startswith('python fix_') or cmd == 'python verify_imports.py':
                            # Actually, don't run verify_imports.py if it was empty, it will crash.
                            # Just run the scripts.
                            if cmd != 'python verify_imports.py':
                                print(f"Executing: {cmd}")
                                os.system(cmd)

if __name__ == "__main__":
    replay_edits()