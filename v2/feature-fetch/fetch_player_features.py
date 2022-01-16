import time
import json
import argparse
import requests
from typing import List
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse


import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_precision() -> int:
    return 3

def get_pro_players_url() -> str:
    return "https://api.opendota.com/api/proPlayers"

def get_player_profile_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}"

def get_counts_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/counts?significant=1&game_mode=1"

def get_totals_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/totals?significant=1&game_mode=1"


def get_totals_exp_dict() -> dict:
    return {
        'kills': '$[?field="kills"]',
        'deaths': '$[?field="deaths"]',
        'assists': '$[?field="assists"]',
        'kda': '$[?field="kda"]',
        'tower_damage': '$[?field="tower_damage"]',
        'hero_damage': '$[?field="hero_damage"]',
        'hero_healing': '$[?field="hero_healing"]',
        'stuns': '$[?field="stuns"]',
        'tower_kills': '$[?field="tower_kills"]',
        'neutral_kills': '$[?field="neutral_kills"]',
        'courier_kills': '$[?field="courier_kills"]',
        'denies': '$[?field="denies"]',
        'last_hits': '$[?field="last_hits"]'
    }


def get_counts_exp_dict() -> dict:
    return {
        'radiant_games': "$.is_radiant.\'1\'.games",
        'radiant_wins': "$.is_radiant.\'1\'.win",
        'dire_games': "$.is_radiant.\'0\'.games",
        'dire_wins': "$.is_radiant.\'0\'.win",
        'lane_role_games': "$.lane_role.\'{}\'.games",
        'lane_role_wins': "$.lane_role.\'{}\'.win"
    }

class HTTPMethods:
    get = "GET"
    post = "POST"
    patch = "PATCH"


def get_max_retries() -> int:
    return 10


def get_backoff_duration() -> int:
    return 5


def get_default_response() -> requests.Response:
    response = requests.Response()
    response.code = "default response"
    response.error_type = "default response error type"
    response.status_code = 500
    response._content = b'{ "message" : "this is the default response" }'
    return response

def request_with_retries(method: str, url: str, req_kwargs: dict, accepted_status_codes: List[str]) -> requests.Response:
    response = get_default_response()
    backoff = get_backoff_duration()
    max_retries = get_max_retries()
    for i in range(max_retries):
        response = requests.request(url=url, method=method, **req_kwargs)
        if response.status_code in accepted_status_codes:
            break
        logging.info(f"Retrying after {backoff} seconds")
        time.sleep(backoff)
    return response

def parse_dict(exp: str, data: dict) -> list:
    jsonpath_exp = parse(exp)
    return [match.value for match in jsonpath_exp.find(data)]


def parse_data(exp: str, data: dict, default: any = 0):
    match = parse_dict(exp, data)
    return match[0] if len(match) > 0 else default


def get_pro_players(limit: int = 10) -> List[dict]:
    logging.info("Fetching player data")
    url = get_pro_players_url()
    response = request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[200])
    logging.info("Fetched player data")
    if limit == -1:
        return response.json()
    return response.json()[:limit]


def get_player_ids(players: List[dict]) -> List[str]:
    logging.info("Fetching player ids")
    return [player["account_id"] for player in players]



def get_profile_data(account_id: str) -> dict:
    logging.info(f"Fetching profile data for account_id: {account_id}")
    url = get_player_profile_url(account_id=account_id)
    response = request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[200])
    response.raise_for_status()
    profile_data = response.json()
    return {
        'solo_competitive_rank': parse_dict("$.solo_competitive_rank", profile_data)[0],
        'rank_tier': parse_dict("$.rank_tier", profile_data)[0],
        'mmr_estimate': parse_dict("$.mmr_estimate.estimate", profile_data)[0],
        'leaderboard_rank': parse_dict("$.leaderboard_rank", profile_data)[0]
    }


