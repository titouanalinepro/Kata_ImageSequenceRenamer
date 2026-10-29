"""Generate the fake `renders/` folder used by the image sequence kata.

Usage:
    python make_test_renders.py            # creates ./renders
    python make_test_renders.py some/dir   # creates some/dir

The same `make_renders(path)` function can be reused as a pytest fixture:

    import pytest
    from make_test_renders import make_renders

    @pytest.fixture
    def renders(tmp_path):
        return make_renders(tmp_path / "renders")
"""

import sys
from pathlib import Path

MISSING_SHOT010 = {1042, 1067, 1068, 1069}


def make_renders(root: Path) -> Path:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)

    # shot010: 1001-1100, '.' separator, padding 4, with gaps
    for frame in range(1001, 1101):
        if frame not in MISSING_SHOT010:
            (root / f"shot010_comp_v003.{frame:04d}.exr").touch()

    # shot020: 1-24, '.' separator, padding 4
    for frame in range(1, 25):
        (root / f"shot020_bg_v001.{frame:04d}.png").touch()

    # shot030: 50-60, '_' separator, padding 4
    for frame in range(50, 61):
        (root / f"shot030_fx_v002_{frame:04d}.exr").touch()

    # standalone files
    (root / "notes.txt").touch()
    (root / "thumbnail.jpg").touch()

    return root


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("renders")
    out = make_renders(target)
    count = sum(1 for _ in out.iterdir())
    print(f"Created {count} files in {out}")