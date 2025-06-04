# pantallas/send_resume.py - VERSIÓN COMPLETA FINAL CON FORMATO PROFESIONAL
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime
import json
import os
import re

class HistorialSesion:
    """Clase para manejar el historial global de la sesión con datos del interesado"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HistorialSesion, cls).__new__(cls)
            cls._instance.historial = []
            cls._instance.sesion_actual = None
            cls._instance.datos_interesado = None
            print("🆕 Nueva instancia de HistorialSesion creada")
        return cls._instance
    
    def iniciar_nueva_sesion(self, datos_interesado):
        """Iniciar una nueva sesión con datos del interesado"""
        self.datos_interesado = datos_interesado
        self.sesion_actual = {
            'inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'interesado': datos_interesado,
            'consultas': []
        }
        print(f"🆕 Nueva sesión iniciada para: {datos_interesado['nombre']}")
        print(f"👤 Testigo: {datos_interesado['testigo']}")
    
    def obtener_datos_interesado(self):
        """Retorna los datos del interesado actual"""
        return self.datos_interesado if self.datos_interesado else {}
    
    def agregar_consulta(self, fuente, titulo, contenido, idioma='es'):
        """Agrega una nueva consulta al historial"""
        if self.sesion_actual is None:
            print("⚠️ No hay sesión activa. Creando sesión temporal...")
            self.iniciar_sesion_temporal()
        
        consulta = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'fuente': fuente,  # 'sugerencias', 'temas_profundos', 'buscar'
            'titulo': titulo,
            'contenido': contenido,
            'idioma': idioma
        }
        
        self.sesion_actual['consultas'].append(consulta)
        print(f"📝 Nueva consulta agregada: {fuente} - {titulo[:50]}...")
    
    def iniciar_sesion_temporal(self):
        """Crear sesión temporal si no existe ninguna"""
        datos_temporales = {
            'nombre': 'Sesión Temporal',
            'telefono': '',
            'email': '',
            'testigo': 'Usuario',
            'fecha_inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'idioma': 'es'
        }
        self.iniciar_nueva_sesion(datos_temporales)
    
    def obtener_historial_sesion(self):
        """Retorna el historial de la sesión actual"""
        if self.sesion_actual is None:
            return {
                'inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'interesado': {},
                'consultas': []
            }
        return self.sesion_actual
    
    def limpiar_sesion(self):
        """Limpia el historial de la sesión actual PERO mantiene datos del interesado"""
        if self.sesion_actual:
            datos_interesado = self.sesion_actual['interesado']
            self.sesion_actual = {
                'inicio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'interesado': datos_interesado,
                'consultas': []
            }
            print("🧹 Historial de consultas limpiado (datos del interesado mantenidos)")
        else:
            print("⚠️ No hay sesión activa para limpiar")
    
    def finalizar_sesion(self):
        """Finaliza la sesión actual completamente"""
        if self.sesion_actual:
            nombre = self.sesion_actual['interesado'].get('nombre', 'Desconocido')
            print(f"🏁 Sesión finalizada para: {nombre}")
            
            # Guardar en historial general si es necesario
            self.historial.append(self.sesion_actual.copy())
            
            # Limpiar sesión actual
            self.sesion_actual = None
            self.datos_interesado = None
        else:
            print("⚠️ No hay sesión activa para finalizar")
    
    def contar_consultas(self):
        """Retorna el número de consultas en la sesión"""
        if self.sesion_actual:
            return len(self.sesion_actual['consultas'])
        return 0
    
    def obtener_resumen_sesion(self):
        """Obtiene un resumen completo de la sesión actual"""
        if not self.sesion_actual:
            return "No hay sesión activa"
        
        datos = self.sesion_actual['interesado']
        consultas = self.sesion_actual['consultas']
        
        resumen = f"""
