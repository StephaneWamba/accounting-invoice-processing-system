from fastapi import FastAPI

from .auth import verify_api_key  # noqa: F401  # ensure module import
from .routers import invoices

app = FastAPI(title="Invoice Processing API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(invoices.router, prefix="/v1")
