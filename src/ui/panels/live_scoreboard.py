"""Live scoreboard display panel.

Pure display. No data fetching.
Layer: src/ui/panels
"""

from __future__ import annotations
from src.state.game_state import GameState


def render_scoreboard(states: list[GameState]) -> str:
    """Render a text-based scoreboard table from GameState list.

    Args:
        states: List of GameState objects.

    Returns:
        Formatted string table.
    """
    if not states:
        return "No games found."

    lines = []
    header = f"{'ID':<14} {'Matchup':<28} {'Score':>11} {'Period':<6} {'Clock':<8} {'Status':<6}"
    lines.append(header)
    lines.append("-" * len(header))

    for s in states:
        matchup = f"{s.away_abbr} @ {s.home_abbr}"
        score = f"{s.away_score}-{s.home_score}"
        lines.append(
            f"{s.game_id:<14} {matchup:<28} {score:>11} {s.period_label:<6} {s.clock:<8} {s.status:<6}"
        )

    return "\n".join(lines)


def print_scoreboard(states: list[GameState]) -> None:
    """Print scoreboard to stdout."""
    print(render_scoreboard(states))
