from customtkinter import CTkSlider

class Slider(CTkSlider):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, command=command, **kwargs)
