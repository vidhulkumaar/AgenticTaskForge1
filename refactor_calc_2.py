import os
import re

def refactor_calc():
    with open('task3_1_calculator.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add ActionResult import
    content = re.sub(
        r'from utils import wait_for_window',
        r'from utils import wait_for_window, ActionResult',
        content
    )
    
    # evaluate_locally returning None
    content = re.sub(
        r'    except Exception:\n        return None',
        r'    except Exception as e:\n        raise RuntimeError(f"Local evaluation failed: {e}") from e',
        content
    )
    
    # run_task_3_1 currently returns float | str. We want it to return ActionResult.
    # We will wrap the successful return.
    content = re.sub(
        r'            return result',
        r'            return ActionResult(success=True, data=result, message=f"Result: {result}")',
        content
    )
    # The final return: return result_num if result_num is not None else ...
    content = re.sub(
        r'    if result_num is not None:\n        return result_num\n    return f"Calculated: {disp}"',
        r'    if result_num is not None:\n        return ActionResult(success=True, data=result_num, message=f"Calculated: {result_num}")\n    return ActionResult(success=True, message=f"Calculated: {disp}")',
        content
    )

    with open('task3_1_calculator.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    refactor_calc()
