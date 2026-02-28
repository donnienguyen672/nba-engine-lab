"""Scoreboard adapter — normalizes raw scoreboard data into GameState list.

Handles both ESPN and NBA Official formats.
Layer: src/adapters
"""

from __future__ import annotations
from src.state.game_state import GameState


def normalize_espn_scoreboard(raw: dict) -> list[GameState]:
    """Convert raw ESPN scoreboard JSON to list of GameState.

    Args:
        raw: Raw dict from espn_scoreboard.fetch_scoreboard().

    Returns:
        List of GameState objects.
    """
    states = []
    events = raw.get("events", [])

    for event in events:
        competition = event.get("competitions", [{}])[0]
        competitors = competition.get("competitors", [])

        home = next((c for c in competitors if c.get("homeAway") == "home"), {})
        away = next((c for c in competitors if c.get("homeAway") == "away"), {})

        status_obj = event.get("status", {})
        status_type = status_obj.get("type", {})

        # Map ESPN status to canonical
        espn_state = status_type.get("state", "pre")  # "pre", "in", "post"

        period = status_obj.get("period", 0)
        clock = status_obj.get("displayClock", "")

        # Period label
        if period <= 4:
            period_label = f"Q{period}" if period > 0 else ""
        else:
            period_label = f"OT{period - 4}"

        gs = GameState(
            game_id=event.get("id", ""),
            source="espn",
            status=espn_state,
            home_team=home.get("team", {}).get("displayName", ""),
            away_team=away.get("team", {}).get("displayName", ""),
            home_abbr=home.get("team", {}).get("abbreviation", ""),
            away_abbr=away.get("team", {}).get("abbreviation", ""),
            home_score=int(home.get("score", 0)),
            away_score=int(away.get("score", 0)),
            period=period,
            period_label=period_label,
            clock=clock,
            start_time_utc=event.get("date", ""),
            venue=competition.get("venue", {}).get("fullName", ""),
        )
        states.append(gs)

    return states


def normalize_nba_scoreboard(raw: dict) -> list[GameState]:
    """Convert raw NBA official scoreboard JSON to list of GameState.

    Args:
        raw: Raw dict from nba_scoreboard.fetch_scoreboard().

    Returns:
        List of GameState objects.
    """
    states = []
    scoreboard = raw.get("scoreboard", {})
    games = scoreboard.get("games", [])

    for game in games:
        # Map NBA gameStatus: 1=pre, 2=in, 3=post
        status_code = game.get("gameStatus", 1)
        status_map = {1: "pre", 2: "in", 3: "post"}
        status = status_map.get(status_code, "pre")

        period = game.get("period", 0)
        clock = game.get("gameClock", "")
        # NBA gameClock comes as "PT05M32.00S" ISO duration — parse it
        clock = _parse_nba_clock(clock)

        if period <= 4:
            period_label = f"Q{period}" if period > 0 else ""
        else:
            period_label = f"OT{period - 4}"

        home = game.get("homeTeam", {})
        away = game.get("awayTeam", {})

        gs = GameState(
            game_id=str(game.get("gameId", "")),
            source="nba",
            status=status,
            home_team=home.get("teamName", ""),
            away_team=away.get("teamName", ""),
            home_abbr=home.get("teamTricode", ""),
            away_abbr=away.get("teamTricode", ""),
            home_score=int(home.get("score", 0)),
            away_score=int(away.get("score", 0)),
            period=period,
            period_label=period_label,
            clock=clock,
            start_time_utc=game.get("gameTimeUTC", ""),
            venue=game.get("arenaName", ""),
        )
        states.append(gs)

    return states


def _parse_nba_clock(iso_clock: str) -> str:
    """Parse NBA ISO duration clock 'PT05M32.00S' → '5:32'."""
    if not iso_clock or iso_clock == "":
        return ""
    try:
        s = iso_clock.replace("PT", "").replace("S", "")
        if "M" in s:
            parts = s.split("M")
            minutes = int(float(parts[0]))
            seconds = int(float(parts[1])) if parts[1] else 0
            return f"{minutes}:{seconds:02d}"
        else:
            seconds = int(float(s))
            return f"0:{seconds:02d}"
    except (ValueError, IndexError):
        return iso_clock
