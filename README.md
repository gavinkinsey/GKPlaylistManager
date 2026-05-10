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

## Project Structure

```
GKPlaylistManager/
├── main.py
├── requirements.txt
├── README.md
├── gkplaylistmanager/
│   ├── __init__.py
│   ├── core.py
│   ├── file_scanner.py
│   ├── data_store.py
│   ├── playlists/
│   │   ├── __init__.py
│   │   ├── album.py
│   │   └── category.py
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py
│       └── playlist_view.py
└── tests/
    └── test_core.py
```

---

For questions, new features, or bug reports, open an issue on GitHub. Contributions welcome!
