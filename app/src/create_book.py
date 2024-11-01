import logging
import requests
from app import DATABASE_ID, headers
from ..src.utils import get_response_message

logger = logging.getLogger(__name__)


def create_page(data: dict):
    if data != None:
        url = "https://api.notion.com/v1/pages"
        cover = data.pop("cover")
        icon = data.pop("icon")
        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": data,
            "cover": cover,
            "icon": icon,
        }
        result = requests.post(url, headers=headers, json=payload)
        logger.info(
            str(result.status_code)
            + " "
            + result.reason
            + " "
            + get_response_message(result)
        )
        return result
