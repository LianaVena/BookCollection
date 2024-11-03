import logging
import requests
from bs4 import BeautifulSoup

ol_url = "https://openlibrary.org/"
dot_json = ".json"

logger = logging.getLogger(__name__)

headers = {"Content-Type": "application/json"}


def get_data_openlibrary(isbn):
    url = ol_url + "isbn/" + isbn + dot_json
    response = requests.get(url, headers=headers)
    if response.status_code != 404:
        return response.json()


def get_work_url(json):
    works = _get_value(json, "works")
    if works != None:
        return ol_url + _get_value(works[0], "key") + dot_json


def get_data_openlibrary_work(work_url):
    response = requests.get(work_url, headers=headers)
    return response.json()


def get_data_blackwells(isbn):
    response = requests.get("https://blackwells.co.uk/bookshop/product/" + isbn)
    return BeautifulSoup(response.content, "html.parser")


#


def get_title(json):
    return _get_value(json, "title")


def get_subtitle(json):
    return _get_value(json, "subtitle")


def get_cover_url(json):
    cover_id = _get_value(json, "covers")
    if cover_id != None:
        if isinstance(cover_id, list):
            cover_id = cover_id[0]
        return "https://covers.openlibrary.org/b/id/" + str(cover_id) + ".jpg"
    return None


def get_authors(json, soup):
    result = set()
    authors_json = _get_value(json, "authors")
    if authors_json != None:
        for a in authors_json:
            for link in dict(a).values():
                author = _get_value(_get_author_json(link), "name")
                if author != None:
                    result.add(_replace_commas(author))
    if len(result) == 0:
        result = _get_authors_blackwells(soup)
    return list(result)


def _get_author_json(link):
    url = ol_url + link + dot_json
    return requests.get(url).json()


def _get_authors_blackwells(soup):
    result = set()
    s = soup.find("p", {"class": "product__author"})
    for i in range(1, len(s.contents), 2):
        name = _get_text_from_html(s, i)
        if len(name) == 0 or "\n" in name:
            break
        result.add(_replace_commas(name))
    return result


def get_editors(contributors):
    keys = ["Editor", "Compiler"]
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] in keys:
                result.append(key)
    return result


def get_illustrators(contributors):
    keys = ["Illustrator", "Cover Art", "Drawings"]
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] in keys:
                result.append(key)
    return result


def get_translators(contributors):
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] == "Translator":
                result.append(key)
    return result


def get_contributors(json):
    result = dict()
    cons1 = _get_value(json, "contributions")
    if cons1 != None:
        for c in cons1:
            if "(" in c:
                contributor_list = c.split("(")
                name = contributor_list[0]
                name = _replace_commas(name[:-1])
                result[name] = contributor_list[1][:-1]
    name = ""
    cons2 = _get_value(json, "contributors")
    if cons2 != None:
        for c in cons2:
            role = _get_value(c, "role")
            name = _replace_commas(_get_value(c, "name"))
            if role != None and name != None:
                result[name] = role
    return result


def get_publishers(soup):
    s = soup.find("td", itemprop="publisher")
    text = _get_text_from_html(s, 1)
    if text != None:
        return [_replace_commas(text)]


def get_imprints(soup):
    s = soup.find("td", itemprop="publisherImprint")
    text = _get_text_from_html(s, 1)
    if text != None:
        return [_replace_commas(text)]


def get_series(json):
    series = _get_value(json, "series")
    if series != None:
        return [str(series[0]).split(",")[0]]


def get_formats(json, soup):
    result = set()
    book_format = _replace_commas(_get_value(json, "physical_format"))
    book_format2 = _replace_commas(_get_value(json, "edition_name"))
    book_format3 = _replace_commas(_find_in_table(soup, "Edition:"))
    if book_format != None:
        result.add(book_format)
    if book_format2 != None:
        result.add(book_format2)
    if book_format3 != None:
        result.add(book_format3)
    return list(result)


def get_genres(work_json):
    result = []
    genres = _get_value(work_json, "subjects")
    if genres != None:
        for i in range(15):
            result.append(_replace_commas(genres[i]))
    return result


def get_first_pub_year(work_json):
    return _get_year(_get_value(work_json, "first_publish_date"))


def get_pub_year(json, soup):
    date = _get_value(json, "publish_date")
    if date is None:
        s = soup.find("td", itemprop="datePublished")
        return _get_year(_get_text_from_html(s, 1))
    return _get_year(date)


def _get_year(date):
    if date is None:
        return
    if date.isnumeric() and len(date) <= 4:
        return date
    date = date[-4:]
    while date.isdigit() == False:
        date = date[-1:]
        if len(date) == 0:
            return None
    return date


def get_setting_places(work_json):
    result = []
    places = _get_value(work_json, "subject_places")
    if places != None:
        for p in places:
            result.append(_replace_commas(p))
    return result


def get_setting_times(work_json):
    result = []
    times = _get_value(work_json, "subject_times")
    if times != None:
        for t in times:
            result.append(_replace_commas(t))
    return result


def get_languages(json):
    result = []
    lang = _get_value(json, "languages")
    if lang != None:
        for l in lang:
            url = ol_url + _get_value(l, "key") + dot_json
            response = requests.get(url)
            lang_name = _get_value(response.json(), "name")
            if lang_name != None:
                result.append(_replace_commas(lang_name))
    return result


def get_pages(json, soup):
    num = _get_value(json, "number_of_pages")
    if num == None:
        s = soup.find("td", itemprop="numberOfPages")
        return _get_text_from_html(s, 1)
    return num


def get_weight(json, soup):
    weight = _get_value(json, "weight")
    if weight == None:
        return _get_number_only(_find_in_table(soup, "Weight:"))
    return _get_number_only(weight)


def get_width(soup):
    return _get_number_only(_find_in_table(soup, "Width:"))


def get_height(soup):
    return _get_number_only(_find_in_table(soup, "Height:"))


def get_spine_width(soup):
    return _get_number_only(_find_in_table(soup, "Spine width:"))


#


def _get_value(json, key):
    if key in json:
        return json[key]
    logging.info("Key " + key + " does not exist")
    return None


def _replace_commas(text):
    if text == None:
        return text
    return text.replace(",", "")


def _find_in_table(soup, key):
    s = soup.find("table", {"class": "u-separator-right"})
    td = s.find("td", string=key)
    if td != None:
        tr = td.find_parent("tr")
        return _get_text_from_html(tr, 3)


def _get_text_from_html(source, i):
    if source != None and len(source.contents) > i:
        return source.contents[i].text


def _get_number_only(result):
    if result == None:
        return None
    return "".join(i for i in result if i.isdigit())
