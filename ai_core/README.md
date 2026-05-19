# ai_core — Hikaru's Day AI Engine

FastAPI service driving the AI-cabinet dialogue for Hikaru's Day.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Run

```bash
cd ai_core
uvicorn app.main:app --reload
```

## Test

```bash
pytest                    # mocked tests only
RUN_GOLDEN=1 pytest       # includes live Ollama tests
```

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /health | Liveness check |
| POST | /turn | Generate AI messages + player choices for a day turn |
| POST | /commit | Apply player choices, update journals, return summary |

## Environment variables

See `.env.example` for all configurable values.
