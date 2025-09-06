---
title: skillsculptor
app_file: app.py
sdk: gradio
sdk_version: 5.44.1
---
# SkillSculptor

Multi-agent workforce planning assistant that analyzes skills, identifies project staffing gaps, and suggests upskilling paths. A coordinator agent orchestrates specialized worker agents (skill matching, gap coverage, upskilling, reporting, and guardrails) and serves responses via a Gradio chat UI with optional short-term or long-term memory.

## Features
- Multi-agent orchestration via a coordinator
- Worker agents for skill matching, gap coverage, upskilling, reporting, and guardrails
- Gradio chat interface with streaming and memory mode toggle
- Sample data and generated reports saved locally

## Project structure
```
app.py                      # Gradio app + chat handler
worker_agents/              # Coordinator + worker agents
  coordinator.py
  skill_matching.py
  gap_coverage.py
  upskill.py
  reporter.py
  guardian.py
tools/                      # Tooling used by agents
ai_clients/                 # Model client(s), e.g., Gemini
utils/                      # Guardrails and utilities
data/                       # Sample CSV datasets (employees, projects, trends, upskill)
reports/                    # Generated reports (gap report, suggestions, violations)
requirements.txt            # Python dependencies
```

## Prerequisites
- Python 3.9–3.11 recommended
- API keys
  - Google Gemini: set `GOOGLE_API_KEY` (free; app can run solely on Gemini)
  - OpenAI (optional): set `OPENAI_API_KEY` to enable OpenAI tracing logs
  - Without `OPENAI_API_KEY`, the app still runs; OpenAI tracing is disabled

## Setup (Windows PowerShell)
```powershell
# From the repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Optionally store keys in a .env file at the project root
# (python-dotenv is included; many agent clients honor .env)
# Create .env with lines like:
# GOOGLE_API_KEY=...
# OPENAI_API_KEY=sk-...   # optional, only needed for OpenAI tracing logs
```

## Run locally
```powershell
# From the activated virtual environment
python app.py
```
- The app launches a Gradio UI (auto-opens browser). If not, open the printed `http://127.0.0.1:7860` URL.
- In the UI, choose memory mode (Short-term vs Long-term) and start chatting about staffing, skills, or gaps.

## Data and outputs
- Input data: CSVs in `data/`
- Generated reports: Markdown/text in `reports/`

## Tracing and observability
- The app emits traces (see `app.py` usage of `trace`). When `OPENAI_API_KEY` is set, traces are sent to OpenAI tracing logs for observability and debugging.
- If you omit `OPENAI_API_KEY`, the app still runs (especially with Gemini) and incurs no OpenAI cost; OpenAI tracing is simply disabled.

## Notes
- If you use Gemini, ensure `ai_clients/gemini_client.py` is configured and `GOOGLE_API_KEY` is set.
- To extend behavior, add/modify worker agents in `worker_agents/` and tools in `tools/`.
- Cost note: Running with Gemini only is free; OpenAI key is used for tracing, not required for core functionality.
