import json
import customtkinter as ctk
from ui.components.label import Label
from ui.components.buttons import Button
from ui.components.frame import Frame

class Add_Note(ctk.CTkFrame):
    def __init__(self, master, notes_file="data/notes.json", on_note_added=None, **kwargs):
        super().__init__(master, **kwargs)
        self.notes_file = notes_file
        self.notes = self.load_notes()
        self.on_note_added = on_note_added

        self.category_var = ctk.StringVar(value="поддержка")

        Label(self, text="Введите свою заметку", font=("Arial", 14)).pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, height=100)
        self.textbox.pack(pady=10, padx=10, fill="both", expand=True)

        category_frame = Frame(self, fg_color="#333333")
        category_frame.pack(pady=10)

        for category in ["поддержка", "мотивация", "отвлечение"]:
            rb = ctk.CTkRadioButton(category_frame, text=category.capitalize(), variable=self.category_var, value=category)
            rb.pack(side="left", padx=10)

        self.message_label = Label(self, text="", font=("Arial", 12))
        self.message_label.pack()

        save_button = Button(self, text="Сохранить", command=self.save_note)
        save_button.pack(pady=10)

    def load_notes(self):
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_note(self):
        note_text = self.textbox.get("0.0", "end").strip()
        category = self.category_var.get()
        if note_text:
            self.notes.append({"text": note_text, "category": category})
            with open(self.notes_file, "w", encoding="utf-8") as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=4)
            self.message_label.configure(text="Заметка добавлена!")
            self.textbox.delete("0.0", "end")  # очистить поле

            if self.on_note_added:
                self.on_note_added()
        else:
            self.message_label.configure(text="Пустая заметка не будет сохранена.")
