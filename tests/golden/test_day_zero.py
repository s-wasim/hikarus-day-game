"""
Golden-file test: run Day 0 against real Ollama 5 times and assert schema validity.

Skip by default. Run with:  pytest -m real_llm
"""

import json
import time
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.engine.filler import run_filler
from app.engine.planner import run_planner
from app.llm.client import OllamaClient
from app.schemas.day import DayRequest

FIXTURE = Path(__file__).parent / "fixtures" / "day_zero_request.json"
SAMPLE_OUTPUT_DIR = Path(__file__).parent / "fixtures" / "samples"

RUNS = 5
MIN_PASS = 4  # 80% reliability floor


@pytest.mark.slow
@pytest.mark.real_llm
async def test_day_zero_schema_validity_over_5_runs() -> None:
    SAMPLE_OUTPUT_DIR.mkdir(exist_ok=True)
    request_data = json.loads(FIXTURE.read_text())
    request = DayRequest.model_validate(request_data)
    client = OllamaClient()

    passes = 0
    failures: list[str] = []

    for run_idx in range(RUNS):
        t0 = time.monotonic()
        try:
            plan = await run_planner(client, request)
            response = await run_filler(client, request, plan)
            elapsed = int((time.monotonic() - t0) * 1000)

            output_path = SAMPLE_OUTPUT_DIR / f"day_zero_run_{run_idx}.json"
            output_path.write_text(response.model_dump_json(indent=2))
            passes += 1
            print(f"\nRun {run_idx}: PASS in {elapsed}ms, themes={response.themes}")

        except (ValidationError, ValueError) as exc:
            elapsed = int((time.monotonic() - t0) * 1000)
            error_msg = str(exc)[:400]
            failures.append(f"Run {run_idx}: {error_msg}")
            print(f"\nRun {run_idx}: FAIL in {elapsed}ms\n{error_msg}")

    print(f"\n=== Results: {passes}/{RUNS} passed ===")
    for f in failures:
        print(f"FAILURE: {f}")

    assert passes >= MIN_PASS, (
        f"Only {passes}/{RUNS} runs passed schema validation (need {MIN_PASS}). "
        f"Failures:\n" + "\n".join(failures)
    )
