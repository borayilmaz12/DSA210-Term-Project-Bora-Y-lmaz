import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
REGION = os.getenv("PLATFORM_REGION", "euw1")

headers = {
    "X-Riot-Token": API_KEY
}

def get_league_entries(url, tier_name):
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(f"Error for {tier_name}: {r.status_code}")
        return []

    data = r.json()
    entries = data.get("entries", [])

    cleaned = []

    for e in entries:
        puuid = e.get("puuid")

        if puuid is None:
            continue

        cleaned.append({
            "puuid": puuid,
            "leaguePoints": e.get("leaguePoints"),
            "wins": e.get("wins"),
            "losses": e.get("losses"),
            "tier": tier_name
        })

    return cleaned

# endpoints
challenger_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
grandmaster_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"
master_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5"

all_players = []
all_players.extend(get_league_entries(challenger_url, "CHALLENGER"))
all_players.extend(get_league_entries(grandmaster_url, "GRANDMASTER"))
all_players.extend(get_league_entries(master_url, "MASTER"))

df = pd.DataFrame(all_players)

df = df.drop_duplicates(subset=["puuid"])

df.to_csv("data/raw/players.csv", index=False)

print(f"Saved {len(df)} players!")