"""NBA Official Play-by-Play data fetcher.

Fetches play-by-play from NBA CDN live data endpoint.
Layer: src/data (raw fetch only, no normalization).
"""

import requests


NBA_PBP_URL_TEMPLATE = "https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{game_id}.json"


def fetch_playbyplay(game_id: str) -> dict:
    """Fetch NBA official play-by-play for a specific game.

    Args:
        game_id: NBA game ID string (e.g., '0022400001').

    Returns:
        Raw NBA PBP JSON as dict.

    Raises:
        requests.HTTPError: On non-2xx response.
    """
    url = NBA_PBP_URL_TEMPLATE.format(game_id=game_id)
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nba.com/",
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    import json
    import sys

    gid = sys.argv[1] if len(sys.argv) > 1 else "0022400001"
    data = fetch_playbyplay(gid)
    print(json.dumps(data, indent=2)[:2000])
