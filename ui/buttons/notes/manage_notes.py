import customtkinter as ctk
from ui.views.base_view import BaseView
from ui.widgets.enhanced_button import EnhancedButton
from ui.widgets.note_card import NoteCard
from ui.widgets.navigation_bar import NavigationBar
from ui.components.label import Label
from ui.components.frame import Frame
from ui.style import get_color, get_font
from core.services.note_service import NoteService
from ui.animations.transitions import AnimationManager

class ManageNotes(BaseView):
    def __init__(self, master, on_update=None, on_add_note=None, on_back=None, on_home=None, **kwargs):
        self.note_service = NoteService()
        self.on_update = on_update
        self.on_add_note = on_add_note
        self.on_back = on_back
        self.on_home = on_home
        self.selected_category = None
        self.current_edit_note_id = None
        super().__init__(master, **kwargs)

    def setup_ui(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))

        # Панель навигации
        if self.on_back or self.on_home:
            self.nav_bar = NavigationBar(
                self,
                title="🛠️ Управление заметками",
                on_back=self.on_back,
                on_home=self.on_home
            )
            self.nav_bar.pack(fill="x", padx=20, pady=(10, 0))

        # Панель действий
        self.actions_frame = Frame(self, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=20, pady=10)

        self.add_btn = EnhancedButton(
            self.actions_frame,
            text="➕ Добавить",
            command=self.open_add_note,
            fg_color=get_color("COLOR_SUCCESS"),
            hover_animation=True
        )
        self.add_btn.pack(side="left", padx=5)

        # Панель категорий
        self.category_frame = Frame(self, fg_color="transparent")
        self.category_frame.pack(fill="x", padx=20, pady=10)

        self.category_label = Label(
            self.category_frame,
            text="Выберите категорию:",
            font=get_font("FONT_SUBTITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.category_label.pack(anchor="w", pady=(0, 10))

        self.category_buttons_frame = Frame(self.category_frame, fg_color="transparent")
        self.category_buttons_frame.pack(fill="x")

        categories = self.note_service.get_categories()
        self.category_buttons = []
        
        for cat in categories:
            btn = EnhancedButton(
                self.category_buttons_frame,
                text=cat,
                command=lambda c=cat: self.select_category(c),
                fg_color=get_color("COLOR_BUTTON_BG"),
                hover_animation=True
            )
            btn.pack(side="left", padx=5, expand=True, fill="x")
            self.category_buttons.append(btn)

        # Область прокрутки для заметок
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=0
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Область редактирования
        self.edit_frame = Frame(
            self,
            fg_color=get_color("COLOR_FRAME_BG"),
            corner_radius=12,
            border_width=2,
            border_color=get_color("COLOR_INFO")
        )
        
        self.edit_title = Label(
            self.edit_frame,
            text="✏️ Редактирование заметки",
            font=get_font("FONT_SUBTITLE"),
            text_color=get_color("COLOR_TEXT")
        )
        self.edit_title.pack(pady=15)
        
        self.edit_textbox = ctk.CTkTextbox(
            self.edit_frame,
            height=120,
            fg_color=get_color("COLOR_INPUT_BG"),
            text_color=get_color("COLOR_TEXT"),
            border_color=get_color("COLOR_INPUT_BORDER"),
            border_width=2,
            font=get_font("FONT_NORMAL"),
            corner_radius=8
        )
        self.edit_textbox.pack(padx=20, pady=10, fill="both", expand=True)
        self.edit_textbox.bind("<Control-v>", self.on_paste)
        self.edit_textbox.bind("<Control-c>", self.on_copy)
        self.edit_textbox.bind("<Control-a>", self.on_select_all)
        
        self.edit_buttons_frame = Frame(self.edit_frame, fg_color="transparent")
        self.edit_buttons_frame.pack(fill="x", padx=20, pady=15)
        
        self.save_edit_btn = EnhancedButton(
            self.edit_buttons_frame,
            text="✓ Сохранить",
            command=self.save_edit,
            fg_color=get_color("COLOR_SUCCESS"),
            hover_animation=True
        )
        self.save_edit_btn.pack(side="right", padx=5)
        
        self.cancel_edit_btn = EnhancedButton(
            self.edit_buttons_frame,
            text="✖ Отмена",
            command=self.cancel_edit,
            fg_color=get_color("COLOR_WARNING"),
            hover_animation=True
        )
        self.cancel_edit_btn.pack(side="right", padx=5)

        # Статус
        self.status_label = Label(
            self,
            text="Выберите категорию для просмотра заметок",
            font=get_font("FONT_NORMAL"),
            text_color=get_color("COLOR_TEXT_SECONDARY")
        )
        self.status_label.pack(pady=10)

    def select_category(self, category):
        self.selected_category = category
        
        # Обновляем кнопки категорий
        for btn in self.category_buttons:
            is_active = btn.cget("text") == category
            btn.configure(
                fg_color=get_color("COLOR_ACCENT") if is_active else get_color("COLOR_BUTTON_BG")
            )
            if is_active:
                AnimationManager.scale_in(btn, duration=0.2)
        
        self.show_notes_for_category(category)
        self.status_label.configure(
            text=f"Категория: {category}",
            text_color=get_color("COLOR_INFO")
        )

    def show_notes_for_category(self, category):
        # Очищаем текущие заметки
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        notes = self.note_service.get_notes(category)
        
        if not notes:
            no_notes_label = Label(
                self.scrollable_frame,
                text=f"Нет заметок в категории '{category}'",
                font=get_font("FONT_NORMAL"),
                text_color=get_color("COLOR_TEXT_SECONDARY")
            )
            no_notes_label.pack(pady=50)
            return
        
        # Создаем карточки заметок с кнопками управления
        for note in notes:
            note_frame = Frame(
                self.scrollable_frame,
                fg_color=get_color("COLOR_FRAME_BG"),
                corner_radius=8,
                border_width=1,
                border_color=get_color("COLOR_DIVIDER")
            )
            note_frame.pack(fill="x", pady=5, padx=10)
            
            # Текст заметки
            note_text = Label(
                note_frame,
                text=note.text,
                font=get_font("FONT_NORMAL"),
                text_color=get_color("COLOR_TEXT"),
                wraplength=400,
                justify="left"
            )
            note_text.pack(pady=10, padx=15, fill="x")
            
            # Кнопки управления
            buttons_frame = Frame(note_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            edit_btn = EnhancedButton(
                buttons_frame,
                text="✏️",
                width=30,
                height=30,
                command=lambda n=note: self.start_edit(n),
                fg_color=get_color("COLOR_INFO"),
                hover_animation=True
            )
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = EnhancedButton(
                buttons_frame,
                text="🗑️",
                width=30,
                height=30,
                command=lambda n=note: self.delete_note(n),
                fg_color=get_color("COLOR_ERROR"),
                hover_animation=True
            )
            delete_btn.pack(side="right", padx=2)
            
            favorite_btn = EnhancedButton(
                buttons_frame,
                text="★" if note.is_favorite else "☆",
                width=30,
                height=30,
                command=lambda n=note: self.toggle_favorite(n),
                fg_color=get_color("COLOR_WARNING") if note.is_favorite else get_color("COLOR_BUTTON_BG"),
                hover_animation=True
            )
            favorite_btn.pack(side="right", padx=2)

    def start_edit(self, note):
        self.current_edit_note_id = note.id
        self.edit_textbox.delete("0.0", "end")
        self.edit_textbox.insert("0.0", note.text)
        self.edit_frame.pack(fill="x", padx=20, pady=10)
        AnimationManager.slide_in(self.edit_frame, direction="right", duration=0.1)
        
        self.status_label.configure(
            text="Редактирование заметки...",
            text_color=get_color("COLOR_INFO")
        )

    def save_edit(self):
        if not self.current_edit_note_id:
            return
            
        new_text = self.edit_textbox.get("0.0", "end").strip()
        if not new_text:
            self.status_label.configure(
                text="⚠️ Заметка не может быть пустой!",
                text_color=get_color("COLOR_ERROR")
            )
            return
        
        # Обновляем заметку через сервис
        notes = self.note_service.get_notes()
        for note in notes:
            if note.id == self.current_edit_note_id:
                note.text = new_text
                break
        
        self.note_service.save_notes()
        
        # Сначала скрываем окно редактирования
        self.cancel_edit()
        
        # Затем обновляем список заметок
        self.show_notes_for_category(self.selected_category)
        
        self.status_label.configure(
            text="✓ Заметка успешно обновлена!",
            text_color=get_color("COLOR_SUCCESS")
        )
        
        if self.on_update:
            self.on_update()
    
    def on_paste(self, event):
        """Ctrl+V - вставка."""
        try:
            clipboard_text = self.clipboard_get()
            self.edit_textbox.insert("insert", clipboard_text)
        except:
            pass
        return "break"
    
    def on_copy(self, event):
        """Ctrl+C - копирование."""
        try:
            selected_text = self.edit_textbox.selection_get()
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except:
            pass
        return "break"
    
    def on_select_all(self, event):
        """Ctrl+A - выделить все."""
        self.edit_textbox.tag_add("sel", "1.0", "end")
        return "break"

    def cancel_edit(self):
        # Полностью скрываем фрейм редактирования
        self.edit_frame.pack_forget()
        self.edit_frame.place_forget()
        self.current_edit_note_id = None
        self.edit_textbox.delete("0.0", "end")
        self.status_label.configure(
            text=f"Категория: {self.selected_category}" if self.selected_category else "",
            text_color=get_color("COLOR_TEXT_SECONDARY")
        )

    def delete_note(self, note):
        if self.note_service.delete_note(note.id):
            self.show_notes_for_category(self.selected_category)
            self.status_label.configure(
                text="✓ Заметка удалена",
                text_color=get_color("COLOR_SUCCESS")
            )
            if self.on_update:
                self.on_update()

    def toggle_favorite(self, note):
        if self.note_service.toggle_favorite(note.id):
            self.show_notes_for_category(self.selected_category)
            status_text = "★ Добавлено в избранное" if not note.is_favorite else "☆ Убрано из избранного"
            self.status_label.configure(
                text=status_text,
                text_color=get_color("COLOR_INFO")
            )

    def open_add_note(self):
        if self.on_add_note:
            self.on_add_note()

    def refresh(self):
        self.note_service.load_notes()
        if self.selected_category:
            self.show_notes_for_category(self.selected_category)

    def update_theme(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        
        # Обновляем навигацию
        if hasattr(self, 'nav_bar'):
            self.nav_bar.update_theme()
        
        if hasattr(self, 'title_label'):
            self.title_label.configure(
                text_color=get_color("COLOR_TEXT"),
                font=get_font("FONT_TITLE")
            )
        
        self.category_label.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_SUBTITLE")
        )
        
        self.scrollable_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        
        self.edit_frame.configure(
            fg_color=get_color("COLOR_FRAME_BG"),
            border_color=get_color("COLOR_INFO")
        )
        
        self.edit_title.configure(
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_SUBTITLE")
        )
        
        self.edit_textbox.configure(
            fg_color=get_color("COLOR_INPUT_BG"),
            text_color=get_color("COLOR_TEXT"),
            border_color=get_color("COLOR_INPUT_BORDER")
        )
        
        self.status_label.configure(
            text_color=get_color("COLOR_TEXT_SECONDARY"),
            font=get_font("FONT_NORMAL")
        )
        
        # Обновляем кнопки
        self.add_btn.update_theme()
        for btn in self.category_buttons:
            btn.update_theme()
        self.save_edit_btn.update_theme()
        self.cancel_edit_btn.update_theme()