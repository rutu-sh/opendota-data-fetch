import json

import pandas as pd

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_vals_from_dict(data: dict, vals: list) -> dict:
    filtered_dict = {k: data.get(k) for k in vals}
    return filtered_dict


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
