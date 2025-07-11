import customtkinter as ctk
from ui.components.frame import Frame
from ui.components.label import Label
from ui.components.buttons import Button
from ui.buttons.notes.notes_view import NotesView
from ui.buttons.notes.add_notes import Add_Note
from ui.buttons.notes.manage_notes import ManageNotes
from ui.style import set_theme, get_color, get_font
from ui.assistant.view import AssistantView
from ui.assistant.logic import AssistantLogic

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()



        # Инициализация темы
        self.current_theme_name = "light"
        set_theme(self.current_theme_name)


        # Настройка главного окна
        self.title("Relieve Stress")
        self.geometry("1200x960")
        self.minsize(700, 850)
        self.configure(fg_color=get_color("COLOR_BG"))
        self.iconbitmap(self,"assets/icon.ico")
        # Сначала создаем основные фреймы
        self._create_widgets()

        # Затем инициализируем представления
        self._init_views()

        # Показываем начальное представление
        self.show_notes()
        # Инициализация ассистента
        self.assistant_logic = AssistantLogic(api_key="API_KEY")
        self.assistant_view = AssistantView(
            self.content_frame,
            on_send_message=self.assistant_logic.get_response
        )
        # Центрируем окно
        self.center_window()

    def _create_widgets(self):
        """Создает основные элементы интерфейса"""
        # Заголовок
        self.title_label = Label(
            self,
            text="Relieve Stress",
            font=get_font("FONT_TITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.title_label.pack(pady=(20, 15))

        # Панель кнопок
        self.buttons_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=8
        )
        self.buttons_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Кнопки навигации
        self.btn_show_notes = Button(
            self.buttons_frame,
            text="Показать заметки",
            command=self.show_notes
        )
        self.btn_show_notes.pack(side="left", padx=10, pady=5)

        self.btn_manage_notes = Button(
            self.buttons_frame,
            text="Управление заметками",
            command=self.show_manage_notes
        )
        self.btn_manage_notes.pack(side="left", padx=10, pady=5)

        # Кнопка смены темы
        self.theme_toggle_btn = Button(
            self.buttons_frame,
            text="🌙" if self.current_theme_name == "light" else "☀️",
            command=self.toggle_theme,
            width=40
        )
        self.theme_toggle_btn.pack(side="left", padx=10, pady=5)

        # Кнопка выхода
        self.exit_button = Button(
            self.buttons_frame,
            text="Выход",
            command=self.destroy
        )
        self.exit_button.pack(side="right", padx=10, pady=5)

        self.btn_assistant = Button(
            self.buttons_frame,
            text="AI",
            command=self.show_assistant,
            fg_color=get_color("COLOR_ACCENT")
        )
        self.btn_assistant.pack(side="left", padx=10, pady=5)

    # Основная область контента (теперь создается до представлений)
        self.content_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=8
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _init_views(self):
        """Инициализирует все представления"""
        self.notes_view = NotesView(
            self.content_frame,
            show_add_note=self.show_add_note
        )
        self.add_note_view = Add_Note(
            self.content_frame,
            on_note_added=self.on_note_added
        )
        self.manage_notes_view = ManageNotes(
            self.content_frame,
            on_update=self.on_notes_updated,
            on_add_note=self.show_add_note
        )

    # Остальные методы остаются без изменений...
    def center_window(self):
        """Центрирует окно на экране"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_theme(self):
        """Переключает тему между светлой и темной"""
        self.current_theme_name = "dark" if self.current_theme_name == "light" else "light"
        set_theme(self.current_theme_name)

        # Обновляем иконку кнопки темы
        self.theme_toggle_btn.configure(
            text="🌙" if self.current_theme_name == "light" else "☀️"
        )

        # Обновляем основные цвета
        self.configure(fg_color=get_color("COLOR_BG"))
        self.buttons_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.content_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))

        # Обновляем заголовок
        self.title_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_TITLE")
        )

        # Обновляем кнопки
        buttons = [
            self.btn_show_notes,
            self.btn_manage_notes,
            self.theme_toggle_btn,
            self.exit_button,
            self.btn_assistant
        ]

        for btn in buttons:
            btn.update_theme()

        # Обновляем представления
        self.notes_view.update_theme()
        self.add_note_view.update_theme()
        self.manage_notes_view.update_theme()
        self.assistant_view.update_theme()

    def clear_content(self):
        """Очищает область контента"""
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

    def show_notes(self):
        """Показывает представление с заметками"""
        self.clear_content()
        self.notes_view.pack(fill="both", expand=True, padx=10, pady=10)

    def show_add_note(self):
        """Показывает форму добавления заметки"""
        self.clear_content()
        self.add_note_view.pack(fill="both", expand=True, padx=10, pady=10)

    def on_note_added(self):
        """Обработчик добавления новой заметки"""
        self.notes_view.refresh_notes()
        self.add_note_view.notes = self.notes_view.notes
        self.manage_notes_view.refresh()
        self.show_manage_notes()
        self.manage_notes_view.status_label.configure(
            text="Заметка добавлена! Выберите категорию для управления.",
            text_color=get_color("COLOR_SUCCESS")
        )

    def show_manage_notes(self):
        """Показывает представление управления заметками"""
        self.clear_content()
        self.manage_notes_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.manage_notes_view.refresh()

    def on_notes_updated(self):
        """Обработчик обновления заметок"""
        self.notes_view.refresh_notes()
        self.add_note_view.notes = self.notes_view.notes
        self.show_notes()

    def show_assistant(self):
        """Показывает интерфейс ассистента"""
        self.clear_content()
        self.assistant_view.pack(fill="both", expand=True, padx=10, pady=10)
