import os
import csv
import ast


from music.adapters.memory_repository import MemoryRepository
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre

new_repository = MemoryRepository()
