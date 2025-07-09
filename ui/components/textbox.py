from customtkinter import CTkTextbox

class Textbox(CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def set(self, text):
        self.delete("0.0", "end")
        self.insert("0.0", text)
