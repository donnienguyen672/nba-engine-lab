"""Game evaluation display panel.

Shows regime classification and basic eval for each game.
Pure display. No data fetching.
Layer: src/ui/panels
"""

from __future__ import annotations
from src.state.game_state import GameState
from src.state.regime import classify_regime
from src.state.bonus_detect import detect_bonus


def render_eval(states: list[GameState]) -> str:
    """Render evaluation table with regime classification.

    Args:
        states: List of GameState objects.

    Returns:
        Formatted string table.
    """
    if not states:
        return "No games to evaluate."

    lines = []
    header = f"{'ID':<14} {'Matchup':<28} {'Score':>11} {'Regime':<10} {'Diff':>5}"
    lines.append(header)
    lines.append("-" * len(header))

    for s in states:
        matchup = f"{s.away_abbr} @ {s.home_abbr}"
        score = f"{s.away_score}-{s.home_score}"
        regime = classify_regime(s)
        diff = f"{s.score_diff:+d}"
        lines.append(
            f"{s.game_id:<14} {matchup:<28} {score:>11} {regime:<10} {diff:>5}"
        )

    return "\n".join(lines)


def print_eval(states: list[GameState]) -> None:
    """Print eval table to stdout."""
    print(render_eval(states))
