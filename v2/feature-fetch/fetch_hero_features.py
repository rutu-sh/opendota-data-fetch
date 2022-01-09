import sys
import json
import argparse
from os import P_PGID
from typing import List
import logging

import requests


logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_required_keys() -> List[str]:
    required_keys = [
        'id', 'hero_id', 'name', 'localized_name', 'primary_attr', 'attack_type', 'roles', 
        'base_health', 'base_health_regen', 'base_mana', 'base_mana_regen', 'base_armor', 'base_mr', 
        'base_attack_min', 'base_attack_max', 'base_str', 'base_agi', 'base_int', 'str_gain', 
        'agi_gain', 'int_gain', 'attack_range', 'projectile_speed', 'attack_rate', 'move_speed'
        ]
    return required_keys

def process_hero(res) -> List[dict]:
    h = {k: res[k] for k in get_required_keys()}
    h['hero_idx'] = h['hero_id'] - 1
    return h

def get_hero_stats_url():
    hero_stats_url = "https://api.opendota.com/api/heroStats"
    return hero_stats_url


def fetch_hero_data() -> List[dict]:
    logging.info("Sending get request")
    response = requests.get(get_hero_stats_url())

    hero_data = response.json()
    filtered_data = []

    logging.info("Processing data")
    for hero in hero_data:
        filtered_data.append(process_hero(hero))
    return filtered_data

def get_parser():
    parser = argparse.ArgumentParser(description='Fetch hero stats')
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser


def parse_args() -> dict:
    parser = get_parser()
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":

    args = parse_args()
    hero_data = fetch_hero_data()
    logging.info("Writing to file")
    with open(args["output_path"][0], "w") as f:
        json.dump(hero_data, f, indent=4)
        f.close()
    logging.info("Done")
