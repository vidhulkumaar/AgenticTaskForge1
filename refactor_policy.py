import os
import re

def patch_security_policy():
    filepath = 'security/policy.py'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    target = """def is_safe_executable(executable: str) -> bool:
    \"\"\"Ensures an executable string doesn't contain shell injection.\"\"\"
    if not executable:
        return False
    # Allow only alphanumeric, dashes, underscores, spaces, dots (for .exe)
    if not re.match(r"^[a-zA-Z0-9_\-\.\ ]+$", executable):
        return False
    return True"""
    
    repl = """def is_safe_executable(executable: str) -> bool:
    \"\"\"Ensures an executable string doesn't contain shell injection or invoke prohibited shells.\"\"\"
    if not executable:
        return False
    # Allow only alphanumeric, dashes, underscores, spaces, dots (for .exe)
    if not re.match(r"^[a-zA-Z0-9_\-\.\ ]+$", executable):
        return False
        
    lower_exe = executable.strip().lower()
    prohibited_shells = ["cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe", "bash", "bash.exe", "wsl", "wsl.exe", "sh", "sh.exe"]
    if lower_exe in prohibited_shells:
        return False
        
    return True"""
    
    content = content.replace(target, repl)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    patch_security_policy()
    print("Policy patched.")