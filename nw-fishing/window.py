import numpy as np
import pyautogui
from PIL import Image
from mss import mss

from models import Window


def get_nw_window():
    windows = pyautogui.getWindowsWithTitle("New World")
    nw_window = None

    for window in windows:
        if window.title == "New World":
            nw_window = window
            break

    if not nw_window:
        raise RuntimeError("Couldn't find New World window")

    return Window(
        nw_window.top,
        nw_window.left,
        nw_window.width,
        nw_window.height,
        nw_window,
    )


def get_screenshot_region(window: Window) -> tuple[Window, any]:
    return Window(
        top=window.top,
        left=window.left + round(window.width / 3),
        width=round(window.width / 3),
        height=window.height,
        pywindow=window,
    )


nw_window = get_nw_window()
ss_region = get_screenshot_region(nw_window).__dict__


def locate(image_path: str, confidence=0.6, grayscale=True):
    with mss() as sct:
        screenshot = Image.fromarray(np.array(sct.grab(ss_region)))

    return pyautogui.locate(
        image_path,
        screenshot,
        grayscale=grayscale,
        confidence=confidence,
    )
