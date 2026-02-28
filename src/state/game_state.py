"""Canonical GameState dataclass.

Pure state representation. No I/O, no side effects.
Layer: src/state
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GameState:
    """Canonical representation of a single NBA game's state."""

    game_id: str
    source: str  # "espn" | "nba"
    status: str  # "pre" | "in" | "post"

    # Teams
    home_team: str = ""
    away_team: str = ""
    home_abbr: str = ""
    away_abbr: str = ""

    # Scores
    home_score: int = 0
    away_score: int = 0

    # Clock
    period: int = 0
    period_label: str = ""  # "Q1", "Q2", "OT1", etc.
    clock: str = ""  # "5:32", "END", ""

    # Derived
    score_diff: int = 0  # home - away
    is_final: bool = False

    # Metadata
    start_time_utc: str = ""
    venue: str = ""

    # Extensible
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        self.score_diff = self.home_score - self.away_score
        if self.status == "post":
            self.is_final = True
