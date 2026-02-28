"""NBA Official Scoreboard data fetcher.

Fetches NBA scoreboard from the official NBA CDN / nba_api.
Layer: src/data (raw fetch only, no normalization).
"""

import requests
from datetime import datetime


NBA_SCOREBOARD_URL = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"


def fetch_scoreboard(date: str | None = None) -> dict:
    """Fetch NBA official scoreboard.

    Args:
        date: Date string in YYYY-MM-DD format. Currently fetches today's
              scoreboard from CDN (date param reserved for future nba_api use).

    Returns:
        Raw NBA scoreboard JSON as dict.

    Raises:
        requests.HTTPError: On non-2xx response.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nba.com/",
    }

    # CDN endpoint always returns today's games.
    # For historical dates, swap to nba_api when ready.
    resp = requests.get(NBA_SCOREBOARD_URL, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import json
    data = fetch_scoreboard()
    print(json.dumps(data, indent=2)[:2000])
