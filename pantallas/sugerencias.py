import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.core.window import Window

# Fondo blanco
Window.clearcolor = (1, 1, 1, 1)

# Asegura acceso a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.temas_handler import cargar_todos_los_bloques
from utils.traducciones import traducir as t


class PantallaSugerencias(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        self.temas = cargar_todos_los_bloques()

        layout_general = BoxLayout(orientation='vertical', spacing=20, padding=20)

        # Título
        titulo = Label(
            text=t('sugerencias', self.idioma).upper(),
            font_size=50,
            size_hint_y=None,
            height=80,
            color=(0, 0, 0, 1)
        )
        layout_general.add_widget(titulo)

        # Scroll con botones de temas
        scroll = ScrollView(size_hint=(1, 1))
        contenedor = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        contenedor.bind(minimum_height=contenedor.setter('height'))

        for tema in self.temas:
            texto_boton = tema['titulo'].get(self.idioma, 'Título')
            btn = Button(
                text=texto_boton,
                size_hint_y=None,
                height=120,
                font_size=28,
                background_color=(0.2, 0.5, 1, 1),
                color=(1, 1, 1, 1),
                on_release=lambda btn, t=tema: self.mostrar_tema(t)
            )
            contenedor.add_widget(btn)

        scroll.add_widget(contenedor)
        layout_general.add_widget(scroll)

        # Botón Volver
        btn_volver = Button(
            text=t('volver', self.idioma),
            size_hint_y=None,
            height=80,
            font_size=30,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            on_release=self.volver_callback
        )
        layout_general.add_widget(btn_volver)

        self.add_widget(layout_general)

    def mostrar_tema(self, tema):
        titulo = tema['titulo'].get(self.idioma, '')
        respuesta = tema['respuesta'].get(self.idioma, '')
        cita = tema.get('cita', '')
        link = tema.get('link', '')

        contenido = f"[b]{titulo}[/b]\n\n{respuesta}\n\n[b]{cita}[/b]\n\n{link}"

        popup = Popup(
            title=titulo,
            content=Label(
                text=contenido,
                markup=True,
                font_size=24,
                text_size=(800, None),
                size_hint_y=None
            ),
            size_hint=(0.9, 0.9)
        )
        popup.content.bind(texture_size=popup.content.setter('size'))
        popup.open()