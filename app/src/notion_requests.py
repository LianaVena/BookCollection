import json
import logging
import os

import requests

from app import DATABASE_ID, headers
from ..src import STRINGS
from ..src.messages import log_info, log_warning
from ..src.update_books import get_update_page_data_dict

logger = logging.getLogger(__name__)


def get_pages(payload=None):
    if not payload:
        payload = dict()
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    all_pages = []
    next_cursor = None
    while True:
        if next_cursor:
            payload["start_cursor"] = next_cursor
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            log_warning(STRINGS["warning_could_not_retrieve_from_db"], response)
            break
        data = response.json()
        all_pages.extend(data["results"])
        next_cursor = data.get("next_cursor")
        if not next_cursor:
            break
    result = dict()
    result["results"] = all_pages
    with open(os.getcwd() + "/app/files/db.json", "w", encoding="utf8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


def get_pages_to_be_edited():
    json_pages = get_pages(
        {"filter": {"property": "Data status", "select": {"equals": "To be retrieved"}}}
    )
    result = dict()
    for x in json_pages["results"]:
        result[x["id"]] = x["properties"]["ISBN"]["title"][0]["text"]["content"]
    return result


def create_page(data):
    if data:
        url = "https://api.notion.com/v1/pages"
        result = requests.post(url, headers=headers, json=_create_payload(data))
        log_info(STRINGS["info_add_book"], result)
        return result


def update_page(page_id, data):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = _create_payload(data)
    result = requests.patch(url, json=payload, headers=headers)
    log_info(STRINGS["info_update_book"], result)
    return result


def update_pages(pages):
    for page_id in pages.keys():
        data = get_update_page_data_dict(pages[page_id])
        logger.info(
            STRINGS["info_updating_book"]
            + data["Title"]["rich_text"][0]["text"]["content"]
            + "..."
        )
        update_page(page_id, data)


def _create_payload(data):
    payload = {"parent": {"database_id": DATABASE_ID}}
    if "cover" in data:
        payload["cover"] = data.pop("cover")
    if "icon" in data:
        payload["icon"] = data.pop("icon")
    payload["properties"] = data
    return payload


def check_duplicate(isbn):
    data = get_pages({"filter": {"property": "ISBN", "title": {"equals": isbn}}})
    return len(data["results"]) > 0
