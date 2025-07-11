import customtkinter as ctk
from ui.views.base_view import BaseView
from ui.widgets.enhanced_button import EnhancedButton
from ui.components.label import Label
from ui.components.frame import Frame
from ui.style import get_color, get_font
from core.services.note_service import NoteService
from ui.animations.transitions import AnimationManager

class Add_Note(BaseView):
    def __init__(self, master, on_note_added=None, **kwargs):
        self.note_service = NoteService()
        self.on_note_added = on_note_added
        super().__init__(master, **kwargs)

    def setup_ui(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))

        # Заголовок
        self.title_label = Label(
            self,
            text="✨ Добавить новую заметку",
            font=get_font("FONT_TITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.title_label.pack(pady=30)

        # Основная область
        self.main_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=12,
            border_width=1,
            border_color=get_color("COLOR_DIVIDER")
        )
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Поле для ввода текста
        self.text_label = Label(
            self.main_frame,
            text="Текст заметки:",
            font=get_font("FONT_SUBTITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.text_label.pack(pady=(20, 10), padx=20, anchor="w")

        self.textbox = ctk.CTkTextbox(
            self.main_frame,
            height=150,
            fg_color=get_color("COLOR_INPUT_BG"),
            text_color=get_color("COLOR_TEXT"),
            border_color=get_color("COLOR_INPUT_BORDER"),
            border_width=2,
            font=get_font("FONT_NORMAL"),
            corner_radius=8
        )
        self.textbox.pack(pady=10, padx=20, fill="both", expand=True)
        self.textbox.bind("<FocusIn>", self.on_textbox_focus)

        # Выбор категории
        self.category_label = Label(
            self.main_frame,
            text="Категория:",
            font=get_font("FONT_SUBTITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.category_label.pack(pady=(20, 10), padx=20, anchor="w")

        self.category_option = ctk.CTkOptionMenu(
            self.main_frame,
            values=["Поддержка", "Мотивация", "Отвлечение"],
            fg_color=get_color("COLOR_BUTTON_BG"),
            button_color=get_color("COLOR_BUTTON_BG"),
            button_hover_color=get_color("COLOR_BUTTON_HOVER"),
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL"),
            dropdown_font=get_font("FONT_NORMAL"),
            corner_radius=8,
            height=35
        )
        self.category_option.pack(pady=10, padx=20, fill="x")

        # Кнопки
        self.buttons_frame = Frame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=20, padx=20)

        self.save_button = EnhancedButton(
            self.buttons_frame,
            text="✓ Сохранить заметку",
            command=self.save_note,
            fg_color=get_color("COLOR_SUCCESS"),
            hover_animation=True,
            height=45,
            font=get_font("FONT_SUBTITLE")
        )
        self.save_button.pack(side="right", padx=10, fill="x", expand=True)

        self.clear_button = EnhancedButton(
            self.buttons_frame,
            text="✖ Очистить",
            command=self.clear_form,
            fg_color=get_color("COLOR_WARNING"),
            hover_animation=True,
            height=45,
            width=120
        )
        self.clear_button.pack(side="left", padx=10)

        # Статус
        self.status_label = Label(
            self,
            text="",
            font=get_font("FONT_NORMAL"),
            text_color=get_color("COLOR_TEXT_SECONDARY")
        )
        self.status_label.pack(pady=10)

    def on_textbox_focus(self, event):
        self.textbox.configure(border_color=get_color("COLOR_INPUT_FOCUS"))
        AnimationManager.scale_in(self.textbox, duration=0.1)

    def clear_form(self):
        self.textbox.delete("0.0", "end")
        self.category_option.set("Поддержка")
        self.status_label.configure(text="Форма очищена", text_color=get_color("COLOR_INFO"))
        AnimationManager.scale_in(self.main_frame, duration=0.2)

    def save_note(self):
        note_text = self.textbox.get("0.0", "end").strip()
        category = self.category_option.get()

        if not note_text:
            self.status_label.configure(
                text="⚠️ Пустая заметка не будет сохранена!",
                text_color=get_color("COLOR_ERROR")
            )
            AnimationManager.scale_in(self.textbox, duration=0.2)
            return

        try:
            self.note_service.add_note(note_text, category)
            self.textbox.delete("0.0", "end")
            self.status_label.configure(
                text="✓ Заметка успешно сохранена!",
                text_color=get_color("COLOR_SUCCESS")
            )
            
            # Анимация успеха
            AnimationManager.scale_in(self.save_button, duration=0.2)
            
            if self.on_note_added:
                self.on_note_added()

        except Exception as e:
            self.status_label.configure(
                text=f"❌ Ошибка при сохранении: {str(e)}",
                text_color=get_color("COLOR_ERROR")
            )

    def update_theme(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        
        self.title_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_TITLE")
        )
        
        self.main_frame.configure(
            fg_color=get_color("COLOR_FRAME_BG"),
            border_color=get_color("COLOR_DIVIDER")
        )
        
        self.text_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_SUBTITLE")
        )
        
        self.category_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_SUBTITLE")
        )
        
        self.textbox.configure(
            fg_color=get_color("COLOR_INPUT_BG"),
            text_color=get_color("COLOR_TEXT"),
            border_color=get_color("COLOR_INPUT_BORDER")
        )
        
        self.category_option.configure(
            fg_color=get_color("COLOR_BUTTON_BG"),
            button_color=get_color("COLOR_BUTTON_BG"),
            button_hover_color=get_color("COLOR_BUTTON_HOVER"),
            text_color=get_color("COLOR_TEXT")
        )
        
        self.save_button.update_theme()
        self.clear_button.update_theme()
        
        self.status_label.configure(
            text_color=get_color("COLOR_TEXT_SECONDARY"),
            font=get_font("FONT_NORMAL")
        )