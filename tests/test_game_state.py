"""Tests for GameState dataclass."""

from src.state.game_state import GameState


def test_game_state_defaults():
    gs = GameState(game_id="1", source="espn", status="pre")
    assert gs.game_id == "1"
    assert gs.source == "espn"
    assert gs.status == "pre"
    assert gs.home_score == 0
    assert gs.away_score == 0
    assert gs.score_diff == 0
    assert gs.is_final is False


def test_game_state_score_diff():
    gs = GameState(game_id="2", source="nba", status="in", home_score=95, away_score=88)
    assert gs.score_diff == 7


def test_game_state_final():
    gs = GameState(game_id="3", source="espn", status="post", home_score=110, away_score=105)
    assert gs.is_final is True
    assert gs.score_diff == 5


def test_game_state_negative_diff():
    gs = GameState(game_id="4", source="nba", status="in", home_score=80, away_score=92)
    assert gs.score_diff == -12
