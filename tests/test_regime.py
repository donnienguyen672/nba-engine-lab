"""Tests for regime classifier."""

from src.state.game_state import GameState
from src.state.regime import classify_regime


def _make_state(**kwargs) -> GameState:
    defaults = {"game_id": "test", "source": "espn", "status": "in"}
    defaults.update(kwargs)
    return GameState(**defaults)


def test_pregame():
    s = _make_state(status="pre")
    assert classify_regime(s) == "pregame"


def test_final():
    s = _make_state(status="post", home_score=100, away_score=95)
    assert classify_regime(s) == "final"


def test_early_q1():
    s = _make_state(period=1, clock="8:00")
    assert classify_regime(s) == "early"


def test_early_q2():
    s = _make_state(period=2, clock="3:00")
    assert classify_regime(s) == "early"


def test_mid_q3():
    s = _make_state(period=3, clock="6:00")
    assert classify_regime(s) == "mid"


def test_clutch():
    s = _make_state(period=4, clock="2:30", home_score=100, away_score=98)
    assert classify_regime(s) == "clutch"


def test_garbage():
    s = _make_state(period=4, clock="4:00", home_score=120, away_score=90)
    assert classify_regime(s) == "garbage"


def test_closing():
    s = _make_state(period=4, clock="8:00", home_score=90, away_score=85)
    assert classify_regime(s) == "closing"


def test_overtime():
    s = _make_state(period=5, clock="3:00", home_score=110, away_score=110)
    assert classify_regime(s) == "overtime"
