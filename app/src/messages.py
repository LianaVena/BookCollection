import json
import logging

logger = logging.getLogger(__name__)


def log_info(message, result):
    logger.info(
        message
        + str(result.status_code)
        + " "
        + result.reason
        + " "
        + _get_response_message(result)
    )

def log_warning(message, result):
    logger.warning(
        message
        + str(result.status_code)
        + " "
        + result.reason
        + " "
        + _get_response_message(result)
    )

def _get_response_message(response):
    response_dict = json.loads(response.text)
    if "message" in response_dict:
        return response_dict["message"]
    return ""
