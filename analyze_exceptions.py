import os
import ast

def analyze_exceptions():
    results = []
    for root, _, files in os.walk('.'):
        if '.git' in root or '__pycache__' in root or 'venv' in root:
            continue
        for file in files:
            if not file.endswith('.py'):
                continue
            if 'refactor' in file or 'analyze' in file or 'append' in file or 'classify' in file:
                continue
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            try:
                tree = ast.parse(content)
            except SyntaxError:
                continue
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    is_broad = False
                    if node.type is None:
                        is_broad = True
                    elif isinstance(node.type, ast.Name) and node.type.id == 'Exception':
                        is_broad = True
                    
                    if is_broad:
                        # Find enclosing function
                        func_name = "<module>"
                        for parent in ast.walk(tree):
                            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                # Check if node is inside this function
                                if parent.lineno <= node.lineno <= parent.end_lineno:
                                    func_name = parent.name
                        
                        handler_body = ast.get_source_segment(content, node)
                        is_pass = False
                        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                            is_pass = True
                            
                        # Also check if it returns False/None
                        returns_false = False
                        for child in ast.walk(node):
                            if isinstance(child, ast.Return):
                                if isinstance(child.value, ast.Constant) and child.value.value in (False, None):
                                    returns_false = True
                                elif isinstance(child.value, ast.Dict):
                                    # check if it returns {"success": False}
                                    for k, v in zip(child.value.keys, child.value.values):
                                        if isinstance(k, ast.Constant) and k.value == "success":
                                            if isinstance(v, ast.Constant) and v.value == False:
                                                returns_false = True

                        results.append({
                            "file": path,
                            "function": func_name,
                            "line": node.lineno,
                            "is_pass": is_pass,
                            "returns_false": returns_false,
                            "code": handler_body
                        })
    
    with open('exception_audit.txt', 'w', encoding='utf-8') as f:
        for r in results:
            f.write(f"File: {r['file']} | Func: {r['function']} | Line: {r['line']} | Pass: {r['is_pass']} | Returns False/None: {r['returns_false']}\n")
            f.write(r['code'] + "\n")
            f.write("-" * 80 + "\n")
            
if __name__ == "__main__":
    analyze_exceptions()
