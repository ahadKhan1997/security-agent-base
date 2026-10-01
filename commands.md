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

to scan image:
    docker scout cves local://security-agent-base-app:latest

Execute Code Format Compliance Checking Linting:
    ruff check

Run Your Offline Test Coverage Checks:
    $env:PYTHONPATH="." ; pytest