# utils/temas_handler2.py

import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RUTA_TEMAS_PROFUNDOS = os.path.join(BASE_DIR, 'datos', 'temas_profundos')

def cargar_temas_profundos(idioma='es'):
    temas = []
    for nombre_archivo in os.listdir(RUTA_TEMAS_PROFUNDOS):
        if nombre_archivo.endswith('.json'):
            ruta = os.path.join(RUTA_TEMAS_PROFUNDOS, nombre_archivo)
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    datos = json.load(f)

                    # Si es una lista de temas
                    if isinstance(datos, list):
                        for tema in datos:
                            temas.append(_formatear_tema(tema, idioma))
                    # Si es un único tema como diccionario
                    elif isinstance(datos, dict):
                        temas.append(_formatear_tema(datos, idioma))

            except Exception as e:
                print(f"Error al leer {nombre_archivo}: {e}")
    return temas

def _formatear_tema(tema, idioma):
    return {
        "titulo": tema.get('titulo', {}).get(idioma, ''),
        "contenido": tema.get('contenido', {}).get(idioma, ''),
        "versiculos": tema.get('versiculos', []),
        "fuente": tema.get('fuente', {}),
        "copyright": tema.get('copyright', {}),
    }