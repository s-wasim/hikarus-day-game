# Hikaru's Day Game — API Backend

Stateless FastAPI service that generates branching conversation trees for an AI character living inside a 1990s arcade cabinet.

## Install

```bash
uv sync --extra dev
```

## Run

```bash
make run
```

## Test

```bash
make check          # lint + type-check + unit tests
make test-real      # also runs tests that require live Ollama
```

## Ollama setup

See `docs/ollama_setup.md`. The service expects Ollama at `http://localhost:11434` with `qwen2.5:3b-instruct` pulled.
