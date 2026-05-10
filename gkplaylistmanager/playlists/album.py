from ..core import Playlist

class Album(Playlist):
    def __init__(self, name: str):
        super().__init__(name, "album")
