# ui/button.py
from customtkinter import CTkButton

class Button(CTkButton):
    def __init__(self, master, text="", command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)

    def set_text(self, text):
        self.configure(text=text)
