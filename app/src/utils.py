import logging

logger = logging.getLogger(__name__)


def get_value(json: str, key: str):
    if key in json:
        return json[key]
    # logging.warning("Key " + key + " does not exist")
    return None


def fix_result_empty(result):
    if result == None:
        return ""
    if len(result) == 0:
        return ""
    return result
