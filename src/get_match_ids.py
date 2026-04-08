import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
REGION = os.getenv("REGIONAL_ROUTING", "europe")

headers = {
    "X-Riot-Token": API_KEY
}

df = pd.read_csv("data/raw/players.csv")

all_rows = []

# önce test için sadece ilk 50 oyuncu
test_players = df["puuid"].dropna().head(200)

for i, puuid in enumerate(test_players, start=1):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

    params = {
        "start": 0,
        "count": 10,
        "queue": 420
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code == 200:
        match_ids = r.json()
        for match_id in match_ids:
            all_rows.append({
                "puuid": puuid,
                "match_id": match_id
            })
        print(f"{i}. player done, {len(match_ids)} matches")
    else:
        print(f"{i}. player error: {r.status_code}")

    time.sleep(1.2)

match_df = pd.DataFrame(all_rows)
match_df = match_df.drop_duplicates()

match_df.to_csv("data/raw/player_match_ids.csv", index=False)

print(f"Saved {len(match_df)} player-match rows.")