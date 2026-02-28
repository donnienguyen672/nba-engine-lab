"""ESPN Play-by-Play data fetcher.

Fetches play-by-play data for a specific game from ESPN's public API.
Layer: src/data (raw fetch only, no normalization).
"""

import requests


ESPN_PBP_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary"


def fetch_playbyplay(game_id: str) -> dict:
    """Fetch ESPN play-by-play data for a specific game.

    Args:
        game_id: ESPN game ID string.

    Returns:
        Raw ESPN game summary/PBP JSON as dict.

    Raises:
        requests.HTTPError: On non-2xx response.
    """
    params = {"event": game_id}
    resp = requests.get(ESPN_PBP_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import json
    import sys

    gid = sys.argv[1] if len(sys.argv) > 1 else "401584793"
    data = fetch_playbyplay(gid)
    print(json.dumps(data, indent=2)[:2000])
