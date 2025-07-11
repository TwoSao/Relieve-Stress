import json
import random
import customtkinter as ctk
from ui.components.label import Label
from ui.components.buttons import Button
from ui.components.frame import Frame
from ui.style import get_color, get_font

class NotesView(Frame):
    def __init__(self, master, notes_file="data/notes.json", show_add_note=None, **kwargs):
        super().__init__(master, **kwargs)
        self.notes_file = notes_file
        self.notes = self.load_notes()
        self.filtered_notes = self.notes.copy()
        self.show_add_note = show_add_note

        # Настройка основного фрейма
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))

        # Панель управления
        self.control_buttons_frame = Frame(self, fg_color=get_color("COLOR_FRAME_BG"))
        self.control_buttons_frame.pack(fill="x", pady=(0, 10))


        # Панель категорий
        self.category_buttons_frame = Frame(self, fg_color=get_color("COLOR_FRAME_BG"))
        self.category_buttons_frame.pack(fill="x", pady=(0, 15))

        # Кнопки категорий
        self.categories = ["Все", "Поддержка", "Мотивация", "Отвлечение"]
        self.active_category = "Все"

        for cat in self.categories:
            btn = Button(
                self.category_buttons_frame,
                text=cat,
                command=lambda c=cat: self.filter_notes_by_category(c),
                fg_color=get_color("COLOR_ACCENT") if cat == self.active_category else get_color("COLOR_BUTTON_BG")
            )
            btn.pack(side="left", padx=5, expand=True, fill="x")

        # Отображение заметки
        self.note_frame = Frame(self, fg_color=get_color("COLOR_FRAME_BG"), corner_radius=8)
        self.note_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.note_display = Label(
            self.note_frame,
            text="Нажмите кнопку, чтобы показать случайную заметку",
            wraplength=400,
            font=get_font("FONT_NORMAL"),
            text_color=get_color("COLOR_TEXT_SECONDARY")
        )
        self.note_display.pack(pady=20, padx=20)

        # Кнопка показа заметки
        self.show_button = Button(
            self,
            text="Показать случайную заметку",
            command=self.show_random_note,
            fg_color=get_color("COLOR_BUTTON_BG"),
            hover_color=get_color("COLOR_BUTTON_HOVER")
        )
        self.show_button.pack(pady=10, padx=10, fill="x")

    def load_notes(self):
        """Загружает заметки из JSON-файла"""
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except Exception as e:
            print(f"Ошибка загрузки заметок: {e}")
            return []

    def refresh_notes(self):
        """Обновляет список заметок"""
        self.notes = self.load_notes()
        self.filtered_notes = self.notes.copy()
        self.show_random_note()

    def show_random_note(self):
        """Показывает случайную заметку из выбранной категории"""
        if not self.filtered_notes:
            self.note_display.configure(
                text="Нет заметок в выбранной категории.",
                text_color=get_color("COLOR_TEXT_SECONDARY")
            )
            return

        note = random.choice(self.filtered_notes)
        self.note_display.configure(
            text=note["text"],
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL")
        )

    def filter_notes_by_category(self, category):
        """Фильтрует заметки по категории"""
        self.active_category = category

        # Обновляем стиль кнопок категорий
        for btn in self.category_buttons_frame.winfo_children():
            btn.configure(
                fg_color=get_color("COLOR_ACCENT") if btn.cget("text") == category else get_color("COLOR_BUTTON_BG")
            )

        if category == "Все":
            self.filtered_notes = self.notes.copy()
        else:
            self.filtered_notes = [note for note in self.notes if note.get("category") == category]

        self.show_random_note()

    def update_theme(self):
        """Обновляет цвета при смене темы"""
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.control_buttons_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.category_buttons_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.note_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))

        self.note_display.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL")
        )

        self.show_button.update_theme()

        # Обновляем кнопки категорий
        for btn in self.category_buttons_frame.winfo_children():
            btn.configure(
                fg_color=get_color("COLOR_ACCENT") if btn.cget("text") == self.active_category else get_color("COLOR_BUTTON_BG"),
                text_color=get_color("COLOR_TEXT")
            )