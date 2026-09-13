"""
[API] api/v1/auth.py - Endpoints de autenticación y perfil de usuario (register, login, me, patch).
Ubicación: app/api/v1/auth.py
Responsabilidad: Capa API - Autenticación con JWT, hasheo con bcrypt y consulta de perfil con estadísticas.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.security import create_access_token, get_password_hash, verify_password
from database.connection import get_db
from database.models.prediction import Prediction
from database.models.tournament import TournamentParticipant
from database.models.user import User
from app.schemas.user import TokenOut, UserCreate, UserLogin, UserOut, UserProfileOut, UserUpdate

router = APIRouter()


async def _build_user_profile(user: User, db: AsyncSession) -> UserProfileOut:
    # Cantidad de torneos donde participa
    tournaments_count = await db.scalar(
        select(func.count()).select_from(TournamentParticipant).where(TournamentParticipant.user_id == user.id)
    ) or 0

    # Total de predicciones y precisión
    preds_res = await db.scalars(
        select(Prediction).where(Prediction.user_id == user.id)
    )
    all_preds = preds_res.all()
    total_preds = len(all_preds)
    scored_preds = [p for p in all_preds if p.is_scored]
    correct_preds = sum(1 for p in scored_preds if (p.points_earned or 0) > 0)
    accuracy = round((correct_preds / len(scored_preds)) * 100, 1) if scored_preds else 0.0

    # Mejor posición en torneos (rank menor)
    best_rank = await db.scalar(
        select(func.min(TournamentParticipant.rank))
        .where(TournamentParticipant.user_id == user.id, TournamentParticipant.rank.is_not(None))
    )

    return UserProfileOut(
        id=user.id,
        email=user.email,
        username=user.username,
        is_premium=user.is_premium,
        current_streak=user.current_streak,
        longest_streak=user.longest_streak,
        created_at=user.created_at,
        tournaments_played=tournaments_count,
        total_predictions=total_preds,
        accuracy_percentage=accuracy,
        best_finish=best_rank,
        favorite_teams=[],
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="Registro de usuario")
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea una nueva cuenta de usuario con email y username únicos y contraseña hasheada.
    """
    existing_email = await db.scalar(select(User).where(User.email == payload.email))
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")
    existing_user = await db.scalar(select(User).where(User.username == payload.username))
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenOut, summary="Iniciar sesión")
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Valida credenciales y retorna un JWT Bearer Token válido por 24 horas.
    """
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return TokenOut(access_token=token)


@router.get("/me", response_model=UserProfileOut, summary="Mi perfil y estadísticas")
async def me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna el perfil del usuario autenticado con sus estadísticas de juego (torneos jugados,
    total de pronósticos, precisión histórica y racha actual).
    """
    return await _build_user_profile(current_user, db)


@router.patch("/me", response_model=UserProfileOut, summary="Actualizar perfil")
async def update_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Permite modificar datos del perfil del usuario (como email).
    """
    if payload.email and payload.email != current_user.email:
        existing = await db.scalar(select(User).where(User.email == payload.email))
        if existing:
            raise HTTPException(status_code=409, detail="Email already exists")
        current_user.email = payload.email

    await db.commit()
    await db.refresh(current_user)
    return await _build_user_profile(current_user, db)
