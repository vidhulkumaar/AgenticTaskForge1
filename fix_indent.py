with open('task6_computer_control.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "from utils import wait_for_clipboard_sync, wait_for_window, ActionResult\n\nfrom utils import get_logger\nlogger = get_logger(__name__)\n\n    \n    tess_path",
    "    from utils import wait_for_clipboard_sync, wait_for_window, ActionResult\n\n    from utils import get_logger\n    logger = get_logger(__name__)\n\n    \n    tess_path"
)

with open('task6_computer_control.py', 'w', encoding='utf-8') as f:
    f.write(content)
