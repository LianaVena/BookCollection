from unittest import TestCase

from app.src import STRINGS, update_books


class TestOpenLibrary(TestCase):
    def setUp(self):
        self.min_data = update_books.get_minimal_data("9781529381009")
        self.full_data = update_books.get_update_page_data_dict("9781529381009")

    def test_get_minimal_data(self):
        self.assertEqual(update_books._get_isbn_value(self.min_data[STRINGS["isbn"]]), "9781529381009")
        self.assertEqual(update_books._get_rich_text_value(self.min_data[STRINGS["title"]]), "Ballad of Never After")
        self.assertEqual(update_books._get_multi_select_value(self.min_data[STRINGS["author"]]), ["Stephanie Garber"])
        self.assertEqual(self.min_data["cover"],
                         {"type": "external", "external": {"url": "https://covers.openlibrary.org/b/id/14804920.jpg"}})
        self.assertEqual(self.min_data["icon"],
                         {"type": "external", "external": {"url": "https://covers.openlibrary.org/b/id/14804920.jpg"}})
        self.assertEqual(self.min_data[STRINGS["data_status"]], {"select": {"name": "To be retrieved"}})

    def test_get_update_page_data_dict(self):
        self.assertEqual(update_books._get_isbn_value(self.full_data[STRINGS["isbn"]]), "9781529381009")
        self.assertEqual(self.full_data["cover"],
                         {"type": "external", "external": {"url": "https://covers.openlibrary.org/b/id/14804920.jpg"}})
        self.assertEqual(self.full_data["icon"],
                         {"type": "external", "external": {"url": "https://covers.openlibrary.org/b/id/14804920.jpg"}})

        self.assertEqual(update_books._get_rich_text_value(self.full_data[STRINGS["title"]]), "Ballad of Never After")
        self.assertEqual(update_books._get_rich_text_value(self.full_data[STRINGS["subtitle"]]),
                         "The Stunning Sequel to the Sunday Times Bestseller Once upon a Broken Heart")
        self.assertEqual(update_books._get_multi_select_value(self.full_data[STRINGS["author"]]), ["Stephanie Garber"])
        self.assertEqual(update_books._get_multi_select_value(self.full_data[STRINGS["publisher"]]),
                         ["Hodder & Stoughton"])
        self.assertEqual(update_books._get_multi_select_value(self.full_data[STRINGS["imprint"]]), ["Hodderscape"])
        self.assertEqual(update_books._get_multi_select_value(self.full_data[STRINGS["series"]]),
                         ["Once Upon a Broken Heart"])
        self.assertEqual(update_books._get_multi_select_value(self.full_data[STRINGS["format"]]), ["Paperback"])
        self.assertEqual(update_books._get_multi_select_value(self.full_data[STRINGS["genres"]]),
                         ["Fantasy", "Young Adult", "Romantasy", "Fantasy Romance", "Fiction", "Magic",
                          "Young Adult Fantasy"])
        self.assertEqual(update_books._get_number_value(self.full_data[STRINGS["first_pub_year"]]), 2022)
        self.assertEqual(update_books._get_number_value(self.full_data[STRINGS["pub_year"]]), 2023)
        self.assertEqual(update_books._get_multi_select_value(self.full_data[STRINGS["language"]]), ["English"])
        self.assertEqual(update_books._get_number_value(self.full_data[STRINGS["pages"]]), 403)
        self.assertEqual(update_books._get_number_value(self.full_data[STRINGS["weight"]]), 310)
        self.assertEqual(update_books._get_number_value(self.full_data[STRINGS["width"]]), 197)
        self.assertEqual(update_books._get_number_value(self.full_data[STRINGS["height"]]), 130)
        self.assertEqual(update_books._get_number_value(self.full_data[STRINGS["spine_width"]]), 31)
        self.assertEqual(self.full_data[STRINGS["data_status"]], {"select": {"name": "To be edited"}})
