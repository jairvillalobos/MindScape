# utils.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, error_title: str, error_message: str):
        super().__init__(status_code=status_code, detail=error_message)
        self.error_title = error_title


async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "title": exc.error_title,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": exc.detail,
            "type": "genericError",
            "source": "internal"
        },
    )


def custom_exception(status_code: int, error_title: str, error_message: str):
    raise CustomHTTPException(
        status_code=status_code, error_title=error_title, error_message=error_message)
