import time
import requests
from typing import List


import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


def get_max_retries() -> int:
    return 10


def get_backoff_duration() -> int:
    return 5


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
        logging.info(f"Retrying after {backoff} seconds. url={url}")
        time.sleep(backoff)
    return response


