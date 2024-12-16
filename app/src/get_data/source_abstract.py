from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def get_title(self):
        ...

    @abstractmethod
    def get_subtitle(self):
        ...

    @abstractmethod
    def get_cover_url(self):
        ...

    @abstractmethod
    def get_authors(self):
        ...

    @abstractmethod
    def get_contributors(self):
        ...

    @abstractmethod
    def get_publishers(self):
        ...

    @abstractmethod
    def get_imprints(self):
        ...

    @abstractmethod
    def get_series(self):
        ...

    @abstractmethod
    def get_formats(self):
        ...

    @abstractmethod
    def get_genres(self):
        ...

    @abstractmethod
    def get_first_pub_year(self):
        ...

    @abstractmethod
    def get_pub_year(self):
        ...

    @abstractmethod
    def get_setting_places(self):
        ...

    @abstractmethod
    def get_setting_times(self):
        ...

    @abstractmethod
    def get_languages(self):
        ...

    @abstractmethod
    def get_pages(self):
        ...

    @abstractmethod
    def get_weight(self):
        ...

    @abstractmethod
    def get_width(self):
        ...

    @abstractmethod
    def get_height(self):
        ...

    @abstractmethod
    def get_spine_width(self):
        ...
