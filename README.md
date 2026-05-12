# GKPlaylistManager

A local Python/Qt application for managing your music playlists. 

**Features:**
- No online components: all data is local only.
- Album support: a track may be in 0 or 1 album.
- Category support: a track may be in 0 or more categories (uncategorized == not in any category).
- Album/category logic follows music organization best practices.
- Scans user-specified directories for tracks (mp3, flac, ogg supported via `mutagen`).
- Drag-and-drop playlist and category management.
- M3U playlist export and local JSON data storage.

**Requirements:**
- Python 3.8+
- PyQt5
- mutagen

## Install

    pip install -r requirements.txt

## Run

    python main.py

## Architecture

This project uses **clean architecture** with a clear separation between business logic and GUI:

- **Application Layer** (`application.py`) - All business logic, testable without GUI
- **Controller Layer** (`ui/controllers/main_controller.py`) - Bridges Qt to Application
- **View Layer** (`ui/main_window.py`) - Pure Qt presentation, thin and focused
- **Data Layer** (`core.py`, `data_store.py`, `file_scanner.py`) - Models and persistence

See the core code, documentation, and issue tracker for detailed information.

## Project Structure

```
GKPlaylistManager/
├── main.py                          # Entry point
├── requirements.txt
├── README.md
├── ARCHITECTURE.md                  # Architecture documentation
├── README.md
├── HOW_TO_EXTEND.md                 # Extension patterns
├── gkplaylistmanager/
│   ├── __init__.py
│   ├── application.py               # Business logic layer (testable)
│   ├── core.py                      # Domain models
│   ├── file_scanner.py              # File I/O
│   ├── data_store.py                # Persistence
│   ├── playlists/
│   │   ├── __init__.py
│   │   ├── album.py
│   │   └── category.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py           # Qt GUI (thin layer)
│   │   ├── playlist_view.py
│   │   └── controllers/
│   │       └── main_controller.py   # Bridge layer
│   └── cli/
│       └── cli.py                   # CLI demo (reuses Application)
└── tests/
    ├── test_core.py                 # Core model tests
    └── test_application.py          # Application layer tests (no GUI!)
```

## Testing

Test the application **without GUI**:

    pytest tests/test_application.py -v

This demonstrates the clean separation - all business logic is testable independently!

## Extending

Add new features once, work everywhere:
- **CLI**: See `gkplaylistmanager/cli/cli.py` for example
- **Web API**: Create a new controller, reuse Application layer
- **Mobile**: Create a new controller, reuse Application layer

See the issue tracker for detailed patterns.

---

For questions, new features, or bug reports, open an issue on GitHub. Contributions welcome!
