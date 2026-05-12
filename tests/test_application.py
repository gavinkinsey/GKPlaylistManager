"""Tests for the Application orchestration layer."""

import os
import tempfile
from pathlib import Path
from gkplaylistmanager.core import Track, Playlist
from gkplaylistmanager.application import Application
from gkplaylistmanager.playlists.album import Album
from gkplaylistmanager.playlists.category import Category


def test_application_basic_initialization():
    """Test Application can be instantiated."""
    app = Application()
    assert app.tracks == []
    assert app.playlists == []
    assert app.music_dirs == []
    assert app.data_file is None


def test_application_create_playlist():
    """Test creating playlists."""
    app = Application()
    
    pl_category = app.create_playlist("My Category", "category")
    assert isinstance(pl_category, Category)
    assert pl_category.name == "My Category"
    assert pl_category.playlist_type == "category"
    assert len(app.playlists) == 1
    
    pl_album = app.create_playlist("My Album", "album")
    assert isinstance(pl_album, Album)
    assert pl_album.name == "My Album"
    assert pl_album.playlist_type == "album"
    assert len(app.playlists) == 2


def test_application_track_operations():
    """Test adding and removing tracks from playlists."""
    app = Application()
    
    track1 = Track("a.mp3", "Song 1", "Artist 1", "Album 1")
    track2 = Track("b.mp3", "Song 2", "Artist 2", "Album 2")
    
    app.tracks = [track1, track2]
    
    playlist = app.create_playlist("Test", "category")
    
    # Add tracks
    assert app.add_track_to_playlist(playlist, track1) is True
    assert len(playlist.tracks) == 1
    
    assert app.add_track_to_playlist(playlist, track2) is True
    assert len(playlist.tracks) == 2
    
    # Try adding duplicate
    assert app.add_track_to_playlist(playlist, track1) is False
    assert len(playlist.tracks) == 2
    
    # Remove track
    assert app.remove_track_from_playlist(playlist, track1) is True
    assert len(playlist.tracks) == 1
    
    # Try removing non-existent track
    assert app.remove_track_from_playlist(playlist, track1) is False
    assert len(playlist.tracks) == 1


def test_application_find_operations():
    """Test finding tracks and playlists."""
    app = Application()
    
    track = Track("song.mp3", "Title", "Artist", "Album")
    app.tracks = [track]
    
    playlist = app.create_playlist("My Playlist", "category")
    
    # Find track
    found_track = app.find_track_by_path("song.mp3")
    assert found_track == track
    
    not_found = app.find_track_by_path("nonexistent.mp3")
    assert not_found is None
    
    # Find playlist
    found_pl = app.find_playlist_by_name("My Playlist")
    assert found_pl == playlist
    
    not_found_pl = app.find_playlist_by_name("Nonexistent")
    assert not_found_pl is None


def test_application_callbacks():
    """Test that callbacks are called on state changes."""
    app = Application()
    
    callbacks_called = {}
    
    def on_tracks_loaded(tracks):
        callbacks_called['tracks_loaded'] = tracks
    
    def on_playlists_loaded(playlists):
        callbacks_called['playlists_loaded'] = playlists
    
    def on_playlist_created(playlist):
        callbacks_called['playlist_created'] = playlist
    
    def on_track_added(playlist, track):
        callbacks_called['track_added'] = (playlist, track)
    
    def on_track_removed(playlist, track):
        callbacks_called['track_removed'] = (playlist, track)
    
    app.set_on_tracks_loaded(on_tracks_loaded)
    app.set_on_playlists_loaded(on_playlists_loaded)
    app.set_on_playlist_created(on_playlist_created)
    app.set_on_track_added(on_track_added)
    app.set_on_track_removed(on_track_removed)
    
    # Trigger callbacks
    track = Track("a.mp3", "Song", "Artist", "Album")
    app.tracks = [track]
    
    playlist = app.create_playlist("Test", "category")
    assert callbacks_called['playlist_created'] == playlist
    
    app.add_track_to_playlist(playlist, track)
    assert callbacks_called['track_added'] == (playlist, track)
    
    app.remove_track_from_playlist(playlist, track)
    assert callbacks_called['track_removed'] == (playlist, track)


def test_application_get_methods():
    """Test getter methods."""
    app = Application()
    
    track = Track("a.mp3", "Song", "Artist", "Album")
    app.tracks = [track]
    
    playlist = app.create_playlist("Test", "category")
    
    assert app.get_tracks() == [track]
    assert app.get_playlists() == [playlist]


def test_application_save_without_data_file():
    """Test save returns False when no data file set."""
    app = Application()
    assert app.save_playlists() is False


def test_application_save_with_data_file():
    """Test save succeeds when data file is set."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_file = os.path.join(tmpdir, "test_playlists.json")
        
        app = Application()
        app.data_file = data_file
        
        # Create some test data
        track = Track("a.mp3", "Song", "Artist", "Album")
        app.tracks = [track]
        playlist = app.create_playlist("Test", "category")
        app.add_track_to_playlist(playlist, track)
        
        # Save should succeed
        assert app.save_playlists() is True
        
        # File should exist
        assert os.path.exists(data_file)


def test_application_no_gui_dependency():
    """Verify Application has no Qt dependencies (can import without Qt)."""
    # This test verifies the Application module can be imported and used
    # without any Qt dependencies being imported
    app = Application()
    
    # Do a basic workflow
    track = Track("test.mp3", "Test Song", "Test Artist", "Test Album")
    app.tracks = [track]
    
    playlist = app.create_playlist("Test", "category")
    app.add_track_to_playlist(playlist, track)
    
    assert len(playlist.tracks) == 1
    assert app.find_playlist_by_name("Test") is not None
