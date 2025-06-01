import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window

# Fondo blanco
Window.clearcolor = (1, 1, 1, 1)

# Asegura acceso al directorio raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.traducciones import traducir as t

class PantallaMenu(Screen):
    def __init__(self, sugerencias_callback=None, profundos_callback=None, buscar_callback=None, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.sugerencias_callback = sugerencias_callback
        self.profundos_callback = profundos_callback
        self.buscar_callback = buscar_callback
        self.volver_callback = volver_callback
        self.idioma = idioma

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=40)
        self.add_widget(self.layout)

        self.construir_interfaz()

    def construir_interfaz(self):
        self.layout.clear_widgets()

        # Título
        self.layout.add_widget(Label(
            text=t('titulo_menu', self.idioma),
            font_size=60,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=120
        ))

        # Botón Sugerencias
        btn_sugerencias = Button(
            text=t('sugerencias', self.idioma),
            font_size=50,
            size_hint_y=None,
            height=120,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            on_press=self.sugerencias_callback
        )
        self.layout.add_widget(btn_sugerencias)

        # Botón Temas Profundos
        btn_profundos = Button(
            text=t('temas_profundos', self.idioma),
            font_size=50,
            size_hint_y=None,
            height=120,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            on_press=self.profundos_callback
        )
        self.layout.add_widget(btn_profundos)

        # Botón Buscar
        btn_buscar = Button(
            text=t('buscar', self.idioma),
            font_size=50,
            size_hint_y=None,
            height=120,
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            on_press=self.buscar_callback  # Ya está corregido
        )
        self.layout.add_widget(btn_buscar)

        # Espaciador
        self.layout.add_widget(Widget())

        # Botón Volver
        btn_volver = Button(
            text=t('volver', self.idioma),
            font_size=40,
            size_hint_y=None,
            height=100,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            on_press=self.volver_callback
        )
        self.layout.add_widget(btn_volver)