import customtkinter as ctk
from ui.components.frame import Frame
from ui.components.label import Label
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
        
        # Оптимизация: применяем тему сразу после создания виджетов
        self._theme_update_pending = False


        # Настройка главного окна
        self.title("Relieve Stress")
        
        # Адаптивные размеры окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Компактные размеры
        optimal_width = 900
        optimal_height = 650
        
        width = self.settings_manager.get('window_width', optimal_width)
        height = self.settings_manager.get('window_height', optimal_height)
        
        # Ограничиваем размеры экраном
        width = min(width, screen_width - 100)
        height = min(height, screen_height - 100)
        
        self.geometry(f"{width}x{height}")
        self.minsize(900, 650)
        self.configure(fg_color=get_color("COLOR_BG"))
        self.iconbitmap(self,"assets/icon.ico")
        # Мгновенная инициализация
        self._create_widgets()
        self._init_views()
        self.show_notes()
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

        # Панель кнопок (адаптивная)
        self.buttons_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=10,
            height=60
        )
        self.buttons_frame.pack(fill="x", padx=15, pady=(0, 10))
        self.buttons_frame.pack_propagate(False)

        # Кнопки навигации (адаптивные)
        self.btn_show_notes = EnhancedButton(
            self.buttons_frame,
            text="📚 Заметки",
            command=self.show_notes,
            hover_animation=True,
            height=40
        )
        self.btn_show_notes.pack(side="left", padx=5, pady=10, fill="x", expand=True)

        self.btn_manage_notes = EnhancedButton(
            self.buttons_frame,
            text="🛠️ Управление",
            command=self.show_manage_notes,
            hover_animation=True,
            height=40
        )
        self.btn_manage_notes.pack(side="left", padx=5, pady=10, fill="x", expand=True)


        
        # Кнопка профиля
        self.btn_profile = EnhancedButton(
            self.buttons_frame,
            text="👤 Профиль",
            command=self.show_profile,
            hover_animation=True,
            height=40
        )
        self.btn_profile.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        # Кнопка AI ассистента
        self.btn_ai_assistant = EnhancedButton(
            self.buttons_frame,
            text="🤖 AI",
            command=self.show_ai_assistant,
            hover_animation=True,
            height=40
        )
        self.btn_ai_assistant.pack(side="left", padx=5, pady=10, fill="x", expand=True)

        # Кнопка смены темы
        self.theme_toggle_btn = EnhancedButton(
            self.buttons_frame,
            text="🌙" if self.current_theme_name == "light" else "☀️",
            command=self.toggle_theme,
            width=50,
            height=40,
            hover_animation=True
        )
        self.theme_toggle_btn.pack(side="right", padx=5, pady=10)

        # Кнопка выхода
        self.exit_button = EnhancedButton(
            self.buttons_frame,
            text="❌ Выход",
            command=self.on_exit,
            hover_animation=True,
            width=80,
            height=40
        )
        self.exit_button.pack(side="right", padx=5, pady=10)



        # Основная область контента (оптимизированная)
        self.content_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=10  # Уменьшено для производительности
        )
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))


    def _init_views(self):
        """Инициализирует все представления"""
        # Изначально никаких представлений нет
        self.current_view = None
        self.notes_view = None
        self.add_note_view = None
        self.manage_notes_view = None
        self.emotion_wheel_view = None
        self.profile_view = None
        self.ai_assistant_view = None
        self.view_history = []  # История просмотров для умной навигации

    # Остальные методы остаются без изменений...
    def center_window(self):
        """Центрирует окно на экране"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Центрируем, но не выходим за границы экрана
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        
        # Проверяем, что окно помещается на экране
        if x + width > screen_width:
            x = screen_width - width
        if y + height > screen_height:
            y = screen_height - height
            
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
        """Оптимизированный обработчик изменения темы."""
        # Предотвращаем множественные обновления
        if self._theme_update_pending:
            return
        self._theme_update_pending = True
        
        def update_theme():
            try:
                # Обновляем основные элементы
                self.configure(fg_color=get_color("COLOR_BG"))
                
                if hasattr(self, 'buttons_frame'):
                    self.buttons_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
                if hasattr(self, 'content_frame'):
                    self.content_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
                if hasattr(self, 'title_label'):
                    self.title_label.configure(text_color=get_color("COLOR_TEXT"))

                # Обновляем кнопки одним списком
                for attr_name in ['btn_show_notes', 'btn_manage_notes', 
                                'btn_profile', 'btn_ai_assistant', 'theme_toggle_btn', 'exit_button']:
                    if hasattr(self, attr_name):
                        btn = getattr(self, attr_name)
                        if hasattr(btn, 'update_theme'):
                            btn.update_theme()

                # Обновляем текущее представление
                if self.current_view and hasattr(self.current_view, 'update_theme'):
                    self.current_view.update_theme()
                    
            except Exception as e:
                print(f"Ошибка обновления темы: {e}")
            finally:
                self._theme_update_pending = False
        
        # Отложенное обновление для производительности
        self.after(10, update_theme)

    def clear_content(self):
        """Мгновенная очистка контента."""
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
        self.notes_view.pack(fill="both", expand=True, padx=5, pady=5)
        self._add_to_history(self.current_view)
        self.current_view = self.notes_view
        # Отключены для производительности

    def show_add_note(self):
        """Показывает форму добавления заметки"""
        self.clear_content()
        self.add_note_view = Add_Note(
            self.content_frame,
            on_note_added=self.on_note_added,
            on_back=self._get_previous_view,
            on_home=self.show_notes
        )
        self.add_note_view.pack(fill="both", expand=True, padx=5, pady=5)
        self._add_to_history(self.current_view)
        self.current_view = self.add_note_view
        # Отключены для производительности

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
            on_add_note=self.show_add_note,
            on_back=self._get_previous_view,
            on_home=self.show_notes
        )
        self.manage_notes_view.pack(fill="both", expand=True, padx=5, pady=5)
        self._add_to_history(self.current_view)
        self.current_view = self.manage_notes_view
        self.manage_notes_view.refresh()
        # Отключены для производительности

    def on_notes_updated(self):
        """Обработчик обновления заметок"""
        # Просто обновляем текущее представление
        if self.manage_notes_view and hasattr(self.manage_notes_view, 'refresh'):
            self.manage_notes_view.refresh()


    
    def show_profile(self):
        """Показывает профиль пользователя"""
        from ui.views.profile_view import ProfileView
        
        self.clear_content()
        self.profile_view = ProfileView(
            self.content_frame,
            on_back=self._get_previous_view
        )
        self.profile_view.pack(fill="both", expand=True)
        self._add_to_history(self.current_view)
        self.current_view = self.profile_view
        # Отключены для производительности


    
    def _add_to_history(self, view):
        """Добавляет представление в историю."""
        if view and view != self.current_view:
            self.view_history.append(view)
            # Ограничиваем историю 5 элементами
            if len(self.view_history) > 5:
                self.view_history.pop(0)
    
    def _get_previous_view(self):
        """Возвращает к предыдущему представлению."""
        if self.view_history:
            # Находим последнее валидное представление
            while self.view_history:
                prev_view = self.view_history.pop()
                if hasattr(prev_view, 'winfo_exists'):
                    try:
                        if prev_view.winfo_exists():
                            continue
                    except:
                        pass
                
                # Определяем тип представления и показываем соответствующий экран
                if hasattr(prev_view, '__class__'):
                    view_name = prev_view.__class__.__name__
                    if 'NotesView' in view_name:
                        self.show_notes()
                        return
                    elif 'ManageNotes' in view_name:
                        self.show_manage_notes()
                        return

                    elif 'AIAssistant' in view_name:
                        self.show_ai_assistant()
                        return
        
        # Если история пуста, возвращаемся к заметкам
        self.show_notes()
    
    def show_ai_assistant(self):
        """Показывает AI ассистента"""
        from ui.views.ai_assistant_view import AIAssistantView
        
        self.clear_content()
        self.ai_assistant_view = AIAssistantView(
            self.content_frame,
            on_back=self._get_previous_view
        )
        self.ai_assistant_view.pack(fill="both", expand=True)
        self._add_to_history(self.current_view)
        self.current_view = self.ai_assistant_view
        # Отключены для производительности
    
    def on_exit(self):
        """Обработчик выхода с сохранением настроек"""
        # Сохраняем размеры окна
        self.settings_manager.set('window_width', self.winfo_width())
        self.settings_manager.set('window_height', self.winfo_height())
        
        # Очищаем наблюдателей
        ThemeManager.remove_observer(self.on_theme_changed)
        
        self.destroy()
