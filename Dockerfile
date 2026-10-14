# Stage 1: Build phase
FROM python:3.12-slim AS package-builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    pydantic \
    pydantic-settings \
    httpx \
    python-dotenv \
    langchain \
    langchain-groq \
    langchain-postgres \
    pgvector \
    "psycopg[binary]" \
    langchain-community \
    langchain-huggingface \
    sentence-transformers \
    sqlalchemy \
    fastapi \
    uvicorn

ENV HF_HOME=/app/.cache/huggingface
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Stage 2: Hardened Runtime environment
FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=package-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=package-builder /usr/local/bin /usr/local/bin
COPY --from=package-builder /app/.cache /app/.cache

RUN useradd -u 1001 -m appuser && chown -R appuser /app
USER appuser

ENV HF_HOME=/app/.cache/huggingface

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]