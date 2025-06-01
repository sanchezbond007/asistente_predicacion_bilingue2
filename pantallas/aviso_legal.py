import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Fondo blanco
Window.clearcolor = (1, 1, 1, 1)

# Asegura acceso a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

class PantallaAvisoLegal(Screen):
    def __init__(self, continuar_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.continuar_callback = continuar_callback

        layout_principal = BoxLayout(orientation='vertical', spacing=20, padding=30)

        # ScrollView para el texto largo
        scroll = ScrollView(size_hint=(1, 1))
        contenedor = BoxLayout(orientation='vertical', size_hint_y=None, padding=10)
        contenedor.bind(minimum_height=contenedor.setter('height'))

        # Texto legal en español e inglés
        texto = (
            "[b]Aviso Legal:[/b]\n\n"
            "Esta aplicación no está afiliada ni respaldada por los Testigos de Jehová. "
            "El contenido presentado tiene únicamente fines educativos y de estudio personal. "
            "Se incluyen enlaces a contenido de jw.org con respeto y sin ánimo de lucro. "
            "Todos los derechos pertenecen a sus respectivos propietarios.\n\n"
            "[b]Legal Notice:[/b]\n\n"
            "This app is not affiliated with or endorsed by Jehovah’s Witnesses. "
            "The content presented is for educational and personal study purposes only. "
            "Links to content from jw.org are included respectfully and non-commercially. "
            "All rights belong to their respective owners."
        )

        label = Label(
            text=texto,
            markup=True,
            font_size=26,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            text_size=(Window.width * 0.9, None),
            halign='left',
            valign='top'
        )
        label.bind(texture_size=label.setter('size'))
        contenedor.add_widget(label)
        scroll.add_widget(contenedor)

        # Botón para aceptar
        boton = Button(
            text="Aceptar / Accept",
            size_hint=(1, None),
            height=90,
            font_size=24,
            background_color=(0.1, 0.4, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        boton.bind(on_press=self.continuar_callback)

        layout_principal.add_widget(scroll)
        layout_principal.add_widget(boton)
        self.add_widget(layout_principal)