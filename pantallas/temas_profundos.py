import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window

# Fondo blanco
Window.clearcolor = (1, 1, 1, 1)

# Acceso a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.traducciones import traducir as t
from utils.temas_handler2 import cargar_temas_profundos

class PantallaTemasProfundos(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        self.indice = 0
        self.temas = cargar_temas_profundos()

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)

        self.btn_volver = Button(size_hint_y=None, height=100, font_size=40)
        self.btn_volver.bind(on_press=self.volver_callback)
        self.layout.add_widget(self.btn_volver)

        self.add_widget(self.layout)

        Clock.schedule_once(lambda dt: self.construir_interfaz())

    def construir_interfaz(self):
        self.grid.clear_widgets()
        self.btn_volver.text = t('volver', self.idioma)
        self.mostrar_temas()

    def mostrar_temas(self):
        self.grid.clear_widgets()
        temas_filtrados = self.temas[self.indice:self.indice + 5]

        for tema in temas_filtrados:
            if not isinstance(tema, dict) or 'titulo' not in tema or not isinstance(tema['titulo'], dict):
                continue

            titulo = tema['titulo'].get(self.idioma, 'Sin título')
            btn = Button(
                text=titulo,
                size_hint_y=None,
                height=100,
                font_size=40,
                halign='left',
                valign='middle',
                text_size=(self.width - 40, None)
            )
            btn.bind(on_press=lambda instance, tema=tema: self.mostrar_detalle_tema(tema))
            self.grid.add_widget(btn)

        if self.indice + 5 < len(self.temas):
            btn_mas = Button(
                text=t('mostrar_mas', self.idioma),
                size_hint_y=None,
                height=80,
                font_size=35
            )
            btn_mas.bind(on_press=self.mostrar_mas)
            self.grid.add_widget(btn_mas)

    def mostrar_mas(self, instance):
        self.indice += 5
        self.mostrar_temas()

    def mostrar_detalle_tema(self, tema):
        contenido = tema.get('contenido', {}).get(self.idioma, '')
        versiculos = tema.get('versiculos', [])
        fuente = tema.get('fuente', {}).get(self.idioma, '')
        copyright_text = tema.get('copyright', {}).get(self.idioma, '')

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        def agregar_label(texto, **kwargs):
            lbl = Label(
                text=texto,
                markup=True,
                size_hint_y=None,
                text_size=(self.width - 40, None),
                halign='left',
                valign='top',
                **kwargs
            )
            lbl.texture_update()
            lbl.height = lbl.texture_size[1] + 20
            layout.add_widget(lbl)

        agregar_label(contenido)

        for vers in versiculos:
            cita = vers.get('cita', '')
            texto = vers.get('texto', {}).get(self.idioma, '')
            agregar_label(f"[b]{cita}[/b]: {texto}")

        if fuente:
            agregar_label(f"[ref={fuente}][color=0000ff]{fuente}[/color][/ref]", markup=True)

        if copyright_text:
            agregar_label(copyright_text, markup=True, color=(0.5, 0.5, 0.5, 1))

        btn_cerrar = Button(text=t('volver', self.idioma), size_hint_y=None, height=80, font_size=35)

        popup = Popup(
            title=tema.get('titulo', {}).get(self.idioma, 'Detalle'),
            content=BoxLayout(orientation='vertical', spacing=10, padding=10),
            size_hint=(0.95, 0.95)
        )
        popup.content.add_widget(ScrollView(content=layout))
        popup.content.add_widget(btn_cerrar)
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()