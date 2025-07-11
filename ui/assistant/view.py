import customtkinter as ctk
from typing import Callable
from ui.components.frame import Frame
from ui.components.label import Label
from ui.components.buttons import Button
from ui.components.entry import Entry
from ui.style import get_color, get_font
import threading
import asyncio

class AssistantView(Frame):
    def __init__(self, master, on_send_message: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.on_send_message = on_send_message
        self.setup_ui()

    def setup_ui(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))

        self.messages_frame = Frame(self, fg_color=get_color("COLOR_FRAME_BG"))
        self.messages_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = ctk.CTkCanvas(
            self.messages_frame,
            bg=get_color("COLOR_FRAME_BG"),
            highlightthickness=0
        )
        self.scrollbar = ctk.CTkScrollbar(
            self.messages_frame,
            orientation="vertical",
            command=self.canvas.yview
        )
        self.scrollable_frame = Frame(self.canvas, fg_color=get_color("COLOR_FRAME_BG"))

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.input_frame = Frame(self, fg_color=get_color("COLOR_FRAME_BG"))
        self.input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.message_entry = Entry(
            self.input_frame,
            placeholder="Введите ваше сообщение...",
            fg_color=get_color("COLOR_INPUT_BG")
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.send_button = Button(
            self.input_frame,
            text="➤",
            width=50,
            command=self.send_message
        )
        self.send_button.pack(side="right")

        self.add_message("assistant", "Привет! Я ваш ассистент по снятию стресса. Чем могу помочь?")

    def add_message(self, sender: str, text: str):
        frame = Frame(
            self.scrollable_frame,
            fg_color=get_color("COLOR_ACCENT") if sender == "assistant" else get_color("COLOR_BUTTON_BG"),
            corner_radius=12
        )
        frame.pack(fill="x", padx=5, pady=5, anchor="w" if sender == "user" else "e")

        label = Label(
            frame,
            text=text,
            text_color=get_color("COLOR_TEXT"),
            font=get_font("FONT_NORMAL"),
            wraplength=400,
            justify="left"
        )
        label.pack(padx=10, pady=10)

        self.canvas.yview_moveto(1.0)

    def send_message(self):
        # Запускаем отправку в отдельном потоке
        threading.Thread(target=self._send_message_thread, daemon=True).start()

    def _send_message_thread(self):
        message = self.message_entry.get().strip()
        if not message:
            return

        def ui_before_sending():
            self.message_entry.set("")
            self.add_message("user", message)
            self.send_button.configure(state="disabled")

            if hasattr(self, "loading_frame") and self.loading_frame.winfo_exists():
                self.loading_frame.destroy()

            self.loading_frame = Frame(
                self.scrollable_frame,
                fg_color=get_color("COLOR_ACCENT"),
                corner_radius=12
            )
            self.loading_frame.pack(fill="x", padx=5, pady=5, anchor="e")

            self.loading_label = Label(
                self.loading_frame,
                text="...",
                text_color=get_color("COLOR_TEXT"),
                font=get_font("FONT_NORMAL")
            )
            self.loading_label.pack(padx=10, pady=10)
            self.canvas.yview_moveto(1.0)

        self.after(0, ui_before_sending)

        try:
            response = self.on_send_message(message)
        except Exception as e:
            response = f"Ошибка: {str(e)}"

        def ui_after_sending():
            self.loading_frame.destroy()
            self.add_message("assistant", response)
            self.send_button.configure(state="normal")
            self.canvas.yview_moveto(1.0)

        self.after(0, ui_after_sending)


    def update_theme(self):
        self.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.messages_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.scrollable_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.input_frame.configure(fg_color=get_color("COLOR_FRAME_BG"))
        self.canvas.configure(bg=get_color("COLOR_FRAME_BG"))
        self.message_entry.update_theme()
        self.send_button.update_theme()
