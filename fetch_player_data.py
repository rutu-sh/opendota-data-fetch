import time
import json
import argparse
import requests
from typing import List
from jsonpath_ng import jsonpath, parse


import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

def get_pro_players_url():
    return "https://api.opendota.com/api/proPlayers"

def get_player_profile_url():
    return "https://api.opendota.com/api/players/{account_id}"

def get_counts_url():
    return "https://api.opendota.com/api/players/{account_id}/counts?significant=1"

def get_json_file_path():
    return "data/players/players_data.json"


def parse_dict(exp: str, data: dict) -> list:
    jsonpath_exp = parse(exp)
    return [match.value for match in jsonpath_exp.find(data)]


def parse_data(exp: str, data: dict, default: any = 0):
    match = parse_dict(exp, data)
    return match[0] if len(match) > 0 else default


def get_pro_players(limit: int = 10) -> List[dict]:
    logging.info("Fetching player data")
    response = requests.get(get_pro_players_url())
    logging.info("Fetched player data")
    if limit == -1:
        return response.json()
    return response.json()[:limit]


def get_player_ids(players: List[dict]) -> List[str]:
    logging.info("Fetching player ids")
    return [player["account_id"] for player in players]



def get_profile_data(account_id: str) -> dict:
    logging.info(f"Fetching profile data for account_id: {account_id}")
    url = get_player_profile_url().format(account_id=account_id)
    response = requests.get(url)
    response.raise_for_status()
    profile_data = response.json()
    return {
        'solo_competitive_rank': parse_dict("$.solo_competitive_rank", profile_data)[0],
        'rank_tier': parse_dict("$.rank_tier", profile_data)[0],
        'mmr_estimate': parse_dict("$.mmr_estimate.estimate", profile_data)[0],
        'leaderboard_rank': parse_dict("$.leaderboard_rank", profile_data)[0]
    }


def get_counts(account_id: str) -> dict:
    url = get_counts_url().format(account_id=account_id)
    response = requests.get(url)
    response.raise_for_status()
    counts_data = response.json()

    player_counts_data = {
        'radiant_games': parse_data("$.is_radiant.\'1\'.games", counts_data, 0),
        'radiant_wins': parse_data("$.is_radiant.\'1\'.win", counts_data, 0),
        'dire_games': parse_data("$.is_radiant.\'0\'.games", counts_data, 0),
        'dire_wins': parse_data("$.is_radiant.\'0\'.win", counts_data, 0),
    }
    for r in ['radiant', 'dire']:
        player_counts_data[f"{r}_lose"] = player_counts_data[f"{r}_games"] - player_counts_data[f"{r}_wins"]
    for i in range(0, 5, 1):
        lri = f"lane_role_{i}" # lane role i
        player_counts_data[f"{lri}_games"] = parse_data(f"$.lane_role.\'{i}\'.games", counts_data, 0)
        player_counts_data[f"{lri}_wins"] = parse_data(f"$.lane_role.\'{i}\'.win", counts_data, 0) 
        player_counts_data[f"{lri}_lose"] = player_counts_data[f"{lri}_games"] - player_counts_data[f"{lri}_wins"]
    
    return player_counts_data


def get_player_data(account_id: str) -> dict:
    player_data = {"account_id": str(account_id)}
    profile_data = get_profile_data(account_id=account_id)
    counts_data = get_counts(account_id=account_id)
    player_data.update(profile_data)
    player_data.update(counts_data)
    return player_data


def get_pro_players_data(n_players: int = -1):
    pro_players_data = []
    player_ids = get_player_ids(get_pro_players(limit=n_players))
    for account_id in player_ids:
        pro_players_data.append(get_player_data(account_id=account_id))
        time.sleep(2) # prevent too many calls in a min
    return pro_players_data


if __name__ == "__main__":
    players_data = get_pro_players_data(n_players=50)
    with open(get_json_file_path(), "w") as f:
        json.dump(players_data, f, indent=4)