📋 RESUMEN DE SESIÓN
{'='*40}
👤 Interesado: {datos.get('nombre', 'N/A')}
📞 Teléfono: {datos.get('telefono', 'N/A')}
📧 Email: {datos.get('email', 'N/A')}
🙋‍♂️ Testigo: {datos.get('testigo', 'N/A')}
🕐 Inicio: {self.sesion_actual['inicio']}
📊 Consultas realizadas: {len(consultas)}
        """
        
        return resumen.strip()
    
    def tiene_sesion_activa(self):
        """Verifica si hay una sesión activa"""
        return self.sesion_actual is not None
    
    def get_info_for_sharing(self):
        """Obtiene información formateada para compartir"""
        if not self.datos_interesado:
            return {
                'destinatario': '',
                'telefono': '',
                'email': '',
                'testigo': ''
            }
        
        return {
            'destinatario': self.datos_interesado.get('nombre', ''),
            'telefono': self.datos_interesado.get('telefono', ''),
            'email': self.datos_interesado.get('email', ''),
            'testigo': self.datos_interesado.get('testigo', '')
        }

class PantallaSendResume(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        self.historial = HistorialSesion()
        
        # Textos en diferentes idiomas
        self.textos = {
            'es': {
                'titulo': 'Enviar Resumen de Estudio',
                'historial_titulo': 'Historial de la Sesión',
                'no_consultas': 'No hay consultas en esta sesión',
                'consultas_encontradas': 'consultas encontradas',
                'personalizar_titulo': 'Personalizar Resumen',
                'mensaje_titulo': 'Mensaje personalizado (opcional):',
                'mensaje_placeholder': 'Escribe un mensaje personal aquí...',
                'incluir_timestamp': 'Incluir fecha y hora',
                'incluir_fuente': 'Incluir fuente de cada consulta',
                'formato_titulo': 'Formato del resumen:',
                'formato_completo': 'Completo (título + contenido)',
                'formato_titulos': 'Solo títulos',
                'formato_resumido': 'Resumido',
                'enviar_titulo': 'Opciones de Envío',
                'btn_whatsapp': '📱 WhatsApp',
                'btn_email': '📧 Email',
                'btn_copiar': '📋 Copiar',
                'btn_generar': 'Generar Vista Previa',
                'btn_limpiar': '🧹 Limpiar Historial',
                'btn_volver': 'Volver al Menú',
                'vista_previa_titulo': 'Vista Previa del Resumen',
                'confirmar_limpiar': '¿Limpiar Historial?',
                'confirmar_limpiar_texto': '¿Estás seguro de que quieres limpiar el historial de esta sesión?',
                'si': 'Sí',
                'no': 'No',
                'cerrar': 'Cerrar',
                'resumen_generado': 'Resumen Generado',
                'resumen_copiado': 'Resumen copiado exitosamente',
                'error_titulo': 'Error',
                'error_sin_consultas': 'No hay consultas para incluir en el resumen',
                'desde_fuente': 'desde',
                'hora': 'Hora:',
                'fuente': 'Fuente:',
                'btn_agregar_prueba': '+ Agregar Consulta de Prueba',
                'whatsapp_titulo': 'WhatsApp',
                'email_titulo': 'Email',
                'consulta_agregada': 'Consulta Agregada',
                'nueva_consulta_agregada': 'Nueva consulta de prueba agregada',
                'historial_limpiado': 'Historial Limpiado',
                'historial_limpiado_texto': 'Historial de sesión limpiado correctamente',
                'email_exito': 'Cliente de email abierto con el resumen',
                'email_error': 'Error abriendo email. Usa "Copiar" para obtener el texto',
                'whatsapp_exito': 'WhatsApp Web abierto con el resumen',
                'whatsapp_error': 'Error abriendo WhatsApp. Usa "Copiar" para obtener el texto'
            },
            'en': {
                'titulo': 'Send Study Summary',
                'historial_titulo': 'Session History',
                'no_consultas': 'No queries in this session',
                'consultas_encontradas': 'queries found',
                'personalizar_titulo': 'Customize Summary',
                'mensaje_titulo': 'Custom message (optional):',
                'mensaje_placeholder': 'Write a personal message here...',
                'incluir_timestamp': 'Include date and time',
                'incluir_fuente': 'Include source of each query',
                'formato_titulo': 'Summary format:',
                'formato_completo': 'Complete (title + content)',
                'formato_titulos': 'Titles only',
                'formato_resumido': 'Summary',
                'enviar_titulo': 'Send Options',
                'btn_whatsapp': '📱 WhatsApp',
                'btn_email': '📧 Email',
                'btn_copiar': '📋 Copy',
                'btn_generar': 'Generate Preview',
                'btn_limpiar': '🧹 Clear History',
                'btn_volver': 'Back to Menu',
                'vista_previa_titulo': 'Summary Preview',
                'confirmar_limpiar': 'Clear History?',
                'confirmar_limpiar_texto': 'Are you sure you want to clear this session\'s history?',
                'si': 'Yes',
                'no': 'No',
                'cerrar': 'Close',
                'resumen_generado': 'Summary Generated',
                'resumen_copiado': 'Summary copied successfully',
                'error_titulo': 'Error',
                'error_sin_consultas': 'No queries to include in summary',
                'desde_fuente': 'from',
                'hora': 'Time:',
                'fuente': 'Source:',
                'btn_agregar_prueba': '+ Add Test Query',
                'whatsapp_titulo': 'WhatsApp',
                'email_titulo': 'Email',
                'consulta_agregada': 'Query Added',
                'nueva_consulta_agregada': 'New test query added',
                'historial_limpiado': 'History Cleared',
                'historial_limpiado_texto': 'Session history cleared successfully',
                'email_exito': 'Email client opened with the summary',
                'email_error': 'Error opening email. Use "Copy" to get the text',
                'whatsapp_exito': 'WhatsApp Web opened with the summary',
                'whatsapp_error': 'Error opening WhatsApp. Use "Copy" to get the text'
            }
        }
        
        self.construir_interfaz()
    
    def construir_interfaz(self):
        """Construir la interfaz de usuario"""
        self.clear_widgets()
        
        # Layout principal
        layout_principal = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(15)
        )
        
        # Título
        titulo = Label(
            text=self.textos[self.idioma]['titulo'],
            font_size=dp(22),
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.6, 0.9, 1)
        )
        layout_principal.add_widget(titulo)
        
        # Scroll principal
        scroll_principal = ScrollView()
        contenido_scroll = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        contenido_scroll.bind(minimum_height=contenido_scroll.setter('height'))
        
        # Sección: Historial
        self.crear_seccion_historial(contenido_scroll)
        
        # Sección: Personalización
        self.crear_seccion_personalizacion(contenido_scroll)
        
        # Sección: Envío
        self.crear_seccion_envio(contenido_scroll)
        
        scroll_principal.add_widget(contenido_scroll)
        layout_principal.add_widget(scroll_principal)
        
        # Botones inferiores
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Botón agregar consulta de prueba
        btn_prueba = Button(
            text=self.textos[self.idioma]['btn_agregar_prueba'],
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=dp(10)
        )
        btn_prueba.bind(on_press=self.agregar_consulta_prueba)
        botones_layout.add_widget(btn_prueba)
        
        # Botón limpiar historial
        btn_limpiar = Button(
            text=self.textos[self.idioma]['btn_limpiar'],
            background_color=(0.7, 0.4, 0.2, 1),
            font_size=dp(10)
        )
        btn_limpiar.bind(on_press=self.confirmar_limpiar_historial)
        botones_layout.add_widget(btn_limpiar)
        
        # Botón volver
        btn_volver = Button(
            text=self.textos[self.idioma]['btn_volver'],
            background_color=(0.7, 0.3, 0.3, 1),
            font_size=dp(10)
        )
        btn_volver.bind(on_press=self.volver_menu)
        botones_layout.add_widget(btn_volver)
        
        layout_principal.add_widget(botones_layout)
        self.add_widget(layout_principal)
    
    def crear_seccion_historial(self, parent_layout):
        """Crear la sección de historial"""
        # Título de sección
        titulo_historial = Label(
            text=self.textos[self.idioma]['historial_titulo'],
            font_size=dp(18),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 0.8, 1)
        )
        parent_layout.add_widget(titulo_historial)
        
        # Contenedor del historial
        self.historial_container = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(150)
        )
        
        # ScrollView para el historial
        historial_scroll = ScrollView(
            size_hint_y=None,
            height=dp(150)
        )
        
        self.historial_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None
        )
        self.historial_layout.bind(minimum_height=self.historial_layout.setter('height'))
        
        historial_scroll.add_widget(self.historial_layout)
        self.historial_container.add_widget(historial_scroll)
        parent_layout.add_widget(self.historial_container)
        
        # Actualizar historial
        self.actualizar_historial()
    
    def crear_seccion_personalizacion(self, parent_layout):
        """Crear la sección de personalización"""
        # Título de sección
        titulo_personalizacion = Label(
            text=self.textos[self.idioma]['personalizar_titulo'],
            font_size=dp(18),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 0.8, 1)
        )
        parent_layout.add_widget(titulo_personalizacion)
        
        # Mensaje personalizado
        mensaje_label = Label(
            text=self.textos[self.idioma]['mensaje_titulo'],
            font_size=dp(14),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        mensaje_label.bind(size=mensaje_label.setter('text_size'))
        parent_layout.add_widget(mensaje_label)
        
        self.mensaje_input = TextInput(
            hint_text=self.textos[self.idioma]['mensaje_placeholder'],
            multiline=True,
            size_hint_y=None,
            height=dp(80),
            font_size=dp(12)
        )
        parent_layout.add_widget(self.mensaje_input)
        
        # Opciones con checkboxes
        opciones_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(70)
        )
        
        # Checkbox incluir timestamp
        timestamp_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30)
        )
        self.checkbox_timestamp = CheckBox(
            active=True,
            size_hint_x=None,
            width=dp(30)
        )
        timestamp_label = Label(
            text=self.textos[self.idioma]['incluir_timestamp'],
            font_size=dp(12),
            halign='left'
        )
        timestamp_label.bind(size=timestamp_label.setter('text_size'))
        timestamp_layout.add_widget(self.checkbox_timestamp)
        timestamp_layout.add_widget(timestamp_label)
        opciones_layout.add_widget(timestamp_layout)
        
        # Checkbox incluir fuente
        fuente_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30)
        )
        self.checkbox_fuente = CheckBox(
            active=True,
            size_hint_x=None,
            width=dp(30)
        )
        fuente_label = Label(
            text=self.textos[self.idioma]['incluir_fuente'],
            font_size=dp(12),
            halign='left'
        )
        fuente_label.bind(size=fuente_label.setter('text_size'))
        fuente_layout.add_widget(self.checkbox_fuente)
        fuente_layout.add_widget(fuente_label)
        opciones_layout.add_widget(fuente_layout)
        
        parent_layout.add_widget(opciones_layout)
        
        # Formato del resumen
        formato_label = Label(
            text=self.textos[self.idioma]['formato_titulo'],
            font_size=dp(14),
            size_hint_y=None,
            height=dp(25),
            halign='left'
        )
        formato_label.bind(size=formato_label.setter('text_size'))
        parent_layout.add_widget(formato_label)
        
        self.formato_spinner = Spinner(
            text=self.textos[self.idioma]['formato_completo'],
            values=[
                self.textos[self.idioma]['formato_completo'],
                self.textos[self.idioma]['formato_titulos'],
                self.textos[self.idioma]['formato_resumido']
            ],
            size_hint_y=None,
            height=dp(40),
            font_size=dp(12)
        )
        parent_layout.add_widget(self.formato_spinner)
    
    def crear_seccion_envio(self, parent_layout):
        """Crear la sección de envío"""
        # Título de sección
        titulo_envio = Label(
            text=self.textos[self.idioma]['enviar_titulo'],
            font_size=dp(18),
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 0.8, 1)
        )
        parent_layout.add_widget(titulo_envio)
        
        # Botón generar vista previa
        btn_generar = Button(
            text=self.textos[self.idioma]['btn_generar'],
            size_hint_y=None,
            height=dp(45),
            background_color=(0.2, 0.7, 0.2, 1),
            font_size=dp(14)
        )
        btn_generar.bind(on_press=self.generar_vista_previa)
        parent_layout.add_widget(btn_generar)
        
        # Botones de envío
        envio_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        # WhatsApp
        btn_whatsapp = Button(
            text=self.textos[self.idioma]['btn_whatsapp'],
            background_color=(0.1, 0.7, 0.1, 1),
            font_size=dp(12)
        )
        btn_whatsapp.bind(on_press=self.enviar_whatsapp)
        envio_layout.add_widget(btn_whatsapp)
        
        # Email
        btn_email = Button(
            text=self.textos[self.idioma]['btn_email'],
            background_color=(0.1, 0.4, 0.7, 1),
            font_size=dp(12)
        )
        btn_email.bind(on_press=self.enviar_email)
        envio_layout.add_widget(btn_email)
        
        # Copiar
        btn_copiar = Button(
            text=self.textos[self.idioma]['btn_copiar'],
            background_color=(0.6, 0.6, 0.2, 1),
            font_size=dp(12)
        )
        btn_copiar.bind(on_press=self.copiar_resumen)
        envio_layout.add_widget(btn_copiar)
        
        parent_layout.add_widget(envio_layout)
    
    def actualizar_historial(self):
        """Actualizar la visualización del historial"""
        self.historial_layout.clear_widgets()
        
        sesion = self.historial.obtener_historial_sesion()
        consultas = sesion['consultas']
        
        if not consultas:
            # No hay consultas
            no_consultas_label = Label(
                text=self.textos[self.idioma]['no_consultas'],
                font_size=dp(12),
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=None,
                height=dp(30)
            )
            self.historial_layout.add_widget(no_consultas_label)
        else:
            # Mostrar número de consultas
            info_label = Label(
                text=f"{len(consultas)} {self.textos[self.idioma]['consultas_encontradas']}",
                font_size=dp(12),
                color=(0.8, 0.8, 1, 1),
                size_hint_y=None,
                height=dp(25)
            )
            self.historial_layout.add_widget(info_label)
            
            # Mostrar últimas 5 consultas
            for i, consulta in enumerate(consultas[-5:]):
                consulta_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(25),
                    spacing=dp(5)
                )
                
                # Número
                num_label = Label(
                    text=f"{len(consultas) - 4 + i}.",
                    font_size=dp(10),
                    size_hint_x=None,
                    width=dp(25)
                )
                consulta_layout.add_widget(num_label)
                
                # Título truncado
                titulo_truncado = consulta['titulo'][:35] + "..." if len(consulta['titulo']) > 35 else consulta['titulo']
                titulo_label = Label(
                    text=titulo_truncado,
                    font_size=dp(10),
                    halign='left',
                    color=(0.9, 0.9, 0.9, 1)
                )
                titulo_label.bind(size=titulo_label.setter('text_size'))
                consulta_layout.add_widget(titulo_label)
                
                # Fuente
                fuente_label = Label(
                    text=f"({consulta['fuente']})",
                    font_size=dp(9),
                    size_hint_x=None,
                    width=dp(80),
                    color=(0.7, 0.7, 1, 1)
                )
                consulta_layout.add_widget(fuente_label)
                
                self.historial_layout.add_widget(consulta_layout)
    
    def agregar_consulta_prueba(self, instance):
        """Agregar una consulta de prueba para testing"""
        import random
        
        consultas_prueba = [
            {
                'fuente': 'sugerencias',
                'titulo': '¿Qué es la vida eterna?',
                'contenido': 'La vida eterna es el regalo de Dios para aquellos que ejercen fe en Jesucristo. Es vida sin fin en un paraíso terrestre donde no habrá más muerte, dolor ni llanto.\n\nCita Bíblica: Juan 17:3 - "Esto significa vida eterna: que lleguen a conocerte a ti, el único Dios verdadero, y a aquel a quien tú enviaste, Jesucristo."'
            },
            {
                'fuente': 'temas_profundos',
                'titulo': '¿Es bíblica la doctrina de la Trinidad?',
                'contenido': 'No. La Biblia enseña que Jehová es uno y Jesús es su Hijo.\n\nLa doctrina de la Trinidad no se encuentra en las Escrituras. La Biblia claramente distingue entre el Padre y el Hijo.\n\nCita Bíblica: Juan 14:28 - "El Padre es mayor que yo"'
            },
            {
                'fuente': 'buscar',
                'titulo': 'Búsqueda: Amor de Dios',
                'contenido': 'El amor de Dios es incondicional y eterno. Se manifiesta a través de Su paciencia, misericordia y el sacrificio de Su Hijo Jesucristo para la salvación de la humanidad.\n\nVersículos:\n1 Juan 4:8 - "El que no ama no ha llegado a conocer a Dios, porque Dios es amor."\nJuan 3:16 - "Porque tanto amó Dios al mundo que dio a su Hijo unigénito..."'
            },
            {
                'fuente': 'sugerencias',
                'titulo': '¿Por qué permite Dios el sufrimiento?',
                'contenido': 'Dios permite temporalmente el sufrimiento para que se resuelvan las cuestiones planteadas en Edén. También para demostrar que los humanos no pueden gobernarse exitosamente sin Él.\n\nCita Bíblica: Jeremías 10:23 - "Bien sé yo, oh Jehová, que al hombre terrestre no le pertenece su camino."'
            }
        ]
        
        consulta_seleccionada = random.choice(consultas_prueba)
        
        self.historial.agregar_consulta(
            fuente=consulta_seleccionada['fuente'],
            titulo=consulta_seleccionada['titulo'],
            contenido=consulta_seleccionada['contenido'],
            idioma=self.idioma
        )
        
        self.actualizar_historial()
        
        self.mostrar_info(
            self.textos[self.idioma]['consulta_agregada'],
            f"{self.textos[self.idioma]['nueva_consulta_agregada']} desde '{consulta_seleccionada['fuente']}'"
        )
        # PARTE 2 - CONTINÚA DESPUÉS DE agregar_consulta_prueba()
    
    def generar_resumen_texto(self):
        """Generar el texto del resumen con formato profesional"""
        sesion = self.historial.obtener_historial_sesion()
        consultas = sesion['consultas']
        
        if not consultas:
            return ""
        
        # Obtener datos del interesado
        datos_interesado = sesion.get('interesado', {})
        
        # Obtener mensaje personalizado
        mensaje_personalizado = self.mensaje_input.text.strip()
        
        # FORMATO PROFESIONAL
        lineas = []
        
        # Saludo inicial
        lineas.append("Saludos cordiales,")
        lineas.append("")
        
        # Mensaje personalizado si existe
        if mensaje_personalizado:
            lineas.append(mensaje_personalizado)
            lineas.append("")
        
        # Introducción
        lineas.append("Aquí tienes el resumen de tu conversación con el Asistente de Predicación:")
        lineas.append("")
        
        # Datos del interesado
        lineas.append(f"Nombre del interesado: {datos_interesado.get('nombre', 'N/A')}")
        if datos_interesado.get('email'):
            lineas.append(f"Correo: {datos_interesado.get('email')}")
        if datos_interesado.get('telefono'):
            lineas.append(f"Teléfono: {datos_interesado.get('telefono')}")
        lineas.append(f"Nombre del Testigo de Jehová: {datos_interesado.get('testigo', 'N/A')}")
        lineas.append("")
        
        # Contenido según formato seleccionado
        formato = self.formato_spinner.text
        
        if formato == self.textos[self.idioma]['formato_titulos']:
            # Solo títulos - Formato simplificado
            lineas.append("Temas consultados:")
            for i, consulta in enumerate(consultas, 1):
                lineas.append(f"{i}. {consulta['titulo']}")
            lineas.append("")
            
        elif formato == self.textos[self.idioma]['formato_resumido']:
            # Formato resumido - Un tema por línea
            for i, consulta in enumerate(consultas, 1):
                lineas.append(f"Tema {i}: {consulta['titulo']}")
                
                # Extraer respuesta resumida
                contenido = consulta['contenido']
                
                # Buscar si hay una respuesta clara en el contenido
                respuesta = self.extraer_respuesta_principal(contenido)
                lineas.append(f"Respuesta: {respuesta}")
                
                # Buscar cita bíblica
                cita = self.extraer_cita_biblica(contenido)
                if cita:
                    lineas.append(f"Cita bíblica: {cita}")
                
                lineas.append("")
        
        else:
            # Formato completo - Detallado por tema
            for i, consulta in enumerate(consultas, 1):
                lineas.append(f"Tema seleccionado: {consulta['titulo']}")
                
                # Respuesta principal
                respuesta = self.extraer_respuesta_principal(consulta['contenido'])
                lineas.append(f"Respuesta: {respuesta}")
                
                # Cita bíblica principal
                cita = self.extraer_cita_biblica(consulta['contenido'])
                if cita:
                    lineas.append(f"Cita bíblica: {cita}")
                
                # Si hay más de un tema, agregar separador
                if i < len(consultas):
                    lineas.append("")
                    lineas.append("---")
                    lineas.append("")
        
        # Información adicional y enlaces
        lineas.append("Más información en:")
        lineas.append("JW Library: https://www.jw.org/es/biblioteca/libros/jw-library/")
        lineas.append("Solicita un curso bíblico: https://www.jw.org/es/testigos-de-jehová/curso-biblico/")
        lineas.append("")
        
        # Despedida
        lineas.append("Atentamente,")
        lineas.append("Asistente de Predicación Digital")
        
        # Información de la sesión (opcional)
        if self.checkbox_timestamp.active:
            lineas.append("")
            lineas.append(f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M')}")
        
        return "\n".join(lineas)

    def extraer_respuesta_principal(self, contenido):
        """Extraer la respuesta principal del contenido"""
        try:
            # Buscar patrones comunes de respuestas
            lineas = contenido.split('\n')
            
            # Buscar la primera línea que parece una respuesta directa
            for linea in lineas:
                linea = linea.strip()
                if len(linea) > 20 and len(linea) < 200:  # Longitud razonable
                    # Evitar líneas que son solo títulos o categorías
                    if not linea.startswith(('Introducción:', 'Conclusión:', 'Cita Bíblica:', 'Versículos:')):
                        return linea
            
            # Si no encuentra una respuesta específica, usar las primeras 150 caracteres
            texto_limpio = contenido.replace('\n', ' ').strip()
            if len(texto_limpio) > 150:
                return texto_limpio[:150] + "..."
            return texto_limpio
            
        except:
            return "Ver contenido completo en el resumen detallado."

    def extraer_cita_biblica(self, contenido):
        """Extraer la primera cita bíblica del contenido"""
        try:
            # Patrones para encontrar citas bíblicas
            patrones = [
                r'([1-3]?\s*[A-Za-zí]+\s+\d+:\d+(?:-\d+)?)',  # Ejemplo: Juan 3:16, 1 Juan 4:8
                r'([A-Za-zí]+\s+\d+:\d+(?:-\d+)?)',           # Ejemplo: Salmo 83:18
            ]
            
            for patron in patrones:
                matches = re.findall(patron, contenido)
                if matches:
                    # Limpiar y retornar la primera cita encontrada
                    cita = matches[0].strip()
                    # Capitalizar primera letra de cada palabra
                    return ' '.join(word.capitalize() for word in cita.split())
            
            # Si no encuentra patrón, buscar manualmente después de "Cita Bíblica:"
            if "Cita Bíblica:" in contenido:
                texto_despues = contenido.split("Cita Bíblica:")[1]
                primera_linea = texto_despues.split('\n')[0].strip()
                if primera_linea and len(primera_linea) < 50:
                    return primera_linea.replace('"', '').replace('-', '').strip()
            
            return None
            
        except:
            return None

    def generar_resumen_whatsapp(self):
        """Generar resumen optimizado para WhatsApp"""
        texto_base = self.generar_resumen_texto()
        
        # Agregar formato especial para WhatsApp
        texto_whatsapp = f"🙏 *Resumen de Estudio Bíblico*\n\n{texto_base}"
        
        # Reemplazar algunos elementos para mejor formato en WhatsApp
        texto_whatsapp = texto_whatsapp.replace("Tema seleccionado:", "*Tema:*")
        texto_whatsapp = texto_whatsapp.replace("Respuesta:", "*Respuesta:*")
        texto_whatsapp = texto_whatsapp.replace("Cita bíblica:", "*Cita bíblica:*")
        texto_whatsapp = texto_whatsapp.replace("Nombre del interesado:", "*Nombre del interesado:*")
        texto_whatsapp = texto_whatsapp.replace("Nombre del Testigo de Jehová:", "*Testigo de Jehová:*")
        
        return texto_whatsapp

    def generar_resumen_email(self):
        """Generar resumen optimizado para Email"""
        return self.generar_resumen_texto()  # El formato base ya es bueno para email
    
    def generar_vista_previa(self, instance):
        """Mostrar vista previa del resumen con formato profesional"""
        if self.historial.contar_consultas() == 0:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        # Usar formato base para vista previa
        texto_resumen = self.generar_resumen_texto()
        
        # Crear popup de vista previa
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # ScrollView con el contenido
        scroll = ScrollView()
        
        contenido_label = Label(
            text=texto_resumen,
            text_size=(dp(350), None),
            halign='left',
            valign='top',
            font_size=dp(11),
            color=(1, 1, 1, 1),
            size_hint_y=None
        )
        contenido_label.bind(texture_size=contenido_label.setter('size'))
        
        scroll.add_widget(contenido_label)
        content.add_widget(scroll)
        
        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        btn_copiar_preview = Button(
            text=self.textos[self.idioma]['btn_copiar'],
            background_color=(0.2, 0.7, 0.2, 1)
        )
        btn_copiar_preview.bind(on_press=lambda x: self.copiar_texto(texto_resumen))
        botones_layout.add_widget(btn_copiar_preview)
        
        btn_cerrar = Button(
            text=self.textos[self.idioma]['cerrar'],
            background_color=(0.7, 0.3, 0.3, 1)
        )
        botones_layout.add_widget(btn_cerrar)
        
        content.add_widget(botones_layout)
        
        popup = Popup(
            title=self.textos[self.idioma]['vista_previa_titulo'],
            content=content,
            size_hint=(0.95, 0.8),
            auto_dismiss=False
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        
        # Scroll al tope
        def scroll_al_tope(*args):
            scroll.scroll_y = 1
        
        popup.bind(on_open=lambda *args: Clock.schedule_once(scroll_al_tope, 0.1))
        popup.open()
    
    def enviar_whatsapp(self, instance):
        """Enviar por WhatsApp usando WhatsApp Web con formato profesional"""
        if self.historial.contar_consultas() == 0:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        # Usar formato específico para WhatsApp
        texto_resumen = self.generar_resumen_whatsapp()
        
        try:
            import webbrowser
            import urllib.parse
            
            # Obtener datos del interesado para el teléfono
            datos = self.historial.obtener_datos_interesado()
            telefono = datos.get('telefono', '') if datos else ''
            
            # Limpiar número de teléfono (solo números)
            telefono_limpio = ''.join(filter(str.isdigit, telefono)) if telefono else ''
            
            # Codificar para URL
            texto_encoded = urllib.parse.quote(texto_resumen)
            
            # Crear URL de WhatsApp Web
            if telefono_limpio and len(telefono_limpio) >= 10:
                # Si tenemos teléfono, enviarlo directo
                whatsapp_url = f"https://wa.me/{telefono_limpio}?text={texto_encoded}"
                print(f"📱 Enviando a WhatsApp: {telefono_limpio}")
            else:
                # Si no hay teléfono, abrir WhatsApp Web general
                whatsapp_url = f"https://wa.me/?text={texto_encoded}"
                print("📱 Abriendo WhatsApp Web general")
            
            # Abrir WhatsApp Web
            webbrowser.open(whatsapp_url)
            
            # Mostrar confirmación
            self.mostrar_info("📱 WhatsApp", self.textos[self.idioma]['whatsapp_exito'])
            
        except Exception as e:
            print(f"❌ Error con WhatsApp: {e}")
            self.mostrar_info("📱 WhatsApp", self.textos[self.idioma]['whatsapp_error'])
    
    def enviar_email(self, instance):
        """Enviar por Email usando mailto con formato profesional"""
        if self.historial.contar_consultas() == 0:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        # Usar formato específico para Email
        texto_resumen = self.generar_resumen_email()
        
        try:
            import webbrowser
            import urllib.parse
            
            # Obtener datos del interesado
            datos = self.historial.obtener_datos_interesado()
            email_destinatario = datos.get('email', '') if datos else ''
            nombre_interesado = datos.get('nombre', 'Estimado/a') if datos else 'Estimado/a'
            
            # Crear subject personalizado
            if self.idioma == 'en':
                subject = f"Bible Study Summary - {nombre_interesado}"
            else:
                subject = f"Resumen de Estudio Bíblico - {nombre_interesado}"
            
            # Crear URL de mailto
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(texto_resumen)
            
            # Si tenemos email del interesado, enviarlo directo
            if email_destinatario and '@' in email_destinatario:
                mailto_url = f"mailto:{email_destinatario}?subject={subject_encoded}&body={body_encoded}"
                print(f"📧 Enviando email a: {email_destinatario}")
            else:
                mailto_url = f"mailto:?subject={subject_encoded}&body={body_encoded}"
                print("📧 Abriendo cliente de email general")
            
            # Abrir cliente de email
            webbrowser.open(mailto_url)
            
            # Mostrar confirmación
            self.mostrar_info("📧 Email", self.textos[self.idioma]['email_exito'])
            
        except Exception as e:
            print(f"❌ Error con mailto: {e}")
            self.mostrar_info("📧 Email", self.textos[self.idioma]['email_error'])
    
    def copiar_resumen(self, instance):
        """Copiar resumen al portapapeles con formato profesional"""
        if self.historial.contar_consultas() == 0:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        # Usar formato base para copiar
        texto_resumen = self.generar_resumen_texto()
        self.copiar_texto(texto_resumen)
    
    def copiar_texto(self, texto):
        """Copiar texto al portapapeles"""
        try:
            from kivy.utils import platform
            if platform == 'android':
                print("📋 Texto copiado (funcionalidad limitada en Android)")
                print(f"Resumen: {len(texto)} caracteres")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(texto)
                    print("📋 Texto copiado al portapapeles")
                except ImportError:
                    print("📋 pyperclip no disponible")
            
            self.mostrar_info(
                self.textos[self.idioma]['resumen_generado'],
                self.textos[self.idioma]['resumen_copiado']
            )
            
        except Exception as e:
            print(f"Error copiando: {e}")
    
    def confirmar_limpiar_historial(self, instance):
        """Confirmar antes de limpiar el historial"""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15))
        
        mensaje = Label(
            text=self.textos[self.idioma]['confirmar_limpiar_texto'],
            text_size=(dp(250), None),
            halign='center',
            font_size=dp(14)
        )
        content.add_widget(mensaje)
        
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Botón Sí
        btn_si = Button(
            text=self.textos[self.idioma]['si'],
            background_color=(0.7, 0.2, 0.2, 1)
        )
        botones_layout.add_widget(btn_si)
        
        # Botón No
        btn_no = Button(
            text=self.textos[self.idioma]['no'],
            background_color=(0.2, 0.7, 0.2, 1)
        )
        botones_layout.add_widget(btn_no)
        
        content.add_widget(botones_layout)
        
        popup = Popup(
            title=self.textos[self.idioma]['confirmar_limpiar'],
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        btn_si.bind(on_press=lambda x: self.limpiar_historial_confirmado(popup))
        btn_no.bind(on_press=lambda x: popup.dismiss())
        
        popup.open()
    
    def limpiar_historial_confirmado(self, popup):
        """Limpiar el historial después de confirmación"""
        self.historial.limpiar_sesion()
        self.actualizar_historial()
        popup.dismiss()
        
        self.mostrar_info(
            self.textos[self.idioma]['historial_limpiado'],
            self.textos[self.idioma]['historial_limpiado_texto']
        )
    
    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        error_label = Label(
            text=mensaje,
            text_size=(dp(250), None),
            halign='center',
            font_size=dp(14)
        )
        content.add_widget(error_label)
        
        btn_ok = Button(
            text="OK",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.7, 0.3, 0.3, 1)
        )
        content.add_widget(btn_ok)
        
        popup = Popup(
            title=self.textos[self.idioma]['error_titulo'],
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=False
        )
        
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()
    
    def mostrar_info(self, titulo, mensaje):
        """Mostrar mensaje informativo"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        info_label = Label(
            text=mensaje,
            text_size=(dp(250), None),
            halign='center',
            font_size=dp(14)
        )
        content.add_widget(info_label)
        
        btn_ok = Button(
            text="OK",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.7, 0.2, 1)
        )
        content.add_widget(btn_ok)
        
        popup = Popup(
            title=titulo,
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=False
        )
        
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()
    
    def cambiar_idioma(self, nuevo_idioma):
        """Cambiar el idioma de la pantalla"""
        if nuevo_idioma in self.textos:
            self.idioma = nuevo_idioma
            self.construir_interfaz()
    
    def on_enter(self):
        """Al entrar a la pantalla, actualizar el historial"""
        self.actualizar_historial()
    
    def volver_menu(self, instance):
        """Volver al menú principal"""
        if self.volver_callback:
            self.volver_callback()
        else:
            print("⚠️ volver_callback no definido en PantallaSendResume")


