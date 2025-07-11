import customtkinter as ctk
from ui.style import get_color, get_font

class Label(ctk.CTkLabel):
    def __init__(self, master, **kwargs):
        if "text_color" not in kwargs:
            kwargs["text_color"] = get_color("COLOR_TEXT")
        if "font" not in kwargs:
            kwargs["font"] = get_font("FONT_MAIN")
        super().__init__(master, **kwargs)
