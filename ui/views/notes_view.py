import customtkinter as ctk
from typing import Callable, Optional
from ui.views.base_view import BaseView
from ui.widgets.note_card import NoteCard
from ui.widgets.enhanced_button import EnhancedButton
from ui.style import get_color, get_font
from core.services.note_service import NoteService

class NotesView(BaseView):
    def __init__(self, parent, note_service: NoteService, on_add_note: Optional[Callable] = None):
        self.note_service = note_service
        self.on_add_note = on_add_note
        self.selected_category = "Все"
        super().__init__(parent)
    
    def setup_ui(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self,
            text="Мои заметки для снятия стресса",
            font=get_font("FONT_TITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.title_label.pack(pady=20)
        
        # Панель фильтров
        self.filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.filter_frame.pack(fill="x", padx=20, pady=10)
        
        # Выбор категории
        categories = ["Все"] + self.note_service.get_categories()
        self.category_menu = ctk.CTkOptionMenu(
            self.filter_frame,
            values=categories,
            command=self.on_category_changed
        )
        self.category_menu.pack(side="left", padx=10)
        
        # Кнопка добавления
        self.add_btn = EnhancedButton(
            self.filter_frame,
            text="+ Добавить заметку",
            command=self._on_add_click,
            fg_color=get_color("COLOR_ACCENT")
        )
        self.add_btn.pack(side="right", padx=10)
        
        # Область прокрутки для заметок
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=0
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.refresh_notes()
    
    def refresh_notes(self):
        # Очищаем текущие заметки
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Получаем заметки
        category = None if self.selected_category == "Все" else self.selected_category
        notes = self.note_service.get_notes(category)
        
        if not notes:
            no_notes_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Пока нет заметок. Добавьте первую!",
                font=get_font("FONT_NORMAL"),
                text_color=get_color("COLOR_TEXT_SECONDARY")
            )
            no_notes_label.pack(pady=50)
            return
        
        # Создаем карточки заметок
        for note in notes:
            card = NoteCard(
                self.scrollable_frame,
                note=note,
                on_delete=self.on_note_delete,
                on_favorite=self.on_note_favorite
            )
            card.pack(fill="x", pady=5, padx=10)
    
    def on_category_changed(self, category: str):
        self.selected_category = category
        self.refresh_notes()
    
    def on_note_delete(self, note_id: str):
        if self.note_service.delete_note(note_id):
            self.refresh_notes()
    
    def on_note_favorite(self, note_id: str):
        if self.note_service.toggle_favorite(note_id):
            self.refresh_notes()
    
    def _on_add_click(self):
        if self.on_add_note:
            self.on_add_note()
    
    def update_theme(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.title_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_TITLE")
        )
        self.scrollable_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.add_btn.update_theme()