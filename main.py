import re
from pathlib import Path
from Classes.Frame import Frame

def parse(render):
    """
    Parses the given name and returns a structured representation.

    Args:
        render (str): The name to be parsed.

    Returns:
        Frame: A Frame instance containing the parsed components.
    """
    # Regular expression pattern to match the name format
    pattern = r"^(?P<base>.+?)(?P<sep>[._])(?P<frame>\d+)(?P<ext>\.\w+)$"
    match = re.match(pattern, render)

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

def group_sequence(sequence):
    """
    Groups a sequence of frame names by their base names.

    Args:
        sequence (list): A list of frame names to be grouped.

    Returns:
        dict: A dictionary where keys are base names and values are lists of corresponding frame names.
    """
    groups = {}
    for render in sequence:
        parsed = parse(render)
        if parsed is not None:
            if parsed.base not in groups:
                groups[parsed.base] = []
            groups[parsed.base].append(parsed.frame)
        else:
            groups[render] = [render]
    return groups

def group_sequence_names(sequence):
    """
    Groups a sequence of frame names by their base names.

    Args:
        sequence (list): A list of frame names to be grouped.

    Returns:
        list: A list of different base names of the sequences.
    """
    return group_sequence(sequence).keys()

def sort(frames):
    """
    Sorts a list of frame numbers in ascending order.

    Args:
        frames (list): A list of frame numbers to be sorted.

    Returns:
        list: A sorted list of frame numbers.
    """
    return sorted(frames)

def detect_gaps(sequence):
    """
    Detects gaps in a sequence of frames.

    Args:
        sequence (list): A list of frame names to be checked for gaps.
    """
    grouped = group_sequence(sequence)
    grouped_gaps = {}
    for base, frames in grouped.items():
        sorted = sort(frames)
        gaps = []
        for i in range(len(sorted) - 1):
            if sorted[i + 1] != sorted[i] + 1:
                if (sorted[i] + 1 == sorted[i + 1] - 1 ):
                    gaps.append(sorted[i] + 1)
                else:
                    gaps.append((sorted[i] + 1, sorted[i + 1]-1))
        grouped_gaps[base] = gaps
    return grouped_gaps

    

if __name__ == "__main__":
    renders = [p.name for p in Path("renders").iterdir()]
    grouped_gaps = detect_gaps(renders)
    print (grouped_gaps)