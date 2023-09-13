from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
import jwt
from sqlalchemy.orm import Session
from utils import custom_exception
from infrastructure.database import get_db
from domain.models import User
from domain.services import ALGORITHM, SECRET_KEY, authenticate_user, create_access_token, send_verification_email
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, validator

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

router = APIRouter()


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str

    # Este validador se asegura de que el nombre sea alfanumérico
    @validator('name')
    def name_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            custom_exception(status.HTTP_400_BAD_REQUEST,
                             "INVALID_NAME", 'El nombre debe ser alfanumérico')
        return v

    # Este validador se asegura de que la contraseña tenga al menos 8 caracteres,
    # incluyendo al menos una letra y un número.
    @validator('password')
    def password_must_be_secure(cls, v):
        if len(v) < 8 or not any(char.isdigit() for char in v) or not any(char.isalpha() for char in v):
            custom_exception(status.HTTP_400_BAD_REQUEST, "INSECURE_PASSWORD",
                             'La contraseña no es segura. Debe tener al menos 8 caracteres, incluyendo al menos una letra y un número.')
        return v


@router.post("/register")
async def register(user_in: UserIn, db: Session = Depends(get_db)):
    # Verificar si el correo electrónico ya existe en la base de datos.
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user is not None:
        custom_exception(status.HTTP_400_BAD_REQUEST,
                         "EMAIL_EXISTS", "El correo electrónico ya existe")

    # Verificar si el nombre de usuario ya existe en la base de datos.
    existing_user = db.query(User).filter(User.name == user_in.name).first()
    if existing_user is not None:
        custom_exception(status.HTTP_400_BAD_REQUEST,
                         "USERNAME_EXISTS", "El nombre de usuario ya existe")

    # Si no existen, puedes continuar con la creación del usuario.
    user = User(name=user_in.name, email=user_in.email)
    user.hashed_password = pwd_context.hash(
        user_in.password)  # Hash the password and assign it
    user.registration_date = datetime.now()  # Set the registration date to now
    db.add(user)
    db.commit()

    # Después de guardar al usuario en la base de datos, puedes enviarle un correo electrónico con el enlace de verificación.
    verification_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(hours=24))
    send_verification_email(user, verification_token)

    return {"message": "Usuario creado con éxito. Por favor, revisa tu correo electrónico para verificar tu cuenta."}


@router.get("/verify/{token}")
async def verify(token: str, db: Session = Depends(get_db)):
    try:
        # Decodifica el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            custom_exception(status.HTTP_401_UNAUTHORIZED,
                             "INVALID_TOKEN", "Invalid token")
        # Busca al usuario en la base de datos
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            custom_exception(status.HTTP_404_NOT_FOUND,
                             "USER_NOT_FOUND", "User not found")
        # Marca al usuario como verificado
        user.is_verified = True
        db.commit()
    except JWTError:
        custom_exception(status.HTTP_401_UNAUTHORIZED,
                         "INVALID_TOKEN", "Invalid token")
    # Si todo va bien, devuelve un mensaje de éxito
    return {"message": "Account verified successfully"}

#with login per email and passwonrd 
class LoginIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/token")
async def login(login_in: LoginIn, db: Session = Depends(get_db)):
    # Intenta autenticar al usuario con el correo electrónico y la contraseña proporcionados
    user = authenticate_user(db, login_in.email, login_in.password)

    # Si la autenticación falla o el correo electrónico del usuario no ha sido verificado, lanza una excepción
    if not user or not user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect email or password or email not verified")

    # Si la autenticación tiene éxito y el correo electrónico del usuario ha sido verificado, crea un token de acceso para el usuario
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}

#with OAuth2PasswordBearer
"""
@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Intenta autenticar al usuario con el correo electrónico y la contraseña proporcionados
    user = authenticate_user(db, form_data.username, form_data.password)

    # Si la autenticación falla o el correo electrónico del usuario no ha sido verificado, lanza una excepción
    if not user or not user.is_verified:
        custom_exception(status.HTTP_400_BAD_REQUEST, "AUTHENTICATION_FAILED",
                         "Incorrect email or password or email not verified")

    # Si la autenticación tiene éxito y el correo electrónico del usuario ha sido verificado, crea un token de acceso para el usuario
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
"""
