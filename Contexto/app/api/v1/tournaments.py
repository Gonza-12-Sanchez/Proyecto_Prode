"""
[API] api/v1/tournaments.py - Endpoints de torneos (crear, previsualizar, unirse, listar, detalle, start y leaderboard).
Ubicación: app/api/v1/tournaments.py
Responsabilidad: Capa API - Valida payloads, chequea league y capacidad vía app.services.tournament_service, genera invite_code, resuelve preview/join y expone leaderboard.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from database.connection import get_db
from database.models.tournament import League, ScoringRule, Tournament, TournamentParticipant
from database.models.user import User
from app.schemas.tournament import (
    JoinByCodeIn,
    LeaderboardEntry,
    LeaderboardOut,
    ScoringRulesOut,
    TournamentCreate,
    TournamentOut,
    TournamentPreviewOut,
)
from app.services.tournament_service import generate_unique_invite_code, validate_capacity

router = APIRouter()


@router.post("", response_model=TournamentOut, status_code=status.HTTP_201_CREATED, summary="Crear nuevo torneo")
async def create_tournament(
    payload: TournamentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Crea un nuevo torneo con código de invitación único.
    El usuario creador se convierte automáticamente en el primer participante.
    """
    league = await db.scalar(select(League).where(League.id == payload.league_id))
    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    if not validate_capacity(bool(current_user.is_premium), payload.max_participants):
        raise HTTPException(status_code=403, detail="Free users can only create tournaments with max_participants=10")

    invite_code = await generate_unique_invite_code(db)
    tournament = Tournament(
        name=payload.name,
        description=payload.description,
        league_id=payload.league_id,
        creator_id=current_user.id,
        invite_code=invite_code,
        max_participants=payload.max_participants,
        status="Setup",
    )
    db.add(tournament)
    await db.flush()

    rules_in = payload.scoring_rules
    scoring_rule = ScoringRule(
        tournament_id=tournament.id,
        exact_score=rules_in.exact_score if rules_in else 5,
        correct_winner=rules_in.correct_winner if rules_in else 3,
        goal_difference=rules_in.goal_difference if rules_in else 2,
    )
    db.add(scoring_rule)

    participant = TournamentParticipant(
        tournament_id=tournament.id,
        user_id=current_user.id,
        total_points=0,
        predictions_count=0,
        accuracy=0,
    )
    db.add(participant)
    await db.commit()
    await db.refresh(tournament)

    return TournamentOut(
        id=tournament.id,
        name=tournament.name,
        description=tournament.description,
        league_id=tournament.league_id,
        creator_id=tournament.creator_id,
        invite_code=tournament.invite_code,
        max_participants=tournament.max_participants,
        status=tournament.status,
        created_at=tournament.created_at,
        scoring_rules=ScoringRulesOut(
            exact_score=scoring_rule.exact_score,
            correct_winner=scoring_rule.correct_winner,
            goal_difference=scoring_rule.goal_difference,
        ),
    )


