# Stage 1: Build phase
FROM python:3.12-slim AS package-builder
WORKDIR /app
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pydantic pydantic-settings httpx python-dotenv

# Stage 2: Hardened Runtime environment
FROM python:3.12-slim
WORKDIR /app

# Copy dependencies directly out of our builder framework
COPY --from=package-builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=package-builder /usr/local/bin /usr/local/bin

# Copy app code cleanly into runtime area
COPY . .

# Drop root privileges for container defense
RUN useradd -u 1001 -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "main.py"]
