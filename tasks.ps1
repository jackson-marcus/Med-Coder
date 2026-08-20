# PowerShell task runner mirroring the Makefile.
# Usage: .\tasks.ps1 <task>   e.g. .\tasks.ps1 test
param([Parameter(Mandatory = $true)][string]$Task)

switch ($Task) {
    "install"    { uv sync --group dev }
    "lint"       { uv run ruff check .; uv run ruff format --check . }
    "format"     { uv run ruff check --fix .; uv run ruff format . }
    "test"       { uv run pytest --cov }
    "api"        { uv run uvicorn medcoder.api.main:app --reload --port 8150 }
    "ui"         { $env:MEDCODER_API_URL = "http://localhost:8150"; uv run streamlit run src/medcoder/ui/app.py --server.port 8651 }
    "mlflow"     { uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5016 }
    "docker-up"  { docker compose up --build -d }
    "docker-down"{ docker compose down }
    default      { Write-Host "Unknown task: $Task" }
}
