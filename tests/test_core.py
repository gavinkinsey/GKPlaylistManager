from gkplaylistmanager.core import Track, Playlist

def test_track_album():
    t = Track("a.flac", "foo", "bar", "baz")
    assert t.title == "foo"
    pl = Playlist("r", "album")
    pl.add_track(t)
    assert pl.has_track(t)
    pl.remove_track(t)
    assert not pl.has_track(t)
