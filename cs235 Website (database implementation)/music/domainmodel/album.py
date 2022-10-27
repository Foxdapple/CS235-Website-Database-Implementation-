class Album:

    def __init__(self, album_id: int, title: str):
        if type(album_id) is not int or album_id < 0:
            raise ValueError("Album ID should be a non negative integer!")
        self.__album_id: int = album_id

        if type(title) is str and title.strip() != '':
            self.__title: str = title.strip()
        else:
            self.__title = None

        self.__album_url: str | None = None
        self.__album_type: str | None = None
        self.__release_year: int | None = None

    @property
    def album_id(self) -> int:
        return self.__album_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title):
        if type(new_title) is str and new_title.strip() != '':
            self.__title = new_title.strip()
        else:
            self.__title = None

    @property
    def album_url(self) -> str:
        return self.__album_url

    @album_url.setter
    def album_url(self, new_album_url: str):
        if type(new_album_url) is str:
            self.__album_url = new_album_url.strip()
        else:
            self.__album_url = None

    @property
    def album_type(self) -> str:
        return self.__album_type

    @album_type.setter
    def album_type(self, new_album_type: str):
        if type(new_album_type) is str:
            self.__album_type = new_album_type.strip()
        else:
            self.__album_type = None

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, new_release_year: int):
        if type(new_release_year) is int and new_release_year >= 0:
            self.__release_year = new_release_year
        else:
            self.__release_year = None

    def __repr__(self) -> str:
        return f"<Album {self.title}, album id = {self.album_id}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.album_id == other.album_id

    def __lt__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return True
        return self.album_id < other.album_id

    def __hash__(self):
        return hash(self.album_id)
