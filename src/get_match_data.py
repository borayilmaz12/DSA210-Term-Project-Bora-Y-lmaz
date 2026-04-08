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

# player listesi: tier bilgisini eklemek için
players_df = pd.read_csv("data/raw/players.csv")

# match id listesi
match_df = pd.read_csv("data/raw/player_match_ids.csv")

# unique match id al
unique_match_ids = match_df["match_id"].dropna().unique()

rows = []

# önce test için ilk 100 unique maç
for i, match_id in enumerate(unique_match_ids[:300], start=1):
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(f"{i}. match error: {r.status_code}")
        time.sleep(1.2)
        continue

    match = r.json()

    info = match.get("info", {})
    participants = info.get("participants", [])
    game_duration = info.get("gameDuration")
    game_creation = info.get("gameCreation")
    queue_id = info.get("queueId")
    game_mode = info.get("gameMode")

    for p in participants:
        puuid = p.get("puuid")

        # players.csv içindeyse tier bilgisini eşleştirelim
        tier_match = players_df.loc[players_df["puuid"] == puuid, "tier"]
        tier = tier_match.iloc[0] if not tier_match.empty else None

        kills = p.get("kills", 0)
        deaths = p.get("deaths", 0)
        assists = p.get("assists", 0)
        total_minions = p.get("totalMinionsKilled", 0)
        neutral_minions = p.get("neutralMinionsKilled", 0)
        cs_total = total_minions + neutral_minions

        row = {
            "match_id": match_id,
            "puuid": puuid,
            "tier": tier,
            "win": int(bool(p.get("win"))),
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kda": (kills + assists) / max(deaths, 1),
            "champion": p.get("championName"),
            "role": p.get("teamPosition"),
            "visionScore": p.get("visionScore"),
            "damage": p.get("totalDamageDealtToChampions"),
            "damageTaken": p.get("totalDamageTaken"),
            "goldEarned": p.get("goldEarned"),
            "champLevel": p.get("champLevel"),
            "cs_total": cs_total,
            "gameDuration": game_duration,
            "gameCreation": game_creation,
            "queueId": queue_id,
            "gameMode": game_mode
        }

        # dakika başına feature'lar
        if game_duration and game_duration > 0:
            minutes = game_duration / 60
            row["cs_per_min"] = cs_total / minutes
            row["damage_per_min"] = p.get("totalDamageDealtToChampions", 0) / minutes
            row["vision_per_min"] = p.get("visionScore", 0) / minutes
        else:
            row["cs_per_min"] = None
            row["damage_per_min"] = None
            row["vision_per_min"] = None

        rows.append(row)

    print(f"{i}. match done")
    time.sleep(1.2)

final_df = pd.DataFrame(rows)

# sadece ranked solo queue tutmak istersen:
final_df = final_df[final_df["queueId"] == 420]

final_df.to_csv("data/processed/lol_ranked_dataset.csv", index=False)

print(f"Saved {len(final_df)} rows to data/processed/lol_ranked_dataset.csv")