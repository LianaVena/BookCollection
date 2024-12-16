import logging
from typing import Optional

import bs4
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from app import GOOGLE_API_KEY, options
from ..src import STRINGS

isbn = ""
g_json = dict()  # JSON from Google Books API call
ol_json: dict = dict()  # JSON from OpenLibrary API call
ol_work_json: dict = dict()  # JSON from OpenLibrary API call for work instead of edition
bw_html: Optional[BeautifulSoup] = None  # HTML from BlackWells
gr_html: Optional[BeautifulSoup] = None  # HTML from Goodreads

ol_url = "https://openlibrary.org/"
dot_json = ".json"

logger = logging.getLogger(__name__)


def init(isbn_input, all_data=True):
    global isbn
    global g_json
    global ol_json
    global ol_work_json
    global bw_html
    global gr_html
    isbn = isbn_input
    ol_json = _get_data_openlibrary()
    if not ol_json:
        logger.info(STRINGS["warning_not_on_open_library"])
    else:
        ol_work_json = _get_data_openlibrary_work(_get_work_url(ol_json))
    if not all_data:
        return
    g_json = _get_data_google()
    bw_html = _get_data_blackwells()
    gr_html = _get_data_goodreads()


def _get_data_goodreads():
    with webdriver.Chrome(options=options) as driver:
        url = "https://www.goodreads.com/search?q=" + isbn
        driver.get(url)
        try:
            logger.debug(STRINGS["info_connecting"] + STRINGS["good_reads"] + "...")
            WebDriverWait(driver, 15).until(
                ec.visibility_of_all_elements_located((By.CLASS_NAME, "Text__title2"))
            )
            logger.debug(STRINGS["info_connected"])
        except TimeoutException:
            logger.warning(
                STRINGS["warning_could_not_load"] + STRINGS["good_reads"] + "."
            )
        html = driver.page_source
        if html:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            return BeautifulSoup(html, "html.parser")


def _get_data_openlibrary():
    url = ol_url + "isbn/" + isbn + dot_json
    response = requests.get(url)
    if response.ok:
        return response.json()
    logger.warning(STRINGS["warning_could_not_load"] + STRINGS["open_library"] + ".")


def _get_work_url(json):
    works = _get_value(json, "works")
    if works:
        return ol_url + _get_value(works[0], "key") + dot_json


def _get_data_openlibrary_work(work_url):
    response = requests.get(work_url)
    if response.ok:
        return response.json()


def _get_data_blackwells():
    response = requests.get("https://blackwells.co.uk/bookshop/product/" + isbn)
    return BeautifulSoup(response.content, "html.parser")


def _get_data_google():
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
            return data["items"][0]["volumeInfo"]
    logger.warning(STRINGS["warning_could_not_load"] + STRINGS["google_books"] + ".")


#


def get_title():
    title = _get_value_from_json(g_json, "title")
    if title:
        return title

    title = _get_value_from_json(ol_json, "title")
    if title:
        return title

    title = _get_title_blackwells()
    if title:
        return title

    if gr_html:
        soup = gr_html.find("h1", {"data-testid": "bookTitle"})
        if soup and soup.text:
            return soup.text.strip()


def _get_title_blackwells():
    if bw_html:
        soup = bw_html.find("h1", {"class": "product__name"})
        if soup and soup.contents:
            if len(soup.contents) > 1:
                soup = soup.contents[0]
            if soup.text:
                return soup.text.strip()


def get_subtitle():
    subtitle = _get_value_from_json(g_json, "subtitle")
    if subtitle:
        return subtitle

    subtitle = _get_value_from_json(ol_json, "subtitle")
    if subtitle:
        return subtitle

    if bw_html:
        soup = bw_html.find("h1", {"class": "product__name"})
        if soup:
            soup = soup.find("small")
            if soup and soup.text:
                return soup.text.strip()


def get_cover_url():
    covers = _get_value_from_json(g_json, "imageLinks")
    if covers:
        cover = _get_value(covers, "thumbnail")
        if cover:
            return cover

    cover_id = _get_value_from_json(ol_json, "covers")
    if cover_id:
        if isinstance(cover_id, list):
            cover_id = cover_id[0]
        return "https://covers.openlibrary.org/b/id/" + str(cover_id) + ".jpg"

    return "https://blackwells.co.uk/jacket/" + isbn + ".webp"


def get_authors():
    authors = set()
    ol_authors = _get_authors_openlibrary()
    if ol_authors:
        authors.update(ol_authors)
        return list(authors)

    authors.update(_get_authors_blackwells())
    if len(authors) != 0:
        return list(authors)

    authors.update(_get_value_from_json(g_json, "authors"))
    if len(authors) != 0:
        authors = [_replace_commas(a) for a in authors]
        return authors


def _get_authors_openlibrary():
    if ol_json:
        result = set()
        authors_json = _get_value(ol_json, "authors")
        if authors_json:
            for a in authors_json:
                for link in dict(a).values():
                    author = _get_value(_get_author_json(link), "name")
                    if author:
                        result.add(_replace_commas(author))
        return result


