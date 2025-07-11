import random
from ui.views.base_view import BaseView
from ui.widgets.enhanced_button import EnhancedButton
from ui.widgets.note_card import NoteCard
from ui.components.label import Label
from ui.components.frame import Frame
from ui.style import get_color, get_font
from core.services.note_service import NoteService
from ui.animations.transitions import AnimationManager
import customtkinter as ctk

class NotesView(BaseView):
    def __init__(self, master, show_add_note=None, **kwargs):
        self.note_service = NoteService()
        self.show_add_note = show_add_note
        self.active_category = "Все"
        self.current_note = None
        super().__init__(master, **kwargs)

    def setup_ui(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))

        # Заголовок
        self.title_label = Label(
            self,
            text="Заметки для снятия стресса",
            font=get_font("FONT_TITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.title_label.pack(pady=20)

        # Панель категорий
        self.category_frame = Frame(self, fg_color="transparent")
        self.category_frame.pack(fill="x", padx=20, pady=10)

        categories = ["Все"] + self.note_service.get_categories()
        self.category_buttons = []
        
        for cat in categories:
            btn = EnhancedButton(
                self.category_frame,
                text=cat,
                command=lambda c=cat: self.filter_by_category(c),
                fg_color=get_color("COLOR_ACCENT") if cat == self.active_category else get_color("COLOR_BUTTON_BG"),
                hover_animation=True
            )
            btn.pack(side="left", padx=5, expand=True, fill="x")
            self.category_buttons.append(btn)

        # Область отображения заметки
        self.note_display_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=12,
            border_width=2,
            border_color=get_color("COLOR_DIVIDER")
        )
        self.note_display_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.note_text = Label(
            self.note_display_frame,
            text="Нажмите кнопку, чтобы показать случайную заметку",
            wraplength=500,
            font=get_font("FONT_SUBTITLE"),
            text_color=get_color("COLOR_TEXT_SECONDARY"),
            justify="center"
        )
        self.note_text.pack(expand=True, pady=40, padx=30)

        # Кнопки управления
        self.buttons_frame = Frame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=20, pady=10)

        self.show_note_btn = EnhancedButton(
            self.buttons_frame,
            text="✨ Показать заметку",
            command=self.show_random_note,
            fg_color=get_color("COLOR_ACCENT"),
            hover_animation=True,
            height=40
        )
        self.show_note_btn.pack(side="left", padx=10, expand=True, fill="x")

        if self.show_add_note:
            self.add_note_btn = EnhancedButton(
                self.buttons_frame,
                text="➕ Добавить заметку",
                command=self.show_add_note,
                fg_color=get_color("COLOR_SUCCESS"),
                hover_animation=True,
                height=40
            )
            self.add_note_btn.pack(side="right", padx=10)

    def filter_by_category(self, category):
        self.active_category = category
        
        # Обновляем кнопки категорий
        for btn in self.category_buttons:
            is_active = btn.cget("text") == category
            btn.configure(
                fg_color=get_color("COLOR_ACCENT") if is_active else get_color("COLOR_BUTTON_BG")
            )
            if is_active:
                AnimationManager.scale_in(btn, duration=0.2)

    def show_random_note(self):
        category = None if self.active_category == "Все" else self.active_category
        notes = self.note_service.get_notes(category)
        
        if not notes:
            self.note_text.configure(
                text="Нет заметок в выбранной категории.\nДобавьте новую заметку!",
                text_color=get_color("COLOR_TEXT_SECONDARY")
            )
            return
        
        self.current_note = random.choice(notes)
        self.note_text.configure(
            text=self.current_note.text,
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_SUBTITLE")
        )
        
        # Анимация появления
        AnimationManager.fade_in(self.note_display_frame, duration=0.4)

    def refresh_notes(self):
        self.note_service.load_notes()
        # Обновляем категории
        categories = ["Все"] + self.note_service.get_categories()
        # Можно добавить логику обновления кнопок категорий

    def update_theme(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        
        self.title_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_TITLE")
        )
        
        self.note_display_frame.configure(
            fg_color=get_color("COLOR_FRAME_BG"),
            border_color=get_color("COLOR_DIVIDER")
        )
        
        self.note_text.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_SUBTITLE")
        )
        
        # Обновляем кнопки
        for btn in self.category_buttons:
            btn.update_theme()
            is_active = btn.cget("text") == self.active_category
            btn.configure(
                fg_color=get_color("COLOR_ACCENT") if is_active else get_color("COLOR_BUTTON_BG")
            )
        
        self.show_note_btn.update_theme()
        if hasattr(self, 'add_note_btn'):
            self.add_note_btn.update_theme()