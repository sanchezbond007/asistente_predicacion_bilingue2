import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

# Asegura acceso a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.temas_handler import cargar_todos_los_bloques
from utils.temas_handler2 import cargar_temas_profundos
from utils.traducciones import traducir as t

class PantallaBuscar(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.text_input = TextInput(hint_text=t("Buscar", self.idioma), size_hint_y=None, height=60, font_size=24)
        self.boton_buscar = Button(text=t("Buscar", self.idioma), size_hint_y=None, height=60, font_size=24, background_color=(0.2, 0.6, 1, 1))
        self.boton_buscar.bind(on_press=self.realizar_busqueda)

        self.resultados_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.scroll = ScrollView()
        self.scroll.add_widget(self.resultados_layout)

        self.boton_volver = Button(text=t("Volver", self.idioma), size_hint_y=None, height=60, font_size=24, background_color=(0.7, 0.7, 0.7, 1))
        self.boton_volver.bind(on_press=self.volver)

        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.boton_buscar)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.boton_volver)

        self.add_widget(self.layout)

    def realizar_busqueda(self, instancia):
        termino = self.text_input.text.strip().lower()
        if not termino:
            return

        print(f"🔍 Buscando: {termino}")

        self.resultados_layout.clear_widgets()
        self.resultados_layout.height = 0

        temas_normales = cargar_todos_los_bloques()
        temas_profundos = cargar_temas_profundos(self.idioma)

        resultados = []

        for tema in temas_normales:
            titulo = tema.get("titulo", {}).get(self.idioma, "").lower()
            respuesta = tema.get("respuesta", {}).get(self.idioma, "").lower()
            if termino in titulo or termino in respuesta:
                resultados.append({"titulo": tema["titulo"].get(self.idioma, ""),
                                   "contenido": tema["respuesta"].get(self.idioma, ""),
                                   "versiculos": [tema.get("cita", "")],
                                   "fuente": "",
                                   "copyright": ""})

        for articulo in temas_profundos:
            titulo = articulo.get("titulo", "").lower()
            contenido = articulo.get("contenido", "").lower()
            if termino in titulo or termino in contenido:
                resultados.append(articulo)

        for resultado in resultados:
            btn = Button(
                text=resultado.get("titulo", "")[:100],
                size_hint_y=None,
                height=80,
                font_size=22,
                background_color=(0.3, 0.5, 0.9, 1)
            )
            btn.bind(on_press=lambda btn, art=resultado: self.mostrar_detalle(art))
            self.resultados_layout.add_widget(btn)
            self.resultados_layout.height += 90

    def mostrar_detalle(self, articulo):
        contenido = articulo.get("contenido", "")
        versiculos = articulo.get("versiculos", [])
        fuente = articulo.get("fuente", "")
        copyright_ = articulo.get("copyright", "")

        texto = f"{contenido}\n\n"
        if versiculos:
            texto += "Versículos:\n"
            for v in versiculos:
                if isinstance(v, dict):
                    cita = v.get("cita", "")
                    texto_verso = v.get("texto", "")
                    texto += f"{cita} - {texto_verso}\n"
                else:
                    texto += f"{v}\n"
            texto += "\n"

        if fuente:
            texto += f"Fuente: {fuente}\n"
        if copyright_:
            texto += f"© {copyright_}"

        contenido_label = Label(
            text=texto,
            font_size=20,
            size_hint_y=None,
            text_size=(Window.width * 0.85, None),
            halign='left',
            valign='top'
        )
        contenido_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        scrollview = ScrollView(size_hint=(1, 1))
        scrollview.add_widget(contenido_label)

        popup = Popup(
            title=articulo.get("titulo", ""),
            content=scrollview,
            size_hint=(0.95, 0.95)
        )
        popup.open()

    def volver(self, instancia):
        if self.volver_callback:
            self.volver_callback()