import time
import json
import argparse
from typing import List, Union

import pandas as pd
import requests
from jsonpath_ng.ext import parse

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)



def get_filter_dict(data: dict, keys: List[str]) -> dict:
    filtered_dict = {}
    for key in keys:
        filtered_dict[key] = data[key]
    return filtered_dict


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


def read_json(path: str) -> Union[List[dict], dict]:
    f = open(path, "r")
    data = json.load(f)
    f.close()
    return data


def get_heroes(heroes_json_path: str) -> List[dict]:
    logging.info("Reading heroes")
    heroes = read_json(heroes_json_path)
    logging.info("Fetched heroes")
    return heroes


def get_hero_id_name_mapping(heroes: List[dict]) -> dict:
    logging.info("Fetching hero-id to hero-name mapping")
    mapping = {}
    for hero in heroes:
        mapping[str(hero["hero_id"])] = hero["name"]
    logging.info("Generated hero-id to hero-name mapping")
    return mapping


def get_player_hero_data(player_hero_json_path: str) -> List[dict]:
    logging.info("Fetching player-hero data")
    player_hero_data = read_json(path=player_hero_json_path)
    logging.info("Fetched player-hero data")
    return player_hero_data


def get_player_hero_features() -> dict:
    player_hero_features = [
                "wins_with",  # wins with hero in player's team
                "wins_against", # wins with hero in opposite team
                "games_with", # games with hero in player's team
                "games_against", # games with hero in opposite team
                "games", # games with played using hero
                "wins", # wins with played using hero
                "avg_kills",
                "avg_assists",
                "avg_deaths",
                "avg_kda"
        ]
    return player_hero_features


def process_player_hero_data(player_hero_data: dict, hero_id_name_mapping: dict, features: List[str]) -> dict:
    player_hero_edge_data = {"source": player_hero_data["account_id"], "target": hero_id_name_mapping[player_hero_data["hero_id"]]}
    filtered_player_hero_data = get_filter_dict(data=player_hero_data, keys=features)
    player_hero_edge_data.update(filtered_player_hero_data)
    return player_hero_edge_data


def fetch_player_hero_edge_features(player_hero_json_path: str, heroes_json_path: str) -> List[dict]:
    logging.info("Generating player-hero edge features")
    heroes = get_heroes(heroes_json_path=heroes_json_path)
    player_hero_data = get_player_hero_data(player_hero_json_path=player_hero_json_path)
    hero_id_name_mapping = get_hero_id_name_mapping(heroes=heroes)
    features = get_player_hero_features()

    player_hero_edge_features = []
    for player_hero_edge in player_hero_data:
        player_hero_edge_feature = process_player_hero_data(player_hero_data=player_hero_edge, 
        hero_id_name_mapping=hero_id_name_mapping, features=features)
        player_hero_edge_features.append(player_hero_edge_feature)
    logging.info("Generated player-hero edge features")
    return player_hero_edge_features


def save_csv(df: pd.DataFrame, path: str):
    logging.info("Saving df to csv")
    df.to_csv(path, index=False)
    logging.info("Saved df to csv")

def get_player_hero_edge_df(edges_data: List[dict]) -> pd.DataFrame:
    df = pd.DataFrame(edges_data)
    return df


def save_player_hero_edge_features_csv(player_hero_json_path: str, heroes_json_path: str, output_path: str):
    logging.info("Saving player-hero edge features csv")
    edges_data = fetch_player_hero_edge_features(player_hero_json_path=player_hero_json_path, heroes_json_path=heroes_json_path)
    df = get_player_hero_edge_df(edges_data=edges_data)
    save_csv(df=df, path=output_path)
    logging.info("Saved player-hero edge features csv")


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch roles')
    parser.add_argument('--player-hero-data-json', dest='player_hero_data_json', type=str, nargs=1)
    parser.add_argument('--heroes-data-json', dest='heroes_data_json', type=str, nargs=1)
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.info("Saving player-hero features to csv")
    args = parse_args()
    save_player_hero_edge_features_csv(player_hero_json_path=args.player_hero_data_json[0], heroes_json_path=args.heroes_data_json[0], output_path=args.output_path[0])
    logging.info("Done")



