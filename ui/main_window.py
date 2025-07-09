import customtkinter as ctk
from ui.components.frame import Frame
from ui.components.label import Label
from ui.components.buttons import Button
from ui.buttons.notes_view import NotesView
from ui.buttons.add_notes import Add_Note

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Relieve Stress")
        self.geometry("600x480")
        self.configure(fg_color="#1E1E1E")

        self.title_label = Label(self, text="Relieve Stress", font=("Arial", 20))
        self.title_label.pack(pady=15)

        self.buttons_frame = Frame(self, fg_color="#2B2B2B")
        self.buttons_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.btn_show_notes = Button(self.buttons_frame, text="Показать заметки", command=self.show_notes)
        self.btn_show_notes.pack(side="left", padx=10, pady=10)

        self.btn_add_note = Button(self.buttons_frame, text="Добавить заметку", command=self.show_add_note)
        self.btn_add_note.pack(side="left", padx=10, pady=10)

        self.exit_button = Button(self.buttons_frame, text="Выход", command=self.destroy)
        self.exit_button.pack(side="right", padx=10, pady=10)

        self.content_frame = Frame(self, fg_color="#2B2B2B")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Создаем views
        self.notes_view = NotesView(self.content_frame)
        self.add_note_view = Add_Note(self.content_frame, on_note_added=self.on_note_added)

        self.show_notes()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

    def show_notes(self):
        self.clear_content()
        self.notes_view.pack(fill="both", expand=True)

    def show_add_note(self):
        self.clear_content()
        self.add_note_view.pack(fill="both", expand=True)

    def on_note_added(self):
        # Обновляем заметки в notes_view
        self.notes_view.refresh_notes()
        # Переключаем на просмотр заметок сразу после добавления
        self.show_notes()
        # Отобразим сообщение
        self.notes_view.note_display.configure(text="Заметка добавлена! Выберите категорию.")
