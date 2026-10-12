import os
import re

def add_logging_to_utils():
    with open('utils.py', 'r', encoding='utf-8') as f:
        content = f.read()

    logging_code = """
import logging
import uuid
import contextvars

# Context var for execution correlation
_execution_id = contextvars.ContextVar("execution_id", default=None)

def set_execution_id(exec_id: str = None) -> str:
    if not exec_id:
        exec_id = str(uuid.uuid4())[:8]
    _execution_id.set(exec_id)
    return exec_id

def get_execution_id() -> str:
    return _execution_id.get()

class ExecutionIDFilter(logging.Filter):
    def filter(self, record):
        eid = get_execution_id()
        record.execution_id = f"[{eid}] " if eid else ""
        return True

_logger_initialized = False

def get_logger(name: str) -> logging.Logger:
    global _logger_initialized
    logger = logging.getLogger(name)
    
    if not _logger_initialized:
        # Root logger setup
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Console handler (INFO level, no debug spam on console by default)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(execution_id)s%(levelname)s - %(name)s: %(message)s', datefmt='%H:%M:%S')
        ch.setFormatter(formatter)
        ch.addFilter(ExecutionIDFilter())
        
        root_logger.addHandler(ch)
        _logger_initialized = True
        
    return logger
"""

    # Add logging block after import win32gui
    content = re.sub(
        r'from config import Config\n',
        r'from config import Config\n' + logging_code,
        content
    )

    with open('utils.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    add_logging_to_utils()
