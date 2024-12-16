import logging

import requests
from bs4 import BeautifulSoup

from app.src import STRINGS
from app.src.get_data import utils
from app.src.get_data.source_abstract import Source


class BlackWells(Source):
    isbn = None
    html = None

    logger = logging.getLogger(__name__)

    def __init__(self, isbn):
        self.isbn = isbn
        response = requests.get("https://blackwells.co.uk/bookshop/product/" + isbn)
        self.html = BeautifulSoup(response.content, "html.parser")
        if not self.html:
            self.logger.warning(STRINGS["warning_could_not_load"] + STRINGS["blackwells"] + ".")

    def get_title(self):
        soup = self._get_title_soup()
        if soup and soup.contents:
            if len(soup.contents) > 1:
                soup = soup.contents[0]
            if soup.text:
                return soup.text.strip()

    def get_subtitle(self):
        soup = self._get_title_soup()
        if soup:
            soup = soup.find("small")
            if soup and soup.text:
                return soup.text.strip()

    def get_cover_url(self):
        return "https://blackwells.co.uk/jacket/" + self.isbn + ".webp"

    def get_authors(self):
        soup = self._get_authors_soup()
        if soup and soup.contents:
            authors = self._get_authors_filter_name(soup)
            if len(authors) != 0:
                return list(authors)

    def get_contributors(self):
        soup = self._get_authors_soup()
        if soup and soup.contents:
            return self._get_contributors_filter_name(soup)

    def get_publishers(self):
        soup = self.html.find("td", itemprop="publisher")
        text = utils.get_text_from_html(soup, 1)
        if text:
            return [utils.replace_commas(text)]

    def get_imprints(self):
        soup = self.html.find("td", itemprop="publisherImprint")
        text = utils.get_text_from_html(soup, 1)
        if text:
            return [utils.replace_commas(text)]

    def get_series(self):
        ...

    def get_formats(self):
        return utils.replace_commas(utils.find_in_table(self.html, "Edition:"))

    def get_genres(self):
        ...

    def get_first_pub_year(self):
        ...

    def get_pub_year(self):
        soup = self.html.find("td", itemprop="datePublished")
        if soup:
            return utils.get_year(utils.get_text_from_html(soup, 0))

    def get_setting_places(self):
        ...

    def get_setting_times(self):
        ...

    def get_languages(self):
        soup = self.html.find("td", itemprop="inLanguage")
        if soup and soup.text:
            return [utils.replace_commas(soup.text)]

    def get_pages(self):
        soup = self.html.find("td", itemprop="numberOfPages")
        return utils.get_text_from_html(soup, 0)

    def get_weight(self):
        return self._get_number("Weight:")

    def get_width(self):
        return self._get_number("Width:")

    def get_height(self):
        return self._get_number("Height:")

    def get_spine_width(self):
        return self._get_number("Spine width:")

    #

    def _get_title_soup(self):
        return self.html.find("h1", {"class": "product__name"})

    def _get_authors_soup(self):
        return self.html.find("p", {"class": "product__author"})

    @staticmethod
    def _get_authors_filter_name(soup):
        result = set()
        for i in range(1, len(soup.contents), 2):
            name = utils.get_text_from_html(soup, i)
            if name:
                if len(name) == 0 or "\n" in name:
                    break
                if "(" in name:
                    if "author" in name:
                        name = str(name).split(" (")[0]
                        result.add(utils.replace_commas(name))
                else:
                    result.add(utils.replace_commas(name))
        return result

    @staticmethod
    def _get_contributors_filter_name(soup):
        result = dict()
        for i in range(1, len(soup.contents), 2):
            name = utils.get_text_from_html(soup, i)
            if name:
                if len(name) == 0 or "\n" in name:
                    break
                if "(" in name and "author" not in name:
                    name = str(name).split(" (")
                    if name[1][-1] != ")":
                        name[1] = name[1][:-1]
                    result[utils.replace_commas(name[0])] = utils.replace_commas(name[1][:-1])
        return result

    def _get_number(self, key):
        return utils.get_number_only(utils.find_in_table(self.html, key))
