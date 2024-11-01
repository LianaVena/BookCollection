from ..src import get_data


def print_list(text: str, l: list):
    if l != None and len(l) > 0:
        print(text)
        for x in l:
            print("\t" + x)


def print_book_data(isbn):
    json = get_data.get_data_openlibrary(isbn)
    print("Title: " + get_data.get_title(json))
    print("Cover URL: " + get_data.get_cover_url(json))
    print_list("Authors:", get_data.get_authors(json))
    contributors = get_data.get_contributors(json)
    print_list("Editors:", get_data.get_editors(contributors))
    print_list("Illustrators:", get_data.get_illustrators(contributors))
    print_list("Translators:", get_data.get_translators(contributors))
    print_list("Publishers:", get_data.get_publishers(json))
    print("Format:" + get_data.get_format(json))
    print("Publication year: " + get_data.get_pub_year(json))
    work = get_data.get_data_openlibrary_work(get_data.get_work_url(json))
    print_list("Setting places:", get_data.get_setting_places(work))
    print_list("Setting times:", get_data.get_setting_times(work))
    print_list("Languages:", get_data.get_languages(json))
    print("Pages: " + get_data.get_pages(json))
    print("Weight: " + get_data.get_weight(json))
