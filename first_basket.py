from modal import App, Image, Volume, Period

API_URL = "https://api.the-odds-api.com"
EVENTS_PATH = "/v4/sports/basketball_nba/events"
ODDS_PATH = "/v4/sports/basketball_nba/events/{event_id}/odds"

QUERY_PARAMS = {
    "bookmakers": "betmgm,draftkings,fanduel",
    "markets": "player_first_basket",
    "oddsFormat": "american",
    "apiKey": "800d662e2f09e9a8c5ec6730ab95796c"
}

volume = Volume.from_name("odds-data")
image = Image.debian_slim().pip_install("requests")
app = App("first-basket", image=image)

with image.imports():
    import requests
    import json
    from datetime import datetime

def get_events():
    response = requests.get(API_URL + EVENTS_PATH, params=QUERY_PARAMS)
    return response.json()

def get_odds(event_id):
    url = API_URL + ODDS_PATH.format(event_id=event_id)
    response = requests.get(url, params=QUERY_PARAMS)
    return response.json()

@app.function(volumes={"/data": volume}, schedule=Period(hours=1))
def get_first_basket_odds():
    events = get_events()

    data = {}
    with open("/data/first_basket.json", "r") as f:
        data = json.load(f)

    for event in events:
        event_id = event["id"]
        commence_time = event["commence_time"]
        home_team = event["home_team"]
        away_team = event["away_team"]

        odds = get_odds(event_id)

        if event_id not in data:
            data[event_id] = {
                "commence_time": commence_time,
                "home_team": home_team,
                "away_team": away_team,
                "odds": {}
            }

        for bookmaker in odds["bookmakers"]:
            key = bookmaker["key"]
            if key not in data[event_id]["odds"]:
                data[event_id]["odds"][key] = []
            
            market = bookmaker["markets"][0]
            data[event_id]["odds"][key].append(market)

    with open("/data/first_basket.json", "w") as f:
        json.dump(data, f)

@app.local_entrypoint()
def main():
    get_first_basket_odds.remote()