import customtkinter as ctk
from ui.style import get_color

class Frame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        if "fg_color" not in kwargs:
            kwargs["fg_color"] = get_color("COLOR_FRAME_BG")
        super().__init__(master, **kwargs)
    
    def update_theme(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))