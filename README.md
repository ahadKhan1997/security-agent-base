# security-agent-base
security-agent-base

setup local env: 
    python -m venv .venv

run local env:
    .venv\Scripts\activate

install tools:
    pip install pydantic pydantic-settings httpx python-dotenv

run docker image of this project:
    cd security-agent-base
    docker compose down
    docker compose up --build -d

to see logs of docker:
    docker compose logs app


week 0:
💻 1. The Python Blueprint: Configuration & Execution

    built a script that safely pulls data from the internet using Asynchronous Programming and Data Ingestion Constraints.
    -------------------------------------------------------------------------------------------------
    | [.env File] ──► [config.py (Pydantic)] ──► [main.py (Async Worker)] ──► Enforces Types Loudly |
    -------------------------------------------------------------------------------------------------

    config.py: (Pydantic Settings)
        - used Pydantic's BaseSettings to ingest the environment variables (.env).
        -  In enterprise applications, missing database strings or invalid keys can crash an application deep into its runtime, causing data    corruption or silent failures. Pydantic acts as a strict cryptographic boundary gatekeeper. If an environment variable is missing or typed incorrectly (e.g., a number instead of a string), the app crashes instantly on startup. This concept is crucial for building secure systems that fail safely.

    main.py: (Asyncio + Httpx + Semaphore)
        -  wrote an asynchronous execution loop using httpx.AsyncClient capped by an asyncio.Semaphore(2).
        -  Standard Python code runs synchronously (line-by-line), meaning if it calls an AI model or API, the system freezes until it receives an answer. By using async, the app can fire off multiple API requests concurrently, leaving the CPU free to handle other tasks while waiting for data.
        - added a Semaphore(2). This strictly limits the system to a maximum of 2 parallel connection tasks. In AI applications, uncontrolled parallel tasks will instantly trigger rate limits or execute expensive API over-billing attacks. Built a defense against resource exhaustion.


🐳 2. The DevOps Blueprint: Multi-Stage Containers & Hardening

    Packaged the Python code into an isolated unit using Docker and attached it to an advanced data engine using Docker Compose.

    -------------------------------------------------------------------------------------------
    |    [BUILDER STAGE]  ──► Installs dependencies via root                                  |
    |       │                                                                                 |
    |       ▼ (Strips out package bloat and compiler tools)                                   |
    |       │                                                                                 |
    |    [RUNTIME STAGE]  ──► Copies ONLY packages ──► Drops down to 'appuser' (Non-Root)     |
    |                                                                                         |
    -------------------------------------------------------------------------------------------

    The Hardened Dockerfile (Multi-Stage Build):
        - Wrote a two-stage build file (FROM ... AS package-builder transitioning into a clean runtime layer) and added RUN useradd ... USER appuser.
        - Standard Docker containers run as the root user by default. If an attacker discovers a vulnerability in the code or a package dependency, they can breakout of the container and gain full control over the physical host server.
        - the first stage installs the tools. the second stage copies only the completed files and drops all root privileges to run as a restricted profile (appuser). If someone hacks the running app container, they are trapped inside an unprivileged sandbox with zero administrative control.
    
    The compose.yaml Layer (pgvector DB Orchestration):
        -  linked the application container to an advanced database variant running pgvector/pgvector:pg16 equipped with a automated dependency healthcheck.
        - Standard databases only search for direct keyword matches. pgvector is a specialized extension designed for Generative AI applications. It stores data as high-dimensional math blocks called vectors (embeddings), allowing the future AI agent to perform semantic semantic similarity search (e.g., reading a long cyber security report and finding similar historical vulnerability matches instantly).
    

🎯 Summary: 
    The Architectural Foundation By combining these elements:
        - A secure Git repo baseline that protects secrets from leaking.
        - An advanced async execution loop built to interact with AI agents without crashing or exhausting resources.
        - A hardened container footprint that protects the application architecture from potential root-privilege exploits.
        - A highly specialized AI database structure (pgvector) primed to act as the AI pipeline's memory core next week.