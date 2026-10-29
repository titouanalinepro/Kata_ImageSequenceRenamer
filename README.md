# Kata: Image Sequence Renamer

Build a Python command-line tool that detects, checks and renames image sequences, the way a Pipeline TD would in a VFX or animation studio.

## Context

In VFX and animation, a rendered shot is not a video but a series of numbered images, one per frame: `shot010_comp_v003.1001.exr`, `shot010_comp_v003.1002.exr`, and so on. Renders crash, frames go missing, versions need renaming. Handling these sequences safely is a daily pipeline task.

This kata trains you in filename parsing, safe file-system manipulation, small CLI design and test-driven development.

## Rules

One step at a time, tests first, and no peeking at existing libraries until the end.

1. **Strict TDD**: red (a failing test), green (the minimal code that makes it pass), refactor. No code without a test that asks for it.
2. **Steps in order**: don't read the next step until the current one is done. Each step may break an assumption in your design; that's the point.
3. **Timebox**: about 45 minutes per step. If you run over, write down where you're stuck and move on.
4. **Allowed libraries**: the standard library (`pathlib`, `re`, `argparse`) and `pytest`. No `fileseq` or `pyseq` during the kata.
5. **No real images**: tests work on empty files created in a temporary directory (pytest's `tmp_path` fixture).
6. **Golden rule of the pipeline**: the tool must never overwrite or lose a file. When in doubt, it refuses and explains why.
7. **Commit on every green**, so you can review how the design evolved afterwards.

## Starting data and conventions

A sequence filename splits into four parts: `<base><separator><frame><extension>`.

| Part      | Example             | Note                                                                     |
| --------- | ------------------- | ------------------------------------------------------------------------ |
| Base      | `shot010_comp_v003` | May contain digits (`v003`, `shot010`) that are not the frame number     |
| Separator | `.` or `_`          | The dot is the most common                                               |
| Frame     | `1001`              | The last group of digits before the extension; padding of 4 by default   |
| Extension | `.exr`              | Also `.png`, `.jpg`, `.dpx`, `.tif`                                      |

Compact sequence notations:

- `shot010_comp_v003.####.exr`: one `#` per digit of padding
- `shot010_comp_v003.%04d.exr`: printf notation, understood by FFmpeg and Nuke

Suggested test folder, generated with a small script:

```
renders/
  shot010_comp_v003.1001.exr … shot010_comp_v003.1100.exr   (without 1042, 1067, 1068, 1069)
  shot020_bg_v001.0001.png … shot020_bg_v001.0024.png
  shot030_fx_v002_0050.exr … shot030_fx_v002_0060.exr      (_ separator)
  notes.txt                                                  (standalone file)
  thumbnail.jpg                                              (standalone file)
```

Tip: reuse this generator as a pytest fixture; every step will need it.

## Steps

Five steps, from read-only to modifying files. Only move on once all tests are green.

### Step 1: Parse a filename

A `parse(name)` function returns the base, separator, frame number (integer), padding and extension, or `None` if the file is not a frame.

```
parse("shot010_comp_v003.1001.exr")  → base="shot010_comp_v003", sep=".", frame=1001, padding=4, ext=".exr"
parse("shot030_fx_v002_0050.exr")    → base="shot030_fx_v002", sep="_", frame=50, padding=4, ext=".exr"
parse("notes.txt")                   → None
```

### Step 2: Group into sequences

Command `seq ls <folder>`: prints one line per sequence, plus standalone files, sorted by name.

```
$ seq ls renders/
shot010_comp_v003.####.exr   1001-1100   (96 frames)
shot020_bg_v001.####.png     1-24        (24 frames)
shot030_fx_v002_####.exr     50-60       (11 frames)
notes.txt
thumbnail.jpg
```

### Step 3: Detect gaps

Command `seq check <folder>`: reports missing frames as compact ranges.

```
$ seq check renders/
shot010_comp_v003.####.exr   missing: 1042, 1067-1069
shot020_bg_v001.####.png     OK
shot030_fx_v002_####.exr     OK
```

Cases to test: a single missing frame, several ranges, the first or last frame missing (hint: you can't know without an expected range, hence the `--range 1001-1100` option).

### Step 4: Renumber

Command `seq offset <sequence> --start 1001`: shifts the whole sequence so it starts at the given number.

```
$ seq offset renders/shot020_bg_v001.####.png --start 1001
shot020_bg_v001.0001.png → shot020_bg_v001.1001.png
…
shot020_bg_v001.0024.png → shot020_bg_v001.1024.png
24 files renamed.
```

Trap to cover with a test: shifting 1-24 to 10-33 would overwrite frame 10 before it has been moved. Find a safe renaming order.

### Step 5: Rename and bump the version

Command `seq rename <sequence> <new notation>`: changes the base or the padding while keeping frame numbers.

```
$ seq rename renders/shot010_comp_v003.####.exr shot010_comp_v004.####.exr
96 files renamed.

$ seq rename renders/shot020_bg_v001.####.png shot020_bg_v001.%05d.png
shot020_bg_v001.0001.png → shot020_bg_v001.00001.png
…
```

The tool refuses if a target file already exists, and has changed nothing in that case (all or nothing).

## Bonus and variations

Pick from these once the five steps are done, in any order.

- **`--dry-run`** on every command that modifies files: shows what would happen without touching anything. An essential reflex in a studio.
- **Mixed padding**: a sequence `0998, 0999, 1000, 1001` versus no fixed padding (`998, 999, 1000`). What should happen?
- **Negative frames**: `shot.-0005.exr` exists in some pipelines (simulation pre-roll).
- **Several sequences with the same name** but different extensions (`.exr` and preview `.jpg`).
- **Undo**: `seq rename` writes a JSON log of the renames, and `seq undo <log>` reverses them.
- **JSON output** (`--json`) so other pipeline scripts can use the tool.
- **GUI**: a small PySide6 window that lists the sequences in a folder and highlights in red those with gaps.
- **FFmpeg integration**: `seq preview <sequence>` generates a preview MP4 using the `%04d` notation, starting from the correct first frame.

## After the kata

The kata is complete when all five steps pass their tests and the tool has never lost a file.

- [ ] All five steps are green
- [ ] A test covers the overwriting-offset trap (step 4)
- [ ] A test checks the all-or-nothing behaviour (step 5)
- [ ] `seq --help` explains every command
- [ ] A README with three usage examples and a short demo (GIF or video)

Only then, compare your version with the libraries used in production, `fileseq` and `pyseq` (on GitHub and PyPI). Look especially at how they handle padding, negative frames and discontinuous range notation (`1-10,20-30`).

Write down in your README what you would change after reading them: that is exactly the kind of reflection a studio likes to find in a portfolio.
