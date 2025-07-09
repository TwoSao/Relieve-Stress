# ui/base_widget.py
import customtkinter as ctk

class BaseWidget:
    def __init__(self, master, **kwargs):
        self.master = master
        self.options = kwargs
