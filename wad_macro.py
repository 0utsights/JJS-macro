import os
import time
import threading
import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab
from pynput import keyboard as kb
from pynput.keyboard import Key, Controller

TOGGLE_KEY   = Key.f6
QUIT_KEY     = Key.f8
SCAN_RATE    = 0.016
KEY_HOLD_S   = 0.05
DEBOUNCE_S   = 0.12
MATCH_THRESH = 0.55
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

ctrl     = Controller()
active   = False
running  = True
last_key = ""
last_t   = 0.0


def load_templates():
    templates = {}
    for key in ("W", "A", "D"):
        path = os.path.join(TEMPLATE_DIR, f"{key}.png")
        img  = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            templates[key] = img
            print(f"[+] {key}.png ({img.shape[1]}x{img.shape[0]})")
        else:
            print(f"[!] Missing template: {path}")
    return templates


def build_scan_box(templates):
    sw, sh     = pyautogui.size()
    th, tw     = next(iter(templates.values())).shape
    pad        = 60
    return (
        sw // 2 - tw // 2 - pad,
        int(sh * 0.80) - pad,
        tw + pad * 2,
        th + pad * 2,
    )


def grab(box):
    l, t, w, h = box
    shot = ImageGrab.grab(bbox=(l, t, l + w, t + h))
    return cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2GRAY)


def best_match(gray, templates):
    best_key, best_score = "", 0.0
    for key, tmpl in templates.items():
        th, tw = tmpl.shape
        fh, fw = gray.shape
        if tw > fw or th > fh:
            continue
        _, score, _, _ = cv2.minMaxLoc(
            cv2.matchTemplate(gray, tmpl, cv2.TM_CCOEFF_NORMED)
        )
        if score > best_score:
            best_score, best_key = score, key
    return (best_key, best_score) if best_score >= MATCH_THRESH else ("", best_score)


def press(key):
    ctrl.press(key.lower())
    time.sleep(KEY_HOLD_S)
    ctrl.release(key.lower())


def scan_loop(templates, box):
    global last_key, last_t, active, running
    while running:
        if not active:
            time.sleep(0.05)
            continue
        t0 = time.perf_counter()
        try:
            key, score = best_match(grab(box), templates)
            if key:
                now = time.time()
                if key != last_key or (now - last_t) > DEBOUNCE_S:
                    print(f"  {key}  ({score:.0%})")
                    press(key)
                    last_key, last_t = key, now
        except Exception as e:
            print(f"[err] {e}")
        time.sleep(max(0, SCAN_RATE - (time.perf_counter() - t0)))


def on_press(key):
    global active, running
    if key == TOGGLE_KEY:
        active = not active
        print(f"[{'ON' if active else 'OFF'}]")
    elif key == QUIT_KEY:
        running = False
        return False


def main():
    templates = load_templates()
    if not templates:
        print("[ERROR] No templates found. Run crop_templates.py first.")
        return

    box = build_scan_box(templates)
    print(f"[+] Scan box: {box}")
    print("[*] F6 toggle  |  F8 quit\n")

    threading.Thread(target=scan_loop, args=(templates, box), daemon=True).start()

    with kb.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()