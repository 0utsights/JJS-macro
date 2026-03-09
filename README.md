# JJS Higuruma Clash Macro

Detects and presses W/A/D clash prompts during Higuruma's ultimate in Jujutsu Shenanigans using OpenCV template matching.

## Setup

```
py -m pip install opencv-python pynput Pillow numpy pyautogui
```

Place `W.png`, `A.png`, `D.png` in a `templates/` folder next to `wad_macro.py`.

```
wad_macro.py
templates/
    W.png
    A.png
    D.png
```

## Usage

```
py wad_macro.py
```

- **F6** — toggle on/off when the clash starts
- **F8** — quit

## Tuning

| Variable | Default | Description |
|----------|---------|-------------|
| `MATCH_THRESH` | `0.55` | Raise if misfiring, lower if missing inputs |
| `DEBOUNCE_S` | `0.12` | Min seconds before re-pressing the same key |
| `KEY_HOLD_S` | `0.05` | How long each keypress is held |
