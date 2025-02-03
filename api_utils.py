import requests
from datetime import datetime, timezone, timedelta

API_URL = "https://api.the-odds-api.com"
EVENTS_PATH = "/v4/sports/basketball_nba/events"
ODDS_PATH = "/v4/sports/basketball_nba/events/{event_id}/odds"

API_KEY = {
    "apiKey": "800d662e2f09e9a8c5ec6730ab95796c"
}

QUERY_PARAMS = {
    "bookmakers": "betmgm,draftkings,fanduel,bovada",
    "oddsFormat": "american",
}

def get_events():
    response = requests.get(API_URL + EVENTS_PATH, params=API_KEY)
    return response.json()

def get_odds(event_id, markets):
    url = API_URL + ODDS_PATH.format(event_id=event_id)
    response = requests.get(url, params=QUERY_PARAMS | API_KEY | {"markets": markets})
    return response.json()

def get_timestamp(date: str) -> int:
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    unix_timestamp = int(dt.timestamp())

    return unix_timestamp

def get_date(timestamp: int) -> str:
    est_tz = timezone(timedelta(hours=-5))
    est_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(est_tz)
    return est_dt.strftime("%Y-%m-%d")

