from main import parse

def test_parse_dot_separator():
    r = parse("shot010_comp_v003.1001.exr")
    assert r.base == "shot010_comp_v003"
    assert r.sep == "."
    assert r.frame == 1001
    assert r.padding == 4
    assert r.ext == ".exr"

def test_parse_underscore_separator():
    r = parse("shot030_fx_v002_0050.exr")
    assert r.base == "shot030_fx_v002"
    assert r.sep == "_"
    assert r.frame == 50
    assert r.padding == 4

def test_parse_not_a_frame():
    assert parse("notes.txt") is None
    assert parse("thumbnail.jpg") is None