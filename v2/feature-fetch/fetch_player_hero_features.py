import time
import json
import argparse
from typing import List

import requests
from jsonpath_ng.ext import parse

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


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
        logging.info(f"Retrying after {backoff} seconds. url={url}")
        time.sleep(backoff)
    return response


def get_precision() -> int:
    return 3

def get_heroes_played_with_url(account_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/heroes?significant=1&game_mode=1"


def get_totals_url(account_id: str, hero_id: str) -> str:
    return f"https://api.opendota.com/api/players/{account_id}/totals?significant=1&game_mode=1&hero_id={hero_id}"


def get_totals_exp_dict() -> dict:
    return {
        'kills': '$[?field="kills"]',
        'deaths': '$[?field="deaths"]',
        'assists': '$[?field="assists"]',
        'kda': '$[?field="kda"]'
    }


def parse_dict(exp: str, data: dict) -> list:
    jsonpath_exp = parse(exp)
    return [match.value for match in jsonpath_exp.find(data)]


def parse_data(exp: str, data: dict, default: any = 0):
    match = parse_dict(exp, data)
    return match[0] if len(match) > 0 else default


def get_avg(data: dict) -> float:
    if data['n'] <= 0 or data['sum'] <= 0:
        return 0
    else:
        return round(data['sum'] / data['n'], get_precision())


def get_heroes_played_with(account_id: str) -> List[dict]:
    url = get_heroes_played_with_url(account_id=account_id)
    response = request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[200])
    response.raise_for_status()
    data = response.json()
    return data


def get_player_hero_totals_data(account_id: str, hero_id: str) -> dict:
    url = get_totals_url(account_id=account_id, hero_id=hero_id)
    response = request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[200])
    response.raise_for_status()
    data = response.json()
    return data


def get_player_hero_totals(account_id: str, hero_id: str) -> dict:

    totals_data = get_player_hero_totals_data(account_id=account_id, hero_id=hero_id)
    default = {'sum': 0, 'n': 0, 'field': 'default'}
    expr = get_totals_exp_dict()

    return {
        'avg_kills': get_avg(parse_data(expr['kills'], totals_data, default)),
        'avg_deaths': get_avg(parse_data(expr['deaths'], totals_data, default)),
        'avg_assists': get_avg(parse_data(expr['assists'], totals_data, default)),
        'avg_kda': get_avg(parse_data(expr['kda'], totals_data, default))
    }


def get_player_hero_data(account_id: str) -> List[dict]:
    logging.info(f"Fetching data for player: {account_id}")
    player_heroes = []
    heroes_played_with = get_heroes_played_with(account_id=account_id)
    for i, hero in enumerate(heroes_played_with):
        print(i)
        player_hero_data = {
            "account_id": account_id, 
            "hero_id": hero["hero_id"],
            "games": hero["games"],
            "wins": hero["win"],
            "games_with": hero["with_games"],
            "wins_with": hero["with_win"],
            "games_against": hero["against_games"],
            "wins_against": hero["against_win"]
        }
        totals_data = get_player_hero_totals(account_id=account_id, hero_id=hero["hero_id"])

        player_hero_data.update(totals_data)
        player_heroes.append(player_hero_data)
        time.sleep(2)

    return player_heroes


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch hero stats')
    parser.add_argument('--heroes-json-path', dest='heroes_json_path', type=str, nargs=1)
    parser.add_argument('--players-json-path', dest='players_json_path', type=str, nargs=1)
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    parser.add_argument('--n-players', dest='n_players', type=int, nargs=1)
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args

def get_players(players_json_path: str, limit: int) -> List[dict]:
    f = open(players_json_path, "r")
    players = json.load(f)
    f.close()
    return players if limit == -1 else players[:limit]


def get_heroes(heroes_json_path: str) -> List[dict]:
    f = open(heroes_json_path, "r")
    heroes = json.load(f)
    f.close()
    return heroes


def fetch_player_hero_edge_features(players: List[dict]) -> List[dict]:
    logging.info("Fetching player-hero edge features")
    edge_features = []
    for i, player in enumerate(players):
        try:
            player_hero_data = get_player_hero_data(account_id=player["account_id"])
            edge_features.extend(player_hero_data)
        except:
            logging.info("Ignoring exception")
            pass
        time.sleep(2)
    logging.info("Fetched player-hero edge features")
    return edge_features


if __name__ == "__main__":
    logging.info("Fetching player-hero data")
    args = parse_args()
    players = get_players(players_json_path=args.players_json_path[0], limit=args.n_players[0])
    data = fetch_player_hero_edge_features(players=players)
    with open(args.output_path[0], "w") as f:
        json.dump(data, f, indent=4)
    f.close()
    logging.info("Done")