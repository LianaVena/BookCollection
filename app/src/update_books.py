from app import SOURCE_BLACKWELLS, SOURCE_GOODREADS, SOURCE_GOOGLE_BOOKS, SOURCE_OPEN_LIBRARY
from .get_data.sources import Sources
from ..src import STRINGS
from ..src.get_data.get_data import GetData


def get_minimal_data(isbn):
    result = dict()
    data = GetData(isbn)
    result[STRINGS["isbn"]] = _get_isbn(isbn)
    _set_rich_text(result, STRINGS["title"], data.get_title())
    cover_url = data.get_cover_url()
    if cover_url:
        cover = {
            "type": "external",
            "external": {"url": cover_url},
        }
        result["cover"] = cover
        result["icon"] = cover
    _set_multi_select(result, STRINGS["author"], data.get_authors())
    result[STRINGS["data_status"]] = {"select": {"name": STRINGS["to_be_retrieved"]}}
    return result


def get_update_page_data_dict(isbn):
    result = dict()
    data = GetData(isbn, Sources(SOURCE_BLACKWELLS, SOURCE_GOODREADS, SOURCE_GOOGLE_BOOKS, SOURCE_OPEN_LIBRARY), True)
    result[STRINGS["isbn"]] = _get_isbn(isbn)
    cover_url = data.get_cover_url()
    if cover_url:
        cover = {
            "type": "external",
            "external": {"url": cover_url},
        }
        result["cover"] = cover
        result["icon"] = cover
    _set_rich_text(result, STRINGS["title"], data.get_title())
    _set_rich_text(result, STRINGS["subtitle"], data.get_subtitle())
    _set_multi_select(result, STRINGS["author"], data.get_authors())
    contributors = data.get_contributors()
    _set_multi_select(result, STRINGS["editor"], data.get_editors(contributors))
    _set_multi_select(
        result, STRINGS["illustrator"], data.get_illustrators(contributors)
    )
    _set_multi_select(
        result, STRINGS["translator"], data.get_translators(contributors)
    )
    _set_multi_select(result, STRINGS["publisher"], data.get_publishers())
    _set_multi_select(result, STRINGS["imprint"], data.get_imprints())
    _set_multi_select(result, STRINGS["series"], data.get_series())
    _set_multi_select(result, STRINGS["format"], data.get_formats())
    _set_multi_select(result, STRINGS["genres"], data.get_genres())
    _set_number(result, STRINGS["first_pub_year"], data.get_first_pub_year())
    _set_number(result, STRINGS["pub_year"], data.get_pub_year())
    _set_multi_select(result, STRINGS["setting_places"], data.get_setting_places())
    _set_multi_select(result, STRINGS["setting_times"], data.get_setting_times())
    _set_multi_select(result, STRINGS["language"], data.get_languages())
    _set_number(result, STRINGS["pages"], data.get_pages())
    _set_number(result, STRINGS["weight"], data.get_weight())
    _set_number(result, STRINGS["width"], data.get_width())
    _set_number(result, STRINGS["height"], data.get_height())
    _set_number(result, STRINGS["spine_width"], data.get_spine_width())
    result[STRINGS["data_status"]] = {"select": {"name": STRINGS["to_be_edited"]}}
    return result


def _get_isbn(text):
    return {"title": [{"text": {"content": text}}]}


def _get_isbn_value(item):
    return item["title"][0]["text"]["content"]


def _get_rich_text(text):
    return {"rich_text": [{"text": {"content": text}}]}


def _set_rich_text(result, name, text):
    if text:
        result[name] = _get_rich_text(text)


def _get_rich_text_value(item):
    return item["rich_text"][0]["text"]["content"]


def _get_number(num):
    return {"number": int(num)}


def _set_number(result, name, num):
    if str(num).isdigit():
        result[name] = _get_number(num)


def _get_number_value(item):
    return item["number"]


def _get_multi_select(items):
    return {"multi_select": [{"name": name} for name in items]}


def _set_multi_select(result, name, items):
    if items and len(items) > 0:
        result[name] = _get_multi_select(items)


def _get_multi_select_value(items):
    return [name["name"] for name in items["multi_select"]]
