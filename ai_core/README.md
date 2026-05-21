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
pytest
```

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | /health | Liveness check |
| POST | /turn | Selects a conversation tree JSON file based on journal state; returns `{file_key, tree}`. No LLM involved. |
| POST | /commit | Applies +1 delta per picked choice to the named AI and Hikaru journal fields, clamped to [-10, 10]. Returns updated journals. |

## turn_configs/

JSON dialogue tree files that drive conversation flow. Each file encodes a tree of AI messages and player choices for a specific day/state combination. The `POST /turn` endpoint selects the appropriate file based on the current journal state and returns the full tree to the client.

## prompts/

The `prompts/` directory (`system.md`, `DAY0.md`, `JSON_SCHEMA.md`) is for **dev-time authoring only** — it is not loaded or used at runtime. Use these files as reference when creating or editing `turn_configs/` JSON trees.

## Environment variables

See `.env.example` for all configurable values.
