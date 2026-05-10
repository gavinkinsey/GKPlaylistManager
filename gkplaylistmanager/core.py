from typing import List, Dict, Optional

class Track:
    def __init__(self, path: str, title: str, artist: str, album: str):
        self.path = path
        self.title = title
        self.artist = artist
        self.album = album

class Playlist:
    def __init__(self, name: str, playlist_type: str):
        self.name = name
        self.playlist_type = playlist_type  # "album" or "category"
        self.tracks: List[Track] = []

    def add_track(self, track: Track):
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track: Track):
        if track in self.tracks:
            self.tracks.remove(track)

    def has_track(self, track: Track) -> bool:
        return track in self.tracks
