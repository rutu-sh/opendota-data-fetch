import json
import argparse
from typing import List, Union, Tuple
from numpy import longlong

import pandas as pd

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def read_json(path: str) -> Union[List[dict], dict]:
    f = open(path, "r")
    data = json.load(f)
    f.close()
    return data


def save_csv(df: pd.DataFrame, path: str):
    logging.info("Saving df to csv")
    df.to_csv(path, index=False)
    logging.info("Saved df to csv")


def get_heroes(heroes_json_path: str) -> List[dict]:
    heroes = read_json(path=heroes_json_path)
    return heroes


def get_hero_role_edges(heroes: List[dict]) -> List[Tuple[str, str]]:
    logging.info("Fetching hero-role edges list")
    hero_role_edges = []
    for hero in heroes:
        for role in hero["roles"]:
            hero_role_edge = (hero["name"], role.lower())
            hero_role_edges.append(hero_role_edge)
    logging.info("Fetched hero-role edges list")
    return hero_role_edges


def get_hero_roles_edges_df(heroes: List[dict]) -> pd.DataFrame:
    logging.info("Generating hero-role edge dataframe")
    cols = ["source", "target"]
    hero_role_edges_list = get_hero_role_edges(heroes=heroes)
    df = pd.DataFrame(hero_role_edges_list, columns=cols)
    logging.info("Generated hero-role edge dataframe")
    return df


def save_hero_role_edge_csv(heroes_data_json_path: str, output_path: str):
    logging.info("Saving hero-role edge csv")
    heroes = get_heroes(heroes_json_path=heroes_data_json_path)
    df = get_hero_roles_edges_df(heroes=heroes)
    save_csv(df=df, path=output_path)
    logging.info("Saved hero-role edge csv")


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch roles')
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
    save_hero_role_edge_csv(heroes_data_json_path=args.heroes_data_json[0], output_path=args.output_path[0])
    logging.info("Done")


