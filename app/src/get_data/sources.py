class Sources:
    blackwells: bool
    goodreads: bool
    google_books: bool
    open_library: bool

    def __init__(self, blackwells=True, goodreads=True, google_books=True, open_library=True):
        self.blackwells = blackwells
        self.goodreads = goodreads
        self.google_books = google_books
        self.open_library = open_library
