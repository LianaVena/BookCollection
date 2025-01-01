from unittest import TestCase

from app.src.get_data.google_books import GoogleBooks


class TestGoogleBooks(TestCase):
    def setUp(self):
        self.gb_1984 = GoogleBooks("9781595404329")
        self.gb_marxism = GoogleBooks("9780422778107")

    def test_init(self):
        self.assertIsNotNone(self.gb_1984.json)

    def test_get_title(self):
        self.assertEqual(self.gb_1984.get_title(), "Nineteen Eighty-Four")

    def test_get_subtitle(self):
        self.assertEqual(self.gb_marxism.get_subtitle(), "A Bourgeois Critique")

    def test_get_cover_url(self):
        self.assertEqual(
            self.gb_1984.get_cover_url(),
            "http://books.google.com/books/content?id=w-rb62wiFAwC&printsec=frontcover&img=1&zoom=1&source=gbs_api"
        )

    def test_get_authors(self):
        self.assertListEqual(self.gb_1984.get_authors(), ["George Orwell"])

    def test_get_publishers(self):
        self.assertListEqual(self.gb_1984.get_publishers(), ["1st World Library"])

    def test_get_genres(self):
        self.assertListEqual(self.gb_1984.get_genres(), ["Fiction"])

    def test_get_pub_year(self):
        self.assertEqual(self.gb_1984.get_pub_year(), "2004")

    def test_get_languages(self):
        self.assertListEqual(self.gb_1984.get_languages(), ["en"])

    def test_get_pages(self):
        self.assertEqual(self.gb_1984.get_pages(), "388")
