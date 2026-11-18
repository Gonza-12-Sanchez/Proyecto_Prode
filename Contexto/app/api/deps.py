"""
[API] deps.py - Dependencias FastAPI (get_db + get_current_user).
Ubicación: app/api/deps.py
Responsabilidad: Capa API - Provee Depends(get_db) desde database.connection y Depends(get_current_user) vía JWT. Es el mozo que autentica antes de llamar al servicio.
Usa: database.connection.get_db, app.core.security.decode_access_token, database.models.user.User
No hace: No implementa endpoints ni scoring, solo inyección de dependencia.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from app.core.security import decode_access_token
from database.models.user import User

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    sub = decode_access_token(token)
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # sub is user id string
    try:
        from uuid import UUID
        user_uuid = UUID(sub)
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    user = await db.scalar(select(User).where(User.id == user_uuid))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
