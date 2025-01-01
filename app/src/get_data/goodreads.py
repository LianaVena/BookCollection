import logging

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from app import options
from app.src import STRINGS
from app.src.get_data import utils
from app.src.get_data.source_abstract import Source


class GoodReads(Source):
    html = None

    logger = logging.getLogger(__name__)

    def __init__(self, isbn):
        with webdriver.Chrome(options=options) as driver:
            url = "https://www.goodreads.com/search?q=" + isbn
            driver.get(url)
            try:
                self.logger.debug(STRINGS["info_connecting"] + STRINGS["good_reads"] + "...")
                WebDriverWait(driver, 15).until(
                    ec.visibility_of_all_elements_located((By.CLASS_NAME, "Text__title2"))
                )
                self.logger.debug(STRINGS["info_connected"])
            except TimeoutException:
                self.logger.warning(
                    STRINGS["warning_could_not_load"] + STRINGS["good_reads"] + "."
                )
            html = driver.page_source
            if html:
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                self.html = BeautifulSoup(html, "html.parser")

    def get_title(self):
        soup = self.html.find("h1", {"data-testid": "bookTitle"})
        if soup and soup.text:
            return soup.text.strip()

    def get_subtitle(self):
        ...

    def get_cover_url(self):
        ...

    def get_authors(self):
        ...

    def get_contributors(self):
        ...

    def get_publishers(self):
        ...

    def get_imprints(self):
        ...

    def get_series(self):
        soup = self.html.find("div", {"class": "BookPageTitleSection__title"})
        if soup:
            soup = soup.find("h3")
            if soup and soup.contents:
                soup = soup.contents[0]
                if soup and isinstance(soup, Tag) and soup.contents:
                    return [utils.replace_commas(str(soup.contents[0]))]

    def get_formats(self):
        ...

    def get_genres(self):
        result = []
        soup = self.html.find("div", {"data-testid": "genresList"})
        soup = self._check_and_go_in_contents(soup)
        soup = self._check_and_go_in_contents(soup)
        if soup and soup.contents:
            for g in soup.contents:
                result.append(utils.replace_commas(utils.get_text_from_html(g, 0)))
        if len(result) > 0 and "Genres" in result:
            result.remove("Genres")
        return result

    def get_first_pub_year(self):
        soup = self.html.find("p", {"data-testid": "publicationInfo"})
        if soup and soup.text:
            return utils.get_year(soup.text)

    def get_pub_year(self):
        ...

    def get_setting_places(self):
        ...

    def get_setting_times(self):
        ...

    def get_languages(self):
        ...

    def get_pages(self):
        ...

    def get_weight(self):
        ...

    def get_width(self):
        ...

    def get_height(self):
        ...

    def get_spine_width(self):
        ...

    #

    @staticmethod
    def _check_and_go_in_contents(genres):
        if genres and genres.contents:
            return genres.contents[0]
