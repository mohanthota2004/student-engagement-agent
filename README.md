
# Student Engagement & Participation Enhancement (Agentic AI)

## Overview
This project is a starter scaffold that demonstrates an Agentic AI engagement facilitator using **FastAPI** as the backend and **LangChain** (placeholder code) for analyzing student interactions. The frontend is a simple HTML+CSS+JS interface that allows submitting forum posts or conversation snippets and receiving suggested interventions.

**What you get in this ZIP:**
- `app/` - FastAPI app with endpoints and a simple integration point for a LangChain agent.
- `agents/` - Example LangChain agent code (requires OpenAI key and internet to run).
- `static/` - CSS and minimal client JS.
- `templates/` - HTML templates (Jinja2).
- `requirements.txt` - Python dependencies.
- `run_uvicorn.bat` and `run_uvicorn.sh` - helper scripts to start the server.
- `sample_data/` - example forum snippets for testing.

## Quick start (local)

1. Create a python venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # mac/linux
   .\.venv\Scripts\activate # windows (PowerShell)
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) If using OpenAI through LangChain, set environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```
4. Run the app:
   ```bash
   # linux / mac
   ./run_uvicorn.sh
   # windows
   run_uvicorn.bat
   ```
5. Open http://127.0.0.1:8000 in your browser.

## Notes
- LangChain and OpenAI usage in `agents/langchain_agent.py` are examples/placeholders. Replace or extend them to call real models or your local LLM.
- This scaffold intentionally keeps the agent simple so you can iterate quickly.
