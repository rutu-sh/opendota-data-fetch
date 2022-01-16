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


def get_heroes(heroes_json_path: str) -> List[dict]:
    logging.info("Reading heroes json")
    f = open(heroes_json_path, "r")
    data = json.load(f)
    f.close()
    return data


def get_hero_features() -> List[str]:
    hero_features = [
                "name",
                "base_health_regen",
                "base_mana_regen",
                "base_armor",
                "base_attack_min",
                "base_attack_max",
                "base_str",
                "base_agi",
                "base_int",
                "str_gain",
                "agi_gain",
                "int_gain",
                "attack_range",
                "projectile_speed",
                "attack_rate",
                "move_speed"
        ]
    return hero_features

def read_heroes_data(hero_data_json: str) -> List[dict]:
    f = open(hero_data_json, "r")
    data = json.load(f)
    f.close()
    return data


def process_heroes(heroes: List[dict]) -> List[dict]:
    logging.info("Processing heroes")
    processed_heroes = []
    hero_features = get_hero_features()
    for hero in heroes:
        processed_hero = get_filter_dict(data=hero, keys=hero_features)
        processed_heroes.append(processed_hero)
    logging.info("Finished processing heroes")
    return processed_heroes


def get_heroes_dataframe(heroes: List[dict]) -> pd.DataFrame:
    logging.info("Generating heroes dataframe")
    processed_heroes = process_heroes(heroes=heroes)
    df = pd.DataFrame(processed_heroes)
    logging.info("Generated heroes dataframe")
    return df


def save_heroes_as_csv(output_path: str, heroes_data_json: str):
    logging.info("Saving heroes as csv")
    heroes = get_heroes(heroes_json_path=heroes_data_json)
    df = get_heroes_dataframe(heroes=heroes)
    df.to_csv(output_path, index=False)
    logging.info("Saved heroes data to csv")


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch hero stats')
    parser.add_argument('--heroes-data-json', dest='heroes_data_json', type=str, nargs=1)
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.info("Saving heroe features to csv")
    args = parse_args()
    save_heroes_as_csv(output_path=args.output_path[0], heroes_data_json=args.heroes_data_json[0])
    logging.info("Done")

