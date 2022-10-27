class Genre:

    def __init__(self, genre_id: int, genre_name: str):
        if type(genre_id) is not int or genre_id < 0:
            raise ValueError('Genre ID should be an integer!')
        self.__genre_id = genre_id

        if type(genre_name) is str:
            self.__name = genre_name.strip()
        else:
            self.__name = None

    @property
    def genre_id(self) -> int:
        return self.__genre_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = None
        if type(name) is str:
            name = name.strip()
            if name != '':
                self.__name = name

    def __repr__(self) -> str:
        return f'<Genre {self.name}, genre id = {self.genre_id}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.genre_id == other.genre_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.genre_id < other.genre_id

    def __hash__(self):
        return hash(self.genre_id)
