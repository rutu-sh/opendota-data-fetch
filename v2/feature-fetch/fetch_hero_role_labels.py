import time
import json
import argparse
from typing import List
from functools import partial

import requests
from jsonpath_ng.ext import parse

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch hero stats')
    parser.add_argument('--heroes-json-path', dest='heroes_json_path', type=str, nargs=1)
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args

def get_roles() -> List[str]:
    roles = ["carry", "nuker", "initiator", "disabler", "durable", "escape", "support", "pusher", "jungler"]
    return roles


def get_default_roles_dict() -> dict:
    all_roles = get_roles()
    roles_dict = {role: False for role in all_roles}
    return roles_dict


def get_bool_roles(hero_id: str, hero_name: str, hero_roles: List[str]) -> dict:
    bool_roles = {"hero_id": hero_id, "name": hero_name}
    bool_roles.update(get_default_roles_dict())
    for role in hero_roles:
        bool_roles[role.lower()] = True 
    return bool_roles


def get_heroes(heroes_json_path: str) -> List[dict]:
    f = open(heroes_json_path, "r")
    heroes = json.load(f)
    f.close()
    return heroes


def get_all_hero_bool_roles(heroes: List[dict]) -> List[dict]:
    logging.info("Fetching hero-role data")
    data = []
    for hero in heroes:
        hero_bool_role = get_bool_roles(hero_id=hero["id"], hero_name=hero["name"], hero_roles=hero["roles"])
        data.append(hero_bool_role)
    logging.info("Fetched role data for all heroes")
    return data


if __name__ == "__main__":
    logging.info("Fetching hero-role data")
    args = parse_args()
    heroes = get_heroes(heroes_json_path=args.heroes_json_path[0])
    hero_role_data = get_all_hero_bool_roles(heroes=heroes)
    logging.info("Saving to file")
    with open(args.output_path[0], "w") as f:
        json.dump(hero_role_data, f, indent=4)
    logging.info("Done")