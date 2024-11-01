import logging
import requests
from app import headers
from ..src import get_data
from ..src.get_books import check_duplicate

logger = logging.getLogger(__name__)


def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": data}
    result = requests.patch(url, json=payload, headers=headers)
    logger.info(str(result.status_code) + " " + result.reason)
    return result


def get_update_page_data_dict(isbn: int):
    result = dict()
    json = get_data.get_data_openlibrary(isbn)
    if json == None or "error" in json:
        logger.info("ISBN not found")
        return
    title = get_data.get_title(json)
    if check_duplicate(title):
        logger.info("Title already in database")
        return
    cover = {
        "type": "external",
        "external": {"url": get_data.get_cover_url(json)},
    }
    result["cover"] = cover
    result["icon"] = cover
    result["Title"] = get_text(title)
    result["ISBN"] = get_number(isbn)
    result["Author"] = get_multi_select(get_data.get_authors(json))
    contributors = get_data.get_contributors(json)
    result["Editor"] = get_multi_select(get_data.get_editors(contributors))
    result["Illustrator"] = get_multi_select(get_data.get_illustrators(contributors))
    result["Translator"] = get_multi_select(get_data.get_translators(contributors))
    result["Publisher"] = get_multi_select(get_data.get_publishers(json))
    result["Format"] = get_multi_select(get_data.get_format(json))
    set_number(result, "Publication Year", get_data.get_pub_year(json))
    work = get_data.get_data_openlibrary_work(get_data.get_work_url(json))
    result["Setting Places"] = get_multi_select(get_data.get_setting_places(work))
    result["Setting Times"] = get_multi_select(get_data.get_setting_times(work))
    result["Language"] = get_multi_select(get_data.get_languages(json))
    set_number(result, "Pages", get_data.get_pages(json))
    set_number(result, "Weight", get_data.get_weight(json))
    return result


def get_text(text: str):
    return {"title": [{"text": {"content": text}}]}


def get_number(num):
    return {"number": int(num)}


def set_number(result: dict, name: str, num):
    if str(num).isdigit() == True:
        result[name] = get_number(num)


def get_multi_select(list: list):
    return {"multi_select": [{"name": name} for name in list]}
