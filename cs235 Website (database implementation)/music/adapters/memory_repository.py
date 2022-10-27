import csv
from pathlib import Path
from datetime import date, datetime
from typing import List
import math
import json

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.csvdatareader import TrackCSVReader, create_track_object, create_artist_object, create_album_object
from music.domainmodel import artist, user, review
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.user import User
from music.domainmodel.genre import Genre


class MemoryRepository:

    def __init__(self):
        self.__tracks = []
        self.__tracks_index = dict()
        self.__albums = []
        self.__artist = []
        self.__users = []
        self.__genres = []
        self.__num_tracks = 0

    def add_user(self, user: user):
        self.__users.append(user)

    def get_users(self):
        return self.__users

    def get_user(self, user_name) -> user:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_number_of_users(self):
        return len(self.__users)

    def add_track(self, track: Track):
        self.__tracks.append(track)
        self.__tracks_index[track.track_id] = track
        self.__num_tracks += 1

    def get_num_tracks(self):
        return self.__num_tracks

    def get_track_by_id(self, track_id):
        return self.__tracks_index[track_id]

    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self.__tracks_index[id]
        except KeyError:
            pass  # Ignore exception and return None.
        return track

    def get_track_list(self) -> List:
        return self.__tracks

    @staticmethod
    def generate_genre_dict(string):
        genre_dict = string.replace("'", "\"")
        new_dict = json.loads(genre_dict)[0]
        return new_dict

    def generate_genre(self, genre_id, title):
        new_genre = Genre(genre_id, title)
        if title not in self.__genres:
            self.__genres.append(title)
        return new_genre

    def populate_tracks(self, track_repo):
        for item in track_repo:
            new_track = Track(int(item['track_id']), item['track_title'])
            new_track.artist = Artist(int(item['artist_id']), item['artist_name'])
            new_track.track_duration = round(float(item['track_duration']))
            new_track.track_url = item['track_url']
            if item['track_genres'].strip() != "":
                new_dict = self.generate_genre_dict(item['track_genres'])
                new_genre = self.generate_genre(int(new_dict['genre_id']), new_dict['genre_title'])
                new_track.add_genre(new_genre)
            if item['album_id'].strip() != "":
                new_track.album = Album(int(item['album_id']), item['album_title'])
            self.__num_tracks += 1
            self.__tracks.append(new_track)
            self.__tracks_index[int(item['track_id'])] = new_track

    def populate_albums(self, album_repo):
        for item in track_repo:
            new_track = Track(item['track_id'], item['track_title'])
            new_track.artist = item['artist_name']
            new_track.track_duration = item['track_duration']
            new_track.track_url = item['track_url']
            new_track.genres = item['track_genres']
            new_track.album = Album(item['album_id'], item['album_title'])
            self.__tracks.append(new_track)
