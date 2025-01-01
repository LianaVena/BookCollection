from unittest import TestCase

from app.src.get_data.goodreads import GoodReads


class TestGoodReads(TestCase):
    def setUp(self):
        self.gr = GoodReads("9781250881205")

    def test_init(self):
        self.assertIsNotNone(self.gr.html)

    def test_get_title(self):
        self.assertEqual(self.gr.get_title(), "Somewhere Beyond the Sea")

    def test_get_series(self):
        self.assertListEqual(self.gr.get_series(), ["Cerulean Chronicles"])

    def test_get_genres(self):
        genres = ["Fantasy", "Fiction", "LGBT", "Audiobook", "Romance", "Queer", "Adult"]
        self.assertListEqual(self.gr.get_genres(), genres)

    def test_get_first_pub_year(self):
        self.assertEqual(self.gr.get_first_pub_year(), "2024")
