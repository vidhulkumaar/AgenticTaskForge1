# ForgeAI — Phase 5 Stage A: Error Handling & Failure Recovery Architecture Audit

## A. Executive Summary

This audit assesses the error handling, failure recovery, and retry architecture of ForgeAI. The system relies heavily on the LLM loop for recovery, but low-level tools often hide failures or provide inconsistent return types, leading to false success signals. 

- **Total exception handlers**: ~84
- **Broad exception handlers (`except Exception:`)**: ~70
- **Silent exception handlers (`pass`)**: 22
- **Potential false-success paths**: 15
- **Retry loops**: Handled primarily via the LLM agent loop; a few internal hardcoded retries exist for LLM generation.
- **Unbounded retry risks**: LLM retry on non-idempotent actions (e.g., typing) can cause repeated keystrokes.
- **Cleanup risks**: 3 (AgentContext cleanup swallows errors).

### Priorities:
- **P0**: False-success paths returning `""` or `False` without context, and missing idempotency in typing operations.
- **P1**: Inconsistent error return types across tools (strings vs JSON vs exceptions).
- **P2**: Silent `pass` blocks in UI traversal paths.
- **P3**: Cleanup failures being swallowed.

---

## B. Failure Architecture

Currently, ForgeAI employs a **heterogeneous failure architecture**:
1. **Low-Level Tools (Task 2/3)**: Often return dicts `{"success": False, "error": str(e)}`.
2. **Mid-Level Execution (execution/*)**: Often return strings `f"ERROR: {e}"` or `f"Action failed: {e}"`, or raise `RuntimeError`.
3. **Agent Loop (`agent_orchestrator.py`)**: Catches exceptions from tools, converts them to strings, and appends them to the history for the LLM to read on the next iteration.
4. **LLM Loop Recovery**: The LLM acts as the recovery engine. If an action fails, the LLM reads the error and decides the next step.

**Flaw**: Because return types are inconsistent, the LLM sometimes receives ambiguous failure messages or believes an action succeeded when it failed (e.g., if a function returns `None` or `""` on error, which the LLM interprets as success). Furthermore, there is no formal mechanism to reverse or reset state before the LLM retries non-idempotent actions.

---

## C. Complete Failure Inventory

| # | File | Function | Failure Mechanism | Current Behavior | Risk | Severity | Recommended Handling |
|---|---|---|---|---|---|---|---|
| 1 | `task6_electron_apps.py` | `_ocr_read` | OCR fails or missing deps | Returns `""` | Agent assumes screen is blank, hallucinates success or gets stuck | P0 | Raise or return explicit error string to agent |
| 2 | `task3_1_calculator.py` | `evaluate_locally` | Local eval fails | Returns `None` | Agent assumes success but no value | P1 | Return error dict |
| 3 | `agent_context.py` | `cleanup` | Playwright/Process close fails | `pass` | Leaves orphan processes; hides underlying driver crashes | P3 | Log failure, do not interrupt outer flow |
| 4 | `task2_1_browser_navigation.py` | `open_in_active_system_chrome` | Dispatch fails | Returns `False` | Agent gets boolean, no context | P1 | Return specific error message |
| 5 | `execution/browser.py` | `action_download_file` | Download fails | Returns `Download failed: {e}` | Safe, but unstructured | P2 | Unify return structure |
| 6 | `task6_computer_control.py` | `type_anywhere` | Pyautogui/Clipboard fails | Returns `Typing failed: {e}` | Safe, but unstructured | P2 | Unify return structure |
| 7 | `task3_2_system_settings.py` | `handle_with_ai_powershell` | LLM HTTP error | Returns JSON with `success: False` | Agent must parse JSON | P2 | Unify return structure |
| 8 | `execution/desktop.py` | `action_save_file` | Overwrite dialog unclickable | `pass` | Waits for file exists, times out, returns unconfirmed save | P1 | Explicitly check if dialog is blocking |

---

## D. Exception Handling Problems

1. **Information Loss (Silent Failures):**
   - `except Exception: pass` is frequently used in `agent_context.cleanup()`. If a browser context crashes, the crash is silently ignored during cleanup.
   - UI traversal (e.g., `execution/desktop.py` overwrite dialog) uses `pass`. If the dialog is partially obscured, the agent silently skips clicking "Yes" and waits for a file that will never save.
   
2. **Inconsistent Propagation:**
   - Some tools `raise RuntimeError`.
   - Some return `{"success": False, "error": "..."}`.
   - Some return string messages `f"Error: {e}"`.
   The `agent_orchestrator.py` handles this by stringifying whatever comes back. This is somewhat robust but makes programmatic verification impossible.

---

## E. Retry & Idempotency Analysis

The LLM is currently the retry engine. This is dangerous for non-idempotent actions.

| Action | Class | Retry Danger | State Reset Required |
|---|---|---|---|
| `type_anywhere` / `type_text` | Non-Idempotent | Retrying appends text (e.g., `JohnJohn`) | `clear_input()` via `ctrl+a`, `del` |
| `press_key` | Non-Idempotent | Multiple submits, dialog spam | Must re-perceive screen state |
| `click_text` | Non-Idempotent | May click wrong element if screen shifted | Must re-perceive OCR layout |
| `open_browser` | Idempotent | None (creates new tab if already open) | None |
| `save_file` | Conditionally Idempotent | Overwrite dialog requires different flow | Check for file existence first |
| `rename_file` | Conditionally Idempotent | Target may already exist | Verify old/new name existence |

**Dangerous Path**:
If `type_text` fails halfway through, the agent will loop, see the failure, and issue `type_text` again. The resulting text will be corrupted.

---

## F. Recovery Architecture

The proposed architecture relies on the existing LLM loop but introduces a **Structured Result Pattern** and **State Reset Primitives**.

```text
                    ┌─────────────┐
                    │   TOOL      │
                    └──────┬──────┘
                           ↓
                       EXCEPTION?
                      /        \
                   YES          NO
                    ↓            ↓
             CATCH & FORMAT    VERIFY
                    ↓            ↓
          RETURN ActionResult  RETURN ActionResult
                    ↓            ↓
            AGENT LOOP APPENDS TO HISTORY
                    ↓
        LLM READS HISTORY, CLASSIFIES FAILURE
                    ↓
    LLM INVOKES STATE RESET TOOL (e.g. clear_input)
                    ↓
        LLM RETRIES OR TRIES NEW STRATEGY
```

### Proposed Changes (Not to be implemented yet):
1. **ActionResult Class**: A simple local dataclass (e.g., `success: bool, message: str, error: str = None`) used by ALL tools to prevent the LLM from guessing what a boolean or `None` means.
2. **State Reset Tools**: Provide the LLM with explicit recovery tools (`clear_focused_input`, `close_top_dialog`) so it can reset state before retrying.

---

## G. Failure/Retry Matrix

| Exception/Failure | Where | Expected? | Recoverable? | Propagate? | Log? | Recovery Strategy |
|---|---|---|---|---|---|---|
| `FileNotFoundError` | Filesystem | Yes | Yes | Return to LLM | Yes | LLM searches for correct path |
| `TimeoutError` | UI Element | Yes | Yes | Return to LLM | Yes | LLM re-perceives UI or scrolls |
| `Playwright Timeout` | Browser | Yes | Yes | Return to LLM | Yes | LLM refreshes page or goes back |
| `RuntimeError` | LLM HTTP | No | Yes | Abort Step | Yes | Orchestrator pauses, retries LLM |
| `Exception` (Cleanup) | AgentContext | No | Yes | Swallow | Yes | Log to dashboard, continue |

---

## H. Logging Audit

- **Current State**: Uses `print()` exclusively. Errors are printed directly to `sys.stdout`.
- **Sensitive Data Risk**: When UI typing fails, the error message sometimes includes the text being typed (e.g., `print(f"Typing failed: {text}")`). If this text contains credentials, it is printed to the terminal.
- **Tracebacks**: Preserved in `agent_orchestrator.py` via `traceback.print_exc()`, which is good for debugging but clutters the terminal.

---

## I. Configuration Audit

Most timeouts were centralized to `config.py` in Phase 4. However, LLM retry logic (`LLM_RETRIES = 2`) is still hardcoded in `agent_orchestrator.py`. 
No arbitrary polling intervals were found remaining (they were replaced with bounded UI waits in Phase 4).

---

## J. Testing Plan (For Stage B)

Stage B should implement Pytest suites for:
1. **Failure Injection**: Mock `subprocess.Popen` to fail, ensuring `focus_app` returns a properly structured failure instead of raising uncaught exceptions.
2. **Idempotency Verification**: Test that calling `type_text` twice triggers a `clear_input` operation, or that the LLM is correctly prompted to clear first.
3. **False-Success Prevention**: Ensure `_ocr_read` failure throws/returns a specific error state rather than an empty string.

---

## K. Priority Roadmap

- **P0**: Standardize return values (`ActionResult`) across `task6_electron_apps`, `task2_4`, and `execution` modules to prevent false successes. Fix `_ocr_read` empty string return.
- **P1**: Add `clear_input` tool or automatic clearing for `type_text` to fix non-idempotent retries.
- **P2**: Move `LLM_RETRIES` to `config.py`. Convert `print()` statements in exception handlers to structured dashboard logs.
- **P3**: Improve `cleanup()` blocks to log exceptions instead of silently passing.

---

**NO-CODE-CHANGE VERIFICATION:**
- Production files modified: 0
- Retry counts changed: 0
- Timeouts changed: 0
- LLM prompts changed: 0
- Action behavior changed: 0
- Architecture changed: 0