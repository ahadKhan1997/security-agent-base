# Commands & Environment Operations

### Install specialized libraries for LangGraph, FastAPI, and Groq integration:
```powershell
pip install langgraph langchain-groq fastapi uvicorn pydantic-settings anyio pytest ruff
```

### Direct test for Groq API authentication and active model verification:
```powershell
python test_groq_direct.py
```

### Execute the FastAPI application with embedded LangGraph engine:
```powershell
python main.py
```

### Query the agent endpoint using native PowerShell (`Invoke-RestMethod`):
```powershell
$res = Invoke-RestMethod -Uri "http://localhost:8000/agent/query" -Method Post -ContentType "application/json" -Body '{"question": "What is the details for CVE-2024-1234?"}'
$res.response
```

### Query the agent endpoint using `curl.exe` with single-quoted `--data-raw`:
```powershell
curl.exe -X POST "http://localhost:8000/agent/query" -H "Content-Type: application/json" --data-raw '{"question": "What is the details for CVE-2024-1234?"}'
```

### Clear stale process environment variable overrides in PowerShell:
```powershell
Remove-Item Env:\GROQ_API_KEY
```

### Verify test coverage across asynchronous agent graph workflows:
```powershell
$env:PYTHONPATH="." ; pytest tests/
```

---

# security-agent-base — Week 3

## 🦜 1. The GenAI Blueprint: Agentic Workflows with LangGraph & FastAPI

This week, you engineered a production-grade, state-driven security agent backend using **LangGraph** and **FastAPI**. Unlike linear chains, this agent utilizes a cyclic graph structure with state persistence (`AgentState`) that autonomously decides when to invoke tool functions (e.g., `cve_lookup`, `calculate_severity`) and when to synthesize final responses.

```text
                      ┌───────────────────────────┐
                      │          START            │
                      └─────────────┬─────────────┘
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │        agent Node         │ ◄──┐
                      │    (LLM + Tool Binding)   │    │
                      └─────────────┬─────────────┘    │
                                    │                  │
                                    ▼                  │ (Tool Output)
                       /─────────────────────────\     │
                      <  should_continue (Edge)   >    │
                       \─────────────────────────/     │
                            │               │          │
                 (Tools)    │               │ (END)    │
                            ▼               ▼          │
              ┌──────────────────┐     ┌───────────┐   │
              │    tools Node    │     │    END    │   │
              │  (cve_lookup /   │     └───────────┘   │
              │calculate_severity)                     │
              └─────────────┬──────────────────────────┘
                            │
                            └──────────────────────────┘
```

* **Cyclic State Engine (`AgentState`)**
  * **What you did:** Defined a `TypedDict` state schema using `Annotated[list[BaseMessage], add_messages]` as a message reducer to maintain full conversational history across state transitions.
  * **The "Why":** Standard state objects overwrite properties upon updates. Adding `add_messages` allows new message outputs from LLMs and tools to append sequentially, giving the model complete historical context for multi-step reasoning.

* **Dynamic Tool Binding & Routing**
  * **What you did:** Bound specialized tools (`cve_lookup`, `calculate_severity`) to `ChatGroq` via `bind_tools()`. Engineered a conditional edge (`should_continue`) that inspects the latest `AIMessage` for `tool_calls` and dynamically routes state to either the `tools` execution node or `END`.
  * **The "Why":** Hardcoded decision trees fail on complex cybersecurity queries. Binding tools directly to the model empowers the LLM to dynamically determine its execution plan based on input intent.

* **Asynchronous FastAPI Service Integration**
  * **What you did:** Exposed the compiled state machine via a POST endpoint (`/agent/query`), passing request bodies asynchronously into `await compiled_graph.ainvoke(input_state)`.
  * **The "Why":** Wrapping the graph inside an ASGI FastAPI architecture allows remote clients, frontends, or automated pipelines to interact with the security agent asynchronously over HTTP with complete data validation (`Pydantic`).

---

## 🔧 2. The Infrastructure & Resiliency Blueprint: Key Sanitization & Fallback Routing

Runtime cloud API failures (e.g., decommissioned models, 401 authentication errors, or quote-corrupted environment keys) can crash web services. You implemented defensive safeguards in `config.py` and `agent_graph.py` to keep the application resilient.

