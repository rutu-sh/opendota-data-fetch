import json
import argparse
from typing import List

import pandas as pd

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_filter_dict(data: dict, keys: List[str]) -> dict:
    filtered_dict = {}
    for key in keys:
        filtered_dict[key] = data[key]
    return filtered_dict


def get_players(players_json_path: str) -> List[dict]:
    logging.info("Reading players data")
    f = open(players_json_path, "r")
    data = json.load(f)
    f.close()
    return data


def get_player_features() -> dict:
    player_features = [
        "account_id",
        "mmr_estimate",
        "lane_role_0_games",
        "lane_role_0_wins",
        "lane_role_0_loss",
        "lane_role_1_games",
        "lane_role_1_wins",
        "lane_role_1_loss",
        "lane_role_2_games",
        "lane_role_2_wins",
        "lane_role_2_loss",
        "lane_role_3_games",
        "lane_role_3_wins",
        "lane_role_3_loss",
        "lane_role_4_games",
        "lane_role_4_wins",
        "lane_role_4_loss",
        "avg_kills",
        "avg_deaths",
        "avg_assists",
        "avg_kda",
        "avg_tower_damage",
        "avg_hero_damage",
        "avg_hero_healing",
        "avg_stuns",
        "avg_tower_kills",
        "avg_neutral_kills",
        "avg_courier_kills",
        "avg_denies",
        "avg_last_hits",
        "win_rate"
    ]
    return player_features


def process_players(players: List[dict]) -> List[dict]:
    logging.info("Processing players")
    processed_players = []
    player_features = get_player_features()
    for player in players:
        processed_player = get_filter_dict(data=player, keys=player_features)
        processed_players.append(processed_player)
    logging.info("Finished processing players")
    return processed_players


def get_players_dataframe(players: List[dict]) -> pd.DataFrame:
    logging.info("Generating players dataframe")
    processed_players = process_players(players=players)
    df = pd.DataFrame(processed_players)
    logging.info("Generated players dataframe")
    return df


def save_players_as_csv(output_path: str, players_data_json: str):
    logging.info("Saving players as csv")
    players = get_players(players_json_path=players_data_json)
    df = get_players_dataframe(players=players)
    df.to_csv(output_path, index=False)
    logging.info("Saved players data as csv")


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch player stats')
    parser.add_argument('--players-data-json', dest='players_data_json', type=str, nargs=1)
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.info("Saving heroe features to csv")
    args = parse_args()
    save_players_as_csv(output_path=args.output_path[0], players_data_json=args.players_data_json[0])
    logging.info("Done")
