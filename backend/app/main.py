from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .api.routes import categories, tasks, timeline, dashboard
from .schemas import ErrorResponse

app = FastAPI(title="Backlog風TODO API", version="0.1.0")

app.include_router(categories.router)
app.include_router(tasks.router)
app.include_router(timeline.router)
app.include_router(dashboard.router)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    payload = ErrorResponse(code="http_error", message=str(exc.detail), details=None)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    payload = ErrorResponse(code="validation_error", message="Validation failed", details={"errors": exc.errors()})
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.get("/health")
def health():
    return {"status": "ok"}
