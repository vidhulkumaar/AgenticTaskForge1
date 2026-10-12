import pytest
import os
from security.schemas import validate_tool_args
from security.policy import safe_path_join, is_safe_url, is_safe_executable

def test_schema_validation_valid():
    is_valid, err, validated = validate_tool_args("save_file", {"filename": "test.txt"})
    assert is_valid is True
    assert validated["filename"] == "test.txt"

def test_schema_validation_missing_arg():
    is_valid, err, validated = validate_tool_args("save_file", {})
    assert is_valid is False
    assert "validation failed" in err.lower() or "field required" in err.lower()

def test_schema_validation_unknown_tool():
    is_valid, err, validated = validate_tool_args("hack_system", {})
    assert is_valid is False
    assert "no defined schema" in err.lower()

def test_path_join_safe():
    path = safe_path_join("downloads", "test.txt")
    assert "test.txt" in path
    assert not path.startswith("C:\\test.txt")

def test_path_join_traversal():
    with pytest.raises(ValueError, match="Absolute paths|Path traversal"):
        safe_path_join("downloads", "../../Windows/System32/hal.dll")

def test_path_join_absolute():
    with pytest.raises(ValueError, match="Absolute paths|Path traversal"):
        safe_path_join("downloads", "C:\\Windows\\System32\\cmd.exe")

def test_url_validation_safe():
    is_safe, err = is_safe_url("https://www.google.com")
    assert is_safe is True

def test_url_validation_unsafe():
    is_safe, err = is_safe_url("javascript:alert(1)")
    assert is_safe is False
    assert "not allowed" in err

def test_executable_validation():
    assert is_safe_executable("notepad") is True
    assert is_safe_executable("calc.exe") is True
    assert is_safe_executable("calc && del C:\\Windows") is False
    assert is_safe_executable("cmd.exe /c start") is False
