import os
import sys
import json

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window

# Fondo blanco
Window.clearcolor = (1, 1, 1, 1)

# Ruta base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.traducciones import traducir as t
from usuario import validar_login

CREDENCIALES_PATH = os.path.join(BASE_DIR, 'credenciales.json')

class PantallaLogin(Screen):
    def __init__(self, idioma_callback=None, continuar_callback=None,
                 crear_usuario_callback=None, actualizar_callback=None,
                 idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.idioma = idioma
        self.idioma_callback = idioma_callback
        self.continuar_callback = continuar_callback
        self.crear_usuario_callback = crear_usuario_callback
        self.actualizar_callback = actualizar_callback

        self.tamano_fuente = 50
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=30)
        self.add_widget(self.layout)

        self.construir_interfaz()
        self.cargar_credenciales_guardadas()

    def construir_interfaz(self):
        self.layout.clear_widgets()

        self.layout.add_widget(Label(
            text=t('asistente_predicacion', self.idioma),
            font_size=self.tamano_fuente,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=100
        ))

        # Botones de idioma (sin símbolos)
        self.layout.add_widget(self.crear_boton('Español', lambda x: self.seleccionar_idioma('es')))
        self.layout.add_widget(self.crear_boton('English', lambda x: self.seleccionar_idioma('en')))

        self.input_usuario = TextInput(
            hint_text=t('usuario', self.idioma),
            font_size=self.tamano_fuente,
            size_hint_y=None,
            height=100
        )
        self.layout.add_widget(self.input_usuario)

        self.input_contrasena = TextInput(
            hint_text=t('contrasena', self.idioma),
            font_size=self.tamano_fuente,
            size_hint_y=None,
            height=100,
            password=True
        )
        self.layout.add_widget(self.input_contrasena)

        recordar_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
        self.checkbox_recordar = CheckBox(size_hint_x=None, width=60)
        recordar_label = Label(
            text=t('recordar_usuario', self.idioma),
            font_size=26,
            color=(0, 0, 0, 1)
        )
        recordar_layout.add_widget(self.checkbox_recordar)
        recordar_layout.add_widget(recordar_label)
        self.layout.add_widget(recordar_layout)

        self.layout.add_widget(self.crear_boton(t('login', self.idioma), self.validar_login))
        self.layout.add_widget(self.crear_boton(t('crear_usuario', self.idioma), self.ir_a_crear_usuario))
        self.layout.add_widget(self.crear_boton(t('buscar_actualizaciones', self.idioma), self.buscar_actualizaciones))

    def crear_boton(self, texto, accion):
        return Button(
            text=texto,
            on_press=accion,
            font_size=self.tamano_fuente,
            background_color=(0, 0.2, 0.4, 1),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=120
        )

    def seleccionar_idioma(self, idioma):
        self.idioma = idioma
        if self.idioma_callback:
            self.idioma_callback(idioma)
        self.construir_interfaz()

    def mostrar_popup_error(self, titulo, mensaje):
        popup = Popup(
            title=titulo,
            content=Label(text=mensaje),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()

    def validar_login(self, instancia):
        usuario = self.input_usuario.text.strip()
        contrasena = self.input_contrasena.text.strip()
        if validar_login(usuario, contrasena):
            if self.checkbox_recordar.active:
                self.guardar_credenciales(usuario, contrasena)
            else:
                self.borrar_credenciales()
            if self.continuar_callback:
                self.continuar_callback()
        else:
            self.mostrar_popup_error(t('error', self.idioma), t('campos_obligatorios', self.idioma))

    def ir_a_crear_usuario(self, instancia):
        if self.crear_usuario_callback:
            self.crear_usuario_callback()

    def buscar_actualizaciones(self, instancia):
        if self.actualizar_callback:
            self.actualizar_callback()

    def guardar_credenciales(self, usuario, contrasena):
        with open(CREDENCIALES_PATH, 'w', encoding='utf-8') as f:
            json.dump({'usuario': usuario, 'contrasena': contrasena}, f, ensure_ascii=False, indent=2)

    def cargar_credenciales_guardadas(self):
        if os.path.exists(CREDENCIALES_PATH):
            try:
                with open(CREDENCIALES_PATH, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.input_usuario.text = datos.get('usuario', '')
                    self.input_contrasena.text = datos.get('contrasena', '')
                    self.checkbox_recordar.active = True
            except Exception as e:
                print("⚠️ Error al cargar credenciales:", e)

    def borrar_credenciales(self):
        if os.path.exists(CREDENCIALES_PATH):
            try:
                os.remove(CREDENCIALES_PATH)
            except Exception as e:
                print("⚠️ Error al borrar credenciales:", e)