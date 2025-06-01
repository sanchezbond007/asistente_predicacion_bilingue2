import os
import sys
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Fondo blanco
Window.clearcolor = (1, 1, 1, 1)

# Ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.traducciones import traducir as t

USUARIOS_PATH = os.path.join(BASE_DIR, 'usuarios.json')


class PantallaCrearUsuario(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma

        alto_pantalla = Window.height
        font_size = alto_pantalla * 0.03  # Responsive (≈ 50 en móvil estándar)

        scroll = ScrollView(size_hint=(1, 1))
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=30, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.campos = {}

        for campo in ['nombre', 'apellido', 'telefono', 'correo', 'usuario', 'contrasena']:
            etiqueta = Label(
                text=t(campo, self.idioma),
                font_size=font_size,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=font_size * 1.3
            )
            entrada = TextInput(
                size_hint_y=None,
                height=font_size * 2,
                multiline=False
            )
            self.layout.add_widget(etiqueta)
            self.layout.add_widget(entrada)
            self.campos[campo] = entrada

        # Botón crear usuario
        btn_crear = Button(
            text=t('crear_usuario', self.idioma),
            size_hint_y=None,
            height=font_size * 2.5,
            background_color=(0, 0.2, 0.5, 1),
            color=(1, 1, 1, 1),
            font_size=font_size
        )
        btn_crear.bind(on_release=self.crear_usuario)
        self.layout.add_widget(btn_crear)

        # Botón volver
        btn_volver = Button(
            text=t('volver', self.idioma),
            size_hint_y=None,
            height=font_size * 2.5,
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            font_size=font_size
        )
        btn_volver.bind(on_release=self.volver)
        self.layout.add_widget(btn_volver)

        scroll.add_widget(self.layout)
        self.add_widget(scroll)

    def crear_usuario(self, instance):
        datos = {k: v.text.strip() for k, v in self.campos.items()}
        obligatorios = ['nombre', 'usuario', 'contrasena']
        faltantes = [t(campo, self.idioma) for campo in obligatorios if not datos[campo]]

        if faltantes:
            mensaje = t('campos_obligatorios', self.idioma) + ": " + ", ".join(faltantes)
            self.mostrar_popup(t('error', self.idioma), mensaje)
            return

        self.guardar_usuario(datos)
        self.mostrar_popup(t('exito', self.idioma), t('usuario_creado', self.idioma))
        self.limpiar_campos()

    def guardar_usuario(self, datos):
        if os.path.exists(USUARIOS_PATH):
            with open(USUARIOS_PATH, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
        else:
            usuarios = []

        usuarios.append(datos)
        with open(USUARIOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)

    def mostrar_popup(self, titulo, mensaje):
        contenido = BoxLayout(orientation='vertical', padding=20, spacing=20)
        contenido.add_widget(Label(text=mensaje, color=(0, 0, 0, 1), font_size=22))
        btn_cerrar = Button(text='OK', size_hint_y=None, height=50)
        contenido.add_widget(btn_cerrar)

        popup = Popup(title=titulo, content=contenido, size_hint=(0.8, 0.4))
        btn_cerrar.bind(on_release=popup.dismiss)
        popup.open()

    def volver(self, instance):
        if self.volver_callback:
            self.volver_callback()

    def limpiar_campos(self):
        for entrada in self.campos.values():
            entrada.text = ''