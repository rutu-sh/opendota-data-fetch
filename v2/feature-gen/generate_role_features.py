import json
import argparse
from typing import List
from numpy import longlong

import pandas as pd

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_roles_df() -> pd.DataFrame:
    roles = [
                "carry", 
                "nuker", 
                "initiator", 
                "disabler", 
                "durable", 
                "escape", 
                "support", 
                "pusher", 
                "jungler"
        ]
    df = pd.DataFrame({"roles": roles})
    return df


def save_csv(df: pd.DataFrame, path: str):
    logging.info("Saving csv")
    df.to_csv(path, index=False)
    logging.info("Saved csv")


def save_roles_csv(output_path: str):
    df = get_roles_df()
    save_csv(df=df, path=output_path)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch roles')
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    logging.info("Saving heroe features to csv")
    args = parse_args()
    save_roles_csv(output_path=args.output_path[0])
    logging.info("Done")
