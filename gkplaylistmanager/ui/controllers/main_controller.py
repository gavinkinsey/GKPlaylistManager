"""
Main controller - bridges Qt UI events to Application layer.

Translates user interactions in MainWindow into Application method calls,
and updates the UI based on Application state changes.
"""

from typing import Optional
from ...application import Application
from PyQt5.QtCore import QObject, pyqtSignal


class MainController(QObject):
    """
    Controller that bridges Qt signals to Application layer.
    
    Receives events from MainWindow, calls Application methods,
    and emits signals to update UI.
    """

    # Signals emitted when state changes
    tracks_updated = pyqtSignal(list)  # List[Track]
    playlists_updated = pyqtSignal(list)  # List[Playlist]
    playlist_created = pyqtSignal(object)  # Playlist
    track_added_to_playlist = pyqtSignal(object, object)  # Playlist, Track
    track_removed_from_playlist = pyqtSignal(object, object)  # Playlist, Track
    error_occurred = pyqtSignal(str)  # error message

    def __init__(self, application: Application):
        super().__init__()
        self.app = application
        
        # Register Application callbacks to emit our signals
        self.app.set_on_tracks_loaded(lambda tracks: self.tracks_updated.emit(tracks))
        self.app.set_on_playlists_loaded(lambda playlists: self.playlists_updated.emit(playlists))
        self.app.set_on_playlist_created(lambda playlist: self.playlist_created.emit(playlist))
        self.app.set_on_track_added(lambda pl, track: self.track_added_to_playlist.emit(pl, track))
        self.app.set_on_track_removed(lambda pl, track: self.track_removed_from_playlist.emit(pl, track))

    def load_music_directories(self, directories: list) -> list:
        """Scan music directories for tracks."""
        try:
            return self.app.load_music_directories(directories)
        except Exception as e:
            self.error_occurred.emit(f"Failed to load music directories: {str(e)}")
            return []

    def initialize_playlists(self, data_file: str) -> list:
        """Load playlists from file."""
        try:
            return self.app.initialize_playlists(data_file)
        except Exception as e:
            self.error_occurred.emit(f"Failed to load playlists: {str(e)}")
            return []

    def create_playlist(self, name: str, playlist_type: str = "category"):
        """Create a new playlist."""
        try:
            return self.app.create_playlist(name, playlist_type)
        except Exception as e:
            self.error_occurred.emit(f"Failed to create playlist: {str(e)}")
            return None

    def add_track_to_playlist(self, playlist, track) -> bool:
        """Add a track to a playlist."""
        try:
            return self.app.add_track_to_playlist(playlist, track)
        except Exception as e:
            self.error_occurred.emit(f"Failed to add track: {str(e)}")
            return False

    def remove_track_from_playlist(self, playlist, track) -> bool:
        """Remove a track from a playlist."""
        try:
            return self.app.remove_track_from_playlist(playlist, track)
        except Exception as e:
            self.error_occurred.emit(f"Failed to remove track: {str(e)}")
            return False

    def save_playlists(self) -> bool:
        """Save playlists to file."""
        try:
            success = self.app.save_playlists()
            if not success:
                self.error_occurred.emit("Failed to save playlists")
            return success
        except Exception as e:
            self.error_occurred.emit(f"Error saving playlists: {str(e)}")
            return False

    def get_tracks(self) -> list:
        """Get all loaded tracks."""
        return self.app.get_tracks()

    def get_playlists(self) -> list:
        """Get all playlists."""
        return self.app.get_playlists()

    def find_track_by_path(self, path: str):
        """Find a track by path."""
        return self.app.find_track_by_path(path)

    def find_playlist_by_name(self, name: str):
        """Find a playlist by name."""
        return self.app.find_playlist_by_name(name)
