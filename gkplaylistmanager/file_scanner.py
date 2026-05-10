import os
from mutagen import File
from .core import Track

def read_metadata(path):
    try:
        audio = File(path, easy=True)
        if audio is not None:
            title = audio.get('title', [os.path.splitext(os.path.basename(path))[0]])[0]
            artist = audio.get('artist', [''])[0]
            album = audio.get('album', [''])[0]
            return Track(path, title, artist, album)
    except Exception:
        pass
    # Fallback: just the filename
    return Track(path, os.path.splitext(os.path.basename(path))[0])

def scan_music_dirs(dirs):
    tracks = []
    for music_dir in dirs:
        for root, _, files in os.walk(music_dir):
            for f in files:
                if f.lower().endswith((".mp3", ".flac", ".wav", ".aac", ".ogg")):
                    path = os.path.join(root, f)
                    t = read_metadata(path)
                    tracks.append(t)
    return tracks
