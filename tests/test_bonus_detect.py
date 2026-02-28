"""Tests for bonus detection stub."""

from src.state.game_state import GameState
from src.state.bonus_detect import detect_bonus


def test_bonus_defaults():
    gs = GameState(game_id="1", source="espn", status="in")
    result = detect_bonus(gs)
    assert result["home_bonus"] is False
    assert result["away_bonus"] is False
    assert result["home_double_bonus"] is False
    assert result["away_double_bonus"] is False


def test_bonus_from_extra():
    gs = GameState(
        game_id="2",
        source="nba",
        status="in",
        extra={"home_bonus": True, "away_bonus": False},
    )
    result = detect_bonus(gs)
    assert result["home_bonus"] is True
    assert result["away_bonus"] is False
