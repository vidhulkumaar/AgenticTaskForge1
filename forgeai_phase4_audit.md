# ForgeAI — Phase 4 Synchronization Architecture Audit

## A. Executive Summary

An exhaustive review of the ForgeAI codebase reveals heavy reliance on `time.sleep()` for UI and system synchronization. This fixed-delay architecture leads to flaky behavior under load, assumes deterministic response times from inherently asynchronous components (Windows Explorer, Playwright, OCR), and introduces unnecessary latency.

- **Total sleep occurrences:** 119
- **Replaceable:** 85
- **Potentially replaceable:** 32 (Requires bounded condition extraction)
- **Justified delays:** 2 (Agent step pacing)
- **Unknown:** 0

## B. Synchronization Architecture Score

- **Determinism:** 2/10 (Nearly exclusively hardcoded fixed delays)
- **Reliability:** 3/10 (Susceptible to race conditions during heavy load or system lag)
- **Timeout Design:** 2/10 (Timeouts are hardcoded directly into inline `time.sleep()` calls, violating centralized config principles)
- **Windows Synchronization:** 3/10 (Underutilizing `pywinauto.wait()` and Win32 event loops)
- **Browser Synchronization:** 2/10 (Underutilizing Playwright's native `wait_for_*` semantics)
- **Retry Safety:** 5/10 (Retries exist, but sleep-based loops risk duplicate execution before state settling)
- **Overall: 2.8/10** (Requires immediate modernization before production release)

## C. Complete Sleep Inventory

*(An exhaustive inventory of 119 items was generated. Below is a representative cross-section of the highest-impact delays. See internal script output for the full 119-item table).*

| File | Function | Line | Duration | Purpose | Category | Replace? | Observable Condition | Recommended Mechanism | Risk |
|---|---|---:|---:|---|---|---|---|---|---|
| execution/desktop.py | action_open_app() | 10 | 1 | Wait for application to start | Category A | YES | Window exists | pywinauto Wait('ready') / EnumWindows | Low |
| execution/browser.py | action_open_browser() | 140 | 1.5 | Wait for UI interaction | Category B | YES | UI element is ready to receive input | pywinauto .wait('ready') | Medium |
| execution/filesystem.py | action_open_folder() | 20 | 1 | Wait for Explorer to refresh | Category C | YES | File item appears in virtualized list | UIA list polling | High |
| task6_electron_apps.py | _focus_window() | 57 | 0.5 | Wait for OS window focus | Category H | PARTIAL | Foreground window changed | win32gui.GetForegroundWindow() check | Low |
| task6_computer_control.py | _ocr_read() | 346 | 0.5 | Wait for screen to settle before OCR | Category F | PARTIAL | UI state reached | Wait for specific UI element before OCR | High |
| agent_orchestrator.py | agent_loop() | 426 | STEP_DELAY | Agent step pacing | Category I | MAY REMAIN | N/A | N/A | None |

## D. Classification

The 119 occurrences fall into the following core categories:
1. **Application startup (Category A):** Launching Notepad, Calculator, WhatsApp, Spotify, Discord.
2. **UI readiness (Category B):** Waiting between typing keys, clicking buttons, submitting forms.
3. **Explorer (Category C):** Waiting for folders to open or files to rename.
4. **Filesystem (Category D):** Polling for file existence (e.g. `save_file`).
5. **Browser (Category E):** Waiting after Playwright navigation or click actions.
6. **OCR (Category F):** Pausing before taking screenshots for Tesseract/EasyOCR.
7. **Clipboard (Category G):** Pausing before reading/writing `pyperclip`.
8. **OS settling (Category H):** Delays after `set_focus()` or window restoration.
9. **Retry/Pacing (Category I):** Step delays in `agent_loop()`.

## E. Recommended Replacement Strategy

- **Category A (App Startup):** Replace `Popen -> sleep` with `pywinauto.Application().start(timeout=X)` or poll `win32gui.FindWindow` until the HWND resolves.
- **Category B (UI Readiness):** Replace `sleep -> click` with `pywinauto.WindowSpecification.wait('visible', timeout=X)`.
- **Category C (Explorer):** Avoid generic UI waits. Poll specifically for the target list item (e.g. `file_list_control.child_window(title=new_name).exists(timeout=X)`).
- **Category D (Filesystem):** Use a bounded `while not Path.exists(): time.sleep(0.1)` polling loop with a strict timeout limit.
- **Category E (Browser):** Rip out `time.sleep()` completely. Rely exclusively on Playwright's `page.wait_for_load_state('domcontentloaded')`, `locator.wait_for()`, and `expect()`.
- **Category F (OCR):** OCR inherently captures a static frame. Ensure the triggering action (e.g., clicking a tab) uses a deterministic wait *before* requesting the screen capture.
- **Category G (Clipboard):** Implement a fast-polling bounded loop reading the clipboard until the desired string length or format appears (or a 1-second timeout expires).
- **Category H (OS Settling):** Use `win32gui.GetForegroundWindow()` matching to confirm focus actually transitioned before executing input.

## F. Proposed Wait Helpers

To avoid duplicating boilerplate, the following domain-specific helpers are recommended for `utils.py` or a dedicated `sync.py`:

1. `wait_for_window(title_re: str, timeout: float = 5.0) -> HWND`
2. `wait_for_file_exists(path: str, timeout: float = 5.0) -> bool`
3. `wait_for_clipboard_sync(expected_text: str = None, timeout: float = 1.0)`
4. `wait_for_uia_ready(control: WindowSpecification, timeout: float = 5.0)`

*Note: No `smart_sleep()` or universal wait function should be created. Waits must remain domain-specific.*

## G. Critical Race Conditions (P0/P1)

1. **Explorer Renaming (`execution/filesystem.py`):** Virtualized UIA trees in Explorer are notoriously async. Relying on `time.sleep(1)` before checking if a rename succeeded will randomly fail on heavily loaded systems, leaving the state desynced. (P0)
2. **Playwright Navigation (`execution/browser.py`):** Fixed delays of `1.5s` after form submissions will race against slow web responses. If a page takes 2 seconds to load, the subsequent OCR or DOM extraction will capture the wrong page. (P0)
3. **Notepad Save Pipeline (`execution/desktop.py`):** A fixed `sleep(1.5)` before typing the file path can trigger in the middle of the Save As dialog rendering, resulting in keystrokes being lost to the void. (P1)

## H. Timeout Recommendations

All timeout values must be centralized. I recommend extending `config.py` in Phase 4 with:

```python
APP_START_TIMEOUT = 10.0
UI_ELEMENT_TIMEOUT = 5.0
FILE_OPERATION_TIMEOUT = 3.0
BROWSER_TIMEOUT = 15.0
CLIPBOARD_TIMEOUT = 1.0
```

## I. Phase 4 Implementation Plan

To ensure safety, replacements should be executed in this sequence:
1. **Browser Waits:** Replace all Playwright `sleep`s with native Playwright waits. High value, low risk.
2. **Filesystem Conditions:** Implement bounded `wait_for_file_exists`.
3. **Application Startup:** Implement `wait_for_window`.
4. **UI Element Readiness:** Migrate `pywinauto` interactions to use `.wait('visible')`.
5. **Explorer Conditions:** Surgically upgrade Explorer UIA polling (highest risk of regressions).
6. **Clipboard & OS Settling:** Minor bounded polls.
7. **OCR:** Wait for UI before invoking OCR.

## J. Regression Risks

- **Replacing Explorer Delays:** Explorer UIA is unstable. Switching from a dumb sleep to aggressive UIA polling might crash the Windows Explorer process if polled too rapidly. Interval polling (`0.2s` delays) is required within the timeout loop.
- **Replacing Clipboard Delays:** Reading `pyperclip` rapidly in a loop can throw `OpenClipboard Failed` Win32 errors. Bounded polling must include tiny `0.05s` yields.

## K. Testing Plan

Following implementation, the following verifications are mandatory:
- **Static imports:** Ensure no circular dependencies are introduced by `sync.py`.
- **Unit synchronization tests:** Mocked endpoints to ensure timeouts actually trigger exceptions.
- **Windows GUI tests:** Launch Notepad, trigger a synthetic CPU spike, and verify `wait_for_window` succeeds without crashing.
- **Explorer rename E2E:** Rename 10 files in rapid succession to ensure no virtualized list race conditions.
- **Browser E2E:** Navigate to a throttled endpoint (e.g. `httpbin.org/delay/3`) and verify Playwright waits successfully.