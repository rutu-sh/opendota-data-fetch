import time
import json
import argparse
from typing import List
from functools import partial

from jsonpath_ng.ext import parse

import logging
from requests.api import request


from commons.http_common import HTTPMethods, HTTPStatusCodes
from opendota import request_handler, url_handler

logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch hero stats')
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser 


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args


def get_heroes_data() -> List[dict]:
    url = url_handler.get_heroes_url()
    response = request_handler.request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[HTTPStatusCodes.OK])
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    logging.info("Fetching hero data")
    args = parse_args()
    hero_data = get_heroes_data()
    logging.info("Saving to file")
    with open(args.output_path[0], "w") as f:
        json.dump(hero_data, f, indent=4)
    logging.info("Done fetching heroes data")

