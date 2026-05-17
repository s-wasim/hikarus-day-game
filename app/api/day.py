import time

import structlog
from fastapi import APIRouter, HTTPException, Request

from app.engine.filler import run_filler
from app.engine.planner import run_planner
from app.llm.client import OllamaClient
from app.schemas.day import DayRequest, DayResponse

log = structlog.get_logger()
router = APIRouter()


@router.post("/day", response_model=DayResponse)
async def day_endpoint(body: DayRequest, request: Request) -> DayResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    client: OllamaClient = request.app.state.ollama

    log.info("day_request", mode=body.mode, day=body.day, request_id=request_id)
    t_start = time.monotonic()

    if body.mode == "day":
        t0 = time.monotonic()
        plan = await run_planner(client, body)
        planner_ms = int((time.monotonic() - t0) * 1000)

        t0 = time.monotonic()
        response = await run_filler(client, body, plan)
        filler_ms = int((time.monotonic() - t0) * 1000)

        total_ms = int((time.monotonic() - t_start) * 1000)
        log.info(
            "day_response",
            mode=body.mode,
            day=body.day,
            ollama_call_count=2,
            planner_latency_ms=planner_ms,
            filler_latency_ms=filler_ms,
            total_latency_ms=total_ms,
            schema_validation_passed=True,
            request_id=request_id,
        )
        return response

    raise HTTPException(status_code=400, detail=f"mode '{body.mode}' not yet implemented")