@router.get("/preview/{invite_code}", response_model=TournamentPreviewOut, summary="Previsualizar torneo por código")
async def preview_tournament(
    invite_code: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Permite a un usuario consultar información pública de un torneo antes de unirse,
    mostrando nombre, liga, reglas de puntuación y ocupación actual.
    """
    normalized_code = invite_code.strip().upper()
    tournament = await db.scalar(
        select(Tournament)
        .options(selectinload(Tournament.league), selectinload(Tournament.scoring_rule))
        .where(func.upper(Tournament.invite_code) == normalized_code)
    )
    if not tournament:
        raise HTTPException(status_code=404, detail="Invalid invite code")

    count = await db.scalar(
        select(func.count()).select_from(TournamentParticipant).where(TournamentParticipant.tournament_id == tournament.id)
    ) or 0

    rule = tournament.scoring_rule
    return TournamentPreviewOut(
        id=tournament.id,
        name=tournament.name,
        league_id=tournament.league_id,
        league_name=tournament.league.name if tournament.league else None,
        max_participants=tournament.max_participants,
        current_participants=count,
        scoring_rules=ScoringRulesOut(
            exact_score=rule.exact_score,
            correct_winner=rule.correct_winner,
            goal_difference=rule.goal_difference,
        ) if rule else None,
        status=tournament.status,
    )


@router.post("/join", response_model=TournamentPreviewOut, summary="Unirse a un torneo con código")
async def join_tournament(
    payload: JoinByCodeIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Une al usuario autenticado a un torneo usando su código de invitación de 8 caracteres.
    """
    normalized_code = payload.invite_code.strip().upper()
    tournament = await db.scalar(
        select(Tournament)
        .options(selectinload(Tournament.league), selectinload(Tournament.scoring_rule))
        .where(func.upper(Tournament.invite_code) == normalized_code)
    )
    if not tournament:
        raise HTTPException(status_code=404, detail="Invalid invite code")

    existing = await db.scalar(
        select(TournamentParticipant).where(
            TournamentParticipant.tournament_id == tournament.id,
            TournamentParticipant.user_id == current_user.id,
        )
    )
    if existing:
        raise HTTPException(status_code=409, detail="Already a participant")

    # Contar participantes actuales
    count = await db.scalar(
        select(func.count()).select_from(TournamentParticipant).where(TournamentParticipant.tournament_id == tournament.id)
    ) or 0

    if count >= tournament.max_participants:
        raise HTTPException(status_code=409, detail="Tournament is full")

    participant = TournamentParticipant(
        tournament_id=tournament.id,
        user_id=current_user.id,
    )
    db.add(participant)
    await db.commit()

    rule = tournament.scoring_rule
    return TournamentPreviewOut(
        id=tournament.id,
        name=tournament.name,
        league_id=tournament.league_id,
        league_name=tournament.league.name if tournament.league else None,
        max_participants=tournament.max_participants,
        current_participants=count + 1,
        scoring_rules=ScoringRulesOut(
            exact_score=rule.exact_score,
            correct_winner=rule.correct_winner,
            goal_difference=rule.goal_difference,
        ) if rule else None,
        status=tournament.status,
    )


@router.get("", response_model=list[TournamentOut], summary="Listar mis torneos")
async def list_my_tournaments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna la lista de torneos donde el usuario autenticado participa.
    """
    q = (
        select(Tournament)
        .options(selectinload(Tournament.scoring_rule))
        .join(TournamentParticipant, TournamentParticipant.tournament_id == Tournament.id)
        .where(TournamentParticipant.user_id == current_user.id)
        .order_by(Tournament.created_at.desc())
    )
    result = await db.scalars(q)
    tournaments = result.all()

    out = []
    for t in tournaments:
        rule = t.scoring_rule
        out.append(
            TournamentOut(
                id=t.id,
                name=t.name,
                description=t.description,
                league_id=t.league_id,
                creator_id=t.creator_id,
                invite_code=t.invite_code,
                max_participants=t.max_participants,
                status=t.status,
                created_at=t.created_at,
                scoring_rules=ScoringRulesOut(
                    exact_score=rule.exact_score,
                    correct_winner=rule.correct_winner,
                    goal_difference=rule.goal_difference,
                ) if rule else None,
            )
        )
    return out


@router.get("/{tournament_id}", response_model=TournamentOut, summary="Obtener detalle de un torneo")
async def get_tournament(
    tournament_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna el detalle completo de un torneo por su UUID.
    """
    tournament = await db.scalar(
        select(Tournament)
        .options(selectinload(Tournament.scoring_rule))
        .where(Tournament.id == tournament_id)
    )
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    rule = tournament.scoring_rule
    return TournamentOut(
        id=tournament.id,
        name=tournament.name,
        description=tournament.description,
        league_id=tournament.league_id,
        creator_id=tournament.creator_id,
        invite_code=tournament.invite_code,
        max_participants=tournament.max_participants,
        status=tournament.status,
        created_at=tournament.created_at,
        scoring_rules=ScoringRulesOut(
            exact_score=rule.exact_score,
            correct_winner=rule.correct_winner,
            goal_difference=rule.goal_difference,
        ) if rule else None,
    )


@router.post("/{tournament_id}/start", summary="Iniciar torneo (solo creador)")
async def start_tournament(
    tournament_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Pasa el torneo de estado 'Setup' a 'Active'. Solo el creador del torneo puede iniciarlo.
    """
    tournament = await db.scalar(select(Tournament).where(Tournament.id == tournament_id))
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    if tournament.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only creator can start tournament")
    if tournament.status != "Setup":
        raise HTTPException(status_code=409, detail=f"Tournament already {tournament.status}")

    tournament.status = "Active"
    await db.commit()
    return {"status": tournament.status}


@router.get("/{tournament_id}/leaderboard", response_model=LeaderboardOut, summary="Tabla de posiciones del torneo")
async def get_leaderboard(
    tournament_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna la tabla de posiciones clasificada por total de puntos DESC,
    porcentaje de precisión DESC y fecha de ingreso ASC.
    Resalta la posición del usuario en sesión.
    """
    tournament = await db.scalar(select(Tournament).where(Tournament.id == tournament_id))
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    q = (
        select(TournamentParticipant)
        .options(selectinload(TournamentParticipant.user))
        .where(TournamentParticipant.tournament_id == tournament_id)
        .order_by(
            TournamentParticipant.total_points.desc(),
            TournamentParticipant.accuracy.desc(),
            TournamentParticipant.joined_at.asc(),
        )
    )
    result = await db.scalars(q)
    participants = result.all()

    entries: list[LeaderboardEntry] = []
    my_rank = None
    my_points = None

    for idx, p in enumerate(participants, start=1):
        entry = LeaderboardEntry(
            user_id=p.user_id,
            username=p.user.username if p.user else "Usuario",
            total_points=p.total_points,
            predictions_count=p.predictions_count,
            accuracy=float(p.accuracy),
            rank=idx,
        )
        entries.append(entry)
        if p.user_id == current_user.id:
            my_rank = idx
            my_points = p.total_points

    return LeaderboardOut(
        tournament_id=tournament_id,
        entries=entries,
        my_rank=my_rank,
        my_points=my_points,
    )
