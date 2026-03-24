from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.exceptions import validation_exception_handler
from fastapi.exceptions import RequestValidationError
app = FastAPI(title="FastAPI Authentication Service", version="1.0.0",)

app.include_router(api_router, prefix="/api/v1")
app.add_exception_handler(RequestValidationError, validation_exception_handler)