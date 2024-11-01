import requests
from ..src import utils
from app import headers

ol_url = "https://openlibrary.org/"
dot_json = ".json"


def get_data_openlibrary(isbn):
    url = ol_url + "isbn/" + str(isbn) + dot_json
    response = requests.get(url, headers=headers)
    if response.status_code != 404:
        return response.json()


def get_work_url(json):
    works = utils.get_value(json, "works")
    if works != None:
        return ol_url + utils.get_value(works[0], "key") + dot_json


def get_data_openlibrary_work(work_url):
    response = requests.get(work_url, headers=headers)
    return response.json()


def get_title(json: str):
    return utils.get_value(json, "title")


def get_cover_url(json: str):
    cover_id = utils.get_value(json, "covers")
    if cover_id != None:
        if isinstance(cover_id, list):
            cover_id = cover_id[0]
        return "https://covers.openlibrary.org/b/id/" + str(cover_id) + ".jpg"
    return None


def get_authors(json: str):
    result = []
    authors_json = utils.get_value(json, "authors")
    if authors_json != None:
        for a in authors_json:
            for link in dict(a).values():
                url = ol_url + link + dot_json
                response = requests.get(url, headers=headers)
                author = utils.get_value(response.json(), "name")
                if author != None:
                    result.append(utils.replace_commas(author))
    return result


def get_contributors(json: str):
    result = dict()
    cons1 = utils.get_value(json, "contributions")
    if cons1 != None:
        for c in cons1:
            if "(" in c:
                contributor_list = c.split("(")
                name = contributor_list[0]
                name = utils.replace_commas(name[:-1])
                result[name] = contributor_list[1][:-1]
    name = ""
    cons2 = utils.get_value(json, "contributors")
    if cons2 != None:
        for c in cons2:
            role = utils.get_value(c, "role")
            name = utils.replace_commas(utils.get_value(c, "name"))
            if role != None and name != None:
                result[name] = role
    return result


def get_editors(contributors: dict):
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] == "Editor":
                result.append(key)
    return result


def get_illustrators(contributors: dict):
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] == "Illustrator":
                result.append(key)
    return result


def get_translators(contributors: dict):
    result = []
    if contributors != None:
        for key in contributors.keys():
            if contributors[key] == "Translator":
                result.append(key)
    return result


def get_publishers(json: str):
    result = []
    pubs = utils.get_value(json, "publishers")
    if pubs != None:
        for p in pubs:
            result.append(utils.replace_commas(p))
    return result


# TODO imprint


# TODO series


def get_format(json: str):
    result = []
    book_format = utils.replace_commas(utils.get_value(json, "physical_format"))
    if book_format != None:
        result.append(book_format)
    book_format2 = utils.replace_commas(utils.get_value(json, "edition_name"))
    if book_format2 != None and book_format != book_format2:
        result.append(book_format2)
    return result


# TODO genres


# TODO First Pub. Year


def get_pub_year(json: str):
    date = utils.get_value(json, "publish_date")
    if date is None:
        return None
    if date.isnumeric() and len(date) <= 4:
        return date
    date = date[-4:]
    while date.isdigit() == False:
        date = date[-1:]
        if len(date) == 0:
            return None
    return date


# TODO pub country "publish_places"


def get_setting_places(work_json: str):
    result = []
    places = utils.get_value(work_json, "subject_places")
    if places != None:
        for p in places:
            result.append(utils.replace_commas(p))
    return result


def get_setting_times(work_json: str):
    result = []
    times = utils.get_value(work_json, "subject_times")
    if times != None:
        for t in times:
            result.append(utils.replace_commas(t))
    return result


def get_languages(json: str):
    result = []
    lang = utils.get_value(json, "languages")
    if lang != None:
        for l in lang:
            url = ol_url + utils.get_value(l, "key") + dot_json
            response = requests.get(url, headers=headers)
            lang_name = utils.get_value(response.json(), "name")
            if lang_name != None:
                result.append(utils.replace_commas(lang_name))
    return result


def get_pages(json: str):
    return str(utils.get_value(json, "number_of_pages"))


def get_weight(json: str):
    weight = utils.get_value(json, "weight")
    if weight == None:
        return None
    weight = weight.split(" ")[0]
    return utils.fix_result_empty(weight)


# TODO width
# TODO height
# TODO spine width
