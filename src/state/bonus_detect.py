"""Bonus detection logic stub.

Detects team foul bonus / double-bonus state.
Pure function. No I/O.
Layer: src/state
"""

from src.state.game_state import GameState


def detect_bonus(state: GameState) -> dict:
    """Detect bonus status for both teams.

    Args:
        state: Current GameState.

    Returns:
        Dict with keys:
            home_bonus: bool
            away_bonus: bool
            home_double_bonus: bool
            away_double_bonus: bool

    Note:
        Stub implementation. Requires foul count data from PBP feed
        to be fully functional. Returns all False until wired up.
    """
    # TODO: Wire up foul counts from play-by-play adapter.
    # NBA bonus: 5th team foul in a quarter → bonus (1-and-1 doesn't apply in NBA,
    # but penalty FTs start at 5th foul). Double bonus isn't standard NBA
    # but keeping the slot for flexibility.
    return {
        "home_bonus": state.extra.get("home_bonus", False),
        "away_bonus": state.extra.get("away_bonus", False),
        "home_double_bonus": state.extra.get("home_double_bonus", False),
        "away_double_bonus": state.extra.get("away_double_bonus", False),
    }
