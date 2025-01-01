from unittest import TestCase

from app.src.get_data.open_library import OpenLibrary


class TestOpenLibrary(TestCase):
    def setUp(self):
        self.ol = OpenLibrary("9780553381689")
        self.ol2 = OpenLibrary("9780007448036")
        self.ol3 = OpenLibrary("9781612680019")
        self.ol4 = OpenLibrary("9780590353427")

    def test_init(self):
        self.assertIsNotNone(self.ol.json)

    def test_get_title(self):
        self.assertEqual(self.ol.get_title(), "A Game of Thrones")

    def test_get_subtitle(self):
        self.assertEqual(self.ol2.get_subtitle(), "Book One of A Song of Ice and Fire")

    def test_get_cover_url(self):
        self.assertEqual(self.ol.get_cover_url(), "https://covers.openlibrary.org/b/id/14830435.jpg")

    def test_get_authors(self):
        self.assertListEqual(self.ol.get_authors(), ["George R. R. Martin"])

    def test_get_contributors(self):
        contributors = {"Jaime S. Warren Youll": "Cover Design",
                        "James Sinclair": "Book Designer",
                        "Stephen Youll": "Cover Art",
                        "Virginia Norey": "Drawings"}
        self.assertDictEqual(self.ol.get_contributors(), contributors)

    def test_get_publishers(self):
        self.assertListEqual(self.ol.get_publishers(), ["Bantam Books"])

    def test_get_imprints(self):
        self.assertListEqual(self.ol3.get_imprints(), ["Plata Publishing"])

    def test_get_series(self):
        self.assertListEqual(self.ol.get_series(), ["A Song of Ice and Fire"])

    def test_get_formats(self):
        self.assertListEqual(self.ol.get_formats(), [
            "Paperback",
            "Bantam Spectra Trade Paperback Reissue Edition (12); Media tie-in"
        ])

    def test_get_genres(self):
        genres = ["Fantasy fiction", "Fiction", "Fiction - Fantasy", "Fantasy",
                  "Fantasy - Epic", "Fantasy - Series", "Fiction / Fantasy / Epic"]
        self.assertListEqual(self.ol.get_genres(), genres)

    def test_get_first_pub_year(self):
        self.assertEqual(self.ol.get_first_pub_year(), "1998")

    def test_get_pub_year(self):
        self.assertEqual(self.ol.get_pub_year(), "2002")

    def test_get_setting_places(self):
        places = ["Winterfell", "King's Landing", "Seven Kingdoms", "Westeros", "Sunset Lands"]
        self.assertListEqual(self.ol.get_setting_places(), places)

    def test_get_setting_times(self):
        self.assertListEqual(self.ol4.get_setting_times(), ["late 1990s", "Witches"])

    def test_get_languages(self):
        self.assertListEqual(self.ol.get_languages(), ["English"])

    def test_get_pages(self):
        self.assertEqual(self.ol.get_pages(), "704")

    def test_get_weight(self):
        self.assertEqual(self.ol.get_weight(), "658")

    def test_get_width(self):
        self.assertEqual(self.ol.get_width(), "154")

    def test_get_height(self):
        self.assertEqual(self.ol.get_height(), "231")

    def test_get_spine_width(self):
        self.assertEqual(self.ol.get_spine_width(), "33")
