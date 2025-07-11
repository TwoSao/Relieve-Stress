import json
import customtkinter as ctk
from ui.components.frame import Frame
from ui.components.label import Label
from ui.components.buttons import Button
from ui.style import CURRENT_THEME  # Добавляем импорт CURRENT_THEME

class ManageNotes(Frame):
    def __init__(self, master, notes_file="data/notes.json", on_update=None, on_add_note=None, **kwargs):
        super().__init__(master, **kwargs)
        self.notes_file = notes_file
        self.notes = self.load_notes()
        self.filtered_notes = []
        self.on_update = on_update
        self.on_add_note = on_add_note
        self.mode = None  # 'delete' или 'edit'

        # Устанавливаем цвет фона согласно текущей теме
        self.configure(fg_color=CURRENT_THEME["COLOR_FRAME_BG"])

        # Верхняя панель с кнопками
        self.mode_frame = Frame(self, fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.mode_frame.pack(fill="x", pady=5)

        self.btn_add_note = Button(
            self.mode_frame,
            text="➕ Добавить",
            command=self.open_add_note,
            fg_color=CURRENT_THEME["COLOR_BUTTON_BG"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.btn_add_note.pack(side="left", padx=5)

        self.btn_delete_mode = Button(
            self.mode_frame,
            text="🗑️ Удалить",
            command=self.set_delete_mode,
            fg_color=CURRENT_THEME["COLOR_BUTTON_BG"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.btn_delete_mode.pack(side="left", padx=5)

        self.btn_edit_mode = Button(
            self.mode_frame,
            text="✏️ Изменить",
            command=self.set_edit_mode,
            fg_color=CURRENT_THEME["COLOR_BUTTON_BG"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.btn_edit_mode.pack(side="left", padx=5)

        # Панель выбора категории
        self.category_frame = Frame(self, fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.category_frame.pack(fill="x", pady=5)

        self.categories = ["Поддержка", "Мотивация", "Отвлечение"]
        self.selected_category = None

        for cat in self.categories:
            btn = Button(
                self.category_frame,
                text=cat,
                command=lambda c=cat: self.select_category(c),
                fg_color=CURRENT_THEME["COLOR_BUTTON_BG"],
                text_color=CURRENT_THEME["COLOR_TEXT"]
            )
            btn.pack(side="left", padx=5)

        # Панель списка заметок
        self.notes_list_frame = Frame(self, fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.notes_list_frame.pack(fill="both", expand=True, pady=10)

        # Редактирование текста
        self.edit_frame = Frame(self, fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.edit_label = Label(
            self.edit_frame,
            text="Редактировать заметку:",
            font=CURRENT_THEME["FONT_NORMAL"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.edit_label.pack(pady=5)

        self.textbox = ctk.CTkTextbox(
            self.edit_frame,
            height=100,
            fg_color=CURRENT_THEME["COLOR_FRAME_BG"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.textbox.pack(padx=10, pady=5, fill="both", expand=True)

        self.save_edit_button = Button(
            self.edit_frame,
            text="Сохранить изменения",
            command=self.save_edit,
            fg_color=CURRENT_THEME["COLOR_BUTTON_BG"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.save_edit_button.pack(pady=10)

        # Статус
        self.status_label = Label(
            self,
            text="",
            font=CURRENT_THEME["FONT_NORMAL"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.status_label.pack(pady=5)

        self.current_edit_index = None

    def load_notes(self):
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_notes(self):
        with open(self.notes_file, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=4)

    def clear_notes_list(self):
        for widget in self.notes_list_frame.winfo_children():
            widget.destroy()
        self.edit_frame.pack_forget()
        self.status_label.configure(text="")

    def set_delete_mode(self):
        self.mode = "delete"
        self.status_label.configure(
            text="Режим удаления: выберите категорию и заметку для удаления.",
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.edit_frame.pack_forget()
        self.clear_notes_list()
        self.reset_mode_buttons()
        self.btn_delete_mode.configure(fg_color="#d9534f")
        if self.selected_category:
            self.show_notes_list(self.selected_category)

    def set_edit_mode(self):
        self.mode = "edit"
        self.status_label.configure(
            text="Режим редактирования: выберите категорию и заметку для редактирования.",
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.edit_frame.pack_forget()
        self.clear_notes_list()
        self.reset_mode_buttons()
        self.btn_edit_mode.configure(fg_color="#5bc0de")
        if self.selected_category:
            self.show_notes_list(self.selected_category)

    def select_category(self, category):
        self.selected_category = category
        self.status_label.configure(
            text=f"Выбрана категория: {category}",
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.edit_frame.pack_forget()
        self.clear_notes_list()
        self.show_notes_list(category)

    def show_notes_list(self, category):
        self.filtered_notes = [note for note in self.notes if note.get("category") == category]

        if not self.filtered_notes:
            self.status_label.configure(
                text="Заметок в этой категории нет.",
                text_color=CURRENT_THEME["COLOR_TEXT"]
            )
            return

        for idx, note in enumerate(self.filtered_notes):
            btn = Button(
                self.notes_list_frame,
                text=note["text"][:40] + ("..." if len(note["text"]) > 40 else ""),
                command=lambda i=idx: self.note_action(i),
                fg_color=CURRENT_THEME["COLOR_BUTTON_BG"],
                text_color=CURRENT_THEME["COLOR_TEXT"]
            )
            btn.pack(fill="x", padx=10, pady=3)

    def note_action(self, index):
        if self.mode == "delete":
            real_index = self.notes.index(self.filtered_notes[index])
            del self.notes[real_index]
            self.save_notes()
            self.status_label.configure(
                text="Заметка удалена.",
                text_color=CURRENT_THEME["COLOR_TEXT"]
            )
            self.clear_notes_list()
            self.show_notes_list(self.selected_category)
            if self.on_update:
                self.on_update()

        elif self.mode == "edit":
            self.current_edit_index = self.notes.index(self.filtered_notes[index])
            note = self.notes[self.current_edit_index]
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", note["text"])
            self.edit_frame.pack(fill="both", padx=10, pady=10)
            self.status_label.configure(
                text="Редактирование заметки. Внесите изменения и нажмите сохранить.",
                text_color=CURRENT_THEME["COLOR_TEXT"]
            )

    def save_edit(self):
        new_text = self.textbox.get("0.0", "end").strip()
        if not new_text:
            self.status_label.configure(
                text="Заметка не может быть пустой!",
                text_color=CURRENT_THEME["COLOR_TEXT"]
            )
            return
        self.notes[self.current_edit_index]["text"] = new_text
        self.save_notes()
        self.status_label.configure(
            text="Заметка успешно обновлена.",
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )
        self.edit_frame.pack_forget()
        self.clear_notes_list()
        self.show_notes_list(self.selected_category)
        if self.on_update:
            self.on_update()

    def reset_mode_buttons(self):
        self.btn_delete_mode.configure(fg_color=CURRENT_THEME["COLOR_BUTTON_BG"])
        self.btn_edit_mode.configure(fg_color=CURRENT_THEME["COLOR_BUTTON_BG"])

    def open_add_note(self):
        if self.on_add_note:
            self.on_add_note()

    def refresh(self):
        self.notes = self.load_notes()
        self.clear_notes_list()

        # Показать заново, если категория уже выбрана
        if self.selected_category:
            self.show_notes_list(self.selected_category)

    def update_theme(self):
        """Метод для обновления цветов при смене темы"""
        self.configure(fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.mode_frame.configure(fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.category_frame.configure(fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.notes_list_frame.configure(fg_color=CURRENT_THEME["COLOR_FRAME_BG"])
        self.edit_frame.configure(fg_color=CURRENT_THEME["COLOR_FRAME_BG"])

        self.edit_label.configure(text_color=CURRENT_THEME["COLOR_TEXT"])
        self.status_label.configure(text_color=CURRENT_THEME["COLOR_TEXT"])

        self.textbox.configure(
            fg_color=CURRENT_THEME["COLOR_FRAME_BG"],
            text_color=CURRENT_THEME["COLOR_TEXT"]
        )

        for btn in [
                       self.btn_add_note, self.btn_delete_mode, self.btn_edit_mode,
                       self.save_edit_button
                   ] + self.category_frame.winfo_children():
            btn.configure(
                fg_color=CURRENT_THEME["COLOR_BUTTON_BG"],
                text_color=CURRENT_THEME["COLOR_TEXT"]
            )