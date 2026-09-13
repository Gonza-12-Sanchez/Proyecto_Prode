"""
[CORE] security.py - Seguridad (bcrypt + JWT 24h).
Ubicación: app/core/security.py
Responsabilidad: Capa CORE - Hashea/verifica passwords con bcrypt y crea/decodifica JWT HS256 con expiración 24h. Pura lógica criptográfica sin I/O.
Usa: app.core.config.settings, passlib, python-jose
No hace: No consulta la DB ni gestiona sesiones HTTP, solo funciones puras.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, expires_hours: int | None = None) -> str:
    expire_delta = timedelta(hours=expires_hours or settings.JWT_EXPIRE_HOURS)
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        sub: str | None = payload.get("sub")
        return sub
    except JWTError:
        return None
