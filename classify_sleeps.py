import os
import re

def classify_sleep(path, func, duration, context):
    context_lower = context.lower()
    
    if 'popen' in context_lower or 'start ' in context_lower or 'launch' in context_lower:
        return ('Wait for application to start', 'Category A', 'YES', 'Window exists', 'pywinauto Wait(ready) / EnumWindows', 'Low')
    elif 'os.path.exists' in context_lower or 'exist_ok' in context_lower:
        return ('Wait for file operation', 'Category D', 'YES', 'Path.exists() == True', 'Bounded while loop poll', 'Low')
    elif 'page.' in context_lower or 'browser' in context_lower:
        return ('Wait for page navigation', 'Category E', 'YES', 'DOM loaded or element visible', 'Playwright wait_for_selector / wait_for_url', 'Low')
    elif 'pyperclip' in context_lower or '^c' in context_lower:
        return ('Wait for clipboard to sync', 'Category G', 'YES', 'Clipboard contains value', 'Bounded loop checking pyperclip.paste()', 'Medium')
    elif 'click' in context_lower or 'type_keys' in context_lower or 'send_keys' in context_lower or 'fill' in context_lower or 'press' in context_lower:
        return ('Wait for UI interaction', 'Category B', 'YES', 'UI element is ready to receive input', 'pywinauto .wait(ready)', 'Medium')
    elif 'explorer' in context_lower:
        return ('Wait for Explorer to refresh', 'Category C', 'YES', 'File item appears in virtualized list', 'UIA list polling', 'High')
    elif 'ocr' in context_lower or 'click_text' in context_lower:
        return ('Wait for screen to settle before OCR', 'Category F', 'PARTIAL', 'UI state reached', 'Wait for specific UI element before OCR', 'High')
    elif 'set_focus' in context_lower:
        return ('Wait for OS window focus', 'Category H', 'PARTIAL', 'Foreground window changed', 'win32gui.GetForegroundWindow() check', 'Low')
    elif 'step_delay' in context_lower or 'agent_loop' in context_lower:
        return ('Agent step pacing', 'Category I', 'MAY REMAIN', 'N/A', 'N/A', 'None')
    else:
        return ('Unknown delay', 'Other', 'PARTIAL', 'Unknown', 'Requires manual inspection', 'Medium')

sleep_pattern = re.compile(r'(?:time\.)?sleep\(([^)]+)\)')
lines_md = []
for root, dirs, files in os.walk('.'):
    if any(skip in root for skip in ['venv', '__pycache__', '.git', 'scratch']): continue
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file).replace('.\\', '')
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines):
                        m = sleep_pattern.search(line)
                        if m:
                            dur = m.group(1).strip()
                            func = 'unknown'
                            for j in range(i, -1, -1):
                                if lines[j].strip().startswith('def '):
                                    func = lines[j].strip().split('def ')[1].split('(')[0]
                                    break
                            ctx = ''.join(lines[max(0, i-3):min(len(lines), i+2)]).strip()
                            purp, cat, repl, cond, mech, risk = classify_sleep(path, func, dur, ctx)
                            lines_md.append(f'| {path} | {func}() | {i+1} | {dur} | {purp} | {cat} | {repl} | {cond} | {mech} | {risk} |')
            except Exception: pass

with open('inventory_full.md', 'w', encoding='utf-8') as f:
    f.write('| File | Function | Line | Duration | Purpose | Category | Replace? | Observable Condition | Recommended Mechanism | Risk |\n')
    f.write('|---|---|---:|---:|---|---|---|---|---|---|\n')
    for l in lines_md: f.write(l + '\n')
