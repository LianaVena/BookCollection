import json
import logging
import requests
from app import DATABASE_ID, headers

logger = logging.getLogger(__name__)


def create_page(data):
    if data != None:
        url = "https://api.notion.com/v1/pages"
        result = requests.post(url, headers=headers, json=_create_payload(data))
        logger.info(
            str(result.status_code)
            + " "
            + result.reason
            + " "
            + _get_response_message(result)
        )
        return result


def _create_payload(data):
    payload = {"parent": {"database_id": DATABASE_ID}}
    if "cover" in data:
        payload["cover"] = data.pop("cover")
    if "icon" in data:
        payload["icon"] = data.pop("icon")
    payload["properties"] = data
    return payload


def _get_response_message(response):
    response_dict = json.loads(response.text)
    if "message" in response_dict:
        return response_dict["message"]
    return ""
