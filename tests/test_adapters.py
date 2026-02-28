"""Tests for scoreboard and playbyplay adapters."""

from src.adapters.scoreboard_adapter import (
    normalize_espn_scoreboard,
    normalize_nba_scoreboard,
    _parse_nba_clock,
)
from src.adapters.playbyplay_adapter import (
    normalize_espn_pbp,
    normalize_nba_pbp,
)


# --- ESPN Scoreboard Adapter ---

MOCK_ESPN_SCOREBOARD = {
    "events": [
        {
            "id": "401584793",
            "date": "2026-02-28T00:00Z",
            "competitions": [
                {
                    "competitors": [
                        {
                            "homeAway": "home",
                            "score": "105",
                            "team": {
                                "displayName": "Los Angeles Lakers",
                                "abbreviation": "LAL",
                            },
                        },
                        {
                            "homeAway": "away",
                            "score": "98",
                            "team": {
                                "displayName": "Boston Celtics",
                                "abbreviation": "BOS",
                            },
                        },
                    ],
                    "venue": {"fullName": "Crypto.com Arena"},
                }
            ],
            "status": {
                "period": 3,
                "displayClock": "4:32",
                "type": {"state": "in"},
            },
        }
    ]
}


def test_espn_scoreboard_basic():
    states = normalize_espn_scoreboard(MOCK_ESPN_SCOREBOARD)
    assert len(states) == 1
    s = states[0]
    assert s.game_id == "401584793"
    assert s.source == "espn"
    assert s.home_abbr == "LAL"
    assert s.away_abbr == "BOS"
    assert s.home_score == 105
    assert s.away_score == 98
    assert s.period == 3
    assert s.period_label == "Q3"
    assert s.clock == "4:32"
    assert s.status == "in"


def test_espn_scoreboard_empty():
    states = normalize_espn_scoreboard({"events": []})
    assert states == []


# --- NBA Scoreboard Adapter ---

MOCK_NBA_SCOREBOARD = {
    "scoreboard": {
        "games": [
            {
                "gameId": "0022400100",
                "gameStatus": 2,
                "period": 4,
                "gameClock": "PT05M32.00S",
                "gameTimeUTC": "2026-02-28T01:00:00Z",
                "arenaName": "Madison Square Garden",
                "homeTeam": {
                    "teamName": "Knicks",
                    "teamTricode": "NYK",
                    "score": 88,
                },
                "awayTeam": {
                    "teamName": "Heat",
                    "teamTricode": "MIA",
                    "score": 85,
                },
            }
        ]
    }
}


def test_nba_scoreboard_basic():
    states = normalize_nba_scoreboard(MOCK_NBA_SCOREBOARD)
    assert len(states) == 1
    s = states[0]
    assert s.game_id == "0022400100"
    assert s.source == "nba"
    assert s.home_abbr == "NYK"
    assert s.away_abbr == "MIA"
    assert s.home_score == 88
    assert s.away_score == 85
    assert s.period == 4
    assert s.clock == "5:32"
    assert s.status == "in"


def test_nba_scoreboard_empty():
    states = normalize_nba_scoreboard({"scoreboard": {"games": []}})
    assert states == []


# --- NBA Clock Parser ---

def test_parse_nba_clock_normal():
    assert _parse_nba_clock("PT05M32.00S") == "5:32"


def test_parse_nba_clock_zero():
    assert _parse_nba_clock("PT00M00.00S") == "0:00"


def test_parse_nba_clock_empty():
    assert _parse_nba_clock("") == ""


# --- PBP Adapters ---

def test_espn_pbp_empty():
    events = normalize_espn_pbp({"plays": []})
    assert events == []


def test_nba_pbp_empty():
    events = normalize_nba_pbp({"game": {"actions": []}})
    assert events == []


def test_espn_pbp_basic():
    raw = {
        "plays": [
            {
                "id": "1",
                "period": {"number": 1},
                "clock": {"displayValue": "10:00"},
                "type": {"text": "Jumpball"},
                "text": "Jump ball won by LAL",
                "homeScore": 0,
                "awayScore": 0,
            }
        ]
    }
    events = normalize_espn_pbp(raw, game_id="401584793")
    assert len(events) == 1
    assert events[0].event_type == "Jumpball"
    assert events[0].source == "espn"


def test_nba_pbp_basic():
    raw = {
        "game": {
            "gameId": "0022400100",
            "actions": [
                {
                    "actionNumber": 1,
                    "period": 1,
                    "clock": "PT12M00.00S",
                    "actionType": "jumpball",
                    "description": "Jump Ball",
                    "teamTricode": "NYK",
                    "playerNameI": "M. Robinson",
                    "scoreHome": 0,
                    "scoreAway": 0,
                }
            ],
        }
    }
    events = normalize_nba_pbp(raw)
    assert len(events) == 1
    assert events[0].event_type == "jumpball"
    assert events[0].source == "nba"
    assert events[0].player_name == "M. Robinson"
