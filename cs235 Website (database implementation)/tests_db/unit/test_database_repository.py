import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository

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


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User(1, 'fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    assert user is None


def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = repo.get_num_tracks()

    # Check that the query returned 177 Articles.
    assert number_of_tracks > 0


def test_repository_can_retrieve_user_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_users = repo.get_num_users()

    # Check that the query returned 177 Articles.
    assert number_of_users > 0


def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = repo.get_num_tracks()

    new_track_id = number_of_tracks + 1

    track = Track(new_track_id, "Gamer")
    genre = Genre(1, "pop")
    track.add_genre(genre)
    repo.add_track(track)

    assert repo.get_track_by_id(new_track_id) == track


def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track_by_id(1)

    # Check that the Article has the expected title.
    assert track.title == 'Gamer'

    # Check that the Article is tagged as expected.
    assert track.genres == [genre]


def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track_by_id(201)
    assert track is None


def test_repository_can_add_a_comment(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('thorke')
    track = repo.get_track_by_id(1)
    review = Review(track, "lets a go", 3)

    repo.add_review(review)
    repo.add_user_to_review(user)

    assert review in repo.get_review_list()


def test_repository_can_add_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album = make_album(1)
    repo.add_album(album)
    album_db = repo.get_album_by_id(1)
    assert album == album_db and album is album_db


def test_repository_can_get_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album_db = repo.get_album_by_id(1)
    assert album_db.title == "Skyrim"


def test_repository_does_not_retrieve_a_non_existent_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    album_db = repo.get_album_by_id(2001)
    assert album_db is None


def test_repository_can_add_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist = make_artist(1)
    repo.add_artist(artist)
    artist_db = repo.get_artist_by_id(1)
    assert artist == artist_db and artist is artist_db


def test_repository_can_get_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist_db = repo.get_artist_by_id(1)
    assert artist_db.title == "Sever"


def test_repository_does_not_retrieve_a_non_existent_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    artist_db = repo.get_artist_by_id(22221)
    assert artist_db is None


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_review_list()) == 3


def make_track(new_track_id):
    track = Track(new_track_id, "Gamer")
    track.artist = Artist(2, "Sever")
    track.album = Album(1, "Skyrim")
    track.track_duration = 5
    return track


def make_artist(new_artist_id):
    artist = Artist(new_artist_id, "Sever")
    return artist


def make_album(new_album_id):
    album = Album(new_album_id, "Skyrim")
    return album


def test_can_retrieve_an_track_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Article and User.
    track = repo.get_track_by_id(5)

    # Create a new Comment, connecting it to the Article and User.
    review = Review(track, "lets a go", 3)

    track_fetched = repo.get_track_by_id(5)

    assert track_fetched in review.track
