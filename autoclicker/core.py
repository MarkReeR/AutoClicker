# autoclicker/core.py

import time
import pyautogui
from threading import Thread, Event

class AutoClicker:
    def __init__(self):
        self._is_running = Event()
        self._thread = None

    def start(self, clicks=1, interval=0.01, button='left', delay=3):
        self._is_running.set()
        self._thread = Thread(
            target=self._click_loop,
            args=(clicks, interval, button.lower(), delay),
            daemon=True
        )
        self._thread.start()

    def stop(self):
        self._is_running.clear()
        if self._thread and self._thread.is_alive():
            self._thread.join()

    def _click_loop(self, clicks, interval, button, delay):
        time.sleep(delay)
        while self._is_running.is_set():
            pyautogui.click(button=button, clicks=clicks, interval=interval)