# FUNCIÓN AUXILIAR PARA INTEGRACIÓN
def agregar_consulta_al_historial(fuente, titulo, contenido, idioma='es'):
    """
    Función global para agregar consultas al historial desde cualquier pantalla
    
    Args:
        fuente (str): 'sugerencias', 'temas_profundos', 'buscar'
        titulo (str): Título de la consulta
        contenido (str): Contenido completo de la respuesta
        idioma (str): Idioma de la consulta
    """
    historial = HistorialSesion()
    historial.agregar_consulta(fuente, titulo, contenido, idioma)
    print(f"✅ Consulta agregada al historial: {fuente} - {titulo[:30]}...")


# FUNCIÓN PARA OBTENER ESTADÍSTICAS DEL HISTORIAL
def obtener_estadisticas_historial():
    """Retorna estadísticas del historial actual"""
    historial = HistorialSesion()
    sesion = historial.obtener_historial_sesion()
    
    return {
        'total_consultas': len(sesion['consultas']),
        'inicio_sesion': sesion['inicio'],
        'fuentes': {
            'sugerencias': len([c for c in sesion['consultas'] if c['fuente'] == 'sugerencias']),
            'temas_profundos': len([c for c in sesion['consultas'] if c['fuente'] == 'temas_profundos']),
            'buscar': len([c for c in sesion['consultas'] if c['fuente'] == 'buscar'])
        }
    }

# FUNCIÓN PARA VERIFICAR SESIÓN ACTIVA
def verificar_sesion_activa():
    """Verifica si hay una sesión activa"""
    historial = HistorialSesion()
    return historial.tiene_sesion_activa()

def obtener_info_interesado():
    """Obtiene información del interesado actual"""
    historial = HistorialSesion()
    return historial.get_info_for_sharing()