from datetime import datetime
from music.domainmodel.track import Track


class Review:

    def __init__(self, track: Track, review_text: str, rating: int):
        self.__track = None
        if isinstance(track, Track):
            self.__track = track

        self.__review_text = 'N/A'
        if isinstance(review_text, str):
            self.__review_text = review_text.strip()

        if isinstance(rating, int) and 1 <= rating <= 5:
            self.__rating = rating
        else:
            raise ValueError('Invalid value for the rating.')

        self.__timestamp = datetime.now()

    @property
    def track(self) -> Track:
        return self.__track

    @property
    def review_text(self) -> str:
        return self.__review_text

    @review_text.setter
    def review_text(self, new_text):
        if type(new_text) is str:
            self.__review_text = new_text.strip()
        else:
            self.__review_text = None

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, new_rating: int):
        if isinstance(new_rating, int) and 1 <= new_rating <= 5:
            self.__rating = new_rating
        else:
            self.__rating = None
            raise ValueError("Wrong value for the rating")

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.track == self.track and other.review_text == self.review_text and other.rating == self.rating and other.timestamp == self.timestamp

    def __repr__(self):
        return f'<Review of track {self.track}, rating = {self.rating}, review_text = {self.review_text}>'