* **Automated API Key Sanitization in Pydantic Settings**
  * **What you did:** Added a custom `@property` (`clean_groq_api_key`) to the Pydantic `Settings` class that strips accidental double quotes (`"`), single quotes (`'`), and leading/trailing whitespace from `.env` values.
  * **The "Why":** Windows command line tools and `.env` editors frequently wrap keys in quotes (e.g., `GROQ_API_KEY="gsk_..."`). When passed to cloud clients like Groq, these quotes are included in HTTP Bearer headers, resulting in `401 Unauthorized` errors. Cleaning keys programmatically eliminates authentication failures at boot time.

* **In-Node Exception Defense & Local Fallback Execution**
  * **What you did:** Wrapped the `ainvoke` call within `call_model` in a `try/except` block. If Groq API calls fail (e.g., `404 model_not_found` due to key/entitlement issues), the node intercepts the exception and executes a deterministic local fallback using `AIMessage` or `FakeListChatModel`.
  * **The "Why":** External API downtime or rate limits should never crash a production web server. Catching invocation exceptions directly inside graph nodes guarantees that `/agent/query` returns a graceful `200 OK` response rather than a `500 Internal Server Error`.

* **PowerShell Process Environment Isolation**
  * **What you did:** Identified and resolved stale process variable overrides using `Remove-Item Env:\GROQ_API_KEY`.
  * **The "Why":** PowerShell process environment variables (`$env:VAR`) take precedence over `.env` files parsed by `pydantic-settings`. Clearing shell-cached variables ensures Python loads fresh credentials directly from `.env`.

---

## 🛠️ 3. The Windows CLI & Shell Encoding Blueprint: Command Formatting Hotfixes

Windows PowerShell introduces distinct behaviors regarding command aliases, quote escaping, and text encoding during HTTP client operations.

* **PowerShell `curl` Alias vs. Native Binary (`curl.exe`)**
  * **What you did:** Replaced standard `curl` commands in PowerShell with native `curl.exe --data-raw` or PowerShell's `Invoke-RestMethod`.
  * **The "Why":** PowerShell aliases `curl` to `Invoke-WebRequest`, which treats `-H` strings as invalid parameter bindings. Using `curl.exe` directly executes the real binary, while `--data-raw '...'` prevents PowerShell from stripping escaped quotes in JSON payloads.

* **Terminal Output Truncation & UTF-8 Encoding Resolution**
  * **What you did:** Fixed `â` display artifacts and table truncation (`...`) by extracting the response property directly (`$res.response`) and configuring UTF-8 console output encoding (`[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`).
  * **The "Why":** PowerShell's default `Format-Table` truncates wide text strings, and Windows PowerShell 5.1 decodes incoming HTTP responses using legacy Windows-1252 encoding. Explicit property extraction and encoding enforcement ensure clean, un-truncated UTF-8 output.

---

## 🧪 4. DevSecOps Testing Blueprint: Offline State Validation

* **Mock-Grounded Test Collection (`pytest` + `anyio`)**
  * **What you did:** Configured unit tests in `tests/test_agent_graph.py` to inject mock LLM instances (`FakeListChatModel`) into `build_agent_graph(llm=...)`.
  * **The "Why":** Unit and integration tests must run quickly, deterministically, and offline in CI/CD pipelines without incurring cloud API costs or failing due to external network instability.

---

## 🎯 Week 3 Technical Architectural Summary

By implementing these structural patterns, you have expanded your ecosystem:
* **Compiled LangGraph State Machine:** Cyclic graph supporting autonomous tool calls and structured message states.
* **Live Groq Integration:** Asynchronous execution against active models (`openai/gpt-oss-120b`, `qwen/qwen3.8-27b`) via `ChatGroq`.
* **Defensive Error Shielding:** Key sanitization and localized node fallback ensuring server uptime during cloud API outages.
* **FastAPI Application:** RESTful web service serving state transitions via `/agent/query`.
* **Cross-Platform CLI Stability:** Hardened command-line workflows across PowerShell, `curl.exe`, and UTF-8 decoders.