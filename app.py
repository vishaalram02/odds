import json
from modal import App, Image, Volume, Period, web_endpoint
from api_utils import get_events, get_odds, get_date, get_timestamp

volume = Volume.from_name("odds-data")
image = Image.debian_slim().pip_install("requests")
app = App("first-basket", image=image)

@app.function(volumes={"/data": volume}, schedule=Period(minutes=30))
def first_basket_cron():
    events = get_events()

    for event in events:
        event_id = event["id"]
        timestamp = get_timestamp(event["commence_time"])
        date = get_date(timestamp)
        home_team = event["home_team"]
        away_team = event["away_team"]

        odds = get_odds(event_id, "player_first_basket")

        try:
            with open(f"/data/first_basket/{date}.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        if event_id not in data:
            data[event_id] = {
                "time": timestamp,
                "home_team": home_team,
                "away_team": away_team,
                "odds": {}
            }

        for bookmaker in odds["bookmakers"]:
            book = bookmaker["key"]
            if book not in data[event_id]["odds"]:
                data[event_id]["odds"][book] = []
            
            market = bookmaker["markets"][0]
            last_update = get_timestamp(market["last_update"])
            players = {outcome["description"]: outcome["price"] for outcome in market["outcomes"]}

            data[event_id]["odds"][book].append({
                "last_update": last_update,
                "players": players
            })

        with open(f"/data/first_basket/{date}.json", "w") as f:
            json.dump(data, f)

@app.function(volumes={"/data": volume})
@web_endpoint()
def first_basket_web(date: str):
    try:
        with open(f"/data/first_basket/{date}.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    return data


@app.local_entrypoint()
def main():
    first_basket_cron.remote()