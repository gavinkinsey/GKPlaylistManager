"""
Simple CLI interface demonstrating Application layer reuse.

This shows how to build a different UI (CLI) without duplicating any
of the GUI code - both Qt UI and this CLI share the same Application layer.
"""

from gkplaylistmanager.application import Application
from gkplaylistmanager.core import Track


def print_menu():
    """Display main menu."""
    print("\n--- GK Playlist Manager CLI ---")
    print("1. Create playlist")
    print("2. List playlists")
    print("3. Add demo track")
    print("4. List tracks")
    print("5. Add track to playlist")
    print("6. Save playlists")
    print("0. Exit")
    print()


def create_playlist(app: Application):
    """Create a new playlist."""
    name = input("Playlist name: ").strip()
    ptype = input("Playlist type (category/album) [category]: ").strip() or "category"
    
    playlist = app.create_playlist(name, ptype)
    print(f"Created playlist: {playlist.name} ({playlist.playlist_type})")


def list_playlists(app: Application):
    """List all playlists."""
    playlists = app.get_playlists()
    if not playlists:
        print("No playlists yet.")
        return
    
    print("\nPlaylists:")
    for i, pl in enumerate(playlists, 1):
        print(f"  {i}. {pl.name} ({pl.playlist_type}) - {len(pl.tracks)} tracks")


def add_demo_track(app: Application):
    """Add a demo track."""
    title = input("Track title: ").strip() or "Demo Track"
    artist = input("Artist: ").strip() or "Unknown Artist"
    path = f"/music/{title.lower().replace(' ', '_')}.mp3"
    
    track = Track(path, title, artist, "")
    app.tracks.append(track)
    print(f"Added track: {artist} - {title}")


def list_tracks(app: Application):
    """List all tracks."""
    tracks = app.get_tracks()
    if not tracks:
        print("No tracks loaded.")
        return
    
    print("\nTracks:")
    for i, track in enumerate(tracks, 1):
        print(f"  {i}. {track.artist} - {track.title}")


def add_track_to_playlist(app: Application):
    """Add a track to a playlist."""
    tracks = app.get_tracks()
    playlists = app.get_playlists()
    
    if not tracks:
        print("No tracks available.")
        return
    
    if not playlists:
        print("No playlists available.")
        return
    
    print("\nTracks:")
    for i, track in enumerate(tracks, 1):
        print(f"  {i}. {track.artist} - {track.title}")
    
    track_idx = int(input("Select track number: ")) - 1
    if 0 <= track_idx < len(tracks):
        track = tracks[track_idx]
    else:
        print("Invalid track selection.")
        return
    
    print("\nPlaylists:")
    for i, pl in enumerate(playlists, 1):
        print(f"  {i}. {pl.name}")
    
    pl_idx = int(input("Select playlist number: ")) - 1
    if 0 <= pl_idx < len(playlists):
        playlist = playlists[pl_idx]
    else:
        print("Invalid playlist selection.")
        return
    
    if app.add_track_to_playlist(playlist, track):
        print(f"Added {track.title} to {playlist.name}")
    else:
        print(f"Track already in {playlist.name}")


def main():
    """CLI main loop."""
    app = Application()
    
    print("Welcome to GK Playlist Manager CLI!")
    print("(This interface reuses the same Application layer as the Qt GUI)")
    
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        
        try:
            if choice == "1":
                create_playlist(app)
            elif choice == "2":
                list_playlists(app)
            elif choice == "3":
                add_demo_track(app)
            elif choice == "4":
                list_tracks(app)
            elif choice == "5":
                add_track_to_playlist(app)
            elif choice == "6":
                if app.save_playlists():
                    print("Playlists saved.")
                else:
                    print("No data file configured.")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
