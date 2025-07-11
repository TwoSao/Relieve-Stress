import customtkinter as ctk
from ui.components.frame import Frame
from ui.components.label import Label
from ui.components.buttons import Button
from ui.buttons.notes.notes_view import NotesView
from ui.buttons.notes.add_notes import Add_Note
from ui.buttons.notes.manage_notes import ManageNotes
from ui.style import set_theme, get_color, get_font


# Новые импорты
from ui.themes.theme_manager import ThemeManager
from ui.animations.transitions import AnimationManager
from ui.widgets.enhanced_button import EnhancedButton
from core.services.note_service import NoteService
from config.settings import SettingsManager

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Инициализация сервисов
        self.settings_manager = SettingsManager()
        self.note_service = NoteService()
        self.animation_manager = AnimationManager()
        
        # Инициализация темы
        self.current_theme_name = self.settings_manager.get('theme', 'light')
        set_theme(self.current_theme_name)
        ThemeManager.add_observer(self.on_theme_changed)
        
        # Принудительно применяем тему после создания всех виджетов
        self.after(100, self.on_theme_changed)  # Задержка для корректной инициализации


        # Настройка главного окна
        self.title("Relieve Stress")
        width = self.settings_manager.get('window_width', 1200)
        height = self.settings_manager.get('window_height', 960)
        self.geometry(f"{width}x{height}")
        self.minsize(700, 850)
        self.configure(fg_color=get_color("COLOR_BG"))
        self.iconbitmap(self,"assets/icon.ico")
        # Сначала создаем основные фреймы
        self._create_widgets()

        # Затем инициализируем представления
        self._init_views()

        # Показываем начальное представление
        self.show_notes()

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
        self.btn_show_notes = EnhancedButton(
            self.buttons_frame,
            text="Показать заметки",
            command=self.show_notes,
            hover_animation=True
        )
        self.btn_show_notes.pack(side="left", padx=10, pady=5)

        self.btn_manage_notes = EnhancedButton(
            self.buttons_frame,
            text="Управление заметками",
            command=self.show_manage_notes,
            hover_animation=True
        )
        self.btn_manage_notes.pack(side="left", padx=10, pady=5)

        # Кнопка колеса эмоций
        self.btn_emotion_wheel = EnhancedButton(
            self.buttons_frame,
            text="Колесо эмоций",
            command=self.show_emotion_wheel,
            hover_animation=True
        )
        self.btn_emotion_wheel.pack(side="left", padx=10, pady=5)

        # Кнопка смены темы
        self.theme_toggle_btn = EnhancedButton(
            self.buttons_frame,
            text="🌙" if self.current_theme_name == "light" else "☀️",
            command=self.toggle_theme,
            width=40,
            hover_animation=True
        )
        self.theme_toggle_btn.pack(side="left", padx=10, pady=5)

        # Кнопка выхода
        self.exit_button = EnhancedButton(
            self.buttons_frame,
            text="Выход",
            command=self.on_exit,
            hover_animation=True
        )
        self.exit_button.pack(side="right", padx=10, pady=5)



    # Основная область контента (теперь создается до представлений)
        self.content_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=8
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _init_views(self):
        """Инициализирует все представления"""
        # Изначально никаких представлений нет
        self.current_view = None
        self.notes_view = None
        self.add_note_view = None
        self.manage_notes_view = None
        self.emotion_wheel_view = None

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
        self.settings_manager.set('theme', self.current_theme_name)
        
        # Обновляем иконку кнопки темы с анимацией
        self.theme_toggle_btn.configure(
            text="🌙" if self.current_theme_name == "light" else "☀️"
        )
        self.animation_manager.scale_in(self.theme_toggle_btn, duration=0.2)
        
        # Обновляем все элементы сразу
        self.on_theme_changed()
    
    def on_theme_changed(self):
        """Обработчик изменения темы через ThemeManager"""
        # Обновляем основные цвета - ГЛАВНОЕ ОКНО!
        self.configure(fg_color=get_color("COLOR_BG"))
        
        # Обновляем фреймы
        if hasattr(self, 'buttons_frame'):
            self.buttons_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        if hasattr(self, 'content_frame'):
            self.content_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))

        # Обновляем заголовок
        if hasattr(self, 'title_label'):
            self.title_label.configure(
                text_color=get_color("COLOR_TEXT"),
                font=get_font("FONT_TITLE")
            )

        # Обновляем кнопки
        buttons = []
        if hasattr(self, 'btn_show_notes'): buttons.append(self.btn_show_notes)
        if hasattr(self, 'btn_manage_notes'): buttons.append(self.btn_manage_notes)
        if hasattr(self, 'btn_emotion_wheel'): buttons.append(self.btn_emotion_wheel)
        if hasattr(self, 'theme_toggle_btn'): buttons.append(self.theme_toggle_btn)
        if hasattr(self, 'exit_button'): buttons.append(self.exit_button)
        
        for btn in buttons:
            if hasattr(btn, 'update_theme'):
                btn.update_theme()

        # Обновляем текущее представление
        if self.current_view and hasattr(self.current_view, 'update_theme'):
            self.current_view.update_theme()
            
        # Принудительно обновляем отображение
        self.update()

    def clear_content(self):
        """Очищает область контента"""
        # Уничтожаем все дочерние виджеты
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_view = None

    def show_notes(self):
        """Показывает представление с заметками"""
        self.clear_content()
        self.notes_view = NotesView(
            self.content_frame,
            show_add_note=self.show_add_note
        )
        self.notes_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_view = self.notes_view
        if self.settings_manager.get('animations_enabled', True):
            self.animation_manager.fade_in(self.notes_view, duration=0.3)

    def show_add_note(self):
        """Показывает форму добавления заметки"""
        self.clear_content()
        self.add_note_view = Add_Note(
            self.content_frame,
            on_note_added=self.on_note_added
        )
        self.add_note_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_view = self.add_note_view
        if self.settings_manager.get('animations_enabled', True):
            self.animation_manager.slide_in(self.add_note_view, direction="right", duration=0.3)

    def on_note_added(self):
        """Обработчик добавления новой заметки"""
        # Переходим к просмотру заметок
        self.show_notes()
        # Показываем уведомление об успехе
        if self.notes_view and hasattr(self.notes_view, 'note_text'):
            self.notes_view.note_text.configure(
                text="✅ Заметка успешно добавлена! Нажмите кнопку, чтобы увидеть случайную заметку.",
                text_color=get_color("COLOR_SUCCESS")
            )

    def show_manage_notes(self):
        """Показывает представление управления заметками"""
        self.clear_content()
        self.manage_notes_view = ManageNotes(
            self.content_frame,
            on_update=self.on_notes_updated,
            on_add_note=self.show_add_note
        )
        self.manage_notes_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_view = self.manage_notes_view
        self.manage_notes_view.refresh()
        if self.settings_manager.get('animations_enabled', True):
            self.animation_manager.slide_in(self.manage_notes_view, direction="left", duration=0.3)

    def on_notes_updated(self):
        """Обработчик обновления заметок"""
        # Просто обновляем текущее представление
        if self.manage_notes_view and hasattr(self.manage_notes_view, 'refresh'):
            self.manage_notes_view.refresh()

    def show_emotion_wheel(self):
        """Показывает колесо эмоций"""
        from ui.views.emotion_wheel_view import EmotionWheelView
        
        self.clear_content()
        self.emotion_wheel_view = EmotionWheelView(self.content_frame)
        self.emotion_wheel_view.pack(fill="both", expand=True, padx=10, pady=10)
        self.current_view = self.emotion_wheel_view
        if self.settings_manager.get('animations_enabled', True):
            self.animation_manager.fade_in(self.emotion_wheel_view, duration=0.3)


    
    def on_exit(self):
        """Обработчик выхода с сохранением настроек"""
        # Сохраняем размеры окна
        self.settings_manager.set('window_width', self.winfo_width())
        self.settings_manager.set('window_height', self.winfo_height())
        
        # Очищаем наблюдателей
        ThemeManager.remove_observer(self.on_theme_changed)
        
        self.destroy()
