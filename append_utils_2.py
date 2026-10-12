with open('utils.py', 'a', encoding='utf-8') as f:
    f.write('''\nfrom dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ActionResult:
    success: bool
    message: str = ""
    error: Optional[str] = None
    data: Optional[Any] = None

    def __str__(self):
        if self.success:
            return self.message if self.message else "Success."
        return f"ERROR: {self.error or self.message}"
''')
