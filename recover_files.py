import json
import os
import re

transcript_path = r"C:\Users\VIDHUL\.gemini\antigravity-ide\brain\777613d5-47b1-4273-a8c8-3d7d4dcc757c\.system_generated\logs\transcript_full.jsonl"

def recover_files():
    files_to_recover = [
        'agent_context.py', 'config.py', 'utils.py'
    ]
    
    norm_paths = {os.path.normpath(os.path.abspath(f)): f for f in files_to_recover}
    recovered = {}
    
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
                        if target:
                            target_norm = os.path.normpath(os.path.abspath(target))
                            if target_norm in norm_paths:
                                recovered[target_norm] = content
                                    
            elif data.get('type') == 'TOOL_RESPONSE':
                content = data.get('content', '')
                if 'File Path: `file:///' in content and 'The following code has been modified to include a line number' in content:
                    match = re.search(r'File Path: `file:///([^`]+)`', content)
                    if match:
                        path = match.group(1).replace('/', '\\')
                        path_norm = os.path.normpath(path)
                        if path_norm in norm_paths:
                            if 'The above content shows the entire, complete file contents' in content:
                                lines = content.split('\n')
                                code_lines = []
                                parsing = False
                                for l in lines:
                                    if l.startswith('The following code has been modified'):
                                        parsing = True
                                        continue
                                    if l.startswith('The above content shows the entire'):
                                        parsing = False
                                        continue
                                    if parsing:
                                        m = re.match(r'^\d+:\s(.*)$', l)
                                        if m:
                                            code_lines.append(m.group(1))
                                        elif l == "":
                                            pass
                                recovered[path_norm] = '\n'.join(code_lines)

    for path, code in recovered.items():
        rel = norm_paths[path]
        print(f"Recovered {rel} ({len(code)} bytes)")
        with open(rel, 'w', encoding='utf-8') as out:
            out.write(code)

if __name__ == "__main__":
    recover_files()