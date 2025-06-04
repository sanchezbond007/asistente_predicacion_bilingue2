from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle, Line
from utils.traducciones import obtener_texto

class ModernTextInput(TextInput):
    """TextInput personalizado con diseño moderno"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.foreground_color = (1, 1, 1, 1)  # White text
        self.cursor_color = (0.3, 0.7, 1, 1)  # Blue cursor
        self.selection_color = (0.3, 0.7, 1, 0.3)  # Blue selection
        
    def on_focus(self, instance, value):
        super().on_focus(instance, value)
        self.update_graphics()
    
    def update_graphics(self):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.focus:
                Color(0.2, 0.6, 1, 0.8)  # Blue when focused
            else:
                Color(0.3, 0.3, 0.3, 0.8)  # Gray when not focused
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
            
            # Border
            Color(0.5, 0.5, 0.5, 1) if not self.focus else Color(0.3, 0.7, 1, 1)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(10)), width=dp(2))

class PantallaCrearUsuario(Screen):
    def __init__(self, **kwargs):
        # Extraer callbacks personalizados
        self.guardar_callback = kwargs.pop('guardar_callback', None)
        self.volver_callback = kwargs.pop('volver_callback', None)
        self.idioma = kwargs.pop('idioma', 'es')
        
        super().__init__(**kwargs)
        self.name = 'crear_usuario'
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Layout principal con scroll
        scroll = ScrollView()
        
        layout_principal = BoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(20),
            size_hint_y=None
        )
        layout_principal.bind(minimum_height=layout_principal.setter('height'))
        
        # Gradiente de fondo
        with layout_principal.canvas.before:
            Color(0.1, 0.1, 0.15, 1)  # Dark blue-gray
            self.bg_rect = RoundedRectangle(
                pos=layout_principal.pos, 
                size=layout_principal.size,
                radius=[dp(0)]
            )
            layout_principal.bind(size=self._update_bg_rect, pos=self._update_bg_rect)
        
        # Header con icono y título
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(15)
        )
        
        # Icono de usuario
        icon_label = Label(
            text='👤',
            font_size=dp(45),
            size_hint_x=None,
            width=dp(60),
            color=(0.3, 0.7, 1, 1)
        )
        
        # Título
        titulo = Label(
            text=obtener_texto('crear_usuario').replace('_', ' ').title(),
            font_size=dp(32),
            bold=True,
            color=(1, 1, 1, 1),
            text_size=(None, None),
            halign='left',
            valign='middle'
        )
        
        header_layout.add_widget(icon_label)
        header_layout.add_widget(titulo)
        layout_principal.add_widget(header_layout)
        
        # Línea decorativa
        line_layout = BoxLayout(size_hint_y=None, height=dp(3))
        with line_layout.canvas:
            Color(0.3, 0.7, 1, 1)
            RoundedRectangle(pos=line_layout.pos, size=line_layout.size, radius=[dp(2)])
        layout_principal.add_widget(line_layout)
        
        # Espaciador
        layout_principal.add_widget(Label(size_hint_y=None, height=dp(20)))
        
        # Contenedor de campos con diseño en tarjeta
        card_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            padding=dp(20)
        )
        
        # Fondo de la tarjeta
        with card_layout.canvas.before:
            Color(0.15, 0.15, 0.2, 0.9)
            self.card_rect = RoundedRectangle(
                pos=card_layout.pos,
                size=card_layout.size,
                radius=[dp(15)]
            )
            card_layout.bind(size=self._update_card_rect, pos=self._update_card_rect)
        
        # Lista de campos con iconos
        campos = [
            ('nombre', 'Nombre', '👤'),
            ('apellido', 'Apellido', '👥'),
            ('telefono', 'Teléfono', '📱'),
            ('correo', 'Correo electrónico', '📧'),
            ('usuario', 'Nombre de usuario', '🔑'),
            ('contrasena', 'Contraseña', '🔒')
        ]
        
        self.inputs = {}
        
        for clave, placeholder, icono in campos:
            # Contenedor para cada campo
            campo_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(85),
                spacing=dp(8)
            )
            
            # Header del campo con icono y etiqueta
            campo_header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(25),
                spacing=dp(10)
            )
            
            icono_label = Label(
                text=icono,
                font_size=dp(16),
                size_hint_x=None,
                width=dp(25),
                color=(0.3, 0.8, 0.4, 1)  # Verde como el botón
            )
            
            try:
                texto_label = obtener_texto(clave)
            except:
                texto_label = placeholder
                
            etiqueta = Label(
                text=texto_label,
                font_size=dp(16),
                color=(1, 1, 1, 1),  # Blanco para mejor contraste
                text_size=(None, None),
                halign='left',
                valign='middle'
            )
            
            campo_header.add_widget(icono_label)
            campo_header.add_widget(etiqueta)
            campo_container.add_widget(campo_header)
            
            # Campo de entrada visible con fondo claro
            input_field = TextInput(
                hint_text=f"Ingresa tu {texto_label.lower()}",
                multiline=False,
                font_size=dp(16),
                size_hint_y=None,
                height=dp(45),
                password=(clave == 'contrasena'),
                background_color=(0.9, 0.9, 0.9, 1),  # Fondo blanco/gris claro
                foreground_color=(0, 0, 0, 1),  # Texto negro
                cursor_color=(0.3, 0.8, 0.4, 1),  # Cursor verde
                selection_color=(0.3, 0.8, 0.4, 0.3),  # Selección verde
                padding=[dp(15), dp(10)],
                border=(0, 0, 0, 0)  # Sin borde por defecto
            )
            
            # Fondo personalizado con borde verde
            with input_field.canvas.before:
                Color(0.95, 0.95, 0.95, 1)  # Fondo gris muy claro
                self.input_bg = RoundedRectangle(
                    pos=input_field.pos,
                    size=input_field.size,
                    radius=[dp(8)]
                )
                Color(0.3, 0.8, 0.4, 1)  # Borde verde
                self.input_border = Line(
                    rounded_rectangle=(input_field.x, input_field.y, input_field.width, input_field.height, dp(8)),
                    width=dp(2)
                )
            
            # Actualizar gráficos cuando cambie
            def update_input_graphics(input_widget):
                input_widget.canvas.before.clear()
                with input_widget.canvas.before:
                    # Fondo
                    Color(0.95, 0.95, 0.95, 1) if not input_widget.focus else Color(1, 1, 1, 1)
                    RoundedRectangle(pos=input_widget.pos, size=input_widget.size, radius=[dp(8)])
                    # Borde
                    if input_widget.focus:
                        Color(0.2, 0.7, 0.3, 1)  # Verde más intenso cuando tiene foco
                    else:
                        Color(0.3, 0.8, 0.4, 0.7)  # Verde normal
                    Line(
                        rounded_rectangle=(input_widget.x, input_widget.y, input_widget.width, input_widget.height, dp(8)),
                        width=dp(2)
                    )
            
            input_field.bind(pos=lambda x, y: update_input_graphics(input_field))
            input_field.bind(size=lambda x, y: update_input_graphics(input_field))
            input_field.bind(focus=lambda x, y: update_input_graphics(input_field))
            
            self.inputs[clave] = input_field
            campo_container.add_widget(input_field)
            card_layout.add_widget(campo_container)
        
        # Calcular altura de la tarjeta
        card_layout.height = len(campos) * dp(93) + dp(40)
        layout_principal.add_widget(card_layout)
        
        # Espaciador
        layout_principal.add_widget(Label(size_hint_y=None, height=dp(30)))
        
        # Botones con diseño moderno
        botones_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(130)
        )
        
        # Botón Guardar (principal)
        btn_guardar = Button(
            text=f"✓  {obtener_texto('aceptar').upper()}",
            size_hint_y=None,
            height=dp(55),
            font_size=dp(20),
            bold=True,
            background_color=(0, 0, 0, 0),  # Transparent
            color=(1, 1, 1, 1)
        )
        
        # Fondo personalizado para botón guardar
        with btn_guardar.canvas.before:
            Color(0.2, 0.7, 0.3, 1)  # Green
            self.btn_guardar_bg = RoundedRectangle(
                pos=btn_guardar.pos,
                size=btn_guardar.size,
                radius=[dp(25)]
            )
            btn_guardar.bind(size=lambda x, y: self._update_btn_guardar_bg(btn_guardar))
            btn_guardar.bind(pos=lambda x, y: self._update_btn_guardar_bg(btn_guardar))
        
        btn_guardar.bind(on_press=self.guardar_usuario)
        botones_layout.add_widget(btn_guardar)
        
        # Botón Volver (secundario)
        btn_volver = Button(
            text=f"←  {obtener_texto('volver').upper()}",
            size_hint_y=None,
            height=dp(55),
            font_size=dp(18),
            background_color=(0, 0, 0, 0),  # Transparent
            color=(0.8, 0.8, 0.8, 1)
        )
        
        # Fondo personalizado para botón volver
        with btn_volver.canvas.before:
            Color(0.4, 0.4, 0.4, 0.8)  # Gray
            self.btn_volver_bg = RoundedRectangle(
                pos=btn_volver.pos,
                size=btn_volver.size,
                radius=[dp(25)]
            )
            btn_volver.bind(size=lambda x, y: self._update_btn_volver_bg(btn_volver))
            btn_volver.bind(pos=lambda x, y: self._update_btn_volver_bg(btn_volver))
        
        btn_volver.bind(on_press=self.volver_login)
        botones_layout.add_widget(btn_volver)
        
        layout_principal.add_widget(botones_layout)
        
        # Espaciador final
        layout_principal.add_widget(Label(size_hint_y=None, height=dp(30)))
        
        scroll.add_widget(layout_principal)
        self.add_widget(scroll)
    
    def _update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size
    
    def _update_card_rect(self, instance, value):
        self.card_rect.pos = instance.pos
        self.card_rect.size = instance.size
    
    def _update_btn_guardar_bg(self, btn):
        self.btn_guardar_bg.pos = btn.pos
        self.btn_guardar_bg.size = btn.size
    
    def _update_btn_volver_bg(self, btn):
        self.btn_volver_bg.pos = btn.pos
        self.btn_volver_bg.size = btn.size
    
    def actualizar_textos(self):
        """Actualiza todos los textos de la interfaz"""
        self.clear_widgets()
        self.crear_interfaz()
    
    def guardar_usuario(self, instance):
        """Maneja el guardado del usuario con validaciones mejoradas"""
        datos_usuario = {}
        campos_vacios = []
        
        for campo, input_widget in self.inputs.items():
            valor = input_widget.text.strip()
            if not valor:
                try:
                    nombre_campo = obtener_texto(campo)
                except:
                    nombre_campo = campo
                campos_vacios.append(nombre_campo)
                # Resaltar campo vacío
                with input_widget.canvas.before:
                    Color(1, 0.3, 0.3, 0.3)  # Red highlight
                    RoundedRectangle(pos=input_widget.pos, size=input_widget.size, radius=[dp(10)])
            else:
                datos_usuario[campo] = valor
        
        if campos_vacios:
            self.mostrar_popup_moderno(
                "⚠️ Campos Requeridos",
                f"Por favor completa: {', '.join(campos_vacios)}",
                "error"
            )
            return
        
        # Validaciones específicas
        if '@' not in datos_usuario.get('correo', '') or '.' not in datos_usuario.get('correo', ''):
            self.mostrar_popup_moderno(
                "📧 Email Inválido",
                "Por favor ingresa un correo electrónico válido",
                "error"
            )
            return
        
        if len(datos_usuario.get('contrasena', '')) < 6:
            self.mostrar_popup_moderno(
                "🔒 Contraseña Débil",
                "La contraseña debe tener al menos 6 caracteres",
                "error"
            )
            return
        
        # Guardar usuario
        if self.guardar_callback:
            resultado = self.guardar_callback(datos_usuario)
            if resultado:
                self.mostrar_popup_moderno(
                    "✅ ¡Éxito!",
                    "Usuario creado correctamente",
                    "success",
                    self.volver_login
                )
        else:
            self.mostrar_popup_moderno(
                "✅ ¡Éxito!",
                "Usuario creado correctamente",
                "success",
                self.volver_login
            )
    
    def volver_login(self, instance=None):
        """Volver a la pantalla de login"""
        if self.volver_callback:
            self.volver_callback()
        else:
            if self.manager and self.manager.has_screen('login'):
                self.manager.current = 'login'
    
    def mostrar_popup_moderno(self, titulo, mensaje, tipo="info", callback=None):
        """Popup con diseño moderno"""
        content = BoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(20)
        )
        
        # Color según el tipo
        if tipo == "error":
            color_bg = (1, 0.3, 0.3, 0.9)
            color_texto = (1, 1, 1, 1)
        elif tipo == "success":
            color_bg = (0.3, 0.8, 0.4, 0.9)
            color_texto = (1, 1, 1, 1)
        else:
            color_bg = (0.2, 0.6, 1, 0.9)
            color_texto = (1, 1, 1, 1)
        
        # Fondo del contenido
        with content.canvas.before:
            Color(*color_bg)
            self.popup_bg = RoundedRectangle(
                pos=content.pos,
                size=content.size,
                radius=[dp(20)]
            )
            content.bind(size=lambda x, y: setattr(self.popup_bg, 'size', x.size))
            content.bind(pos=lambda x, y: setattr(self.popup_bg, 'pos', x.pos))
        
        label = Label(
            text=mensaje,
            font_size=dp(18),
            text_size=(dp(350), None),
            halign='center',
            valign='middle',
            color=color_texto
        )
        content.add_widget(label)
        
        btn_cerrar = Button(
            text="ENTENDIDO",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16),
            bold=True,
            background_color=(1, 1, 1, 0.2),
            color=(1, 1, 1, 1)
        )
        content.add_widget(btn_cerrar)
        
        popup = Popup(
            title=titulo,
            title_size=dp(20),
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=False,
            background_color=(0, 0, 0, 0),
            separator_color=(0, 0, 0, 0)
        )
        
        def cerrar_popup(instance):
            popup.dismiss()
            if callback:
                callback()
        
        btn_cerrar.bind(on_press=cerrar_popup)
        popup.open()