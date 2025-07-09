# ui/entry.py
from customtkinter import CTkEntry

class Entry(CTkEntry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def set(self, text):
        self.delete(0, 'end')
        self.insert(0, text)
