from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from app.llm.client import LLMUnavailableError


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


async def llm_unavailable_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "error": "llm_unavailable",
            "detail": str(exc),
            "request_id": _request_id(request),
        },
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    detail = str(exc) if not isinstance(exc, ValidationError) else exc.errors()
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "detail": detail,
            "request_id": _request_id(request),
        },
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    http_exc = exc if isinstance(exc, HTTPException) else HTTPException(status_code=500)
    return JSONResponse(
        status_code=http_exc.status_code,
        content={
            "error": "http_error",
            "detail": http_exc.detail,
            "request_id": _request_id(request),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": "An unexpected error occurred.",
            "request_id": _request_id(request),
        },
    )


def register_handlers(app: object) -> None:
    from fastapi import FastAPI

    app_: FastAPI = app  # type: ignore[assignment]
    app_.add_exception_handler(LLMUnavailableError, llm_unavailable_handler)
    app_.add_exception_handler(ValidationError, validation_exception_handler)
    app_.add_exception_handler(HTTPException, http_exception_handler)
    app_.add_exception_handler(Exception, generic_exception_handler)
