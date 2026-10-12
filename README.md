# AgenticTaskForge

AgenticTaskForge is an autonomous AI agent framework designed to perceive desktop and browser environments, parse natural language queries, execute window and tab navigation, dynamically discover and populate form fields on live websites, interact with desktop app UI controls, read on-screen content via OCR, and perform closed-loop verification.

## Features

- **Offline / Local AI Brain**: Supports local LLM orchestration and planners via Ollama / Phi-3.
- **Browser Automation**: Active Chrome dispatch, Playwright fallback, and semantic DOM locating.
- **Desktop & Screen Perception**: Desktop UI interaction, screen reading, and OCR-based verification.
- **Modular Pipeline & Policy Engine**: Structured multi-step task planning, failure propagation handling, and security policies.

## Installation

```bash
git clone https://github.com/vidhulkumaar/AgenticTaskForge1.git
cd AgenticTaskForge1
pip install -r requirements.txt
```

## Quick Start

```bash
python agent_orchestrator.py
```
