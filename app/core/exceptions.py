from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request, exc: RequestValidationError):
    errors = {}

    for err in exc.errors():
        field = err["loc"][-1]
        message = err["msg"]

        if message == "Field required":
            message = f"{field} is required"

        if "valid email" in message:
            message = "Invalid email address"

        errors[field] = message

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "code": "VALIDATION_ERROR",
            "fields": errors
        }
    )