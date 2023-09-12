from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.routers import users

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"msg": exc.errors()[0]['msg'].replace("Value error, ", "")},
    )


app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
