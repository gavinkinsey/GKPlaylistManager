import json
from .core import Playlist, Track

# Simple local storage using JSON

def save_playlists(filename, playlists):
    data = []
    for pl in playlists:
        data.append({
            'name': pl.name,
            'type': pl.playlist_type,
            'tracks': [t.path for t in pl.tracks]
        })
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_playlists(filename, all_tracks):
    playlists = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for pl in data:
                playlist = Playlist(pl['name'], pl['type'])
                for path in pl['tracks']:
                    track = next((t for t in all_tracks if t.path == path), None)
                    if track:
                        playlist.add_track(track)
                playlists.append(playlist)
    except FileNotFoundError:
        pass
    return playlists

def export_m3u(filename, playlist):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for track in playlist.tracks:
            f.write(f'#EXTINF:-1,{track.artist} - {track.title}\n')
            f.write(track.path + '\n')
