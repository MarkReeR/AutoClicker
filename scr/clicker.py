import pyautogui
import time
from threading import Thread, Event


class AutoClicker:
    def __init__(self):
        self.is_running = Event()
        self.click_thread = None

    def checker():
        pass

    def start_clicking(self, clicks_ps, mouse_button, clicks_interval, delay):
        self.delay = delay
        self.is_running.set()
        self.click_thread = Thread(target=self._click, args=(clicks_ps, mouse_button, clicks_interval))
        self.click_thread.start()

    def _click(self, clicks_ps, mouse_button, clicks_interval):
        self.delay_timer()
        while self.is_running.is_set():
            pyautogui.click(button=mouse_button, clicks=clicks_ps, interval=clicks_interval)


    def stop_clicking(self):
        self.is_running.clear()
        if self.click_thread and self.click_thread.is_alive():
            self.click_thread.join()

    def delay_timer(self):
        time.sleep(self.delay)

if __name__ == "__main__":
    auto_clicker = AutoClicker()
    auto_clicker.start_clicking(clicks_ps=1, mouse_button='left', clicks_interval=0.1, delay=3)
    time.sleep(10)
    auto_clicker.stop_clicking()