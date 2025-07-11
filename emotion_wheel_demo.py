import customtkinter as ctk
from ui.views.emotion_wheel_view import EmotionWheelView

class EmotionWheelApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Колесо эмоций - Relieve Stress")
        self.root.geometry("600x700")
        
        # Создание и отображение представления
        self.emotion_view = EmotionWheelView(self.root)
        self.emotion_view.pack(fill="both", expand=True)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EmotionWheelApp()
    app.run()