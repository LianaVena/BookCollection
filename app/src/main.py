from ..tests.print_get_json import print_notion_book as get_json
from ..tests.test_update import update_title
from ..tests.print_get_data import print_book_data as get_data


def run():
    while True:
        print()
        print("1. Test get book json")
        print("2. Test update book title")
        print("3. Test get book data")
        print("4. Exit")
        menu = input()
        match menu:
            case "1":
                get_json()
            case "2":
                print("Input new Title:")
                update_title(input())
            case "3":
                print("Input ISBN:")
                get_data(input())
            case "4":
                exit()


run()
