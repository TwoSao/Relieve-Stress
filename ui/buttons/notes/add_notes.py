import json
import customtkinter as ctk
from ui.components.label import Label
from ui.components.buttons import Button
from ui.components.frame import Frame
from ui.style import get_color, get_font

class Add_Note(Frame):
    def __init__(self, master, notes_file="data/notes.json", on_note_added=None, **kwargs):
        super().__init__(master, **kwargs)
        self.notes_file = notes_file
        self.notes = self.load_notes()
        self.on_note_added = on_note_added

        # Настройка фрейма
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))

        # Заголовок
        self.label = Label(
            self,
            text="Введите заметку",
            font=get_font("FONT_NORMAL"),
            text_color=get_color("COLOR_TEXT")
        )
        self.label.pack(pady=10)

        # Поле для ввода текста
        self.textbox = ctk.CTkTextbox(
            self,
            height=100,
            fg_color=get_color("COLOR_INPUT_BG"),
            text_color=get_color("COLOR_TEXT"),
            border_color=get_color("COLOR_INPUT_BORDER"),
            border_width=1,
            font=get_font("FONT_NORMAL")
        )
        self.textbox.pack(pady=10, padx=10, fill="both", expand=True)

        # Выбор категории
        self.category_label = Label(
            self,
            text="Выберите категорию",
            font=get_font("FONT_SMALL"),
            text_color=get_color("COLOR_TEXT_SECONDARY")
        )
        self.category_label.pack(pady=(5, 2))

        self.category_option = ctk.CTkOptionMenu(
            self,
            values=["Поддержка", "Мотивация", "Отвлечение"],
            fg_color=get_color("COLOR_BUTTON_BG"),
            button_color=get_color("COLOR_BUTTON_BG"),
            button_hover_color=get_color("COLOR_BUTTON_HOVER"),
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_SMALL"),
            dropdown_font=get_font("FONT_SMALL")
        )
        self.category_option.pack(pady=5)

        # Кнопка сохранения
        self.save_button = Button(
            self,
            text="Сохранить заметку",
            command=self.save_note,
            highlight=True
        )
        self.save_button.pack(pady=20, padx=10, fill="x")

    def load_notes(self):
        """Загружает заметки из файла"""
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_note_to_file(self, text, category):
        """Сохраняет заметку в файл"""
        self.notes.append({
            "text": text,
            "category": category
        })
        with open(self.notes_file, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=4)

    def save_note(self):
        """Обрабатывает сохранение заметки"""
        note_text = self.textbox.get("0.0", "end").strip()
        category = self.category_option.get()

        if not note_text:
            self.label.configure(
                text="Пустая заметка не будет сохранена!",
                text_color=get_color("COLOR_ERROR")
            )
            return

        try:
            self.save_note_to_file(note_text, category)
            self.textbox.delete("0.0", "end")
            self.label.configure(
                text="Заметка успешно сохранена!",
                text_color=get_color("COLOR_SUCCESS")
            )

            if self.on_note_added:
                self.on_note_added()

        except Exception as e:
            self.label.configure(
                text=f"Ошибка при сохранении: {str(e)}",
                text_color=get_color("COLOR_ERROR")
            )

    def update_theme(self):
        """Обновляет цвета при смене темы"""
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))

        self.label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL")
        )

        self.category_label.configure(
            text_color=get_color("COLOR_TEXT_SECONDARY"),
            font=get_font("FONT_SMALL")
        )

        self.textbox.configure(
            fg_color=get_color("COLOR_INPUT_BG"),
            text_color=get_color("COLOR_TEXT"),
            border_color=get_color("COLOR_INPUT_BORDER")
        )

        self.category_option.configure(
            fg_color=get_color("COLOR_BUTTON_BG"),
            button_color=get_color("COLOR_BUTTON_BG"),
            button_hover_color=get_color("COLOR_BUTTON_HOVER"),
            text_color=get_color("COLOR_TEXT")
        )

        self.save_button.update_theme()