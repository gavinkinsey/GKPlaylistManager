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
- Run app (Qt GUI): `python main.py`
- Run CLI demo: `python -m gkplaylistmanager.cli.cli`
- Run all tests: `pytest -q` (pytest is expected; not included in requirements)
- Run core tests: `pytest tests/test_core.py -v`
- Run Application layer tests (no GUI): `pytest tests/test_application.py -v`
- Run a single test: `pytest tests/test_application.py::test_application_create_playlist`

No repository-provided lint or CI commands found.

---

## High-level architecture

**Clean three-layer architecture** separates business logic from GUI:

1. **Application Layer** (business logic - testable without GUI):
   - gkplaylistmanager/application.py: Application class orchestrates all business logic (playlist management, file scanning, persistence). ZERO Qt dependencies. Used by all UI layers.

2. **Controller Layer** (bridge between UI and Application):
   - gkplaylistmanager/ui/controllers/main_controller.py: MainController bridges Qt signals to Application calls and Application callbacks to Qt signals. Pure translation layer.

3. **View Layer** (Qt presentation - thin):
   - gkplaylistmanager/ui/main_window.py: Thin Qt UI layer. Only creates widgets, manages layout, and binds events. All business logic delegated to MainController.

4. **Data/Infrastructure Layer** (persistence and file I/O):
   - gkplaylistmanager/core.py: Domain models Track and Playlist with basic operations.
   - gkplaylistmanager/playlists/: Thin subclasses for playlist types (Album, Category).
   - gkplaylistmanager/file_scanner.py: Scans filesystem and reads audio metadata using mutagen; returns Track objects.
   - gkplaylistmanager/data_store.py: Local JSON persistence of playlists and M3U export. Playlists are stored as lists of dicts with keys `name`, `type`, and `tracks` (paths).

5. **Alternative UI Examples**:
   - gkplaylistmanager/cli/cli.py: Example CLI interface reusing the Application layer without any Qt code.

6. **Tests**:
   - tests/test_core.py: Unit tests for core model behavior.
   - tests/test_application.py: Integration tests for Application layer workflows (testable without GUI).

**Design philosophy**: One-way dependency flow: View → Controller → Application → Data. The Application layer is the single source of truth for business logic, reusable by any UI (Qt, CLI, Web API, Mobile, etc.). All UI changes go in ui/. All business logic changes go in application.py or lower layers.

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

### Business Logic Changes (application.py is the single source of truth)
- Add/modify high-level playlist operations: gkplaylistmanager/application.py (Application class)
- Add/modify domain model behavior: gkplaylistmanager/core.py (Track, Playlist classes)
- Add/modify playlist types: gkplaylistmanager/playlists/

### Data/Persistence Changes
- Change persistence format or location: gkplaylistmanager/data_store.py
- Change file scanning or supported formats: gkplaylistmanager/file_scanner.py (remember to update supported extensions here)

### UI Changes (Qt only)
- Qt MainWindow changes: gkplaylistmanager/ui/main_window.py
- UI event handling or button logic: MainWindow._on_* methods in main_window.py
- Bridge Qt signals to Application: gkplaylistmanager/ui/controllers/main_controller.py

### Adding New Interfaces (reuse Application layer!)
- Building a Web API: create gkplaylistmanager/ui/controllers/web_controller.py (reuses Application)
- Building a Mobile app: create gkplaylistmanager/ui/controllers/mobile_controller.py (reuses Application)
- Building a Desktop app: create gkplaylistmanager/ui/controllers/desktop_controller.py (reuses Application)

---

## Clean Architecture Notes

**Important**: This codebase uses clean three-layer architecture with strict separation of concerns:

1. **Application Layer** (gkplaylistmanager/application.py) is the single source of truth for all business logic
   - ZERO Qt dependencies - fully reusable and testable
   - Used by: MainController (Qt), CLI, and any future UI layers
   - When adding features: add to Application first, then expose via controller

2. **MainController** (gkplaylistmanager/ui/controllers/main_controller.py) is the ONLY place Qt signals are converted
   - Bridges Qt signals → Application method calls
   - Bridges Application callbacks → Qt signals
   - Keeps business logic out of UI

3. **MainWindow** (gkplaylistmanager/ui/main_window.py) is pure presentation
   - Only Qt widgets, layout, and event binding
   - NEVER add business logic here - delegate to MainController
   - Updates UI via signal connections from MainController

4. **Dependency Flow** (strictly one-way, never reverse):
   - MainWindow → MainController → Application → Data Layer
   - Application has NO imports from ui/

**When Adding Features:**
- Feature affects multiple UIs? → Add to Application layer
- Feature is Qt-specific? → Add to MainWindow or MainController
- Adding validation or state? → Add to Application layer
- Building new UI? → Create new controller, reuse Application

**Testing:**
- Business logic tested in tests/test_application.py (no GUI needed)
- Run without GUI: `pytest tests/test_application.py -v`
- Core models tested in tests/test_core.py

---

## Documentation

For detailed architecture documentation, see:
- ARCHITECTURE.md - Detailed explanation
- HOW_TO_EXTEND.md - Extension patterns and examples

---

If this file exists later, prefer *extending* these sections rather than replacing them wholesale—keep the same structure and callouts so Copilot can find the key entry points.
