import logging

from app.src import STRINGS
from app.src.get_data.blackwells import BlackWells
from app.src.get_data.goodreads import GoodReads
from app.src.get_data.google_books import GoogleBooks
from app.src.get_data.open_library import OpenLibrary
from app.src.get_data.sources import Sources


class GetData:
    sources = None
    blackwells = None
    goodreads = None
    google_books = None
    open_library = None

    ol_url = "https://openlibrary.org/"
    dot_json = ".json"

    logger = logging.getLogger(__name__)

    def __init__(self, isbn_input, sources: Sources = Sources()):
        self.sources = sources
        if sources.blackwells:
            self.blackwells = BlackWells(isbn_input)
            if not self.blackwells.html:
                self.sources.blackwells = False
        if sources.goodreads:
            self.goodreads = GoodReads(isbn_input)
            if not self.goodreads.html:
                self.sources.goodreads = False
        if sources.google_books:
            self.google_books = GoogleBooks(isbn_input)
            if not self.google_books.json:
                self.sources.google_books = False
        if sources.open_library:
            self.open_library = OpenLibrary(isbn_input)
            if not self.open_library.json:
                self.logger.info(STRINGS["warning_not_on_open_library"])
                self.sources.open_library = False

    def get_title(self):
        title = None
        if self.sources.google_books:
            title = self.google_books.get_title()
        if not title and self.sources.open_library:
            title = self.open_library.get_title()
        if not title and self.sources.blackwells:
            title = self.blackwells.get_title()
        if not title and self.sources.goodreads:
            title = self.goodreads.get_title()
        return title

    def get_subtitle(self):
        subtitle = None
        if self.sources.google_books:
            subtitle = self.google_books.get_subtitle()
        if not subtitle and self.sources.open_library:
            subtitle = self.open_library.get_subtitle()
        if not subtitle and self.sources.blackwells:
            subtitle = self.blackwells.get_subtitle()
        return subtitle

    def get_cover_url(self):
        cover = None
        if self.sources.google_books:
            cover = self.google_books.get_cover_url()
        if not cover and self.sources.open_library:
            cover = self.open_library.get_cover_url()
        if not cover and self.sources.blackwells:
            cover = self.blackwells.get_cover_url()
        return cover

    def get_authors(self):
        authors = None
        if self.sources.open_library:
            authors = self.open_library.get_authors()
        if not authors and self.sources.blackwells:
            authors = self.blackwells.get_authors()
        if not authors and self.sources.google_books:
            authors = self.google_books.get_authors()
        return authors

    def get_editors(self, contributors):
        keys = ["Editor", "Compiler", "editor"]
        return self._get_specific_contributors(contributors, keys)

    def get_illustrators(self, contributors):
        keys = [
            "Illustrator",
            "Cover Art",
            "Drawings",
            "artist",
            "illustrator",
            "colourist",
        ]
        return self._get_specific_contributors(contributors, keys)

    def get_translators(self, contributors):
        keys = ["Translator", "translator"]
        return self._get_specific_contributors(contributors, keys)

    @staticmethod
    def _get_specific_contributors(contributors, keys):
        result = []
        if contributors:
            for key in contributors.keys():
                if contributors[key] in keys:
                    result.append(key)
        return result

    def get_contributors(self):
        result = None
        if self.sources.open_library:
            result = self.open_library.get_contributors()
        if not result and self.sources.blackwells:
            result = self.blackwells.get_contributors()
        return result

    def get_publishers(self):
        publishers = None
        if self.sources.blackwells:
            publishers = self.blackwells.get_publishers()
        if not publishers and self.sources.open_library:
            publishers = self.open_library.get_publishers()
        if not publishers and self.sources.google_books:
            publishers = self.google_books.get_publishers()
        return publishers

    def get_imprints(self):
        imprints = None
        if self.sources.blackwells:
            imprints = self.blackwells.get_imprints()
        if not imprints and self.sources.open_library:
            imprints = self.open_library.get_imprints()
        return imprints

    def get_series(self):
        series = None
        if self.sources.open_library:
            series = self.open_library.get_series()
        if not series and self.sources.goodreads:
            series = self.goodreads.get_series()
        return series

    def get_formats(self):
        result = set()
        if self.sources.open_library:
            result.update(self.open_library.get_formats())
        if self.sources.blackwells:
            book_format = self.blackwells.get_formats()
            if book_format:
                result.add(book_format)
        if result:
            return list(result)

    def get_genres(self):
        genres = None
        if self.sources.goodreads:
            genres = self.goodreads.get_genres()
        if not genres and self.sources.google_books:
            genres = self.google_books.get_genres()
        if not genres and self.sources.open_library:
            genres = self.open_library.get_genres()
        return genres

    def get_first_pub_year(self):
        year = None
        if self.sources.goodreads:
            year = self.goodreads.get_first_pub_year()
        if not year and self.sources.open_library:
            year = self.open_library.get_first_pub_year()
        return year

    def get_pub_year(self):
        year = None
        if self.sources.google_books:
            year = self.google_books.get_pub_year()
        if not year and self.sources.open_library:
            year = self.open_library.get_pub_year()
        if not year and self.sources.blackwells:
            year = self.blackwells.get_pub_year()
        return year

    def get_setting_places(self):
        if self.sources.open_library:
            return self.open_library.get_setting_places()

    def get_setting_times(self):
        if self.sources.open_library:
            return self.open_library.get_setting_times()

    def get_languages(self):
        languages = None
        if self.sources.open_library:
            languages = self.open_library.get_languages()
        if not languages and self.sources.blackwells:
            languages = self.blackwells.get_languages()
        if not languages and self.sources.google_books:
            languages = self.google_books.get_languages()
        return languages

    def get_pages(self):
        pages = None
        if self.sources.google_books:
            pages = self.google_books.get_pages()
        if not pages and self.sources.open_library:
            pages = self.open_library.get_pages()
        if not pages and self.sources.blackwells:
            pages = self.blackwells.get_pages()
        return pages

    def get_weight(self):
        weight = None
        if self.sources.open_library:
            weight = self.open_library.get_weight()
        if not weight and self.sources.blackwells:
            weight = self.blackwells.get_weight()
        return weight

    def get_width(self):
        width = None
        if self.sources.blackwells:
            width = self.blackwells.get_width()
        if not width and self.sources.open_library:
            width = self.open_library.get_width()
        return width

    def get_height(self):
        height = None
        if self.sources.blackwells:
            height = self.blackwells.get_height()
        if not height and self.sources.open_library:
            height = self.open_library.get_height()
        return height

    def get_spine_width(self):
        s_width = None
        if self.sources.blackwells:
            s_width = self.blackwells.get_spine_width()
        if not s_width and self.sources.open_library:
            s_width = self.open_library.get_spine_width()
        return s_width
