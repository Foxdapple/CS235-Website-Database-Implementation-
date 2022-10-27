from datetime import date
from typing import List

from sqlalchemy import desc, asc, insert, delete
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session, make_transient

from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.user import User
from music.domainmodel.genre import Genre
from music.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return user

    def get_number_of_users(self):
        number_of_users = self._session_cm.session.query(User).count()
        return number_of_users

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_track_by_id(self, id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return track

    def get_num_tracks(self):
        number_of_tracks = self._session_cm.session.query(Track).count()
        return number_of_tracks

    def get_num_users(self):
        number_of_users = self._session_cm.session.query(User).count()
        return number_of_users

    def get_review_list(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def get_review_by_track(self, track_id: int) -> List[Review]:
        all_reviews = self._session_cm.session.query(Review).all()
        reviews = []
        for review in all_reviews:
            if review.track.track_id == track_id:
                reviews.append(review)
        return reviews

    def get_user_by_track(self, track_id: int) -> List[User]:
        all_reviews = self._session_cm.session.query(Review).all()
        reviews = []
        users = []
        for review in all_reviews:
            if review.track.track_id == track_id:
                reviews.append(review)

        for review in reviews:
            user_id = review.user_id
            if user_id is not None:
                user = self._session_cm.session.query(User).filter(User._User__user_id == user_id).one()
                users.append(user)
        return users

    def get_track_list(self) -> List[Track]:
        tracks = self._session_cm.session.query(Track).all()
        return tracks

    def get_artist_list(self) -> List[Artist]:
        artists = self._session_cm.session.query(Artist).all()
        return artists

    def get_album_list(self) -> List[Album]:
        albums = self._session_cm.session.query(Album).all()
        return albums

    def add_user_to_review(self, user: User):
        with self._session_cm as scm:
            item = scm.session.query(Review).order_by(desc(Review._Review__review_id)).first()
            item.user_id = user.user_id
            scm.commit()

    def add_genre_to_tracks(self, genre_list: List[Genre], track_id: int):
        with self._session_cm as scm:
            track_item = self._session_cm.session.query(Track).filter(Track._Track__track_id == track_id).one()
            genre_string = ""
            for genre in genre_list:
                genre_string += str(genre.genre_id) + ","
            genre_string = genre_string[:-2]
            track_item.genre_id = "9"
            scm.commit()

    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_artist(self, artist: Artist):
        with self._session_cm as scm:
            scm.session.add(artist)
            scm.commit()

    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()

    def get_album_by_id(self, id: int) -> Album:
        album = None
        try:
            album = self._session_cm.session.query(Album).filter(Album._Album__album_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return album

    def get_artist_by_id(self, id: int) -> Artist:
        artist = None
        try:
            artist = self._session_cm.session.query(Artist).filter(Artist._Artist__artist_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        print(artist)
        return artist
