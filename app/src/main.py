import logging
from ..src import notion_requests, STRINGS
from ..src.update_books import get_minimal_data
from ..src.update_books import get_update_page_data_dict as get_data_dict

logger = logging.getLogger(__name__)

def run():
    while True:
        print("\n1. Add Books to Database by ISBN (minimal data)")
        print("2. Update books in Notion")
        print("3. Get json from Notion books DB")
        print("4. Add Books to Database by ISBN (all data)")
        print("c. Exit")
        menu = input()
        match menu:
            case "1":
                add_by_isbn(False)
            case "2":
                notion_requests.update_pages(notion_requests.get_pages_to_be_edited())
            case "3":
                notion_requests.get_pages()
            case "4":
                add_by_isbn(True)
            case "c":
                exit()


def add_by_isbn(all):
    isbn = input(STRINGS["input_isbn"]).strip()
    while isbn.isdigit() and len(isbn) == 13:
        if notion_requests.check_duplicate(isbn):
            logger.info(STRINGS["warning_isbn_exists"])
        else:
            data_amount(all, isbn)
        isbn = input(STRINGS["input_isbn"]).strip()
    logger.warning(STRINGS["warning_isbn_invalid"])

def data_amount(all, isbn):
    if all == True:
        data = get_data_dict(isbn)
        if data != None:
            notion_requests.create_page(data)
    else:
        notion_requests.create_page(get_minimal_data(isbn))


run()
