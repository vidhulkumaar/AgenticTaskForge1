import os
import re

def refactor_task25():
    with open('task2_5_nl_pipeline.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Add ActionResult import
    content = re.sub(
        r'from typing import Optional, List',
        r'from typing import Optional, List\nfrom utils import ActionResult',
        content
    )
    
    # In execute_file_operation
    replace_block = r'''
        if operation in op_map:
            result = op_map[operation]()
            if isinstance(result, ActionResult):
                if not result.success:
                    return {"success": False, "error": result.error or result.message}
            return {"success": True, "operation": operation}
        else:
'''
    
    content = re.sub(
        r'        if operation in op_map:\n            op_map\[operation\]\(\)\n            return \{"success": True, "operation": operation\}\n        else:',
        replace_block.strip(),
        content,
        flags=re.DOTALL
    )

    with open('task2_5_nl_pipeline.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_task25()
