import json
import uuid
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from core.models.note import Note

class NoteService:
    def __init__(self, data_file: str = "data/notes.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        self._notes: List[Note] = []
        self.load_notes()
    
    def load_notes(self) -> None:
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._notes = [Note.from_dict(note_data) for note_data in data]
            except (json.JSONDecodeError, KeyError):
                self._notes = []
    
    def save_notes(self) -> None:
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump([note.to_dict() for note in self._notes], f, ensure_ascii=False, indent=2)
    
    def add_note(self, text: str, category: str) -> Note:
        note = Note(
            id=str(uuid.uuid4()),
            text=text,
            category=category,
            created_at=datetime.now()
        )
        self._notes.append(note)
        self.save_notes()
        return note
    
    def get_notes(self, category: Optional[str] = None) -> List[Note]:
        if category:
            return [note for note in self._notes if note.category == category]
        return self._notes.copy()
    
    def get_categories(self) -> List[str]:
        return list(set(note.category for note in self._notes))
    
    def delete_note(self, note_id: str) -> bool:
        for i, note in enumerate(self._notes):
            if note.id == note_id:
                del self._notes[i]
                self.save_notes()
                return True
        return False
    
    def toggle_favorite(self, note_id: str) -> bool:
        for note in self._notes:
            if note.id == note_id:
                note.is_favorite = not note.is_favorite
                note.updated_at = datetime.now()
                self.save_notes()
                return True
        return False