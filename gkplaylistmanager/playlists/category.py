from ..core import Playlist

class Category(Playlist):
    def __init__(self, name: str):
        super().__init__(name, "category")
