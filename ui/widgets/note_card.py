"""Карточка заметки с интерактивными элементами.

Обеспечивает отображение заметки с возможностью управления.
"""

import customtkinter as ctk
from typing import Optional, Callable
from ui.style import get_color, get_font
from ui.animations.transitions import AnimationManager
from core.models.note import Note


class NoteCard(ctk.CTkFrame):
    """Карточка для отображения заметки с кнопками управления."""
    
    def __init__(self, parent: ctk.CTkBaseClass, note: Note, 
                 on_delete: Optional[Callable[[str], None]] = None,
                 on_favorite: Optional[Callable[[str], None]] = None, **kwargs):
        """Инициализирует карточку заметки.
        
        Args:
            parent: Родительский элемент
            note: Объект заметки
            on_delete: Коллбэк для удаления
            on_favorite: Коллбэк для избранного
        """
        super().__init__(parent, **kwargs)
        self.note = note
        self.on_delete = on_delete
        self.on_favorite = on_favorite
        self._setup_ui()
        self._setup_hover_effects()
    
    def _setup_ui(self) -> None:
        """Настраивает пользовательский интерфейс карточки."""
        self.configure(
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=12,
            border_width=1,
            border_color=get_color("COLOR_DIVIDER")
        )
        
        self._create_text_area()
        self._create_control_panel()
    
    def _create_text_area(self) -> None:
        """Создаёт область с текстом заметки."""
        self.text_label = ctk.CTkLabel(
            self,
            text=self._truncate_text(self.note.text, 150),
            font=get_font("FONT_NORMAL"),
            text_color=get_color("COLOR_TEXT"),
            wraplength=300,
            justify="left",
            anchor="w"
        )
        self.text_label.pack(pady=10, padx=15, fill="x")
    
    def _create_control_panel(self) -> None:
        """Создаёт панель управления."""
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Метка категории
        self.category_label = ctk.CTkLabel(
            self.buttons_frame,
            text=f"#{self.note.category}",
            font=get_font("FONT_SMALL"),
            text_color=get_color("COLOR_TEXT_SECONDARY")
        )
        self.category_label.pack(side="left", padx=5)
        
        # Кнопка избранного
        favorite_text = "★" if self.note.is_favorite else "☆"
        self.favorite_btn = ctk.CTkButton(
            self.buttons_frame,
            text=favorite_text,
            width=30,
            height=30,
            command=self._on_favorite_click,
            fg_color=get_color("COLOR_WARNING") if self.note.is_favorite else get_color("COLOR_BUTTON_BG"),
            hover_color=get_color("COLOR_WARNING") if not self.note.is_favorite else get_color("COLOR_BUTTON_HOVER")
        )
        self.favorite_btn.pack(side="right", padx=2)
        
        # Кнопка удаления
        self.delete_btn = ctk.CTkButton(
            self.buttons_frame,
            text="🗑️",
            width=30,
            height=30,
            command=self._on_delete_click,
            fg_color=get_color("COLOR_ERROR"),
            hover_color=get_color("COLOR_ERROR")
        )
        self.delete_btn.pack(side="right", padx=2)
    
    def _setup_hover_effects(self) -> None:
        """Настраивает эффекты наведения."""
        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)
    
    def _on_hover_enter(self, event) -> None:
        """Обработчик наведения мыши."""
        self.configure(border_color=get_color("COLOR_ACCENT"))
        AnimationManager.scale_in(self, duration=0.1, scale_from=1.0, scale_to=1.02)
    
    def _on_hover_leave(self, event) -> None:
        """Обработчик ухода мыши."""
        self.configure(border_color=get_color("COLOR_DIVIDER"))
        AnimationManager.scale_in(self, duration=0.1, scale_from=1.02, scale_to=1.0)
    
    def _on_favorite_click(self) -> None:
        """Обработчик нажатия кнопки избранного."""
        if self.on_favorite:
            self.on_favorite(self.note.id)
            # Обновляем визуальное состояние
            self._update_favorite_button()
    
    def _on_delete_click(self) -> None:
        """Обработчик нажатия кнопки удаления."""
        if self.on_delete:
            self.on_delete(self.note.id)
    
    def _update_favorite_button(self) -> None:
        """Обновляет внешний вид кнопки избранного."""
        favorite_text = "★" if self.note.is_favorite else "☆"
        self.favorite_btn.configure(
            text=favorite_text,
            fg_color=get_color("COLOR_WARNING") if self.note.is_favorite else get_color("COLOR_BUTTON_BG")
        )
    
    @staticmethod
    def _truncate_text(text: str, max_length: int) -> str:
        """Обрезает текст до указанной длины."""
        return text[:max_length] + "..." if len(text) > max_length else text
    
    def update_theme(self) -> None:
        """Обновляет тему карточки."""
        self.configure(
            fg_color=get_color("COLOR_FRAME_BG"),
            border_color=get_color("COLOR_DIVIDER")
        )
        
        self.text_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL")
        )
        
        self.category_label.configure(
            text_color=get_color("COLOR_TEXT_SECONDARY"),
            font=get_font("FONT_SMALL")
        )
        
        # Обновляем кнопки
        self._update_favorite_button()
        self.delete_btn.configure(fg_color=get_color("COLOR_ERROR"))