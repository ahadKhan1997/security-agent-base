# 🛡️ `security-agent-base` — Cybersecurity AI Agent Engine

A production-grade, asynchronous GenAI backend service that orchestrates stateful cybersecurity workflows using **LangGraph**, **FastAPI**, and **Groq LLM Cloud Inference**. 

The engine processes natural language security queries, dynamically executes specialized security tools (e.g., CVE database lookups and CVSS severity scoring), and provides grounded threat remediation advice.

---

## 🌟 Key Features

* **🤖 LangGraph State Machine**: Cyclic graph structure (`AgentState`) supporting autonomous tool-calling (`cve_lookup`, `calculate_severity`), dynamic conditional edge routing, and full conversation history persistence.
* **⚡ Live Groq LLM Inference**: Integrated directly with `ChatGroq` (`openai/gpt-oss-120b` / `qwen/qwen3.8-27b`) for ultra-fast, high-accuracy inference.
* **🛡️ Defensive Resilience & Key Sanitization**: Built-in `@property` key cleaner (`clean_groq_api_key`) in Pydantic Settings that automatically strips quote corruption from `.env` files. Features in-node `try/except` fallbacks so external API outages never crash the FastAPI service.
* **📚 Idempotent pgvector RAG Engine**: Grounded retrieval system utilizing SHA-256 text hashing (`hashlib.sha256`) to prevent duplicate document indexing in PostgreSQL/pgvector.
* **🚀 ASGI FastAPI Web Gateway**: Asynchronous REST endpoints (`/health` and `/agent/query`) with clean `lifespan` state initialization and cross-origin resource sharing (`CORSMiddleware`).

---

## 🛠️ Tech Stack

* **Language**: Python 3.11+
* **Framework**: FastAPI / Uvicorn (ASGI)
* **Agentic Orchestration**: LangGraph, LangChain Core
* **Inference Cloud**: Groq (`langchain-groq`)
* **Vector Store & Database**: PostgreSQL, `pgvector`, `langchain-postgres`, `psycopg3`
* **Configuration & Validation**: `pydantic-settings`
* **Testing**: `pytest`, `anyio`

---

## 🚀 Quickstart Guide

### 1. Repository Setup

```powershell
git clone https://github.com/your-username/security-agent-base.git
cd security-agent-base
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory (ensure values are unquoted):

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key
TARGET_MODEL=openai/gpt-oss-120b
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/cyber_db
```

### 3. Verify Groq API Authentication

```powershell
python test_groq_direct.py
```

### 4. Start the Server

```powershell
python main.py
```

The API will be available at `http://localhost:8000` (Interactive API Docs at `http://localhost:8000/docs`).

---

## 🧪 Testing

Execute offline unit tests powered by mock LLM builders:

```powershell
$env:PYTHONPATH="." ; pytest tests/
```

---

## 📡 API Reference

### `GET /health`
* **Description**: Verifies backend availability and graph engine initialization.
* **Response**: `{"status": "healthy"}`

### `POST /agent/query`
* **Description**: Submits a prompt to the LangGraph execution state engine.
* **Payload**:
  ```json
  {
    "question": "What is the details for CVE-2024-1234?"
  }
  ```
