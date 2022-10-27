from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, ARRAY
)

from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel import artist, user
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.user import User
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'user_review', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('review', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('track_id', Integer, ForeignKey('tracks.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'))
)

tracks_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(64), nullable=False),
    Column('artist_id', Integer, ForeignKey('artists.id')),
    Column('album_id', Integer, ForeignKey('albums.id')),
    Column('duration', String(255), nullable=False),
    Column('url', String(1024), nullable=True),
)

albums_table = Table(
    'albums', metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('title', String(64), nullable=False),
    Column('year', Integer, nullable=True),
    Column('url', String(1024), nullable=True),
)

artists_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True, unique=True),
    Column('name', String(64), nullable=False)
)

genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_id', Integer),
    Column('name', String(64), nullable=False)
)

track_genres_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_id', ForeignKey('genres.genre_id')),
    Column('track_id', ForeignKey('tracks.id'))
)

def map_model_to_tables():
    # map names i.e '_User__user_name' references the class item.
    # i.e, while the albums_table row is called year, the class calls for
    # self__release_year, therefore, the mapper would need to call '_Artist__release_year'
    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
    })
    mapper(Review, reviews_table, properties={
        '_Review__review_id': reviews_table.c.id,
        '_Review__review_text': reviews_table.c.review,
        '_Review__rating': reviews_table.c.rating,
        '_Review__track': relationship(Track, backref='_Review__track_id'),
        '_Review__user': relationship(User, backref='_Review__user_id')
    })
    mapper(Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.id,
        '_Track__title': tracks_table.c.title,
        '_Track__artist': relationship(Artist, backref='_Track__artist_id'),
        '_Track__album': relationship(Album, backref='_Track__album_id'),
        '_Track__track_duration': tracks_table.c.duration,
        '_Track__track_url': tracks_table.c.url,
        '_Track__genres': relationship(Genre, secondary=track_genres_table)
    })
    mapper(Album, albums_table, properties={
        '_Album__album_id': albums_table.c.id,
        '_Album__title': albums_table.c.title,
        '_Album__release_year': albums_table.c.year,
        '_Album__album_url': albums_table.c.url
    })
    mapper(Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.id,
        '_Artist__full_name': artists_table.c.name
    })
    mapper(Genre, genres_table, properties={
        '_Genre__genre_id': genres_table.c.genre_id,
        '_Genre__name': genres_table.c.name
    })
# MAPS SHIT TO database_repository filters, i.e (.filter(users._User__user_name)

