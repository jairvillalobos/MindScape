from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.routers import users , entries
from api.routers.emotions import router as emotions_router
from utils import CustomHTTPException, custom_exception_handler
from domain.services import ALGORITHM, SECRET_KEY

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

# my cunstom exception
@app.exception_handler(CustomHTTPException)
async def handle_custom_exceptions(request: Request, exc: CustomHTTPException):
    return await custom_exception_handler(request, exc)

app.include_router(users.router)
app.include_router(entries.router)
app.include_router(emotions_router)


@app.get("/ruta_protegida", dependencies=[Depends(get_current_user)])
async def ruta_protegida():
    return {"message": "Esta es una ruta protegida"}