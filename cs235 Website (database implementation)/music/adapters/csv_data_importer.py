import csv
from pathlib import Path
from datetime import date, datetime
from typing import List
import math
import json

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.csvdatareader import TrackCSVReader, create_track_object, create_artist_object, create_album_object, extract_genres
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User

list_of_keys_album = []
list_of_keys_artist = []
list_of_keys_track = []
list_of_genre_keys = []
genre_list = []


def create_objects(tracks, albums, repo: AbstractRepository):
    length_of_albums_list = len(albums)
    length_of_tracks_list = len(tracks)
    index = 0
    create_admin(repo)
    while index < max(length_of_tracks_list, length_of_albums_list):
        if index < length_of_tracks_list:
            track_item = tracks[index]
            artist = create_artist_object(track_item)
            populate_artists(artist, repo)

        if index < length_of_albums_list:
            album_item = albums[index]
            album = create_album_object(album_item)
            populate_albums(album, repo)

        if index < length_of_tracks_list:
            track = create_track_object(track_item)
            if artist is not None:
                current_artist = artist
            track_album_id = tracks[index]['album_id']
            track_album = repo.get_album_by_id(track_album_id)
            genre = extract_genres(track_item)
            populate_tracks(track, track_album, current_artist, genre, repo)
        index += 1

def populate_tracks(track, album, artist, genre_list, repo: AbstractRepository):
    # Create Track objects
    global list_of_keys_track
    track.album = album
    track.artist = artist
    for genre in genre_list:
        track.add_genre(genre)
    if track.track_id not in list_of_keys_track:
        repo.add_track(track)
        list_of_keys_track.append(track.track_id)


def populate_genre(genre, repo: AbstractRepository):
    global list_of_genre_keys
    repo.add_genre(i)
    for i in genre:
        if i.genre_id not in list_of_genre_keys:
            repo.add_genre(i)
            list_of_genre_keys.append(i.genre_id)



def populate_albums(album, repo: AbstractRepository):
    # Create Album object.
    global list_of_keys_album
    if album.album_id not in list_of_keys_album:
        repo.add_album(album)
        list_of_keys_album.append(album.album_id)


def populate_artists(artist, repo: AbstractRepository):
    # Create Artist object.
    if artist is not None:
        repo.add_artist(artist)


def create_admin(repo: AbstractRepository):
    user = User(1, "Silverstream", "Foxdapple")
    repo.add_user(user)


def clear_genre_table(repo: AbstractRepository):
    repo.clear_genre()
