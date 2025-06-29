# autoclicker/utils.py
import json
from pathlib import Path
from autoclicker.core import AutoClicker

clicker = AutoClicker()

CONFIG_PATH = Path(__file__).parent / "config.json"
is_clicking = False


def toggle_clicking(get_clicks, get_interval, get_delay, get_button, set_button_text):
    global is_clicking
    if is_clicking:
        stop_clicking(set_button_text)
    else:
        start_clicking(get_clicks, get_interval, get_delay, get_button, set_button_text)


def start_clicking(get_clicks, get_interval, get_delay, get_button, set_button_text):
    global is_clicking
    try:
        clicks = int(get_clicks())
        interval = float(get_interval())
        delay = float(get_delay())
        button = get_button().lower()

        if not (1 <= clicks <= 100):
            raise ValueError("Кликов должно быть от 1 до 100.")
        if not (0.001 <= interval <= 1.0):
            raise ValueError("Интервал от 0.001 до 1.0 сек.")
        if not (0 <= delay <= 30):
            raise ValueError("Задержка от 0 до 30 сек.")

    except ValueError as e:
        print(f"[Ошибка] {e}")
        return

    clicker.start(clicks, interval, button, delay)
    set_button_text("Stop", "red")
    is_clicking = True


def stop_clicking(set_button_text):
    global is_clicking
    clicker.stop()
    set_button_text("Start", "green")
    is_clicking = False


def on_close(set_button_text, destroy_callback):
    stop_clicking(set_button_text)
    destroy_callback()
    

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config.json not найден.")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_active_preset():
    data = load_config()
    active = data.get("active_preset", "default")
    return data["presets"].get(active, data["presets"]["default"])


def add_preset(name, clicks, interval, delay):
    data = load_config()
    if name in data["presets"]:
        raise ValueError("Пресет с таким именем уже существует.")
    data["presets"][name] = {
        "clicks": clicks,
        "interval": interval,
        "delay": delay
    }
    save_config(data)


def set_active_preset(name):
    data = load_config()
    if name in data["presets"]:
        data["active_preset"] = name
        save_config(data)
        return True
    return False


def get_preset_names():
    return list(load_config().get("presets", {}).keys())