"""Game regime classifier.

Pure function. No I/O, no side effects.
Layer: src/state
"""

from src.state.game_state import GameState


def classify_regime(state: GameState) -> str:
    """Classify the current game regime based on state.

    Returns one of:
        "pregame"   - game has not started
        "early"     - Q1-Q2, no pressure
        "mid"       - Q3 or early Q4
        "clutch"    - Q4 with < 5:00 remaining and score diff <= 5
        "garbage"   - Q4 with score diff > 20
        "closing"   - Q4, not clutch, not garbage
        "overtime"  - any OT period
        "final"     - game is over
    """
    if state.is_final or state.status == "post":
        return "final"

    if state.status == "pre":
        return "pregame"

    period = state.period
    abs_diff = abs(state.score_diff)

    if period <= 2:
        return "early"

    if period == 3:
        return "mid"

    if period >= 5:
        return "overtime"

    # period == 4
    # Parse clock for minutes remaining
    minutes_left = _parse_clock_minutes(state.clock)

    if abs_diff > 20:
        return "garbage"

    if minutes_left is not None and minutes_left < 5.0 and abs_diff <= 5:
        return "clutch"

    return "closing"


def _parse_clock_minutes(clock: str) -> float | None:
    """Parse clock string like '5:32' into total minutes as float."""
    if not clock or clock.upper() in ("END", "FINAL", "0.0", ""):
        return 0.0
    try:
        parts = clock.replace(".", ":").split(":")
        if len(parts) == 2:
            return int(parts[0]) + int(parts[1]) / 60.0
        elif len(parts) == 1:
            return float(parts[0]) / 60.0
    except (ValueError, IndexError):
        return None
    return None
