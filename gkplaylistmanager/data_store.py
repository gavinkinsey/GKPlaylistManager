import json
import os
from .core import Playlist, Track


def _load_m3u_file(path, all_tracks):
    playlists = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [l.rstrip('\n') for l in f]
        tracks = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if line.startswith('#EXTINF'):
                # next non-empty, non-comment line is the file path
                i += 1
                while i < len(lines) and lines[i].strip().startswith('#'):
                    i += 1
                if i < len(lines):
                    tracks.append(lines[i].strip())
            elif not line.startswith('#'):
                tracks.append(line)
            i += 1
        name = os.path.splitext(os.path.basename(path))[0]
        playlist = Playlist(name, "category")
        for p in tracks:
            track = next((t for t in all_tracks if t.path == p), None)
            if track:
                playlist.add_track(track)
        playlists.append(playlist)
    except Exception:
        pass
    return playlists


def export_m3u(filename, playlist):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for track in playlist.tracks:
            f.write(f'#EXTINF:-1,{track.artist} - {track.title}\n')
            f.write(track.path + '\n')


def save_playlists(filename, playlists):
    # Write JSON cache but prefer M3U files as primary source of truth.
    data = []
    for pl in playlists:
        data.append({
            'name': pl.name,
            'type': pl.playlist_type,
            'tracks': [t.path for t in pl.tracks]
        })
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

    base_dir = os.path.dirname(filename) or '.'
    # Write one .m3u per playlist (primary)
    for pl in playlists:
        safe_name = pl.name
        m3u_path = os.path.join(base_dir, f"{safe_name}.m3u")
        export_m3u(m3u_path, pl)


def load_playlists(filename, all_tracks):
    playlists = []
    base_dir = os.path.dirname(filename) or '.'

    # If JSON exists, load it but prefer corresponding .m3u files when present.
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for pl in data:
                m3u_path = os.path.join(base_dir, f"{pl['name']}.m3u")
                if os.path.exists(m3u_path):
                    playlists.extend(_load_m3u_file(m3u_path, all_tracks))
                else:
                    playlist = Playlist(pl['name'], pl['type'])
                    for path in pl['tracks']:
                        track = next((t for t in all_tracks if t.path == path), None)
                        if track:
                            playlist.add_track(track)
                    playlists.append(playlist)
            return playlists
    except FileNotFoundError:
        # No JSON file: fall back to scanning for .m3u files in base_dir
        try:
            for fname in os.listdir(base_dir):
                if fname.lower().endswith('.m3u'):
                    playlists.extend(_load_m3u_file(os.path.join(base_dir, fname), all_tracks))
        except Exception:
            pass
        return playlists
