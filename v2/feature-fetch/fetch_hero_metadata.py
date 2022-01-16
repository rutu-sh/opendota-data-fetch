import time
import json
import argparse
from typing import List
from functools import partial

import requests
from jsonpath_ng.ext import parse

import logging
from requests.api import request

logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


class HTTPMethods:
    get = "GET"
    post = "POST"
    patch = "PATCH"


def get_max_retries() -> int:
    return 10


def get_backoff_duration() -> int:
    return 15


def get_default_response() -> requests.Response:
    response = requests.Response()
    response.code = "default response"
    response.error_type = "default response error type"
    response.status_code = 500
    response._content = b'{ "message" : "this is the default response" }'
    return response

def request_with_retries(method: str, url: str, req_kwargs: dict, accepted_status_codes: List[str]) -> requests.Response:
    response = get_default_response()
    backoff = get_backoff_duration()
    max_retries = get_max_retries()
    for i in range(max_retries):
        response = requests.request(url=url, method=method, **req_kwargs)
        if response.status_code in accepted_status_codes:
            break
        logging.info(f"Retrying after {backoff} seconds")
        time.sleep(backoff)
    return response


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Fetch hero stats')
    parser.add_argument('--output-path', dest='output_path', type=str, nargs=1)
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    return args


def get_heroes_url() -> str:
    return "https://api.opendota.com/api/heroes"


def get_heroes_data() -> List[dict]:
    url = get_heroes_url()
    response = request_with_retries(method=HTTPMethods.get, url=url, req_kwargs={}, accepted_status_codes=[200])
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    logging.info("Fetching hero data")
    args = parse_args()
    heroes_data = get_heroes_data()
    logging.info("Saving to file")
    with open(args.output_path[0], "w") as f:
        json.dump(heroes_data, f, indent=4)
    logging.info("Done")

