"""
[SERVICES] scoring.py - Lógica de scoring acumulativo (R7) pura y testeable.
Ubicación: app/services/scoring.py
Responsabilidad: Capa SERVICES - Función pura calculate_points que implementa reglas exact_score / correct_winner / goal_difference de forma acumulativa e idempotente.
Usa: dataclasses (sin I/O)
No hace: No toca DB ni HTTP, solo aritmética de puntos.
"""

"""Scoring acumulativo (R7) - función pura y testeable.

Regla acumulativa (requirements.md R7 AC6, README §2.3):
- exact_score: si pred == result → award exact_score
- correct_winner: si signo(pred_home - pred_away) == signo(actual_home - actual_away) → award winner
  (incluye empates: 0 == 0)
- goal_difference: si (pred_home - pred_away) == (actual_home - actual_away) → award diff

Acumulativo: si exacto, implica winner Y diff → se suman los 3 (ej: 5+3+2=10).
Si solo winner o solo diff, se suma individual. Si ninguno → 0.
Idempotente: llamar N veces con mismos inputs retorna mismo valor.
"""

from dataclasses import dataclass


@dataclass
class ScoringRules:
    exact: int = 5
    winner: int = 3
    difference: int = 2

    # Compat aliases for SQLAlchemy models: exact_score, correct_winner, goal_difference
    @classmethod
    def from_model(cls, obj) -> "ScoringRules":
        """Accept ScoringRule ORM or dict with various field names."""
        if isinstance(obj, dict):
            return cls(
                exact=obj.get("exact_score", obj.get("exact", 5)),
                winner=obj.get("correct_winner", obj.get("winner", 3)),
                difference=obj.get("goal_difference", obj.get("difference", 2)),
            )
        return cls(
            exact=getattr(obj, "exact_score", getattr(obj, "exact", 5)),
            winner=getattr(obj, "correct_winner", getattr(obj, "winner", 3)),
            difference=getattr(obj, "goal_difference", getattr(obj, "difference", 2)),
        )


def _winner_sign(home: int, away: int) -> int:
    if home > away:
        return 1
    if home < away:
        return -1
    return 0


def calculate_points(
    pred_home: int,
    pred_away: int,
    actual_home: int,
    actual_away: int,
    rules: ScoringRules | dict | object,
) -> int:
    """Calcula puntos acumulativos.

    Args:
        pred_home/away: pronóstico
        actual_home/away: resultado real
        rules: ScoringRules o objeto con exact/correct_winner/goal_difference

    Returns:
        int puntos totales (0 si ningún criterio).
    """
    if not isinstance(rules, ScoringRules):
        rules = ScoringRules.from_model(rules)  # type: ignore

    points = 0
    is_exact = pred_home == actual_home and pred_away == actual_away
    pred_diff = pred_home - pred_away
    actual_diff = actual_home - actual_away
    is_diff = pred_diff == actual_diff
    is_winner = _winner_sign(pred_home, pred_away) == _winner_sign(actual_home, actual_away)

    if is_exact:
        # Exact acumula los 3 (exact implica winner y diff correctos)
        points += rules.exact
        points += rules.winner
        points += rules.difference
        return points

    if is_winner:
        points += rules.winner
    if is_diff:
        points += rules.difference

    return points


# Alias for spec compatibility: score_prediction
def score_prediction(pred: tuple[int, int], result: tuple[int, int], rules) -> int:
    if not isinstance(rules, ScoringRules):
        rules = ScoringRules.from_model(rules)  # type: ignore
    return calculate_points(pred[0], pred[1], result[0], result[1], rules)
