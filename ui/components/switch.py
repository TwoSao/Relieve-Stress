from customtkinter import CTkSwitch

class Switch(CTkSwitch):
    def __init__(self, master, text="", command=None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
