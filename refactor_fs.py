import os
import re

def refactor_filesystem():
    with open('execution/filesystem.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add ActionResult import
    content = re.sub(
        r'from utils import get_known_folder_path, wait_for_window',
        r'from utils import get_known_folder_path, wait_for_window, ActionResult, wait_for_file_exists',
        content
    )

    # Convert returns to ActionResult
    content = re.sub(
        r'def action_open_folder\(context: AgentContext, folder: str\) -> str:',
        r'def action_open_folder(context: AgentContext, folder: str) -> ActionResult:',
        content
    )
    content = re.sub(
        r'            return f"Opened File Explorer at: \{folder_path\}"\n        except Exception:\n            pass\n    return f"Opened File Explorer at \{folder_path\} \(could not connect to UIA\)\."',
        r'            return ActionResult(success=True, message=f"Opened File Explorer at: {folder_path}")\n        except Exception as e:\n            return ActionResult(success=True, message=f"Opened File Explorer at {folder_path} (could not connect to UIA: {e}).")\n    return ActionResult(success=False, error=f"Could not find opened File Explorer window for {folder_path}.")',
        content
    )

    content = re.sub(
        r'def action_rename_file\(context: AgentContext, old_name: str, new_name: str, folder: str = "downloads"\) -> str:',
        r'def action_rename_file(context: AgentContext, old_name: str, new_name: str, folder: str = "downloads") -> ActionResult:',
        content
    )
    
    rename_replace = r'''
    if not os.path.exists(old_path):
        if os.path.exists(new_path):
            return ActionResult(success=True, message=f"File already renamed to '{new_name}' in {folder_path}.")
        return ActionResult(success=False, error=f"Source file not found: {old_path}")
    if os.path.exists(new_path):
        return ActionResult(success=False, error=f"Destination file already exists: {new_path}")
    try:
        os.rename(old_path, new_path)
    except Exception as e:
        return ActionResult(success=False, error=f"Rename failed: {e}")
    if wait_for_file_exists(new_path):
        return ActionResult(success=True, message=f"Renamed '{old_name}' to '{new_name}' in {folder_path}.")
    return ActionResult(success=False, error=f"Rename executed but could not verify '{new_name}' exists.")
'''
    content = re.sub(
        r'    if not os\.path\.exists\(old_path\):\n        raise FileNotFoundError\(f"File not found: \{old_path\}"\)\n    os\.rename\(old_path, new_path\)\n    return f"Renamed \'\{old_name\}\' to \'\{new_name\}\' in \{folder_path\}\."',
        rename_replace.strip(),
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'def action_move_file\(context: AgentContext, filename: str, source_folder: str, dest_folder: str\) -> str:',
        r'def action_move_file(context: AgentContext, filename: str, source_folder: str, dest_folder: str) -> ActionResult:',
        content
    )
    move_replace = r'''
    if not os.path.exists(src_path):
        if os.path.exists(dst_path):
            return ActionResult(success=True, message=f"File already moved to {dest_folder}.")
        return ActionResult(success=False, error=f"Source file not found: {src_path}")
    try:
        shutil.move(src_path, dst_path)
    except Exception as e:
        return ActionResult(success=False, error=f"Move failed: {e}")
    if wait_for_file_exists(dst_path):
        return ActionResult(success=True, message=f"Moved '{filename}' from {source_folder} to {dest_folder}.")
    return ActionResult(success=False, error=f"Move executed but could not verify file at {dst_path}.")
'''
    content = re.sub(
        r'    if not os\.path\.exists\(src_path\):\n        raise FileNotFoundError\(f"Source file not found: \{src_path\}"\)\n    shutil\.move\(src_path, dst_path\)\n    return f"Moved \'\{filename\}\' from \{source_folder\} to \{dest_folder\}\."',
        move_replace.strip(),
        content,
        flags=re.DOTALL
    )

    content = re.sub(
        r'def action_delete_file\(context: AgentContext, filename: str, folder: str = "downloads"\) -> str:',
        r'def action_delete_file(context: AgentContext, filename: str, folder: str = "downloads") -> ActionResult:',
        content
    )
    delete_replace = r'''
    if not os.path.exists(path):
        return ActionResult(success=True, message=f"File already deleted or missing: {path}")
    try:
        os.remove(path)
    except Exception as e:
        return ActionResult(success=False, error=f"Delete failed: {e}")
    if not os.path.exists(path):
        return ActionResult(success=True, message=f"Deleted '{filename}' from {folder_path}.")
    return ActionResult(success=False, error=f"Delete executed but file still exists at {path}.")
'''
    content = re.sub(
        r'    if not os\.path\.exists\(path\):\n        raise FileNotFoundError\(f"File not found: \{path\}"\)\n    os\.remove\(path\)\n    return f"Deleted \'\{filename\}\' from \{folder_path\}\."',
        delete_replace.strip(),
        content,
        flags=re.DOTALL
    )

    with open('execution/filesystem.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_filesystem()
