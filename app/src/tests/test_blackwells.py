from unittest import TestCase

from app.src.get_data.blackwells import Blackwells


class TestBlackwells(TestCase):
    def setUp(self):
        self.bw_almanac = Blackwells("9781856754682")
        self.bw_80k_hours = Blackwells("9781399957090")

    def test_init(self):
        self.assertIsNotNone(self.bw_almanac.html)

    def test_get_title(self):
        self.assertEqual(self.bw_almanac.get_title(), "The Almanac")

    def test_get_subtitle(self):
        self.assertEqual(self.bw_almanac.get_subtitle(), "A Seasonal Guide to 2025")

    def test_get_cover_url(self):
        self.assertEqual(
            self.bw_almanac.get_cover_url(),
            "https://blackwells.co.uk/jacket/9781856754682.webp"
        )

    def test_get_authors(self):
        self.assertListEqual(self.bw_almanac.get_authors(), ["Lia Leendertz"])

    def test_get_contributors(self):
        contributors = {"Maria Gutierrez": "illustrator",
                        "Nik Mastroddi": "illustrator",
                        "Benjamin Hilton": "appendix"}
        self.assertDictEqual(self.bw_80k_hours.get_contributors(), contributors)

    def test_get_publishers(self):
        self.assertListEqual(self.bw_almanac.get_publishers(), ["Octopus"])

    def test_get_imprints(self):
        self.assertListEqual(self.bw_almanac.get_imprints(), ["Gaia"])

    def test_get_formats(self):
        self.assertListEqual(self.bw_almanac.get_formats(), ["Hardback"])

    def test_get_pub_year(self):
        self.assertEqual(self.bw_almanac.get_pub_year(), "2024")

    def test_get_languages(self):
        self.assertListEqual(self.bw_almanac.get_languages(), ["English"])

    def test_get_pages(self):
        self.assertEqual(self.bw_almanac.get_pages(), "288")

    def test_get_weight(self):
        self.assertEqual(self.bw_almanac.get_weight(), "272")

    def test_get_width(self):
        self.assertEqual(self.bw_almanac.get_width(), "114")

    def test_get_height(self):
        self.assertEqual(self.bw_almanac.get_height(), "185")

    def test_get_spine_width(self):
        self.assertEqual(self.bw_almanac.get_spine_width(), "25")
