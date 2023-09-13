from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from domain.models import User
from utils import custom_exception
load_dotenv()  # take environment variables from .env.

# Tus detalles de correo electrónico
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Tus detalles de JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def authenticate_user(db, email: str, password: str):
    if not email or not password:
        custom_exception(status.HTTP_400_BAD_REQUEST, "INVALID_INPUT",
                         "El correo electrónico y la contraseña no deben estar vacíos.")
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        custom_exception(status.HTTP_401_UNAUTHORIZED, "AUTHENTICATION_FAILED",
                         "Correo electrónico o contraseña incorrectos")
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        custom_exception(status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "TOKEN_CREATION_FAILED", "Ocurrió un error al crear el token de acceso.")
    return encoded_jwt


def create_verification_token(*, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        custom_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, "TOKEN_CREATION_FAILED",
                         "Ocurrió un error al crear el token de verificación.")
    return encoded_jwt


def send_verification_email(user, verification_token):
    if not user.email:
        custom_exception(status.HTTP_400_BAD_REQUEST, "INVALID_INPUT",
                         "El correo electrónico del usuario no debe estar vacío.")
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user.email
    msg['Subject'] = "Verifica tu cuenta"

    # Aquí deberías generar un enlace de verificación para el usuario.
    # Podrías generar un token JWT con la información del usuario y luego incluir este token en el enlace de verificación.
    verification_link = "http://localhost:8000/verify/" + verification_token

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .email-content {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .email-button {{
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div class="email-content">
            <h2>Hola {user.name},</h2>
            <p>¡Gracias por registrarte! Para completar tu registro y verificar tu cuenta, por favor haz clic en el botón de abajo.</p>
            <a href="{verification_link}" class="email-button">Verificar mi cuenta</a>
            <p>Si tienes problemas para hacer clic en el botón, copia y pega el siguiente enlace en tu navegador:</p>
            <p>{verification_link}</p>
            <p>Saludos cordiales,</p>
            <p>MindScape</p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(body, 'html'))


    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, user.email, text)
        server.quit()
    except smtplib.SMTPException:
        custom_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, "EMAIL_SENDING_FAILED",
                         "Ocurrió un error al enviar el correo electrónico de verificación.")
