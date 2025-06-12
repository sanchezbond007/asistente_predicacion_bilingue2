import os
import json

# Detecta la ruta base del proyecto, aunque se ejecute desde otro lugar
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMAS_DIR = os.path.join(BASE_DIR, 'datos', 'temas')

def cargar_todos_los_bloques():
    bloques = []
    if not os.path.exists(TEMAS_DIR):
        return bloques

    for archivo in sorted(os.listdir(TEMAS_DIR)):
        if archivo.endswith('.json'):
            ruta = os.path.join(TEMAS_DIR, archivo)
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    bloque = json.load(f)
                    if isinstance(bloque, dict) and 'temas' in bloque:
                        bloques.append(bloque)
            except Exception as e:
                print(f"Error al cargar {archivo}: {e}")
    return bloques

def obtener_sugerencias(idioma='es', limite=10):
    temas = []
    for bloque in cargar_todos_los_bloques():
        for tema in bloque.get('temas', []):
            try:
                item = {
                    'titulo': tema['titulo'][idioma],
                    'respuesta': tema['respuesta'][idioma],
                    'cita': tema.get('cita', ''),
                    'categoria': tema.get('categoria', '')
                }
                temas.append(item)
                if len(temas) >= limite:
                    return temas
            except Exception as e:
                print(f"Error en tema: {tema}, error: {e}")
    return temas

def obtener_detalle_tema(titulo_busqueda, idioma='es'):
    for bloque in cargar_todos_los_bloques():
        for tema in bloque.get('temas', []):
            try:
                if tema['titulo'][idioma] == titulo_busqueda:
                    return {
                        'titulo': tema['titulo'][idioma],
                        'respuesta': tema['respuesta'][idioma],
                        'cita': tema.get('cita', ''),
                        'categoria': tema.get('categoria', '')
                    }
            except Exception as e:
                print(f"Error al buscar tema: {e}")
    return None