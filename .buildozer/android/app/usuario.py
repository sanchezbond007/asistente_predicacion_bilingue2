import os
import json

# Ruta del archivo de usuarios
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
USUARIOS_PATH = os.path.join(BASE_DIR, 'usuarios.json')

def cargar_usuarios():
    if not os.path.exists(USUARIOS_PATH):
        return []
    with open(USUARIOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_usuario(datos_usuario):
    usuarios = cargar_usuarios()
    usuarios.append(datos_usuario)
    with open(USUARIOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=2)

def validar_login(usuario, contrasena):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u['usuario'] == usuario and u['contrasena'] == contrasena:
            return True
    return False

def buscar_email(usuario):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u['usuario'] == usuario:
            return u.get('correo')
    return None