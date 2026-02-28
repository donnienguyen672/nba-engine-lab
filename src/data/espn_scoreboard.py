"""ESPN Scoreboard data fetcher.

Fetches NBA scoreboard data from ESPN's public API.
Layer: src/data (raw fetch only, no normalization).
"""

import requests
from datetime import datetime


ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"


def fetch_scoreboard(date: str | None = None) -> dict:
    """Fetch ESPN NBA scoreboard for a given date.

    Args:
        date: Date string in YYYYMMDD format. Defaults to today.

    Returns:
        Raw ESPN scoreboard JSON as dict.

    Raises:
        requests.HTTPError: On non-2xx response.
    """
    params = {}
    if date:
        params["dates"] = date
    else:
        params["dates"] = datetime.now().strftime("%Y%m%d")

    resp = requests.get(ESPN_SCOREBOARD_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import json
    data = fetch_scoreboard()
    print(json.dumps(data, indent=2)[:2000])
