from ..src.get_books import get_all_pages
from ..tests.test_update import update_title
from ..src.create_book import create_page
from ..src.update_books import get_update_page_data_dict as get_data_dict


def run():
    while True:
        print("\n1. Get json from Notion books DB")
        print("2. Test update book title")
        print("3. Add Books to Database by ISBN")
        print("c. Exit")
        menu = input()
        match menu:
            case "1":
                get_all_pages()
            case "2":
                print("Input new Title:")
                update_title(input())
            case "3":
                print("Input ISBN:")
                isbn = input()
                while isbn.isdigit() and len(isbn) == 13:
                    data = get_data_dict(isbn)
                    if data != None:
                        create_page(data)
                    isbn = input()
                print("Not a valid ISBN")
            case "c":
                exit()


run()
