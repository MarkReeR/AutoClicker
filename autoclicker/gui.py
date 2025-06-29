# autoclicker/gui.py

import customtkinter
import keyboard
from tkinter import simpledialog
from autoclicker.utils import (
    toggle_clicking, stop_clicking, on_close,
    get_preset_names, get_active_preset, set_active_preset,
    load_config, add_preset
)
from autoclicker.spinbox import FloatSpinbox


class AutoClickerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("AutoClicker")
        self.geometry("340x460")
        self.resizable(False, False)

        self.is_clicking = False

        # main button
        self.button = customtkinter.CTkButton(self, text="Start", command=self.toggle_clicking)
        self.button.pack(pady=10)

        # Кнопка мыши
        self.label_mouse = customtkinter.CTkLabel(self, text="Кнопка мыши")
        self.label_mouse.pack()
        self.button_choice = customtkinter.CTkComboBox(self, values=["left", "middle", "right"])
        self.button_choice.set("left")
        self.button_choice.pack(pady=5)

        # Количество кликов
        self.label_clicks = customtkinter.CTkLabel(self, text="Количество кликов за раз")
        self.label_clicks.pack()
        self.clicks_spinbox = FloatSpinbox(self, step_size=1)
        self.clicks_spinbox.set(1)
        self.clicks_spinbox.pack(pady=5)

        # Интервал
        self.label_interval = customtkinter.CTkLabel(self, text="Интервал между кликами (сек)")
        self.label_interval.pack()
        self.interval_spinbox = FloatSpinbox(self, step_size=0.001)
        self.interval_spinbox.set(0.01)
        self.interval_spinbox.pack(pady=5)

        # Задержка
        self.label_delay = customtkinter.CTkLabel(self, text="Задержка перед стартом (сек)")
        self.label_delay.pack()
        self.delay_spinbox = FloatSpinbox(self, step_size=0.5)
        self.delay_spinbox.set(3)
        self.delay_spinbox.pack(pady=5)

        # Пресеты
        self.label_preset = customtkinter.CTkLabel(self, text="Выбор пресета")
        self.label_preset.pack()
        self.preset_menu = customtkinter.CTkComboBox(self, values=get_preset_names(), command=self.apply_preset)
        self.preset_menu.set(get_active_preset()["name"] if "name" in get_active_preset() else "default")
        self.preset_menu.pack(pady=10)

        self.save_button = customtkinter.CTkButton(self, text="Сохранить как пресет", command=self.save_preset)
        self.save_button.pack(pady=(10, 5))

        self.apply_preset(self.preset_menu.get())

        keyboard.add_hotkey('num 0', lambda: self.toggle_clicking())
        keyboard.add_hotkey('esc', lambda: self.stop_clicking())
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        

    def toggle_clicking(self):
        toggle_clicking(
            get_clicks=self.clicks_spinbox.get,
            get_interval=self.interval_spinbox.get,
            get_delay=self.delay_spinbox.get,
            get_button=self.button_choice.get,
            set_button_text=self.set_button_text
        )

    def stop_clicking(self):
        stop_clicking(self.set_button_text)

    def on_close(self):
        on_close(self.set_button_text, self.destroy)

    def set_button_text(self, text, color):
        self.button.configure(text=text, fg_color=color)

    def apply_preset(self, preset_name):
        data = load_config()
        preset = data["presets"].get(preset_name, {})
        self.clicks_spinbox.set(preset.get("clicks", 1))
        self.interval_spinbox.set(preset.get("interval", 0.01))
        self.delay_spinbox.set(preset.get("delay", 3))
        set_active_preset(preset_name)

    def save_preset(self):
        name = simpledialog.askstring("Сохранить пресет", "Введите имя пресета:")
        if name:
            try:
                add_preset(
                    name,
                    clicks=self.clicks_spinbox.get(),
                    interval=self.interval_spinbox.get(),
                    delay=self.delay_spinbox.get()
                )
                self.preset_menu.configure(values=get_preset_names())
                self.preset_menu.set(name)
            except ValueError as e:
                print(f"[Ошибка] {e}")
