import os
import re

def find_sleeps():
    sleep_pattern = re.compile(r'(?:time\.)?sleep\(([^)]+)\)')
    results = []
    for root, dirs, files in os.walk('.'):
        if 'venv' in root or '__pycache__' in root or '.git' in root or 'scratch' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        m = sleep_pattern.search(line)
                        if m:
                            duration = m.group(1)
                            # get 3 lines of context before and 1 after
                            context = ''.join(lines[max(0, i-3):min(len(lines), i+2)]).strip()
                            results.append({
                                'file': path,
                                'line': i+1,
                                'duration': duration,
                                'context': context
                            })
    with open('sleep_report.txt', 'w', encoding='utf-8') as f:
        for r in results:
            f.write(f"File: {r['file']} | Line: {r['line']} | Duration: {r['duration']}\n")
            f.write(f"Context:\n{r['context']}\n")
            f.write('-'*80 + '\n')

if __name__ == '__main__':
    find_sleeps()