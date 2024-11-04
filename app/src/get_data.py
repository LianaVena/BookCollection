import logging
import requests
from bs4 import BeautifulSoup
from app import GOOGLE_API_KEY

isbn = None
g_json = None  # JSON from Google Books API call
ol_json = None  # JSON from OpenLibrary API call
ol_work_json = None  # JSON from OpenLibrary API call for work instead of edition
bw_html = None  # HTML from BlackWells


def init(isbn_input):
    global isbn
    global g_json
    global ol_json
    global ol_work_json
    global bw_html
    isbn = isbn_input
    g_json = get_data_google(isbn)
    ol_json = get_data_openlibrary(isbn)
    if ol_json == None:
        logger.info("This book is not on OpenLibrary. Consider adding it.")
    if ol_json != None:
        ol_work_json = get_data_openlibrary_work(get_work_url(ol_json))
    bw_html = get_data_blackwells(isbn)


ol_url = "https://openlibrary.org/"
dot_json = ".json"

logger = logging.getLogger(__name__)


def get_data_openlibrary(isbn):
    url = ol_url + "isbn/" + isbn + dot_json
    response = requests.get(url)
    if response.ok == True:
        return response.json()


def get_work_url(json):
    works = _get_value(json, "works")
    if works != None:
        return ol_url + _get_value(works[0], "key") + dot_json


def get_data_openlibrary_work(work_url):
    response = requests.get(work_url)
    if response.ok == True:
        return response.json()


def get_data_blackwells(isbn):
    response = requests.get("https://blackwells.co.uk/bookshop/product/" + isbn)
    return BeautifulSoup(response.content, "html.parser")


def get_data_google(isbn):
    url = (
        "https://www.googleapis.com/books/v1/volumes?q="
        + "isbn:"
        + isbn
        + "&key="
        + GOOGLE_API_KEY
    )
    response = requests.get(url)
    if response.ok == True:
        data = response.json()
        if data["totalItems"] > 0:
            return data["items"][0]["volumeInfo"]


#


def get_title():
    title = _get_value_from_json(g_json, "title")
    if title != None:
        return title

    title = _get_value_from_json(ol_json, "title")
    if title != None:
        return title

    if bw_html != None:
        title = bw_html.find("h1", {"class": "product__name"})
        if title != None:
            if len(title.contents) > 1:
                title = title.contents[0]
                return title.strip()
            return title.text.strip()


def get_subtitle():
    subtitle = _get_value_from_json(g_json, "subtitle")
    if subtitle != None:
        return subtitle

    subtitle = _get_value_from_json(ol_json, "subtitle")
    if subtitle != None:
        return subtitle

    if bw_html != None:
        titles = bw_html.find("h1", {"class": "product__name"})
        if titles != None:
            subtitle = titles.find("small")
            if subtitle != None:
                return subtitle.text.strip()


def get_cover_url():
    covers = _get_value_from_json(g_json, "imageLinks")
    if covers != None:
        cover = _get_value(covers, "thumbnail")
        if cover != None:
            return cover

    cover_id = _get_value_from_json(ol_json, "covers")
    if cover_id != None:
        if isinstance(cover_id, list):
            cover_id = cover_id[0]
        return "https://covers.openlibrary.org/b/id/" + str(cover_id) + ".jpg"

    return "https://blackwells.co.uk/jacket/" + isbn + ".webp"


def get_authors():
    authors = set()
    ol_authors = _get_authors_from_ol_json()
    if ol_authors != None:
        authors.update(ol_authors)
        return list(authors)

    authors.update(_get_authors_blackwells())
    if len(authors) != 0:
        return list(authors)

    authors.update(_get_value_from_json(g_json, "authors"))
    if len(authors) != 0:
        authors = [_replace_commas(a) for a in authors]
        return authors


def _get_authors_from_ol_json():
    if ol_json != None:
        result = set()
        authors_json = _get_value(ol_json, "authors")
        if authors_json != None:
            for a in authors_json:
                for link in dict(a).values():
                    author = _get_value(_get_author_json(link), "name")
                    if author != None:
                        result.add(_replace_commas(author))
        return result


def _get_author_json(link):
    url = ol_url + link + dot_json
    result = requests.get(url).json()
    if result != None:
        return result


def _get_authors_blackwells():
    result = set()
    s = bw_html.find("p", {"class": "product__author"})
    for i in range(1, len(s.contents), 2):
        name = _get_text_from_html(s, i)
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
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] in keys:
                result.append(key)
    return result


def get_illustrators(contributors):
    keys = [
        "Illustrator",
        "Cover Art",
        "Drawings",
        "artist",
        "illustrator",
        "colourist",
    ]
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] in keys:
                result.append(key)
    return result


def get_translators(contributors):
    keys = ["Translator", "translator"]
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] in keys:
                result.append(key)
    return result


def get_contributors():
    result = dict()
    cons1 = _get_value_from_json(ol_json, "contributions")
    if cons1 != None:
        for c in cons1:
            if "(" in c:
                contributor_list = c.split("(")
                name = contributor_list[0]
                name = _replace_commas(name[:-1])
                result[name] = contributor_list[1][:-1]
    name = ""
    cons2 = _get_value_from_json(ol_json, "contributors")
    if cons2 != None:
        for c in cons2:
            role = _get_value(c, "role")
            name = _replace_commas(_get_value(c, "name"))
            if role != None and name != None:
                result[name] = role
    if len(result) > 0:
        return result

    return _get_contributors_blackwells()


