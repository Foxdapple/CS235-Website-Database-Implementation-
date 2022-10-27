from music.domainmodel.track import Track


class PlayList:

    def __init__(self):
        self.__list_of_tracks = []

    def size(self):
        size_playlist = len(self.__list_of_tracks)
        if size_playlist > 0:
            return size_playlist

    def add_track(self, track: Track):
        if track not in self.__list_of_tracks:
            self.__list_of_tracks.append(track)
        else:
            pass

    def first_track_in_list(self):
        if len(self.__list_of_tracks) > 0:
            return self.__list_of_tracks[0]
        else:
            return None

    def remove_track(self, track):
        if track in self.__list_of_tracks:
            self.__list_of_tracks.remove(track)
        else:
            pass

    def select_track_to_listen(self, index):
        if 0 <= index < len(self.__list_of_tracks):
            return self.__list_of_tracks[index]
        else:
            return None

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if self.__current >= len(self.__list_of_tracks):
            raise StopIteration
        else:
            self.__current += 1
            return self.__list_of_tracks[self.__current - 1]
