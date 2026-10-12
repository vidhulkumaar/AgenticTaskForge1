# ForgeAI — Phase 6 Stage A: Observability, Testing & Reliability Architecture Audit

## 1. Executive Summary
ForgeAI's current architecture operates entirely without automated tests (0% coverage) and relies on unstructured `print()` statements for all observability. While Phases 1–5 successfully built a deterministic, robust, and safe execution engine, Phase 6 must now implement professional logging, privacy redaction, and a test suite. The system perfectly maintains its closed-loop, local, offline nature, but requires structured diagnostics to be provably reliable.

## 2. Current Observability Architecture
Observability is currently limited to `stdout` via `print()` calls scattered across the repository. There is no usage of Python's standard `logging` module, no log levels, no correlation IDs linking actions to a parent goal, and no persistence of logs to disk for post-mortem debugging.

## 3. Logging Audit
- **Findings**: Hundreds of `print()` statements act as the sole diagnostic tool.
- **Classification**:
  - *INFO*: `print(f"  Action: click on '{target}'")`
  - *DEBUG*: `print(f"  Available monitors: {len(monitors)}")`
  - *ERROR*: `print(f"  [ERROR] Ollama server returned HTTP status...")`
- **Deficiencies**: Lacks timestamps, standardized formatting, verbosity controls, and output routing. 

## 4. Action Lifecycle Trace
The lifecycle (Goal → Plan → Selected tool → Arguments → Execution → Observation → Verification → ActionResult) is currently traced sequentially in stdout by `agent_orchestrator.py`. However, because there are no Execution IDs or Correlation IDs, if multiple agents or threads were to run, or if a user needed to parse the logs programmatically, it would be impossible to isolate a specific action's lifecycle reliably.

## 5. ActionResult Consistency Audit
Phase 5 successfully introduced `ActionResult`. 
- **Consistent Paths**: All `execution/*` modules and `task6_computer_control.py` primitives correctly return `ActionResult`. The agent loop consumes this correctly.
- **Legacy Paths**: Standalone legacy modules (`task2_4`, `task3_2`, `task2_5`) return dictionaries internally for CLI compatibility. However, because they are isolated and either wrapped by `execution/` modules or completely bypassed by the agent loop, they do not pollute the core Agent-Tool contract.
- **Conclusion**: The Phase 5 `ActionResult` contract is successfully enforced at the architectural boundary.

## 6. Agent Loop Audit
The agent loop (`agent_orchestrator.py`) prints the current step, the observation summary, the LLM's raw response, the parsed decision, and the action result. 
- **Observable**: Current step, selected action, arguments, failure classification.
- **Missing**: Explicit "Retry" tags (retries are only inferred by seeing a new step after an `ERROR:` result). 
- **Privacy Violation**: The raw LLM output and the screen observation text are printed in plaintext, potentially leaking sensitive user data to the console.

## 7. LLM Observability Audit
`planning/llm_client.py` captures HTTP errors, timeouts, and JSON parsing failures. It distinguishes between an unreachable server (`Timeout`) and an invalid response (`JSONDecodeError`). Retries are correctly observed (`LLM timed out... retrying...`). No API keys or tokens are logged (the system uses local Ollama).

## 8. Verification Audit
Verifications (e.g., `wait_for_file_exists` after saving) are currently observed as part of the tool's execution print statements (e.g., `print(f"  Typed value. Verified: '{actual}'")`). While functional, verification lacks a distinct log event separate from the action execution, making it harder to parse "Action Succeeded but Verification Failed."

## 9. Retry/Recovery Observability
Retries are agent-driven. The orchestrator records `ERROR: {exc}` into the history, and the LLM decides the next step. 
- **Deficiency**: The system cannot explicitly explain *why* it chose to retry versus taking a different path, as the LLM's internal reasoning is not heavily logged (only its final JSON decision is parsed). There is no explicit "Recovery Attempt X" metric.

## 10. Testing Architecture
- **Unit Test Coverage**: 0% (No `tests/` directory, no `pytest` usage).
- **Integration Test Coverage**: 0%.
- **GUI/E2E Coverage**: 0%.
- **Assessment**: The complete lack of automated testing is the largest risk to reliability. Core logic (`planning`, `utils`, `config`, `ActionResult`) can and must be unit-tested without Windows UI dependencies immediately.

