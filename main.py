import re
from Classes.Frame import Frame

def parse(name):
    """
    Parses the given name and returns a structured representation.

    Args:
        name (str): The name to be parsed.

    Returns:
        Frame: A Frame instance containing the parsed components.
    """
    # Regular expression pattern to match the name format
    pattern = r"^(?P<base>.+?)(?P<sep>[._])(?P<frame>\d+)(?P<ext>\.\w+)$"
    match = re.match(pattern, name)

    if not match:
        return None

    base = match.group("base")
    sep = match.group("sep")
    frame = int(match.group("frame"))
    ext = match.group("ext")
    padding = len(match.group("frame"))

    return Frame(
        base=base,
        sep=sep,
        frame=frame,
        padding=padding,
        ext=ext
    )
