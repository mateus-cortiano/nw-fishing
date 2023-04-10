import random
import time
import functools

import pyautogui
import pydirectinput

from models import Window


def _fuzzy(func):
    @functools.wraps(func)
    def fuzzy(*args, **kwargs):
        fuzz = random.random() / 16
        time.sleep(fuzz)
        func(*args, **kwargs)
        time.sleep(fuzz)

    return fuzzy


@_fuzzy
def click():
    pyautogui.click()


@_fuzzy
def proportional_click(
    window: Window,
    x: float,
    y: float,
    clicks: int = 1,
    interval: float = 0,
    button: str = "primary",
    duration: float = 0,
):
    pyautogui.click(
        round(window.width * x),
        round(window.height * y),
        clicks,
        interval,
        button,
        duration,
    )


@_fuzzy
def mouse_up():
    pyautogui.mouseUp()


@_fuzzy
def mouse_down():
    pyautogui.mouseDown()


@_fuzzy
def key_up(key: str):
    pydirectinput.keyUp(key)


@_fuzzy
def key_down(key: str):
    pydirectinput.keyDown(key)


@_fuzzy
def activate_window(window: Window):
    window.pywindow.activate()


def center_mouse(window: Window):
    x, y = window.center
    pyautogui.moveTo(x, y)


def cast_line(casting_time):
    mouse_down()
    time.sleep(casting_time)
    mouse_up()


def equip_bait(window: Window):
    pyautogui.press("r")
    time.sleep(3)

    proportional_click(
        window=window,
        x=0.62,
        y=0.42,
        clicks=2,
        interval=0.1,
        duration=0.1,
    )
    time.sleep(1.5)

    proportional_click(
        window=window,
        x=0.78,
        y=0.76,
        clicks=2,
        interval=0.1,
        duration=0.1,
    )
    time.sleep(4)

    center_mouse(window)


def repair_tool(window: Window):
    pyautogui.press("tab")
    time.sleep(1.5)

    proportional_click(
        window=window,
        x=0.35,
        y=0.92,
        clicks=2,
        duration=0.1,
        interval=0.1,
    )
    time.sleep(1.5)

    proportional_click(
        window=window,
        x=0.57,
        y=0.60,
        clicks=2,
        duration=0.1,
        interval=0.1,
    )
    time.sleep(1.5)

    pyautogui.press("tab")
    time.sleep(1.5)

    pyautogui.press("f3")
    time.sleep(3)
