from ..tests.print_get_json import print_notion_book as get_json
from ..tests.test_update import update_title
from ..tests.print_get_data import print_book_data as get_data
from ..src.create_book import create_page
from ..src.update_books import get_update_page_data_dict as get_data_dict


def run():
    while True:
        print("\n1. Test get book json")
        print("2. Test update book title")
        print("3. Test get book data")
        print("4. Create database entry")
        print("5. Add Books to Database by ISBN")
        print("c. Exit")
        menu = input()
        match menu:
            case "1":
                get_json()
            case "2":
                print("Input new Title:")
                update_title(input())
            case "3":
                print("Input ISBN:")
                get_data(int(input()))
            case "4":
                create_page(get_data_dict(97800))
            case "5":
                print("Input ISBN:")
                isbn = input()
                while isbn.isdigit() and len(isbn) == 13:
                    data = get_data_dict(int(isbn))
                    if data != None:
                        create_page(data)
                    isbn = input()
                print("Not a valid ISBN")
            case "c":
                exit()


run()