def _get_contributors_blackwells():
    result = dict()
    s = bw_html.find("p", {"class": "product__author"})
    for i in range(1, len(s.contents), 2):
        name = _get_text_from_html(s, i)
        if len(name) == 0 or "\n" in name:
            break
        if "(" in name and "author" not in name:
            name = str(name).split(" (")
            if name[1][-1] != ")":
                name[1] = name[1][:-1]
            result[_replace_commas(name[0])] = _replace_commas(name[1][:-1])
    return result


def get_publishers():
    s = bw_html.find("td", itemprop="publisher")
    text = _get_text_from_html(s, 1)
    if text != None:
        return [_replace_commas(text)]

    publishers = _get_value_from_json(ol_json, "publishers")
    if publishers != None and len(publishers) > 0:
        return [_replace_commas(publishers[0])]

    publisher = _get_value_from_json(g_json, "publisher")
    if publisher != None:
        return [_replace_commas(publisher)]


def get_imprints():
    s = bw_html.find("td", itemprop="publisherImprint")
    text = _get_text_from_html(s, 1)
    if text != None:
        return [_replace_commas(text)]

    imprints = _get_value_from_json(ol_json, "publishers")
    if imprints != None and len(imprints) > 1:
        imprints = imprints[1:]
        return [_replace_commas(i) for i in imprints]


def get_series():
    series = _get_value_from_json(ol_json, "series")
    if series != None:
        return [str(series[0]).split(",")[0]]


def get_formats():
    result = set()
    if ol_json != None:
        book_format = _replace_commas(_get_value(ol_json, "physical_format"))
        book_format2 = _replace_commas(_get_value(ol_json, "edition_name"))
        if book_format != None:
            result.add(book_format)
        if book_format2 != None:
            result.add(book_format2)
    book_format3 = _replace_commas(_find_in_table(bw_html, "Edition:"))
    if book_format3 != None:
        result.add(book_format3)
    return list(result)


def get_genres():
    genres = _get_value_from_json(g_json, "categories")
    if genres == None:
        genres = _get_value_from_json(ol_json, "subjects")
        if genres == None:
            genres = _get_value_from_json(ol_work_json, "subjects")
    if genres != None:
        result = []
        for i in range(min(len(genres), 15)):
            result.append(_replace_commas(genres[i]))
        return result


def get_first_pub_year():
    return _get_year(_get_value_from_json(ol_work_json, "first_publish_date"))


def get_pub_year():
    date = _get_value_from_json(g_json, "publishedDate")
    if date != None:
        return date.split("-")[0]

    date = _get_value_from_json(ol_json, "publish_date")
    if date != None:
        return _get_year(date)

    date = bw_html.find("td", itemprop="datePublished")
    if date != None:
        return _get_year(_get_text_from_html(date, 0))


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


def get_setting_places():
    result = []
    places = _get_value_from_json(ol_work_json, "subject_places")
    if places != None:
        for p in places:
            result.append(_replace_commas(p))
    return result


def get_setting_times():
    result = []
    times = _get_value_from_json(ol_work_json, "subject_times")
    if times != None:
        for t in times:
            result.append(_replace_commas(t))
    return result


def get_languages():
    result = get_language_from_ol()
    if result != None and len(result) > 0:
        return result

    result = bw_html.find("td", itemprop="inLanguage")
    if result != None:
        return [result.text]

    result = _get_value_from_json(g_json, "language")
    if result != None:
        return [result]
    return []


def get_language_from_ol():
    result = []
    lang = _get_value_from_json(ol_json, "languages")
    if lang != None:
        for l in lang:
            url = ol_url + _get_value(l, "key") + dot_json
            response = requests.get(url)
            lang_name = _get_value(response.json(), "name")
            if lang_name != None:
                result.append(_replace_commas(lang_name))
        return result


def get_pages():
    pages = _get_value_from_json(g_json, "pageCount")
    if pages != None and str(pages).isdigit() and int(pages) > 0:
        return pages

    pages = _get_value_from_json(ol_json, "number_of_pages")
    if pages != None and str(pages).isdigit() and int(pages) > 0:
        return pages

    pages = bw_html.find("td", itemprop="numberOfPages")
    return _get_text_from_html(pages, 0)


def get_weight():
    weight = _get_value_from_json(ol_json, "weight")
    if weight == None:
        return _get_number_only(_find_in_table(bw_html, "Weight:"))
    return _get_number_only(weight)


def get_width():
    width = _get_number_only(_find_in_table(bw_html, "Width:"))
    if width != None:
        return width
    dims = get_dimensions_from_ol()
    if dims != None:
        return dims[1]


def get_height():
    height = _get_number_only(_find_in_table(bw_html, "Height:"))
    if height != None:
        return height
    dims = get_dimensions_from_ol()
    if dims != None:
        return dims[0]


def get_spine_width():
    s_width = _get_number_only(_find_in_table(bw_html, "Spine width:"))
    if s_width != None:
        return s_width
    dims = get_dimensions_from_ol()
    if dims != None:
        return dims[2]


def get_dimensions_from_ol():
    dims = _get_value_from_json(ol_json, "physical_dimensions")
    if dims != None:
        dims = dims.split(" x ")
        dims[2] = str(dims[2]).removesuffix(" inches")
        return [str(int(float(d) * 25.4)) for d in dims]


#


def _get_value(json, key):
    if key in json:
        return json[key]
    # logging.info("Key " + key + " does not exist")
    return None


def _get_value_from_json(json, label):
    if json != None:
        result = _get_value(json, label)
        return result


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