def get_counts(account_id: str) -> dict:
    url = get_counts_url(account_id=account_id)
    response = requests.get(url)
    response = request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[200])
    response.raise_for_status()
    counts_data = response.json()


    expr = get_counts_exp_dict()

    player_counts_data = {
        'radiant_games': parse_data(expr['radiant_games'], counts_data, 0),
        'radiant_wins': parse_data(expr['radiant_wins'], counts_data, 0),
        'dire_games': parse_data(expr['dire_games'], counts_data, 0),
        'dire_wins': parse_data(expr['dire_wins'], counts_data, 0),
    }
    for r in ['radiant', 'dire']:
        player_counts_data[f"{r}_loss"] = player_counts_data[f"{r}_games"] - player_counts_data[f"{r}_wins"]
    for i in range(0, 5, 1):
        lri = f"lane_role_{i}" # lane role i
        player_counts_data[f"{lri}_games"] = parse_data(expr['lane_role_games'].format(i), counts_data, 0)
        player_counts_data[f"{lri}_wins"] = parse_data(expr['lane_role_wins'].format(i), counts_data, 0) 
        player_counts_data[f"{lri}_loss"] = player_counts_data[f"{lri}_games"] - player_counts_data[f"{lri}_wins"]
    
    return player_counts_data


def get_avg(data: dict) -> float:
    if data['n'] <= 0 or data['sum'] <= 0:
        return 0
    else:
        return round(data['sum'] / data['n'], get_precision())


def get_averages(account_id: str) -> dict:
    url = get_totals_url(account_id=account_id)
    response = requests.get(url)
    response = request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[200])
    response.raise_for_status()
    totals_data = response.json()

    default = {'sum': 0, 'n': 0, 'field': 'default'}
    expr = get_totals_exp_dict()

    return {
        'avg_kills': get_avg(parse_data(expr['kills'], totals_data, default)),
        'avg_deaths': get_avg(parse_data(expr['deaths'], totals_data, default)),
        'avg_assists': get_avg(parse_data(expr['assists'], totals_data, default)),
        'avg_kda': get_avg(parse_data(expr['kda'], totals_data, default)),
        'avg_tower_damage': get_avg(parse_data(expr['tower_damage'], totals_data, default)),
        'avg_hero_damage': get_avg(parse_data(expr['hero_damage'], totals_data, default)),
        'avg_hero_healing': get_avg(parse_data(expr['hero_healing'], totals_data, default)),
        'avg_stuns': get_avg(parse_data(expr['stuns'], totals_data, default)),  
        'avg_tower_kills': get_avg(parse_data(expr['tower_kills'], totals_data, default)),
        'avg_neutral_kills': get_avg(parse_data(expr['neutral_kills'], totals_data, default)),
        'avg_courier_kills': get_avg(parse_data(expr['courier_kills'], totals_data, default)),
        'avg_denies': get_avg(parse_data(expr['denies'], totals_data, default)),
        'avg_last_hits': get_avg(parse_data(expr['last_hits'], totals_data, default)),
    }



def calculate_win_rate(rad_wins, rad_games, dire_wins, dire_games) -> float:
    if (dire_games + rad_games) == 0:
        return 0
    return (rad_wins + dire_wins) / (rad_games + dire_games)



def get_player_data(account_id: str) -> dict:
    player_data = {"account_id": str(account_id)}
    
    profile_data = get_profile_data(account_id=account_id)
    counts_data = get_counts(account_id=account_id)
    averages_data = get_averages(account_id=account_id)

    player_data.update(profile_data)
    player_data.update(counts_data)
    player_data.update(averages_data)

    player_data["win_rate"] = calculate_win_rate(
        rad_wins=player_data["radiant_wins"],
        rad_games=player_data["radiant_games"],
        dire_wins=player_data["dire_wins"],
        dire_games=player_data["dire_games"]
    )
    return player_data



def get_pro_players_data(n_players: int = -1):
    logging.info("Fetching pro players data")
    pro_players_data = []
    player_ids = get_player_ids(get_pro_players(limit=n_players))
    for account_id in player_ids:
        try:
            player_data = get_player_data(account_id=account_id)

            pro_players_data.append(player_data)
            time.sleep(2) # prevent too many calls in a min
        except:
            logging.info("Ignoring exception")
            continue
    logging.info("Fetched pro players data")
    return pro_players_data


def get_parser():
    parser = argparse.ArgumentParser(description='Fetch hero stats')
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    parser.add_argument('--n-players', dest='n_players', type=int, nargs=1)
    return parser


def parse_args() -> dict:
    parser = get_parser()
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    args = parse_args() 
    players_data = get_pro_players_data(n_players=args["n_players"][0])
    logging.info("Writing to file")
    with open(args["output_path"][0], "w") as f:
        json.dump(players_data, f, indent=4)
    logging.info("Done")
