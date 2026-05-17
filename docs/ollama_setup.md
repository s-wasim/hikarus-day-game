# Ollama Setup

## Install

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:** Download the installer from https://ollama.com/download

## Pull the model

```bash
ollama pull qwen2.5:3b-instruct
```

This downloads ~2 GB. Verify:

```bash
ollama list
# should show: qwen2.5:3b-instruct
curl http://localhost:11434/api/tags
```

## Smoke test

```bash
ollama run qwen2.5:3b-instruct "Say hello in one sentence."
```

Should return a coherent reply in under 10 seconds on a modern CPU.

## Known issues

- **RAM**: Requires ~4 GB free RAM minimum. 6 GB recommended.
- **Default URL**: `http://localhost:11434`. Override with `OLLAMA_URL` env var.
- **Linux systemd**: Ollama installs as a service. Check status with `systemctl status ollama`.
- **Model name**: The exact tag is `qwen2.5:3b-instruct`. Using `qwen2.5:3b` (without `-instruct`) will not work correctly for chat tasks.
