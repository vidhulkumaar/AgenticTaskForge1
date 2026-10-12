import os

def patch_task2_1():
    filepath = 'task2_1_browser_navigation.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    target = """        cmd = f'start chrome "{url}"'
        subprocess.Popen(cmd, shell=True)"""
    repl = """        import webbrowser
        webbrowser.open(url)"""
    content = content.replace(target, repl)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def patch_task2_4():
    filepath = 'task2_4_desktop_interaction.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = """        subprocess.Popen([app_hint], shell=True)"""
    repl = """        import os
        if os.path.exists(app_hint) or os.path.exists(app_hint + '.exe'):
            subprocess.Popen([app_hint])
        else:
            os.startfile(app_hint)"""
    content = content.replace(target, repl)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    patch_task2_1()
    patch_task2_4()
    print("Legacy files patched.")