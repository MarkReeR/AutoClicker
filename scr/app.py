import customtkinter
import keyboard
from clicker import AutoClicker


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.auto_clicker = AutoClicker()

        # Bind the escape key to stop the clicking
        keyboard.add_hotkey('esc', self.stop_clicking)


        # Window size
        self.WIDTH = 315
        self.HEIGHT = 440

        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.iconbitmap(".\\assets\\icon.ico")
        self.title("AutoClicker")

        # Decor
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")

        # Debug
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(5, weight=1)

        self.title = customtkinter.CTkLabel(
            master=self.frame, text="AutoClicker", font=("Roboto Medium", -16)
        )
        self.title.grid(row=0, column=1, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.start_button = customtkinter.CTkButton(
            master=self.frame, 
            text="START",
            font=("Roboto Medium", -16),
            state="normal",
            command=self.toggle_clicking           
            )
        
        self.start_button.grid(row=1, column=1, padx=(20,20), sticky="ew")

        self.lable_info = customtkinter.CTkLabel(
            master=self.frame,
            text="(Press ESC to stop)",
            font=("Roboto Medium", -10),
            text_color="grey"
        )
        self.lable_info.grid(row=2, column=1, padx=20)
    

        self.settings_frame = customtkinter.CTkFrame(master=self.frame)
        self.settings_frame.grid(row=3, column=1, sticky="nsew", padx=20, pady=(0,20))
        self.settings_frame.grid_columnconfigure(1, weight=1)

        # clicks per millisecond
        self.lable_amount_clicks_per_millisecond = customtkinter.CTkLabel(
            master=self.settings_frame,
            font=("Roboto Medium", -14),
            text="Clicks per mS:"
        )
        self.lable_amount_clicks_per_millisecond.grid(row=0, column=1, padx=(40,40), pady=(5,0))

        self.entry_clicks_per_millisecond_var = customtkinter.StringVar(
            master=self.frame, value=str(1)
        )

        self.entry_clicks_per_millisecond = customtkinter.CTkEntry(
            master=self.settings_frame,
            width=140,
            font=("Roboto Medium", -12),
            textvariable=self.entry_clicks_per_millisecond_var,
        )
        self.entry_clicks_per_millisecond.grid(row=1, column=1, padx=(40,40), pady=(0,10))


        # mouse button selection
        self.lable_mouse_button_selection = customtkinter.CTkLabel(
            master=self.settings_frame,
            font=("Roboto Medium", -14),
            text="Mouse button:"
        )
        self.lable_mouse_button_selection.grid(row=2, column=1, padx=(40,40))

        self.combobox_mouse_button_selection_var = customtkinter.StringVar(value='LEFT')
        
        self.combobox_mouse_button_selection = customtkinter.CTkComboBox(
            master=self.settings_frame,
            font=("Roboto Medium", -12),
            width=140,
            values=['LEFT', 'MIDDLE', 'RIGHT'],
            variable=self.combobox_mouse_button_selection_var,
        )
        self.combobox_mouse_button_selection.grid(row=3, column=1, padx=(40,40), pady=(0,10))

        # clicks interval
        self.lable_clicks_interval = customtkinter.CTkLabel(
            master=self.settings_frame,
            font=("Roboto Medium", -14),
            text="Interval:"
        )
        self.lable_clicks_interval.grid(row=4, column=1, padx=(40,40))

        self.entry_clicks_interval_var = customtkinter.StringVar(
            master=self.settings_frame, value=str(0.01)
        )

        self.entry_clicks_interval = customtkinter.CTkEntry(
            master=self.settings_frame,
            width=140,
            font=("Roboto Medium", -12),
            textvariable=self.entry_clicks_interval_var
        )
        self.entry_clicks_interval.grid(row=5, column=1, padx=(40,40), pady=(0,10))

        # start delay
        self.lable_start_delay = customtkinter.CTkLabel(
            master=self.settings_frame,
            font=("Roboto Medium", -14),
            text="Start delay:"
        )
        self.lable_start_delay.grid(row=6, column=1, padx=(40,40))

        self.entry_start_delay_var = customtkinter.StringVar(
            master=self.settings_frame, value=str(3)
        )

        self.entry_start_delay = customtkinter.CTkEntry(
            master=self.settings_frame,
            width=140,
            font=("Roboto Medium", -12),
            textvariable=self.entry_start_delay_var
        )
        self.entry_start_delay.grid(row=7, column=1, padx=(40,40), pady=(0,10))

    def toggle_clicking(self):
        if self.auto_clicker.is_running.is_set():
            self.stop_clicking()
        else:
            self.start_clicking_thread()

    def start_clicking_thread(self):
        clicks_ps = int(self.entry_clicks_per_millisecond.get())
        mouse_button = self.combobox_mouse_button_selection.get()
        clicks_interval = float(self.entry_clicks_interval.get())
        delay = int(self.entry_start_delay.get())

        self.auto_clicker.start_clicking(clicks_ps, mouse_button, clicks_interval, delay)
        self.start_button.configure(text="STOP", fg_color="red", hover_color="darkred")

    def stop_clicking(self):
        self.auto_clicker.stop_clicking()
        self.start_button.configure(text="START", fg_color="green", hover_color="darkgreen")
    
    def on_close(self):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__=="__main__":
    app = App()
    app.update()
    app.start()