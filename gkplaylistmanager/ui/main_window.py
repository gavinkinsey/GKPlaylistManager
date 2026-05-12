"""
Main window - thin UI layer.

Focus: Qt widget creation, layout, and event binding.
All business logic delegated to MainController.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidget, QListWidgetItem, QFileDialog, QInputDialog
)
from PyQt5.QtCore import Qt
from .controllers.main_controller import MainController


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, controller: MainController):
        super().__init__()
        self.controller = controller
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Create and layout UI widgets."""
        self.setWindowTitle("GK Playlist Manager")
        self.setGeometry(100, 100, 800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Header with buttons
        header_layout = QHBoxLayout()
        
        load_music_btn = QPushButton("Load Music Directories")
        load_music_btn.clicked.connect(self._on_load_music)
        header_layout.addWidget(load_music_btn)
        
        new_playlist_btn = QPushButton("New Playlist")
        new_playlist_btn.clicked.connect(self._on_create_playlist)
        header_layout.addWidget(new_playlist_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._on_save)
        header_layout.addWidget(save_btn)
        
        layout.addLayout(header_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Tracks list
        layout.addWidget(QLabel("Tracks:"))
        self.tracks_list = QListWidget()
        layout.addWidget(self.tracks_list)
        
        # Playlists list
        layout.addWidget(QLabel("Playlists:"))
        self.playlists_list = QListWidget()
        layout.addWidget(self.playlists_list)
        
        central.setLayout(layout)

    def _connect_signals(self):
        """Connect controller signals to UI update methods."""
        self.controller.tracks_updated.connect(self._update_tracks_list)
        self.controller.playlists_updated.connect(self._update_playlists_list)
        self.controller.playlist_created.connect(self._on_playlist_created)
        self.controller.error_occurred.connect(self._on_error)

    def _on_load_music(self):
        """Handle load music button click."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Music Directory"
        )
        if directory:
            self.status_label.setText(f"Loading music from {directory}...")
            self.controller.load_music_directories([directory])

    def _on_create_playlist(self):
        """Handle create playlist button click."""
        name, ok = QInputDialog.getText(self, "New Playlist", "Playlist name:")
        if ok and name:
            self.controller.create_playlist(name, "category")

    def _on_save(self):
        """Handle save button click."""
        if self.controller.save_playlists():
            self.status_label.setText("Playlists saved successfully")
        else:
            self.status_label.setText("Failed to save playlists")

    def _update_tracks_list(self, tracks):
        """Update tracks list display."""
        self.tracks_list.clear()
        for track in tracks:
            item = QListWidgetItem(f"{track.artist} - {track.title}")
            item.setData(Qt.UserRole, track)
            self.tracks_list.addItem(item)
        self.status_label.setText(f"Loaded {len(tracks)} tracks")

    def _update_playlists_list(self, playlists):
        """Update playlists list display."""
        self.playlists_list.clear()
        for playlist in playlists:
            item = QListWidgetItem(f"{playlist.name} ({len(playlist.tracks)} tracks)")
            item.setData(Qt.UserRole, playlist)
            self.playlists_list.addItem(item)

    def _on_playlist_created(self, playlist):
        """Handle new playlist created."""
        item = QListWidgetItem(f"{playlist.name} (0 tracks)")
        item.setData(Qt.UserRole, playlist)
        self.playlists_list.addItem(item)

    def _on_error(self, error_msg):
        """Handle error from controller."""
        self.status_label.setText(f"Error: {error_msg}")
