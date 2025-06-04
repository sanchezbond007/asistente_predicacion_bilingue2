import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line

# Asegura acceso al directorio raíz
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

class PantallaAvisoLegal(Screen):
    def __init__(self, continuar_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.name = 'aviso_legal'
        self.continuar_callback = continuar_callback or self._callback_por_defecto
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Layout principal
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(15), dp(25), dp(15), dp(15)]
        )
        
        # Fondo blanco
        with main_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = RoundedRectangle(
                pos=main_layout.pos, 
                size=main_layout.size
            )
            main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # Header compacto
        header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(70),
            spacing=dp(5)
        )
        
        # Icono
        icono = Label(
            text='⚖️',
            font_size=dp(25),
            size_hint_y=None,
            height=dp(30),
            color=(0.2, 0.4, 0.7, 1)
        )
        header.add_widget(icono)
        
        # Título
        titulo = Label(
            text='Aviso Legal / Legal Notice',
            font_size=dp(16),
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0.2, 0.2, 0.2, 1)
        )
        header.add_widget(titulo)
        
        main_layout.add_widget(header)
        
        # ScrollView con contenido completo
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(4),
            scroll_type=['content']
        )
        
        # Contenedor scrolleable
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(10),
            spacing=dp(8)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Fondo del contenido
        with content_layout.canvas.before:
            Color(0.96, 0.96, 0.96, 1)
            self.content_bg = RoundedRectangle(
                pos=content_layout.pos,
                size=content_layout.size,
                radius=[dp(10)]
            )
            content_layout.bind(size=self._update_content_bg, pos=self._update_content_bg)
        
        # Texto completo dividido en secciones más manejables
        secciones = [
            ("📋 TÉRMINOS DE USO", 
             "Este asistente es una herramienta personal para el estudio bíblico y la predicación. "
             "No representa ninguna organización religiosa oficial. El contenido es únicamente "
             "para fines educativos y de estudio personal."),
            
            ("PRIVACIDAD Y SEGURIDAD:", 
             "• La aplicación respeta tu privacidad\n"
             "• Los datos se almacenan localmente\n"
             "• No se comparte información personal\n"
             "• No requiere conexión a internet\n"
             "• Uso responsable bajo tu criterio"),
            
            ("RESPONSABILIDADES:", 
             "• Usar la aplicación responsablemente\n"
             "• Verificar información con fuentes oficiales\n"
             "• Respetar derechos de autor\n"
             "• Solo para uso personal"),
            
            ("📋 TERMS OF USE", 
             "This assistant is a personal tool for Bible study and preaching. "
             "It does not represent any official religious organization. The content "
             "is solely for educational and personal study."),
            
            ("PRIVACY & SECURITY:", 
             "• App respects your privacy\n"
             "• Data stored locally\n"
             "• No personal info shared\n"
             "• No internet required\n"
             "• Responsible use at discretion"),
            
            ("RESPONSIBILITIES:", 
             "• Use application responsibly\n"
             "• Verify info with official sources\n"
             "• Respect copyright\n"
             "• Personal use only"),
            
            ("🤝 ACEPTACIÓN / ACCEPTANCE", 
             "Al continuar, aceptas estos términos.\n"
             "By continuing, you accept these terms.\n\n"
             "📅 Versión 1.0 | Junio 2025")
        ]
        
        # Agregar cada sección como un label separado
        for titulo_seccion, contenido_seccion in secciones:
            # Título de sección
            if titulo_seccion.startswith(("📋", "🤝")):
                titulo_label = Label(
                    text=titulo_seccion,
                    font_size=dp(13),
                    bold=True,
                    size_hint_y=None,
                    color=(0.1, 0.1, 0.1, 1),
                    halign='left',
                    text_size=(None, None)
                )
                titulo_label.bind(texture_size=titulo_label.setter('size'))
                content_layout.add_widget(titulo_label)
            
            # Contenido de sección
            contenido_label = Label(
                text=contenido_seccion if not titulo_seccion.startswith(("📋", "🤝")) else f"{titulo_seccion}\n\n{contenido_seccion}",
                font_size=dp(11),
                size_hint_y=None,
                color=(0.2, 0.2, 0.2, 1),
                halign='left',
                valign='top',
                text_size=(None, None),
                line_height=1.1
            )
            
            # Configurar text_size dinámicamente
            def update_text_width(label, *args):
                label.text_size = (Window.width - dp(80), None)
                label.texture_update()
            
            contenido_label.bind(size=update_text_width)
            Window.bind(size=lambda *args: update_text_width(contenido_label))
            
            # Forzar actualización inicial
            contenido_label.text_size = (Window.width - dp(80), None)
            contenido_label.texture_update()
            contenido_label.height = contenido_label.texture_size[1] + dp(5)
            
            content_layout.add_widget(contenido_label)
            
            # Separador entre secciones (excepto la última)
            if titulo_seccion != "🤝 ACEPTACIÓN / ACCEPTANCE":
                separator = Label(
                    text="",
                    size_hint_y=None,
                    height=dp(8)
                )
                content_layout.add_widget(separator)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        # Botón de aceptar
        btn_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(70),
            spacing=dp(5)
        )
        
        btn_aceptar = Button(
            text="✓ Aceptar / Accept",
            size_hint_y=None,
            height=dp(45),
            font_size=dp(16),
            bold=True,
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            on_press=self.continuar_callback
        )
        
        # Fondo del botón
        with btn_aceptar.canvas.before:
            Color(0.2, 0.7, 0.3, 1)
            self.btn_bg = RoundedRectangle(
                pos=btn_aceptar.pos,
                size=btn_aceptar.size,
                radius=[dp(22)]
            )
            btn_aceptar.bind(size=self._update_btn_bg, pos=self._update_btn_bg)
        
        btn_layout.add_widget(btn_aceptar)
        
        # Nota
        nota = Label(
            text="👆 Toca el botón verde para continuar",
            font_size=dp(10),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(20),
            italic=True
        )
        btn_layout.add_widget(nota)
        
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)
    
    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def _update_content_bg(self, instance, value):
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size
    
    def _update_btn_bg(self, instance, value):
        self.btn_bg.pos = instance.pos
        self.btn_bg.size = instance.size
    
    def _callback_por_defecto(self, instancia):
        print("✅ Aviso legal aceptado - Continuando...")
        if self.manager and hasattr(self.manager, 'current'):
            if self.manager.has_screen('login'):
                self.manager.current = 'login'
            else:
                print("⚠️ No se encontró la pantalla 'login'")
    
    def actualizar_textos(self):
        self.clear_widgets()
        self.crear_interfaz()# Actualizado Mon Jun  2 22:58:27 EDT 2025
# Actualizado Mon Jun  2 22:59:06 EDT 2025
# Actualizado Mon Jun  2 23:00:15 EDT 2025
