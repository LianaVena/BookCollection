import logging

logger = logging.getLogger(__name__)


def get_number_only(result):
    if not result:
        return None
    return "".join(i for i in result if i.isdigit())


def get_year(date):
    if not date:
        return
    if date.isnumeric() and len(date) <= 4:
        return date
    date = date[-4:]
    while not date.isdigit():
        date = date[-1:]
        if len(date) == 0:
            return None
    return date


def replace_commas(text):
    if not text:
        return text
    return text.replace(",", "")


def filter_genres(genres):
    result = []
    for i in range(min(len(genres), 15)):
        result.append(replace_commas(genres[i]))
    return result


def get_value(json, key):
    if key in json:
        return json[key]
    logger.debug("Key " + key + " does not exist")
    return None


def get_text_from_html(source, i):
    if source and source.contents and len(source.contents) > i and source.contents[i].text:
        return source.contents[i].text
