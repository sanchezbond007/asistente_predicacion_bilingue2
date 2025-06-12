# language_manager.py
import json
import os

class LanguageManager:
    @staticmethod
    def load_language(default='es'):
        """Load language from usuario_actual.json, with fallback to default."""
        try:
            if os.path.exists('usuario_actual.json'):
                with open('usuario_actual.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    idioma = data.get('idioma', default)
                    return idioma.strip().lower() if isinstance(idioma, str) else default
            return default
        except Exception as e:
            print(f"❌ Error loading language: {e}")
            return default

    @staticmethod
    def save_language(idioma):
        """Save language to usuario_actual.json."""
        try:
            data = {"usuario": "usuario_auto", "idioma": idioma}
            with open('usuario_actual.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ Language saved: {idioma}")
        except Exception as e:
            print(f"❌ Error saving language: {e}")