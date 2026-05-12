"""
Application orchestration layer.

Coordinates file scanning, playlist management, and persistence.
No GUI dependencies - can be used by Qt UI, CLI, or other interfaces.
"""

from typing import List, Callable, Optional
from .core import Playlist, Track
from .file_scanner import scan_music_dirs
from .data_store import load_playlists, save_playlists
from .playlists.album import Album
from .playlists.category import Category


class Application:
    """
    Application service that manages playlists and tracks.
    
    Provides high-level operations for playlist management, file scanning,
    and persistence. Callbacks notify listeners of state changes.
    """

    def __init__(self):
        self.tracks: List[Track] = []
        self.playlists: List[Playlist] = []
        self.music_dirs: List[str] = []
        self.data_file: Optional[str] = None
        
        # Callbacks for state changes
        self._on_tracks_loaded: Optional[Callable[[List[Track]], None]] = None
        self._on_playlists_loaded: Optional[Callable[[List[Playlist]], None]] = None
        self._on_playlist_created: Optional[Callable[[Playlist], None]] = None
        self._on_track_added: Optional[Callable[[Playlist, Track], None]] = None
        self._on_track_removed: Optional[Callable[[Playlist, Track], None]] = None

    def set_on_tracks_loaded(self, callback: Callable[[List[Track]], None]):
        """Set callback when tracks are loaded from directories."""
        self._on_tracks_loaded = callback

    def set_on_playlists_loaded(self, callback: Callable[[List[Playlist]], None]):
        """Set callback when playlists are loaded from storage."""
        self._on_playlists_loaded = callback

    def set_on_playlist_created(self, callback: Callable[[Playlist], None]):
        """Set callback when a new playlist is created."""
        self._on_playlist_created = callback

    def set_on_track_added(self, callback: Callable[[Playlist, Track], None]):
        """Set callback when a track is added to a playlist."""
        self._on_track_added = callback

    def set_on_track_removed(self, callback: Callable[[Playlist, Track], None]):
        """Set callback when a track is removed from a playlist."""
        self._on_track_removed = callback

    def load_music_directories(self, dirs: List[str]) -> List[Track]:
        """
        Scan music directories and load all tracks.
        
        Args:
            dirs: List of directory paths to scan
            
        Returns:
            List of loaded Track objects
        """
        self.music_dirs = dirs
        self.tracks = scan_music_dirs(dirs)
        
        if self._on_tracks_loaded:
            self._on_tracks_loaded(self.tracks)
        
        return self.tracks

    def initialize_playlists(self, data_file: str) -> List[Playlist]:
        """
        Load playlists from storage file.
        
        Must call load_music_directories() first so tracks are available.
        
        Args:
            data_file: Path to playlists data file
            
        Returns:
            List of loaded Playlist objects
        """
        self.data_file = data_file
        self.playlists = load_playlists(data_file, self.tracks)
        
        if self._on_playlists_loaded:
            self._on_playlists_loaded(self.playlists)
        
        return self.playlists

    def create_playlist(self, name: str, playlist_type: str) -> Playlist:
        """
        Create a new playlist.
        
        Args:
            name: Name of the playlist
            playlist_type: Type of playlist ("album", "category", etc.)
            
        Returns:
            The newly created Playlist object
        """
        if playlist_type == "album":
            playlist = Album(name)
        elif playlist_type == "category":
            playlist = Category(name)
        else:
            playlist = Playlist(name, playlist_type)
        
        self.playlists.append(playlist)
        
        if self._on_playlist_created:
            self._on_playlist_created(playlist)
        
        return playlist

    def add_track_to_playlist(self, playlist: Playlist, track: Track) -> bool:
        """
        Add a track to a playlist.
        
        Args:
            playlist: The Playlist to add to
            track: The Track to add
            
        Returns:
            True if track was added, False if already in playlist
        """
        if track not in playlist.tracks:
            playlist.add_track(track)
            
            if self._on_track_added:
                self._on_track_added(playlist, track)
            
            return True
        
        return False

    def remove_track_from_playlist(self, playlist: Playlist, track: Track) -> bool:
        """
        Remove a track from a playlist.
        
        Args:
            playlist: The Playlist to remove from
            track: The Track to remove
            
        Returns:
            True if track was removed, False if not in playlist
        """
        if track in playlist.tracks:
            playlist.remove_track(track)
            
            if self._on_track_removed:
                self._on_track_removed(playlist, track)
            
            return True
        
        return False

    def save_playlists(self) -> bool:
        """
        Save current playlists to storage.
        
        Args:
            
        Returns:
            True if save was successful, False otherwise
        """
        if not self.data_file:
            return False
        
        try:
            save_playlists(self.data_file, self.playlists)
            return True
        except Exception:
            return False

    def get_playlists(self) -> List[Playlist]:
        """Get all current playlists."""
        return self.playlists

    def get_tracks(self) -> List[Track]:
        """Get all loaded tracks."""
        return self.tracks

    def find_track_by_path(self, path: str) -> Optional[Track]:
        """Find a track by its file path."""
        return next((t for t in self.tracks if t.path == path), None)

    def find_playlist_by_name(self, name: str) -> Optional[Playlist]:
        """Find a playlist by name."""
        return next((p for p in self.playlists if p.name == name), None)
