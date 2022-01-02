import json
import pandas as pd

import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_player_json_loc():
    return "data/players/players_data.json"


def get_player_csv_loc():
    return "data/features/player.csv"


def save_player_csv():
    logging.info("Fetching data from player data json")
    f = open(get_player_json_loc(), "r")
    player_data = json.load(f)
    logging.info("Generating dataframe")
    df = pd.DataFrame(player_data)
    logging.info("Saving df to csv")
    df.to_csv(get_player_csv_loc(), index=False)
    logging.info("Done")


if __name__ == "__main__":
    save_player_csv()
