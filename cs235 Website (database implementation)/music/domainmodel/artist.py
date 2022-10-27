class Artist:

    def __init__(self, artist_id: int, full_name: str):
        if type(artist_id) is not int or artist_id < 0:
            raise ValueError("Arist ID should be a non negative integer!")
        self.__artist_id: int = artist_id

        if type(full_name) is str:
            self.__full_name: str = full_name.strip()
        else:
            self.__full_name = None

    @property
    def artist_id(self) -> int:
        return self.__artist_id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, new_full_name):
        self.__full_name = None

        if type(new_full_name) is str:
            new_full_name = new_full_name.strip()
            if new_full_name != '':
                self.__full_name = new_full_name

    def __repr__(self):
        return f"<Artist {self.full_name}, artist id = {self.artist_id}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.artist_id == other.artist_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.artist_id < other.artist_id

    def __hash__(self):
        return hash(self.__artist_id)
