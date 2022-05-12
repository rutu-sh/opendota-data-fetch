import time
import json
import argparse
import requests
from typing import List
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse


from commons.http_common import HTTPMethods, HTTPStatusCodes
from opendota import request_handler, url_handler


import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_batch_players() -> int:
    return 30


def read_saved_hero_file(fpath: str) -> dict:
    f = open(fpath, "r")
    saved_heroes = json.load(f)
    f.close()
    return saved_heroes


def write_to_saved_hero_file(saved_heroes: dict, fpath: str):
    f = open(fpath, "w")
    json.dump(saved_heroes, f)
    f.close()
    





