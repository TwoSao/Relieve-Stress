from customtkinter import CTkCheckBox

class Checkbox(CTkCheckBox):
    def __init__(self, master, text="", command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
