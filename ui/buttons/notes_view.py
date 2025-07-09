import json
import random
import customtkinter as ctk
from ui.components.label import Label
from ui.components.buttons import Button
from ui.components.frame import Frame

class NotesView(ctk.CTkFrame):
    def __init__(self, master, notes_file="data/notes.json", **kwargs):
        super().__init__(master, **kwargs)
        self.notes_file = notes_file
        self.notes = self.load_notes()

        self.category_var = ctk.StringVar(value="поддержка")  # default category

        # Категории — кнопки сверху
        self.categories_frame = Frame(self, fg_color="#333333")
        self.categories_frame.pack(fill="x", pady=10)

        for category in ["поддержка", "мотивация", "отвлечение"]:
            btn = Button(self.categories_frame, text=category.capitalize(),
                         command=lambda c=category: self.change_category(c))
            btn.pack(side="left", padx=5)

        self.note_display = Label(self, text="", wraplength=450, font=("Arial", 14))
        self.note_display.pack(pady=15)

        self.show_button = Button(self, text="Показать случайную заметку", command=self.show_random_note)
        self.show_button.pack(pady=10)

        self.change_category(self.category_var.get())  # отобразить текущую категорию

    def load_notes(self):
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def change_category(self, category):
        self.category_var.set(category)
        self.note_display.configure(text=f"Категория: {category.capitalize()}")

    def show_random_note(self):
        filtered_notes = [n for n in self.notes if n.get("category") == self.category_var.get()]
        if not filtered_notes:
            self.note_display.configure(text="В выбранной категории нет заметок.")
            return
        note = random.choice(filtered_notes)
        self.note_display.configure(text=note["text"])

    def refresh_notes(self):
        self.notes = self.load_notes()
