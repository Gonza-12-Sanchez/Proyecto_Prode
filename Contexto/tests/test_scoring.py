"""
Tests unitarios para la lógica matemática de scoring acumulativo (R7).
"""

import pytest
from app.services.scoring import ScoringRules, calculate_points, score_prediction


def test_scoring_exact_match():
    """Marcador exacto acumula exact + winner + difference (5 + 3 + 2 = 10)."""
    rules = ScoringRules(exact=5, winner=3, difference=2)
    # Pred: 2-1, Real: 2-1
    points = calculate_points(2, 1, 2, 1, rules)
    assert points == 10


def test_scoring_correct_winner_only():
    """Ganador correcto pero diferente diferencia de goles (ej: 2-1 vs 3-0: ganador local, diff 1 vs 3)."""
    rules = ScoringRules(exact=5, winner=3, difference=2)
    points = calculate_points(2, 1, 3, 0, rules)
    assert points == 3  # Solo winner


def test_scoring_correct_difference_and_winner():
    """Misma diferencia y mismo ganador pero no exacto (ej: 2-1 vs 3-2: ganador local y diff 1)."""
    rules = ScoringRules(exact=5, winner=3, difference=2)
    points = calculate_points(2, 1, 3, 2, rules)
    assert points == 5  # winner (3) + difference (2) = 5


def test_scoring_draw_exact():
    """Empate exacto (ej: 1-1 vs 1-1): 5 exact + 3 winner (0==0) + 2 diff (0==0) = 10."""
    rules = ScoringRules(exact=5, winner=3, difference=2)
    points = calculate_points(1, 1, 1, 1, rules)
    assert points == 10


def test_scoring_draw_not_exact():
    """Empate no exacto (ej: 0-0 vs 2-2): winner (0==0, 3pts) + diff (0==0, 2pts) = 5."""
    rules = ScoringRules(exact=5, winner=3, difference=2)
    points = calculate_points(0, 0, 2, 2, rules)
    assert points == 5


def test_scoring_complete_miss():
    """Predicción totalmente fallida (ej: predice local 2-1, termina visitante 0-2): 0 puntos."""
    rules = ScoringRules(exact=5, winner=3, difference=2)
    points = calculate_points(2, 1, 0, 2, rules)
    assert points == 0


def test_scoring_idempotence():
    """Llamar múltiples veces retorna exactamente el mismo resultado."""
    rules = ScoringRules(exact=5, winner=3, difference=2)
    r1 = calculate_points(3, 1, 3, 1, rules)
    r2 = calculate_points(3, 1, 3, 1, rules)
    assert r1 == r2 == 10
