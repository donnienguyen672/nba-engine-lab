"""Play-by-play adapter — normalizes raw PBP data into canonical events.

Handles both ESPN and NBA Official formats.
Layer: src/adapters
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class PBPEvent:
    """Canonical play-by-play event."""

    event_id: str = ""
    source: str = ""  # "espn" | "nba"
    game_id: str = ""
    period: int = 0
    clock: str = ""
    event_type: str = ""  # "shot", "foul", "turnover", "freethrow", etc.
    description: str = ""
    team_abbr: str = ""
    player_name: str = ""
    home_score: int = 0
    away_score: int = 0
    extra: dict = field(default_factory=dict)


def normalize_espn_pbp(raw: dict, game_id: str = "") -> list[PBPEvent]:
    """Convert raw ESPN PBP/summary JSON to list of canonical PBPEvent.

    Args:
        raw: Raw dict from espn_playbyplay.fetch_playbyplay().
        game_id: Game ID to tag events with.

    Returns:
        List of PBPEvent objects.
    """
    events = []
    plays = raw.get("plays", [])

    for play in plays:
        ev = PBPEvent(
            event_id=str(play.get("id", "")),
            source="espn",
            game_id=game_id,
            period=play.get("period", {}).get("number", 0),
            clock=play.get("clock", {}).get("displayValue", ""),
            event_type=play.get("type", {}).get("text", ""),
            description=play.get("text", ""),
            home_score=play.get("homeScore", 0),
            away_score=play.get("awayScore", 0),
        )
        # Try to extract team
        if "team" in play:
            ev.team_abbr = play["team"].get("abbreviation", "")

        events.append(ev)

    return events


def normalize_nba_pbp(raw: dict, game_id: str = "") -> list[PBPEvent]:
    """Convert raw NBA official PBP JSON to list of canonical PBPEvent.

    Args:
        raw: Raw dict from nba_playbyplay.fetch_playbyplay().
        game_id: Game ID to tag events with.

    Returns:
        List of PBPEvent objects.
    """
    events = []
    game_data = raw.get("game", {})
    actions = game_data.get("actions", [])

    for action in actions:
        ev = PBPEvent(
            event_id=str(action.get("actionNumber", "")),
            source="nba",
            game_id=game_id or str(game_data.get("gameId", "")),
            period=action.get("period", 0),
            clock=action.get("clock", ""),
            event_type=action.get("actionType", ""),
            description=action.get("description", ""),
            team_abbr=action.get("teamTricode", ""),
            player_name=action.get("playerNameI", ""),
            home_score=action.get("scoreHome", 0),
            away_score=action.get("scoreAway", 0),
        )
        events.append(ev)

    return events
