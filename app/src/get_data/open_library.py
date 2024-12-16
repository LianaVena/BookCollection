import logging

import requests

from app.src import STRINGS
from app.src.get_data import utils
from app.src.get_data.source_abstract import Source


class OpenLibrary(Source):
    ol_url = "https://openlibrary.org/"
    dot_json = ".json"

    json = None
    work_json = None

    logger = logging.getLogger(__name__)

    def __init__(self, isbn):
        url = self.ol_url + "isbn/" + isbn + self.dot_json
        response = requests.get(url)
        if response.ok:
            self.json = response.json()
            self.work_json = self._get_work_data(self._get_work_url(self.json))
        else:
            self.logger.warning(STRINGS["warning_could_not_load"] + STRINGS["open_library"] + ".")

    def get_title(self):
        return utils.get_value(self.json, "title")

    def get_subtitle(self):
        return utils.get_value(self.json, "subtitle")

    def get_cover_url(self):
        cover_id = utils.get_value(self.json, "covers")
        if cover_id:
            if isinstance(cover_id, list):
                cover_id = cover_id[0]
            return "https://covers.openlibrary.org/b/id/" + str(cover_id) + ".jpg"

    def get_authors(self):
        result = set()
        authors_json = utils.get_value(self.json, "authors")
        if authors_json:
            for a in authors_json:
                for link in dict(a).values():
                    author = utils.get_value(self._get_author_json(link), "name")
                    if author:
                        if "-" in author:
                            author = author.split("-")[0][:-1]
                        result.add(utils.replace_commas(author))
        if result:
            return list(result)

    def get_contributors(self):
        result = dict()
        cons1 = utils.get_value(self.json, "contributions")
        if cons1:
            for c in cons1:
                if "(" in c:
                    contributor_list = c.split("(")
                    name = contributor_list[0]
                    name = utils.replace_commas(name[:-1])
                    result[name] = contributor_list[1][:-1]
        cons2 = utils.get_value(self.json, "contributors")
        if cons2:
            for c in cons2:
                role = utils.get_value(c, "role")
                name = utils.replace_commas(utils.get_value(c, "name"))
                if role and name:
                    result[name] = role
        if len(result) > 0:
            return result

    def get_publishers(self):
        publishers = utils.get_value(self.json, "publishers")
        if publishers and len(publishers) > 0:
            return [utils.replace_commas(publishers[0])]

    def get_imprints(self):
        imprints = utils.get_value(self.json, "publishers")
        if imprints and len(imprints) > 1:
            imprints = imprints[1:]
            return [utils.replace_commas(i) for i in imprints]

    def get_series(self):
        series = utils.get_value(self.json, "series")
        if series:
            return [utils.replace_commas(str(series[0]).split(",")[0])]

    def get_formats(self):
        result = list()
        book_format = utils.replace_commas(utils.get_value(self.json, "physical_format"))
        if book_format:
            result.append(book_format)
        book_format2 = utils.replace_commas(utils.get_value(self.json, "edition_name"))
        if book_format2:
            result.append(book_format2)
        return result

    def get_genres(self):
        genres = utils.get_value(self.json, "subjects")
        if genres:
            return utils.filter_genres(genres)
        genres = utils.get_value_if_json(self.work_json, "subjects")
        if genres:
            return utils.filter_genres(genres)

    def get_first_pub_year(self):
        return utils.get_year(utils.get_value_if_json(self.work_json, "first_publish_date"))

    def get_pub_year(self):
        date = utils.get_value(self.json, "publish_date")
        if date:
            return utils.get_year(date)

    def get_setting_places(self):
        result = []
        places = utils.get_value_if_json(self.work_json, "subject_places")
        if places:
            for p in places:
                result.append(utils.replace_commas(p))
        return result

    def get_setting_times(self):
        result = []
        times = utils.get_value_if_json(self.work_json, "subject_times")
        if times:
            for t in times:
                result.append(utils.replace_commas(t))
        return result

    def get_languages(self):
        result = []
        lang = utils.get_value(self.json, "languages")
        if lang:
            for l in lang:
                url = self.ol_url + utils.get_value(l, "key") + self.dot_json
                response = requests.get(url)
                name = utils.get_value(response.json(), "name")
                if name:
                    result.append(utils.replace_commas(name))
            return result

    def get_pages(self):
        pages = utils.get_value(self.json, "number_of_pages")
        if pages and str(pages).isdigit() and int(pages) > 0:
            return pages

    def get_weight(self):
        weight = utils.get_value(self.json, "weight")
        if weight:
            return self._get_number_only(weight)

    def get_width(self):
        dims = self._get_dimensions_openlibrary()
        if dims:
            return dims[1]

    def get_height(self):
        dims = self._get_dimensions_openlibrary()
        if dims:
            return dims[0]

    def get_spine_width(self):
        dims = self._get_dimensions_openlibrary()
        if dims:
            return dims[2]

    #

    @staticmethod
    def _get_work_data(work_url):
        response = requests.get(work_url)
        if response.ok:
            return response.json()

    def _get_work_url(self, json):
        works = utils.get_value(json, "works")
        if works:
            return self.ol_url + utils.get_value(works[0], "key") + self.dot_json

    def _get_author_json(self, link):
        url = self.ol_url + link + self.dot_json
        result = requests.get(url).json()
        if result:
            return result

    @staticmethod
    def _get_number_only(result):
        if not result:
            return None
        return "".join(i for i in result if i.isdigit())

    def _get_dimensions_openlibrary(self):
        dims = utils.get_value(self.json, "physical_dimensions")
        if dims:
            if "cent" in dims:
                return
            dims = dims.split(" x ")
            dims[2] = str(dims[2]).removesuffix(" inches")
            return [str(int(float(d) * 25.4)) for d in dims]
