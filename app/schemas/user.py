"""
[SCHEMAS] schemas/user.py - Validación Pydantic para User (registro, login, perfil).
Ubicación: app/schemas/user.py
Responsabilidad: Capa SCHEMAS - Define UserCreate, UserLogin, UserOut, UserUpdate y UserProfileOut.
"""

import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=254)
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]{3,30}$", v):
            raise ValueError("username must match ^[a-zA-Z0-9_-]{3,30}$")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_premium: bool
    current_streak: int
    longest_streak: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileOut(UserOut):
    tournaments_played: int = 0
    total_predictions: int = 0
    accuracy_percentage: float = 0.0
    best_finish: int | None = None
    favorite_teams: list[str] = []


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    favorite_teams: list[str] | None = Field(default=None, max_length=10)
