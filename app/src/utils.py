import json
import logging
import requests

logger = logging.getLogger(__name__)


def get_value(json: str, key: str):
    if key in json:
        return json[key]
    logging.info("Key " + key + " does not exist")
    return None


def fix_result_empty(result):
    if result == None:
        return ""
    if len(result) == 0:
        return ""
    return result


def get_response_message(response: requests.models.Response):
    response_dict = json.loads(response.text)
    if "message" in response_dict:
        return response_dict["message"]
    return ""


# Notion automatically removes commas from select item names
def replace_commas(text: str):
    if text == None:
        return text
    return text.replace(",", "")
