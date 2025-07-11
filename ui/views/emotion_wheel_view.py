"""Представление колеса эмоций.

Обеспечивает интерактивный выбор эмоций и получение соответствующих советов.
"""

import customtkinter as ctk
from typing import Dict
from ui.views.base_view import BaseView
from core.services.emotion_service import EmotionService
from ui.style import get_color, get_font


class EmotionWheelView(BaseView):
    """Представление колеса эмоций для выбора и получения советов."""
    
    # Эмодзи для эмоций
    _EMOTION_EMOJIS: Dict[str, str] = {
        "Злость": "😠",
        "Грусть": "😢",
        "Усталость": "😴",
        "Радость": "😊",
        "Тревога": "😰",
        "Спокойствие": "😌"
    }
    
    def __init__(self, parent):
        """Инициализирует представление колеса эмоций."""
        self.emotion_service = EmotionService()
        self.selected_emotion = ctk.StringVar()
        super().__init__(parent)
    
    def setup_ui(self) -> None:
        """Настраивает пользовательский интерфейс."""
        self._create_header()
        self._create_emotion_wheel()
        self._create_result_area()
    
    def _create_header(self) -> None:
        """Создаёт заголовок с описанием."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=20, fill="x")
        
        # Основной заголовок
        title = ctk.CTkLabel(
            header_frame,
            text="🎭 Колесо эмоций 🎭",
            font=get_font("FONT_TITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        title.pack()
        
        # Подзаголовок
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Выберите свою текущую эмоцию и получите персональные рекомендации",
            font=get_font("FONT_NORMAL"),
            text_color=get_color("COLOR_TEXT_SECONDARY")
        )
        subtitle.pack(pady=(5, 0))
    
    def _create_emotion_wheel(self) -> None:
        """Создаёт колесо эмоций с кнопками."""
        wheel_frame = ctk.CTkFrame(self, fg_color="transparent")
        wheel_frame.pack(pady=30)
        
        emotions = self.emotion_service.get_emotions()
        
        # Создаём кнопки в два ряда
        for i, emotion in enumerate(emotions):
            self._create_emotion_button(wheel_frame, emotion, i)
    
    def _create_emotion_button(self, parent: ctk.CTkFrame, emotion: str, index: int) -> None:
        """Создаёт кнопку для эмоции."""
        color = self.emotion_service.get_emotion_color(emotion)
        
        # Определяем позицию в сетке
        row = 0 if index < 3 else 1
        col = index if index < 3 else index - 3
        
        # Контейнер для кнопки с тенью
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.grid(row=row, column=col, padx=15, pady=15)
        
        # Тень
        shadow = ctk.CTkFrame(
            btn_frame,
            fg_color=get_color("COLOR_DIVIDER"),
            width=140,
            height=80,
            corner_radius=20
        )
        shadow.place(x=3, y=3)
        
        # Кнопка эмоции
        btn = ctk.CTkButton(
            btn_frame,
            text=f"{self._get_emotion_emoji(emotion)}\n{emotion}",
            fg_color=color,
            hover_color=self._darken_color(color),
            font=get_font("FONT_NORMAL"),
            width=140,
            height=80,
            corner_radius=20,
            command=lambda e=emotion: self.select_emotion(e)
        )
        btn.pack()
        btn.lift()  # Поднимаем над тенью
    
    def _create_result_area(self) -> None:
        """Создаёт область для отображения результатов."""
        self.result_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=15
        )
        self.result_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    def _get_emotion_emoji(self, emotion: str) -> str:
        """Возвращает эмодзи для указанной эмоции."""
        return self._EMOTION_EMOJIS.get(emotion, "😐")
    
    def _darken_color(self, color: str) -> str:
        """Затемняет цвет для hover-эффекта."""
        if not color.startswith('#') or len(color) != 7:
            return color
        
        try:
            # Парсим RGB компоненты
            r = max(0, int(color[1:3], 16) - 30)
            g = max(0, int(color[3:5], 16) - 30)
            b = max(0, int(color[5:7], 16) - 30)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return color
    
    def select_emotion(self, emotion: str) -> None:
        """Обрабатывает выбор эмоции и отображает соответствующие советы."""
        self.selected_emotion.set(emotion)
        advice_data = self.emotion_service.get_emotion_advice(emotion)
        
        if not advice_data:
            return
        
        self._clear_result()
        self._display_emotion_advice(emotion, advice_data)
    
    def _display_emotion_advice(self, emotion: str, advice_data) -> None:
        """Отображает советы для выбранной эмоции."""
        color = self.emotion_service.get_emotion_color(emotion)
        emoji = self._get_emotion_emoji(emotion)
        
        # Заголовок с эмоцией
        self._create_emotion_header(emotion, emoji, color)
        
        # Карточки с советами
        self._create_advice_cards(advice_data)
        
        # Кнопки действий
        self._create_action_buttons(emotion)
    
    def _create_emotion_header(self, emotion: str, emoji: str, color: str) -> None:
        """Создаёт заголовок с названием эмоции."""
        header_card = ctk.CTkFrame(
            self.result_frame,
            fg_color=color,
            corner_radius=15
        )
        header_card.pack(fill="x", pady=(0, 20))
        
        result_title = ctk.CTkLabel(
            header_card,
            text=f"{emoji} {emotion} {emoji}",
            font=get_font("FONT_SUBTITLE"),
            text_color="white"
        )
        result_title.pack(pady=15)
    
    def _create_advice_cards(self, advice_data) -> None:
        """Создаёт карточки с советами."""
        cards_data = [
            ("💡", "Совет", advice_data.advice, get_color("COLOR_SUCCESS")),
            ("📜", "Цитата", f'"{advice_data.quote}"', get_color("COLOR_INFO")),
            ("🎯", "Действие", advice_data.action, get_color("COLOR_WARNING"))
        ]
        
        for icon, title, text, card_color in cards_data:
            self._create_advice_card(icon, title, text, card_color)
    
    def _create_advice_card(self, icon: str, title: str, text: str, color: str) -> None:
        """Создаёт одну карточку с советом."""
        card = ctk.CTkFrame(
            self.result_frame,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=12
        )
        card.pack(fill="x", pady=10)
        
        # Заголовок карточки
        card_header = ctk.CTkFrame(card, fg_color=color, corner_radius=8)
        card_header.pack(fill="x", padx=15, pady=(15, 10))
        
        header_label = ctk.CTkLabel(
            card_header,
            text=f"{icon} {title}",
            font=get_font("FONT_NORMAL"),
            text_color="white"
        )
        header_label.pack(pady=8)
        
        # Текст карточки
        text_label = ctk.CTkLabel(
            card,
            text=text,
            font=get_font("FONT_SMALL"),
            text_color=get_color("COLOR_TEXT"),
            wraplength=450,
            justify="left"
        )
        text_label.pack(padx=20, pady=(0, 15), anchor="w")
    
    def _create_action_buttons(self, emotion: str) -> None:
        """Создаёт кнопки действий."""
        buttons_frame = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        # Кнопка получения нового совета
        new_advice_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Получить другой совет",
            command=lambda: self.select_emotion(emotion),
            fg_color=get_color("COLOR_SUCCESS"),
            font=get_font("FONT_NORMAL"),
            height=40,
            corner_radius=20
        )
        new_advice_btn.pack(side="left", padx=10)
        
        # Кнопка возврата
        back_btn = ctk.CTkButton(
            buttons_frame,
            text="⬅️ Выбрать другую эмоцию",
            command=self._clear_result,
            fg_color=get_color("COLOR_BUTTON_BG"),
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL"),
            height=40,
            corner_radius=20
        )
        back_btn.pack(side="left", padx=10)
    
    def _clear_result(self) -> None:
        """Очищает область результатов."""
        for widget in self.result_frame.winfo_children():
            widget.destroy()
    
    def update_theme(self) -> None:
        """Обновляет тему всех элементов интерфейса."""
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        if hasattr(self, 'result_frame'):
            self.result_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))