## 11. Mockability Analysis
The system has hard dependencies on `requests` (Ollama), `pywinauto` (Windows UI), and `subprocess`. 
- `config.py` and `utils.py` are highly mockable.
- `planning/llm_client.py` can be mocked using `responses` or `unittest.mock.patch` on `requests.post`.
- `execution/` modules require heavy patching of `pywinauto` which is notoriously difficult to mock cleanly. E2E tests on a controlled CI runner are recommended over deep unit-mocking for UI actions.

## 12. Offline Dependency Audit
- **PASS**. The repository contains no hidden telemetry, analytics, or external cloud API calls. `requests` is strictly used for `localhost:11434` (Ollama). 

## 13. Privacy / Sensitive Data Audit
- **CRITICAL VIOLATION**: `action_type_text` logs `print(f"  Action: type '{value}' into...")`. If a user asks the agent to type a password, it is logged in plaintext.
- **CRITICAL VIOLATION**: `observation_summary(obs)` prints screen OCR contents which may contain private messages or documents.
- **Recommendation**: Introduce a `is_secret=True` parameter to typing actions to redact logs, and truncate/redact OCR output in general logs.

## 14. Crash & Cleanup Audit
`AgentContext.cleanup()` is well-implemented (logging warnings instead of swallowing). However, the main `while True:` loop in `agent_orchestrator.py` lacks a `finally: context.cleanup()` block. A crash in the orchestrator can bypass cleanup, leaking browser or pywinauto processes.

## 15. Performance Observability
The Single-Pass router tracks `model_time`, `tool_time`, and `browser_time`. The multi-step loop only tracks total task time. Granular metrics for OCR latency and UI tree discovery are missing, making performance bottlenecks hard to diagnose.

## 16. Configuration / Hardcoding Audit
- All Phase 1 configuration rules are respected.
- **Violation Found**: `MAX_STEPS = 15` is hardcoded in `agent_orchestrator.py` instead of utilizing `config.py`.

## 17. Phase 1–5 Regression Check
- Phase 1 Configuration: **PASS**
- Phase 2 Context State: **PASS**
- Phase 3 Modularity: **PASS**
- Phase 4 Synchronization: **PASS**
- Phase 5 Error Handling: **PASS**

## 18. Recommended Architecture
1. **Logging System**: Replace `print()` with Python's standard `logging` module. Introduce a `ForgeLogger` wrapper in `utils.py`.
2. **Testing Suite**: Create `tests/unit/` and `tests/integration/` directories using `pytest`.
3. **Contextual Observability**: Add an `execution_id` to `AgentContext` to correlate logs.

```text
Orchestrator [Logger: INFO]
      ↓ (execution_id: 1234)
Planning [Logger: DEBUG]
      ↓
Tools [Logger: INFO]
      ↓ (is_secret=True)
Execution [Logger: DEBUG] -> Redacts sensitive values
      ↓
ActionResult
```

## 19. Implementation Plan

**P0 — Critical**
- **Test Infrastructure**: Setup `pytest`, `tests/` directory, and write unit tests for `config`, `utils`, and `ActionResult`. (Risk: Low).
- **Structured Logging**: Replace all `print()` calls with standard `logging` (`logger.info`, `logger.debug`). (Risk: Low).

**P1 — High**
- **Privacy Redaction**: Add `is_secret` parameter to `type_text` tools. Redact sensitive values from logs. (Risk: Low).
- **Crash Safety**: Wrap the `agent_orchestrator.py` execution loop in a `try/finally` block invoking `context.cleanup()`. (Risk: Low).
- **Config Fix**: Move `MAX_STEPS` to `config.py`. (Risk: Low).

**P2 — Medium**
- **Action Correlation**: Inject `execution_id` into `AgentContext` for log tracing. (Risk: Low).
- **Mocking**: Implement `unittest.mock` for the LLM client to ensure routing logic can be tested without Ollama running. (Risk: Medium).

**P3 — Optional**
- **Granular Metrics**: Add timing decorators to OCR and UI tree discovery functions. (Risk: Low).

## 20. Hardcoding Audit
- New hardcoded paths: 0
- New hardcoded URLs: 0
- New hardcoded model names: 0
- New hardcoded retry values: 0
- New hardcoded timeout values: 0
- New hardcoded coordinates: 0
- New credentials/secrets: 0

**Existing Violations to Fix in Stage B:**
- `MAX_STEPS = 15` hardcoded in `agent_orchestrator.py`.
