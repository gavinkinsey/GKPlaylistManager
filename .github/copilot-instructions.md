# Copilot instructions for GKPlaylistManager

This repo is a local Python/Qt application for managing my music playlists.
Features:
    No online components: all data is local only.
    Album support: a track may be in 0 or 1 album.
    Category support: a track may be in 0 or more categories (uncategorized == not in any category).
    Scans user-specified directories for tracks (mp3, flac, ogg supported via mutagen).
    Drag-and-drop playlist and category management.

The instructions below are focused and factual to help future Copilot sessions make correct edits.

## Quick commands
- Install runtime deps: `pip install -r requirements.txt`
- Run app: `python main.py`
- Run full tests: `pytest -q` (pytest is expected; not included in requirements)
- Run a single test: `pytest tests/test_core.py::test_track_album`

No repository-provided lint or CI commands found.

---

## High-level architecture
- main.py: application entrypoint; starts a PyQt5 QApplication and MainWindow.
- gkplaylistmanager/core.py: domain models Track and Playlist and basic playlist operations.
- gkplaylistmanager/playlists/: thin subclasses for playlist types (e.g., Album).
- gkplaylistmanager/file_scanner.py: scans filesystem and reads audio metadata using mutagen; returns Track objects.
- gkplaylistmanager/data_store.py: local JSON persistence of playlists and M3U export. Playlists are stored as lists of dicts with keys `name`, `type`, and `tracks` (paths).
- gkplaylistmanager/ui/: Qt widgets (MainWindow, PlaylistView) and UI glue.
- tests/: small unit tests covering core model behavior.

Design notes for Copilot: separate UI (ui/) from domain logic (core/, playlists/) and storage (data_store.py). Changes to playlist behavior should live in core.py or playlists/; storage format is JSON in data_store.py.

---

## Key conventions & invariants
- Track identity: the Track.path (filesystem path) is the primary identifier used when persisting/loading playlists.
- Playlist types: `playlist_type` is a string with at least `"album"` and `"category"`. Album playlists assume a track belongs to at most one album.
- data_store.load_playlists() maps saved track paths back to Track objects by matching `Track.path` against the scanned `all_tracks` list.
- file_scanner.read_metadata(path) returns a Track; fallback uses filename if metadata missing.
- Supported audio extensions are defined in file_scanner.scan_music_dirs: (".mp3", ".flac", ".wav", ".aac", ".ogg"). Update only here to change supported types.
- M3U export: export_m3u writes #EXTINF lines with `artist - title` and then the path; playlist order preserved.

---

## Where to look for common tasks
- Add/modify model behavior: gkplaylistmanager/core.py
- Change how metadata is read or supported formats: gkplaylistmanager/file_scanner.py
- Change persistence format or location: gkplaylistmanager/data_store.py
- UI changes: gkplaylistmanager/ui/

---

If this file exists later, prefer *extending* these sections rather than replacing them wholesale—keep the same structure and callouts so Copilot can find the key entry points.