def _get_author_json(link):
    url = ol_url + link + dot_json
    result = requests.get(url).json()
    if result:
        return result


def _get_authors_blackwells():
    if bw_html:
        soup = bw_html.find("p", {"class": "product__author"})
        if soup and soup.contents:
            return _get_authors_blackwells_filter_name(soup)


def _get_authors_blackwells_filter_name(soup):
    result = set()
    for i in range(1, len(soup.contents), 2):
        name = _get_text_from_html(soup, i)
        if name:
            if len(name) == 0 or "\n" in name:
                break
            if "(" in name:
                if "author" in name:
                    name = str(name).split(" (")[0]
                    result.add(_replace_commas(name))
            else:
                result.add(_replace_commas(name))
    return result


def get_editors(contributors):
    keys = ["Editor", "Compiler", "editor"]
    return _get_specific_contributors(contributors, keys)


def get_illustrators(contributors):
    keys = [
        "Illustrator",
        "Cover Art",
        "Drawings",
        "artist",
        "illustrator",
        "colourist",
    ]
    return _get_specific_contributors(contributors, keys)


def get_translators(contributors):
    keys = ["Translator", "translator"]
    return _get_specific_contributors(contributors, keys)


def _get_specific_contributors(contributors, keys):
    result = []
    if contributors:
        for key in contributors.keys():
            if contributors[key] in keys:
                result.append(key)
    return result


def get_contributors():
    result = dict()
    cons1 = _get_value_from_json(ol_json, "contributions")
    if cons1:
        for c in cons1:
            if "(" in c:
                contributor_list = c.split("(")
                name = contributor_list[0]
                name = _replace_commas(name[:-1])
                result[name] = contributor_list[1][:-1]
    cons2 = _get_value_from_json(ol_json, "contributors")
    if cons2:
        for c in cons2:
            role = _get_value(c, "role")
            name = _replace_commas(_get_value(c, "name"))
            if role and name:
                result[name] = role
    if len(result) > 0:
        return result

    return _get_contributors_blackwells()


def _get_contributors_blackwells():
    if bw_html:
        soup = bw_html.find("p", {"class": "product__author"})
        if soup and soup.contents:
            return _get_contributors_blackwells_filter_name(soup)


def _get_contributors_blackwells_filter_name(s):
    result = dict()
    for i in range(1, len(s.contents), 2):
        name = _get_text_from_html(s, i)
        if name:
            if len(name) == 0 or "\n" in name:
                break
            if "(" in name and "author" not in name:
                name = str(name).split(" (")
                if name[1][-1] != ")":
                    name[1] = name[1][:-1]
                result[_replace_commas(name[0])] = _replace_commas(name[1][:-1])
    return result


def get_publishers():
    if bw_html:
        soup = bw_html.find("td", itemprop="publisher")
        text = _get_text_from_html(soup, 1)
        if text:
            return [_replace_commas(text)]

    publishers = _get_value_from_json(ol_json, "publishers")
    if publishers and len(publishers) > 0:
        return [_replace_commas(publishers[0])]

    publisher = _get_value_from_json(g_json, "publisher")
    if publisher:
        return [_replace_commas(publisher)]


def get_imprints():
    if bw_html:
        soup = bw_html.find("td", itemprop="publisherImprint")
        text = _get_text_from_html(soup, 1)
        if text:
            return [_replace_commas(text)]

    imprints = _get_value_from_json(ol_json, "publishers")
    if imprints and len(imprints) > 1:
        imprints = imprints[1:]
        return [_replace_commas(i) for i in imprints]


def get_series():
    series = _get_value_from_json(ol_json, "series")
    if series:
        return [_replace_commas(str(series[0]).split(",")[0])]

    if gr_html:
        soup = gr_html.find("div", {"class": "BookPageTitleSection__title"})
        if soup:
            soup = soup.find("h3")
            if soup and soup.contents:
                soup = soup.contents[0]
                if soup and isinstance(soup, bs4.Tag) and soup.contents:
                    return [_replace_commas(str(soup.contents[0]))]


def get_formats():
    result = set()
    if ol_json:
        book_format = _replace_commas(_get_value(ol_json, "physical_format"))
        book_format2 = _replace_commas(_get_value(ol_json, "edition_name"))
        if book_format:
            result.add(book_format)
        if book_format2:
            result.add(book_format2)
    if bw_html:
        book_format3 = _replace_commas(_find_in_table(bw_html, "Edition:"))
        if book_format3:
            result.add(book_format3)
    return list(result)


def get_genres():
    result = _get_genres_goodreads()
    if result:
        return result

    genres = _get_value_from_json(g_json, "categories")
    if not genres:
        genres = _get_value_from_json(ol_json, "subjects")
        if not genres:
            genres = _get_value_from_json(ol_work_json, "subjects")
    if genres:
        result = []
        for i in range(min(len(genres), 15)):
            result.append(_replace_commas(genres[i]))
        return result


