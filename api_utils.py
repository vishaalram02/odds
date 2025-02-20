import requests
from datetime import datetime, timezone, timedelta

API_URL = "https://api.the-odds-api.com"
NOTIF_URL = "https://ntfy.vishy.lol/first_basket"
EVENTS_PATH = "/v4/sports/basketball_nba/events"
ODDS_PATH = "/v4/sports/basketball_nba/events/{event_id}/odds"

NOTIFY_BOOKS = ["betmgm", "draftkings"]

API_KEY = {
    "apiKey": "352b2e3a3b90cd38c804cca9cdfe20ee"
}

QUERY_PARAMS = {
    "bookmakers": "betmgm,draftkings,fanduel,bovada,betrivers",
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

def notify_book_open(book: str, timestamp: int, home_team: str, away_team: str):
    if book not in NOTIFY_BOOKS:
        return

    date = get_date(timestamp)
    requests.post(
        NOTIF_URL,
        data=f"{home_team} vs {away_team} on {date}",
        headers={"Title": f"First basket open on {book}"}
    )
