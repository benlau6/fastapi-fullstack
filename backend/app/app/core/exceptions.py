from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.response import err


def _http_error_code(status_code: int) -> int:
    mapping = {
        401: 100401,
        403: 100403,
        404: 100404,
        409: 100409,
        422: 100422,
    }
    return mapping.get(status_code, status_code)


def init_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Any, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=err(100422, "validation_error", {"errors": exc.errors()}),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Any, exc: HTTPException) -> JSONResponse:
        detail = exc.detail
        message = detail if isinstance(detail, str) else "http_error"
        payload: Dict[str, Any] = err(_http_error_code(exc.status_code), message, None)
        return JSONResponse(status_code=exc.status_code, content=payload)
