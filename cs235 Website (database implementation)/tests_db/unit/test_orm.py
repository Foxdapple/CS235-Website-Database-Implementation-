import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel.review import Review
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.user import User
from music.domainmodel.genre import Genre


def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (id, title, artist_id, album_id, duration, url) VALUES '
        '(:id, "AWOL", :artist_id, :album_id, :duration, http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food)',
        {'id': 1, 'artist_id': 1, 'album_id': 2, 'duration': 5})
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


def insert_album(empty_session):
    empty_session.execute(
        'INSERT INTO albums (id, title, year, url) VALUES '
        '(:id, "AWOL", :year, http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food)',
        {'id': 2, 'year': 2004})
    row = empty_session.execute('SELECT id from albums').fetchone()
    return row[0]


def insert_artist(empty_session):
    empty_session.execute(
        'INSERT INTO artists (id, name) VALUES '
        '(:id, "Sever")',
        {'id': 1})
    row = empty_session.execute('SELECT id from artists').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_id, name) VALUES (1), ("Pop")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track_genre_associations(empty_session, track_id, genre_keys):
    stmt = 'INSERT INTO article_tags (track_id, genre_id) VALUES (:track_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'track_id': track_id, 'genre_id': genre_key})


def insert_track_comment(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO user_review (review, rating, track_id, user_id) VALUES '
        '("review", :rating, :track_id, :user_id),'
        '("review2", :rating, :track_id, :user_id)',
        {'user_id': user_key, 'track_id': track_key, 'rating': 3}
    )

    row = empty_session.execute('SELECT id from user_review').fetchone()
    return row[0]


def make_track():
    track = Track(
        1, "Dragonborn Comes"
    )
    return track


def make_user():
    user = User(1, "Andrew", "111")
    return user


def make_genre():
    genre = Genre(1, "pop")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User(1, "Andrew", "1234"),
        User(2, "Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id


def test_loading_of_commented_track(empty_session):
    insert_track_comment(empty_session)

    rows = empty_session.query(User).all()
    track = rows[0]

    for comment in user.reviews:
        assert comment.track is track


def test_saving_of_comment(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Track).all()
    track = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "Some comment text."
    review = make_comment(comment_text, user, track)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT review, track_id, user_id FROM user_review'))

    assert rows == [(review, track_key, user_key)]


def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, title, artist_id, album_id, duration, url FROM tracks'))
    id = 1
    duration = 5
    artist_id = 1
    album_id = 2

    assert rows == [(id, "AWOL", artist_id, album_id, duration,
                     "http://freemusicarchive.org/music/AWOL/AWOL_-_A_Way_Of_Life/Food"
                     )]


def test_saving_track_genre(empty_session):
    track = make_track()
    genre = make_genre()

    # Establish the bidirectional relationship between the Article and the Tag.
    track.add_genre(genre)

    # Persist the Article (and Tag).
    # Note: it doesn't matter whether we add the Tag or the Article. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(track)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT id FROM tracks'))
    track_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT genre_id, name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][1] == "pop"

    # Check that the article_tags table has a new record.
    rows = list(empty_session.execute('SELECT genre_id, track_id from track_genres'))
    genre_foreign_key = rows[0][0]
    track_foreign_key = rows[0][1]

    assert track_key == track_foreign_key
    assert genre_key == genre_foreign_key


def test_save_commented_track(empty_session):
    # Create Article User objects.
    track = make_track()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "Some comment text."
    review = Review(track, comment_text, 1)


    # Save the new Article.
    empty_session.add(track)
    empty_session.add(review)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT id FROM tracks'))
    track_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT track_id, review FROM user_review'))
    assert rows == [(track_key, comment_text)]
