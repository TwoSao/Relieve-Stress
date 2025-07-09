from customtkinter import CTkLabel
from ui.components.base_widget import BaseWidget

class Label(BaseWidget):
    def __init__(self, master, text="", **kwargs):
        super().__init__(master, **kwargs)
        self.label = CTkLabel(master, text=text, **kwargs)

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def grid(self, **kwargs):
        self.label.grid(**kwargs)

    def place(self, **kwargs):
        self.label.place(**kwargs)

    def set(self, text):
        self.label.configure(text=text)

    def get(self):
        return self.label.cget("text")
    def configure(self, text):
        self.label.configure(text=text)