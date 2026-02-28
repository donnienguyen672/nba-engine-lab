#!/usr/bin/env python3
"""ESPN Feed Experiment Runner.

Fetches ESPN scoreboard for today, normalizes via adapter,
prints a small table: game_id, away@home, scores, quarter, clock.

Usage:
    python experiments/espn_feed/run.py
    python experiments/espn_feed/run.py 20260228   # specific date
"""

import sys
import os

# Ensure repo root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.data.espn_scoreboard import fetch_scoreboard
from src.adapters.scoreboard_adapter import normalize_espn_scoreboard
from src.ui.panels.live_scoreboard import print_scoreboard
from src.ui.panels.game_eval import print_eval


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else None

    print("=" * 60)
    print("ESPN FEED EXPERIMENT")
    print(f"Date: {date or 'today'}")
    print("=" * 60)

    try:
        raw = fetch_scoreboard(date)
    except Exception as e:
        print(f"[ERROR] Failed to fetch ESPN scoreboard: {e}")
        sys.exit(1)

    states = normalize_espn_scoreboard(raw)

    print(f"\nGames found: {len(states)}")
    print()

    print("--- SCOREBOARD ---")
    print_scoreboard(states)

    print()
    print("--- GAME EVAL ---")
    print_eval(states)

    print()
    print(f"Source: espn | Games: {len(states)}")


if __name__ == "__main__":
    main()
