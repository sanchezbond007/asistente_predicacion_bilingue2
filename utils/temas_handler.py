import os
import json

def cargar_todos_los_bloques(carpeta='datos/temas'):
    temas = []
    for archivo in sorted(os.listdir(carpeta)):
        if archivo.startswith("bloque_") and archivo.endswith(".json"):
            ruta = os.path.join(carpeta, archivo)
            with open(ruta, 'r', encoding='utf-8') as f:
                bloque = json.load(f)
                if 'temas' in bloque:
                    temas.extend(bloque['temas'])
    return temas

def obtener_sugerencias():
    return cargar_todos_los_bloques()