def _get_genres_goodreads():
    if gr_html:
        result = []
        soup = gr_html.find("div", {"data-testid": "genresList"})
        soup = _check_and_go_in_contents(soup)
        soup = _check_and_go_in_contents(soup)
        if soup and soup.contents:
            result = _get_genres_goodreads_names(soup)
        if len(result) > 0 and "Genres" in result:
            result.remove("Genres")
        return result


def _check_and_go_in_contents(genres):
    if genres and genres.contents:
        return genres.contents[0]


def _get_genres_goodreads_names(genres):
    result = []
    for g in genres.contents:
        result.append(_replace_commas(_get_text_from_html(g, 0)))
    return result


def get_first_pub_year():
    if gr_html:
        soup = gr_html.find("p", {"data-testid": "publicationInfo"})
        if soup and soup.text:
            return _get_year(soup.text)
    return _get_year(_get_value_from_json(ol_work_json, "first_publish_date"))


def get_pub_year():
    date = _get_value_from_json(g_json, "publishedDate")
    if date:
        return date.split("-")[0]

    date = _get_value_from_json(ol_json, "publish_date")
    if date:
        return _get_year(date)

    if bw_html:
        soup = bw_html.find("td", itemprop="datePublished")
        if soup:
            return _get_year(_get_text_from_html(soup, 0))


def _get_year(date):
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


def get_setting_places():
    result = []
    places = _get_value_from_json(ol_work_json, "subject_places")
    if places:
        for p in places:
            result.append(_replace_commas(p))
    return result


def get_setting_times():
    result = []
    times = _get_value_from_json(ol_work_json, "subject_times")
    if times:
        for t in times:
            result.append(_replace_commas(t))
    return result


def get_languages():
    languages = _get_language_openlibrary()
    if languages:
        return languages

    if bw_html:
        soup = bw_html.find("td", itemprop="inLanguage")
        if soup and soup.text:
            return [_replace_commas(soup.text)]

    languages = _get_value_from_json(g_json, "language")
    if languages:
        return [_replace_commas(languages)]


def _get_language_openlibrary():
    result = []
    lang = _get_value_from_json(ol_json, "languages")
    if lang:
        for l in lang:
            url = ol_url + _get_value(l, "key") + dot_json
            response = requests.get(url)
            name = _get_value(response.json(), "name")
            if name:
                result.append(_replace_commas(name))
        return result


def get_pages():
    pages = _get_value_from_json(g_json, "pageCount")
    if pages and str(pages).isdigit() and int(pages) > 0:
        return pages

    pages = _get_value_from_json(ol_json, "number_of_pages")
    if pages and str(pages).isdigit() and int(pages) > 0:
        return pages

    if bw_html:
        soup = bw_html.find("td", itemprop="numberOfPages")
        return _get_text_from_html(soup, 0)


def get_weight():
    weight = _get_value_from_json(ol_json, "weight")
    if not weight and bw_html:
        return _get_number_only(_find_in_table(bw_html, "Weight:"))
    return _get_number_only(weight)


def get_width():
    if bw_html:
        width = _get_number_only(_find_in_table(bw_html, "Width:"))
        if width:
            return width
    dims = _get_dimensions_openlibrary()
    if dims:
        return dims[1]


def get_height():
    if bw_html:
        height = _get_number_only(_find_in_table(bw_html, "Height:"))
        if height:
            return height
    dims = _get_dimensions_openlibrary()
    if dims:
        return dims[0]


def get_spine_width():
    if bw_html:
        s_width = _get_number_only(_find_in_table(bw_html, "Spine width:"))
        if s_width:
            return s_width
    dims = _get_dimensions_openlibrary()
    if dims:
        return dims[2]


def _get_dimensions_openlibrary():
    dims = _get_value_from_json(ol_json, "physical_dimensions")
    if dims:
        if "cent" in dims:
            return
        dims = dims.split(" x ")
        dims[2] = str(dims[2]).removesuffix(" inches")
        return [str(int(float(d) * 25.4)) for d in dims]


#


def _get_value(json, key):
    if key in json:
        return json[key]
    logging.debug("Key " + key + " does not exist")
    return None


def _get_value_from_json(json, label):
    if json:
        result = _get_value(json, label)
        return result


def _replace_commas(text):
    if not text:
        return text
    return text.replace(",", "")


def _find_in_table(soup, key):
    if soup:
        s = soup.find("table", {"class": "u-separator-right"})
        if s:
            td = s.find("td", string=key)
            if td:
                tr = td.find_parent("tr")
                if tr:
                    return _get_text_from_html(tr, 3)


def _get_text_from_html(source, i):
    if source and source.contents and len(source.contents) > i:
        return source.contents[i].text


def _get_number_only(result):
    if not result:
        return None
    return "".join(i for i in result if i.isdigit())
