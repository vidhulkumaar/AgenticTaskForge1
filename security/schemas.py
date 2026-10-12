from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
import re

class OpenAppParams(BaseModel):
    pass

class TypeTextParams(BaseModel):
    value: str

class SaveFileParams(BaseModel):
    filename: str

class OpenFolderParams(BaseModel):
    folder: str

class RenameFileParams(BaseModel):
    old_name: str
    new_name: str
    folder: Optional[str] = "downloads"

class MoveFileParams(BaseModel):
    filename: str
    dest_folder: str
    source_folder: Optional[str] = "downloads"

class DeleteFileParams(BaseModel):
    filename: str
    folder: Optional[str] = "downloads"

class OpenBrowserParams(BaseModel):
    url: str

class CloseBrowserParams(BaseModel):
    pass

class FillFormParams(BaseModel):
    field: str
    value: str
    submit: Optional[bool] = False

class ClickBrowserElementParams(BaseModel):
    selector: Optional[str] = None
    text: Optional[str] = None
    role: Optional[str] = None

class ReadPageContentParams(BaseModel):
    pass

class RunCalculatorParams(BaseModel):
    expression: str

class RunSystemSettingsParams(BaseModel):
    command: str

class ReadScreenParams(BaseModel):
    find: Optional[str] = ""

class DownloadFileParams(BaseModel):
    url: str
    filename: Optional[str] = ""
    folder: Optional[str] = "downloads"

class FocusAppParams(BaseModel):
    app_name: str

class PressKeyParams(BaseModel):
    key: str

class TypeAnywhereParams(BaseModel):
    text: str

class ClickTextParams(BaseModel):
    text: str
    occurrence: Optional[int] = 1

class ClearInputParams(BaseModel):
    pass

class GoalCompletedParams(BaseModel):
    summary: Optional[str] = "Goal completed."

class GoalFailedParams(BaseModel):
    reason: Optional[str] = "Unknown reason."


# Map tool names to Pydantic models
TOOL_SCHEMAS = {
    "open_app": OpenAppParams,
    "type_text": TypeTextParams,
    "save_file": SaveFileParams,
    "open_folder": OpenFolderParams,
    "rename_file": RenameFileParams,
    "move_file": MoveFileParams,
    "delete_file": DeleteFileParams,
    "open_browser": OpenBrowserParams,
    "close_browser": CloseBrowserParams,
    "fill_form": FillFormParams,
    "click_browser_element": ClickBrowserElementParams,
    "read_page_content": ReadPageContentParams,
    "run_calculator": RunCalculatorParams,
    "run_system_settings": RunSystemSettingsParams,
    "read_screen": ReadScreenParams,
    "download_file": DownloadFileParams,
    "focus_app": FocusAppParams,
    "press_key": PressKeyParams,
    "type_anywhere": TypeAnywhereParams,
    "click_text": ClickTextParams,
    "clear_input": ClearInputParams,
    "goal_completed": GoalCompletedParams,
    "goal_failed": GoalFailedParams
}

def validate_tool_args(tool_name: str, args: dict) -> tuple[bool, str, dict]:
    """
    Validates arguments against the Pydantic schema for the given tool.
    Returns (success, error_message, validated_dict)
    """
    if tool_name not in TOOL_SCHEMAS:
        return False, f"Validation failed: Tool '{tool_name}' has no defined schema.", {}
    
    schema_cls = TOOL_SCHEMAS[tool_name]
    try:
        validated = schema_cls(**args)
        return True, "", validated.model_dump()
    except Exception as e:
        return False, f"Argument validation failed for '{tool_name}': {e}", {}
