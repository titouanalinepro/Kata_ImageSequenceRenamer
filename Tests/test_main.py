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

from main import group_sequence_names

def test_group_sequence():
    renders = [
        "shot010_comp_v003.1001.exr",
        "shot010_comp_v003.1002.exr",
        "shot010_comp_v003.1003.exr",
        "shot030_fx_v002_0050.exr",
        "shot030_fx_v002_0051.exr",
        "notes.txt",
        "thumbnail.jpg"
    ]
    grouped = group_sequence_names(renders)
    assert "shot010_comp_v003" in grouped
    assert "shot030_fx_v002" in grouped
    assert "notes.txt" in grouped
    assert "thumbnail.jpg" in grouped
    assert len(grouped) == 4

import pytest
from make_test_render import make_renders
from main import detect_gaps

@pytest.fixture
def renders(tmp_path):
    return make_renders(tmp_path / "renders")

def test_detect_gaps_no_gap():
    renders = [
        "shot010_comp_v003.1001.exr",
        "shot010_comp_v003.1002.exr",
        "shot010_comp_v003.1003.exr"
    ]
    assert detect_gaps(renders) == {"shot010_comp_v003": []}

def test_detect_gaps_single_missing_frame():
    renders = [
        "shot010_comp_v003.1001.exr",
        "shot010_comp_v003.1002.exr",
        "shot010_comp_v003.1004.exr"
    ]
    assert detect_gaps(renders) == {"shot010_comp_v003": [1003]}

def test_detect_gaps_several_ranges():
    renders = [
        "shot010_comp_v003.1001.exr",
        "shot010_comp_v003.1002.exr",
        "shot010_comp_v003.1004.exr",
        "shot010_comp_v003.1005.exr",
        "shot010_comp_v003.1008.exr"
    ]
    assert detect_gaps(renders) == {"shot010_comp_v003": [1003, (1006, 1007)]}

def test_detect_gaps_unsorted_input():
    renders = [
        "shot010_comp_v003.1004.exr",
        "shot010_comp_v003.1001.exr",
        "shot010_comp_v003.1002.exr"
    ]
    assert detect_gaps(renders) == {"shot010_comp_v003": [1003]}

def test_detect_gaps_underscore_separator():
    renders = [
        "shot030_fx_v002_0050.exr",
        "shot030_fx_v002_0052.exr"
    ]
    assert detect_gaps(renders) == {"shot030_fx_v002": [51]}

def test_detect_gaps_sequences_are_independent():
    renders = [
        "shot010_comp_v003.1001.exr",
        "shot010_comp_v003.1003.exr",
        "shot020_bg_v001.0001.png",
        "shot020_bg_v001.0002.png"
    ]
    assert detect_gaps(renders) == {
        "shot010_comp_v003": [1002],
        "shot020_bg_v001": []
    }

def test_detect_gaps_standalone_file_has_no_gap():
    assert detect_gaps(["notes.txt"]) == {"notes.txt": []}

def test_detect_gaps_on_renders_folder(renders):
    names = [p.name for p in renders.iterdir()]
    gaps = detect_gaps(names)
    assert gaps["shot010_comp_v003"] == [1042, (1067, 1069)]
    assert gaps["shot020_bg_v001"] == []
    assert gaps["shot030_fx_v002"] == []
    assert gaps["notes.txt"] == []
    assert gaps["thumbnail.jpg"] == []