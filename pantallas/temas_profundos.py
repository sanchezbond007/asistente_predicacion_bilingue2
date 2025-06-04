import os
import json
import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock

class PantallaTemasProfundos(Screen):
    def __init__(self, **kwargs):
        self.volver_callback = kwargs.pop('volver_callback', None)
        self.idioma_inicial = kwargs.pop('idioma', 'es')
        
        super(PantallaTemasProfundos, self).__init__(**kwargs)
        self.usuario_actual = None
        self.idioma_usuario = self.idioma_inicial
        self.todos_los_temas = []
        self.temas_mostrados = []
        self.temas_por_pagina = 10
        
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # Botón para nuevos temas
        self.btn_nuevas_sugerencias = Button(
            text='Nuevos Temas',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.3, 0.6, 0.3, 1)
        )
        self.btn_nuevas_sugerencias.bind(on_press=self.generar_nuevos_temas)
        main_layout.add_widget(self.btn_nuevas_sugerencias)
        
        # Botón para buscar
        self.btn_buscar = Button(
            text='Buscar',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.6, 0.3, 0.6, 1)
        )
        self.btn_buscar.bind(on_press=self.mostrar_busqueda)
        main_layout.add_widget(self.btn_buscar)
        
        # Scroll con contenido
        scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        scroll.add_widget(self.content_layout)
        main_layout.add_widget(scroll)
        
        # Botón volver
        self.btn_volver = Button(
            text='Volver',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.4, 0.6, 1)
        )
        self.btn_volver.bind(on_press=self.ir_al_menu)
        main_layout.add_widget(self.btn_volver)
        
        self.add_widget(main_layout)

    def on_enter(self):
        self.idioma_usuario = self.idioma_inicial
        self.actualizar_idioma()
        self.cargar_todos_los_temas()
        self.cargar_temas_iniciales()

    def actualizar_idioma(self):
        traducciones = {
            'volver': {'es': 'Volver', 'en': 'Back'},
            'nuevos_temas': {'es': 'Nuevos Temas', 'en': 'New Topics'},
            'buscar': {'es': 'Buscar', 'en': 'Search'}
        }
        
        idioma = self.idioma_usuario.lower().strip()
        
        self.btn_volver.text = traducciones['volver'].get(idioma, 'Volver')
        self.btn_nuevas_sugerencias.text = traducciones['nuevos_temas'].get(idioma, 'Nuevos Temas')
        self.btn_buscar.text = traducciones['buscar'].get(idioma, 'Buscar')

    def cargar_temas_desde_directorio_profundos(self):
        try:
            directorio_temas = os.path.join('datos', 'temas_profundos')
            
            if not os.path.exists(directorio_temas):
                return []
            
            todos_los_temas = []
            
            for archivo in os.listdir(directorio_temas):
                if archivo.endswith('.json'):
                    try:
                        ruta_archivo = os.path.join(directorio_temas, archivo)
                        with open(ruta_archivo, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                        
                        if isinstance(data, list):
                            todos_los_temas.extend(data)
                        elif isinstance(data, dict):
                            todos_los_temas.append(data)
                            
                    except Exception as e:
                        print(f"Error cargando {archivo}: {e}")
                        continue
            
            return todos_los_temas
            
        except Exception as e:
            print(f"Error cargando temas profundos: {e}")
            return []

    def cargar_todos_los_temas(self):
        self.todos_los_temas = self.cargar_temas_desde_directorio_profundos()

    def obtener_temas_no_mostrados(self, cantidad):
        if not self.todos_los_temas:
            return []
        
        temas_disponibles = [tema for tema in self.todos_los_temas if tema not in self.temas_mostrados]
        
        if len(temas_disponibles) < cantidad:
            random.shuffle(self.todos_los_temas)
            self.temas_mostrados = []
            temas_disponibles = self.todos_los_temas
        
        temas_seleccionados = temas_disponibles[:cantidad]
        self.temas_mostrados.extend(temas_seleccionados)
        
        return temas_seleccionados

    def obtener_preguntas_predeterminadas(self):
        return [
            {"titulo": {"es": "¿Cómo mantener la esperanza?", "en": "How to maintain hope?"}, "contenido": {"es": "A través de la oración y el estudio.", "en": "Through prayer and study."}, "conclusion": {"es": "La esperanza fortalece la fe.", "en": "Hope strengthens faith."}},
            {"titulo": {"es": "¿Qué es la vida eterna?", "en": "What is eternal life?"}, "contenido": {"es": "Vida sin fin bajo el Reino.", "en": "Endless life under the Kingdom."}, "conclusion": {"es": "Regalo de Dios para los fieles.", "en": "God's gift to the faithful."}},
            {"titulo": {"es": "¿Cómo enfrentar las pruebas?", "en": "How to face trials?"}, "contenido": {"es": "Con fe en Jehová.", "en": "With faith in Jehovah."}, "conclusion": {"es": "Las pruebas fortalecen.", "en": "Trials strengthen us."}},
            {"titulo": {"es": "¿Qué es el perdón?", "en": "What is forgiveness?"}, "contenido": {"es": "Perdonar de corazón.", "en": "Forgiving from the heart."}, "conclusion": {"es": "El perdón trae paz.", "en": "Forgiveness brings peace."}},
            {"titulo": {"es": "¿Cómo ser humilde?", "en": "How to be humble?"}, "contenido": {"es": "Reconociendo nuestra dependencia.", "en": "Recognizing our dependence."}, "conclusion": {"es": "La humildad agrada a Dios.", "en": "Humility pleases God."}}
        ]

    def cargar_temas_iniciales(self):
        self.content_layout.clear_widgets()
        self.temas_mostrados = []
        
        if not self.todos_los_temas:
            temas_a_mostrar = self.obtener_preguntas_predeterminadas()[:self.temas_por_pagina]
        else:
            temas_a_mostrar = self.obtener_temas_no_mostrados(self.temas_por_pagina)
        
        self.agregar_temas_a_layout(temas_a_mostrar)

    def agregar_temas_a_layout(self, temas):
        if not temas:
            return
        
        for tema in temas:
            try:
                titulo = tema.get('titulo', {})
                idioma = self.idioma_usuario.lower().strip()
                
                if isinstance(titulo, dict):
                    texto_boton = titulo.get(idioma, titulo.get('es', 'Sin título'))
                else:
                    texto_boton = str(titulo)
                
                texto_boton_display = f"• {texto_boton}"
                
                btn = Button(
                    text=texto_boton_display,
                    size_hint_y=None,
                    height=dp(70),
                    background_color=(0.2, 0.4, 0.6, 1),
                    text_size=(dp(280), None),
                    halign='left',
                    valign='middle'
                )
                btn.bind(on_press=lambda x, t=tema: self.mostrar_detalle_tema_profundo(t))
                self.content_layout.add_widget(btn)
                
            except Exception as e:
                print(f"Error procesando tema: {e}")
                continue

    def mostrar_detalle_tema_profundo(self, tema):
        idioma = self.idioma_usuario.lower().strip()
        
        # Extraer información
        titulo = tema.get('titulo', {})
        if isinstance(titulo, dict):
            titulo_texto = titulo.get(idioma, titulo.get('es', 'Sin título'))
        else:
            titulo_texto = str(titulo)
        
        contenido = tema.get('contenido', {})
        if isinstance(contenido, dict):
            contenido_texto = contenido.get(idioma, contenido.get('es', 'Sin contenido'))
        else:
            contenido_texto = str(contenido)
        
        conclusion = tema.get('conclusion', {})
        if isinstance(conclusion, dict):
            conclusion_texto = conclusion.get(idioma, conclusion.get('es', ''))
        else:
            conclusion_texto = str(conclusion) if conclusion else ''
        
        # Construir texto completo
        lineas = [titulo_texto, ""]
        
        if contenido_texto:
            intro_label = "Introduction:" if idioma == 'en' else "Introducción:"
            lineas.extend([intro_label, "", contenido_texto, ""])
        
        if conclusion_texto:
            concl_label = "Conclusion:" if idioma == 'en' else "Conclusión:"
            lineas.extend([concl_label, "", conclusion_texto])
        
        texto_completo = "\n".join(lineas)
        
        # Crear popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        container.bind(minimum_height=container.setter('height'))
        
        label_contenido = Label(
            text=texto_completo,
            text_size=(dp(300), None),
            halign='left',
            valign='top',
            markup=False,
            color=(1, 1, 1, 1),
            font_size='14sp',
            size_hint_y=None
        )
        label_contenido.bind(texture_size=label_contenido.setter('size'))
        
        container.add_widget(label_contenido)
        
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        scroll.add_widget(container)
        content.add_widget(scroll)
        
        # Botones
        botones_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        btn_copiar = Button(
            text='📋 Copy' if idioma == 'en' else '📋 Copiar',
            background_color=(0.3, 0.6, 0.3, 1)
        )
        btn_copiar.bind(on_press=lambda x: self.copiar_tema(texto_completo))
        botones_layout.add_widget(btn_copiar)
        
        btn_cerrar = Button(
            text='Close' if idioma == 'en' else 'Cerrar',
            background_color=(0.6, 0.3, 0.3, 1)
        )
        botones_layout.add_widget(btn_cerrar)
        
        content.add_widget(botones_layout)
        
        popup_titulo = titulo_texto if len(titulo_texto) < 25 else titulo_texto[:22] + "..."
        popup = Popup(
            title=popup_titulo,
            content=content,
            size_hint=(0.95, 0.8),
            auto_dismiss=True,
            separator_color=[0.2, 0.4, 0.6, 1],
            title_color=[1, 1, 1, 1],
            title_size='15sp'
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        
        def scroll_al_tope(*args):
            scroll.scroll_y = 1
        
        popup.bind(on_open=lambda *args: Clock.schedule_once(scroll_al_tope, 0.1))
        popup.open()

    def generar_nuevos_temas(self, instance):
        if self.todos_los_temas:
            random.shuffle(self.todos_los_temas)
        
        self.temas_mostrados = []
        self.cargar_temas_iniciales()

    def mostrar_busqueda(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        idioma = self.idioma_usuario.lower().strip()
        instrucciones = {
            'es': 'Escriba una palabra clave para buscar:',
            'en': 'Enter a keyword to search:'
        }
        texto_instrucciones = instrucciones.get(idioma, instrucciones['es'])
        
        label_instrucciones = Label(
            text=texto_instrucciones,
            size_hint_y=None,
            height=dp(40),
            text_size=(dp(300), None),
            halign='center'
        )
        content.add_widget(label_instrucciones)
        
        self.input_busqueda = TextInput(
            hint_text='Palabra clave...' if idioma == 'es' else 'Keyword...',
            size_hint_y=None,
            height=dp(40),
            multiline=False
        )
        content.add_widget(self.input_busqueda)
        
        botones_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        btn_buscar_popup = Button(
            text='Buscar' if idioma == 'es' else 'Search',
            background_color=(0.3, 0.6, 0.3, 1)
        )
        btn_buscar_popup.bind(on_press=self.ejecutar_busqueda_profundos)
        botones_layout.add_widget(btn_buscar_popup)
        
        btn_cancelar = Button(
            text='Cancelar' if idioma == 'es' else 'Cancel',
            background_color=(0.6, 0.3, 0.3, 1)
        )
        btn_cancelar.bind(on_press=self.cerrar_popup_busqueda)
        botones_layout.add_widget(btn_cancelar)
        
        content.add_widget(botones_layout)
        
        titulo_popup = 'Buscar Temas' if idioma == 'es' else 'Search Topics'
        self.popup_busqueda = Popup(
            title=titulo_popup,
            content=content,
            size_hint=(0.9, 0.4),
            auto_dismiss=False
        )
        self.popup_busqueda.open()

    def ejecutar_busqueda_profundos(self, instance):
        palabra_clave = self.input_busqueda.text.strip().lower()
        
        if not palabra_clave:
            return
        
        self.popup_busqueda.dismiss()
        
        temas_encontrados = []
        idioma = self.idioma_usuario.lower().strip()
        
        for tema in self.todos_los_temas:
            try:
                encontrado = False
                
                # Buscar en título
                titulo = tema.get('titulo', {})
                if isinstance(titulo, dict):
                    texto_titulo = titulo.get(idioma, titulo.get('es', ''))
                else:
                    texto_titulo = str(titulo)
                
                if palabra_clave in texto_titulo.lower():
                    encontrado = True
                
                # Buscar en contenido
                if not encontrado:
                    contenido = tema.get('contenido', {})
                    if isinstance(contenido, dict):
                        texto_contenido = contenido.get(idioma, contenido.get('es', ''))
                    else:
                        texto_contenido = str(contenido)
                    
                    if palabra_clave in texto_contenido.lower():
                        encontrado = True
                
                if encontrado:
                    temas_encontrados.append(tema)
                    
            except Exception as e:
                continue
        
        # Mostrar resultados
        self.content_layout.clear_widgets()
        
        if temas_encontrados:
            texto_resultados = f"Resultados para '{palabra_clave}': {len(temas_encontrados)} temas encontrados"
            if idioma == 'en':
                texto_resultados = f"Results for '{palabra_clave}': {len(temas_encontrados)} topics found"
        else:
            texto_resultados = f"No se encontraron temas para '{palabra_clave}'"
            if idioma == 'en':
                texto_resultados = f"No topics found for '{palabra_clave}'"
        
        label_resultados = Label(
            text=texto_resultados,
            size_hint_y=None,
            height=dp(50),
            text_size=(dp(300), None),
            halign='center',
            color=(1, 1, 0, 1)
        )
        self.content_layout.add_widget(label_resultados)
        
        if temas_encontrados:
            self.agregar_temas_a_layout(temas_encontrados)

    def cerrar_popup_busqueda(self, instance):
        self.popup_busqueda.dismiss()

    def copiar_tema(self, texto):
        try:
            from kivy.utils import platform
            if platform == 'android':
                print("📋 Texto copiado (funcionalidad limitada en Android)")
            else:
                import pyperclip
                pyperclip.copy(texto)
                print("📋 Texto copiado al portapapeles")
        except Exception as e:
            print(f"Error copiando texto: {e}")

    def ir_al_menu(self, instance):
        if self.volver_callback:
            self.volver_callback(instance)
        else:
            self.manager.current = 'menu'