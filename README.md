# JJS Higuruma Clash Macro

Automates the W/A/D clash inputs during Higuruma's ultimate ability in **Jujutsu Shenanigans**. Uses real-time screen capture and OpenCV template matching to detect and press clash prompts the moment they appear.

## How it works

Every ~16ms the macro captures a small region of the screen around the clash prompt, runs template matching against pre-cropped images of the W, A, and D keys, and fires the corresponding keypress if a match exceeds the confidence threshold. No neural networks — pure pixel comparison, sub-millisecond per frame.

## Setup

**Install dependencies**
```
py -m pip install opencv-python pynput Pillow numpy pyautogui
```

**Add templates**

Place `W.png`, `A.png`, and `D.png` inside a `templates/` folder in the same directory as `wad_macro.py`. Use the included `crop_templates.py` to generate these from your own screenshots.

```
wad_macro.py
crop_templates.py
templates/
    W.png
    A.png
    D.png
```

**Crop your own templates**
```
py crop_templates.py
```
Open a screenshot where each clash prompt is visible, draw a box over the letter, then press the matching key (W, A, or D) to save it.

## Usage

```
py wad_macro.py
```

| Key | Action |
|-----|--------|
| `F6` | Toggle ON/OFF — activate when Higuruma's clash starts |
| `F8` | Quit |

The macro prints each detected keypress and confidence score to the terminal so you can verify it's reading correctly.

## Tuning

If the macro is misfiring or missing inputs, adjust these values at the top of `wad_macro.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MATCH_THRESH` | `0.55` | Match confidence cutoff. Raise if misfiring, lower if missing. |
| `DEBOUNCE_S` | `0.12` | Minimum seconds before re-pressing the same key |
| `KEY_HOLD_S` | `0.05` | How long each key is held down |

If the scan region isn't aligned (wrong position on screen), re-run `crop_templates.py` using a screenshot from your own display.
