import logging

import requests

from app import GOOGLE_API_KEY
from app.src import STRINGS
from app.src.get_data import utils
from app.src.get_data.source_abstract import Source


class GoogleBooks(Source):
    json = None

    logger = logging.getLogger(__name__)

    def __init__(self, isbn):
        url = (
                "https://www.googleapis.com/books/v1/volumes?q="
                + "isbn:"
                + isbn
                + "&key="
                + GOOGLE_API_KEY
        )
        response = requests.get(url)
        if response.ok:
            data = response.json()
            if data["totalItems"] > 0:
                self.json = data["items"][0]["volumeInfo"]
        else:
            self.logger.warning(STRINGS["warning_could_not_load"] + STRINGS["google_books"] + ".")

    def get_title(self):
        return utils.get_value(self.json, "title")

    def get_subtitle(self):
        return utils.get_value(self.json, "subtitle")

    def get_cover_url(self):
        covers = utils.get_value(self.json, "imageLinks")
        if covers:
            return utils.get_value(covers, "thumbnail")

    def get_authors(self):
        authors = set(utils.get_value(self.json, "authors"))
        if len(authors) != 0:
            return [utils.replace_commas(a) for a in authors]

    def get_contributors(self):
        ...

    def get_publishers(self):
        publisher = utils.get_value(self.json, "publisher")
        if publisher:
            return [utils.replace_commas(publisher)]

    def get_imprints(self):
        ...

    def get_series(self):
        ...

    def get_formats(self):
        ...

    def get_genres(self):
        genres = utils.get_value(self.json, "categories")
        if genres:
            return utils.filter_genres(genres)

    def get_first_pub_year(self):
        ...

    def get_pub_year(self):
        date = utils.get_value(self.json, "publishedDate")
        if date:
            return date.split("-")[0]

    def get_setting_places(self):
        ...

    def get_setting_times(self):
        ...

    def get_languages(self):
        languages = utils.get_value(self.json, "language")
        if languages:
            return [utils.replace_commas(languages)]

    def get_pages(self):
        pages = utils.get_value(self.json, "pageCount")
        if pages and str(pages).isdigit() and int(pages) > 0:
            return pages

    def get_weight(self):
        ...

    def get_width(self):
        ...

    def get_height(self):
        ...

    def get_spine_width(self):
        ...
