import abc
from typing import List
from datetime import date

from music.domainmodel import artist, user
from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.user import User
from music.domainmodel.genre import Genre


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_users(self):
        """ Returns sum of users in user table.

        If there is no User, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        """ Adds a track to the track table

        If the info is incomplete, doesn't add anything.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a genre to the genre table

        If the info is incomplete, doesn't add anything.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_by_id(self, id: int) -> Track:
        """ Returns specific track at id given. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_num_tracks(self) -> int:
        """ Returns the number of tracks in the database. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_num_users(self) -> int:
        """ Returns the number of users in the database. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_list(self) -> List[Review]:
        """ Returns a list of all reviews in the database. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_review_by_track(self, track_id: int) -> List[Review]:
        """ Returns a list of all reviews in the database
        with specific track id.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_by_track(self, track_id: int, review_id: int) -> List[User]:
        """ Returns a list of all users in the database
        with specific track id.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_list(self) -> List[Track]:
        """ Returns a list of Tracks, from the database.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_artist_list(self) -> List[Artist]:
        """ Returns a list of Artists, from the database.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_album_list(self) -> List[Album]:
        """ Returns a list of Albums, from the database.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user_to_review(self, user: User):
        """ Add's user to the user_id attribute in the database"""
        raise NotImplementedError

    def add_genre_to_tracks(self, genre_list: List[Genre], track_id: int):
        """ Add's user to the user_id attribute in the database"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds review to database."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        """ Returns a list of Tracks, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, artist_id) -> Artist:
        """ Returns a list of Tracks, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_album_by_id(self, artist_id) -> Artist:
        """ Returns a list of Tracks, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_artist_by_id(self, artist_id) -> Artist:
        """ Returns a list of Tracks, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError








