from typing import NamedTuple

class Frame(NamedTuple):
    base: str
    sep: str
    frame: int
    padding: int
    ext: str