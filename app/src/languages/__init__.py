import importlib
import logging
from typing import TypedDict

logger = logging.getLogger(__name__)

class Translations(TypedDict):
    isbn: str
    ownership: str
    reading_status: str
    title: str
    subtitle: str
    author: str
    editor: str
    illustrator: str
    translator: str
    publisher: str
    imprint: str
    collection: str
    series: str
    format: str
    genres: str
    first_pub_year: str
    pub_year: str
    authors_country: str
    setting_places: str
    setting_times: str
    language: str
    pages: str
    weight: str
    width: str
    height: str
    spine_width: str
    data_status: str

    done: str
    to_be_edited: str
    to_be_retrieved: str

    input_isbn: str

    google_books: str
    good_reads: str
    open_library: str

    info_books_retrieved: str
    info_connected: str
    info_connecting: str
    info_updating_book: str

    warning_could_not_load: str
    warning_isbn_exists: str
    warning_isbn_invalid: str
    warning_not_on_open_library: str


def load_language(lang_code: str) -> Translations:
    try:
        lang_module = importlib.import_module("." + lang_code, "app.src.languages")
        logger.debug("Loaded language: " + lang_code)
        return lang_module.STRINGS
    except ModuleNotFoundError as e:
        logger.warning("Module not found: " + e.msg)
    except ImportError as e:
        logger.warning("Import error: " + e.msg)
