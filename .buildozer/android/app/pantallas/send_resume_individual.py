# pantallas/send_resume_individual.py - PARTE 1
# HISTORIAL INDIVIDUAL POR ESTUDIANTE

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

class HistorialIndividual:
    """Clase para manejar historiales individuales por estudiante"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HistorialIndividual, cls).__new__(cls)
            cls._instance.estudiantes = {}
            cls._instance.estudiante_actual = None
            cls._instance._cargar_datos()
        return cls._instance
    
    def _cargar_datos(self):
        """Cargar datos desde archivo"""
        try:
            if os.path.exists('estudiantes_historial.json'):
                with open('estudiantes_historial.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.estudiantes = data.get('estudiantes', {})
                    print(f"📚 Cargados {len(self.estudiantes)} estudiantes")
            else:
                # Crear algunos estudiantes de ejemplo
                self._crear_estudiantes_ejemplo()
        except Exception as e:
            print(f"Error cargando datos: {e}")
            self._crear_estudiantes_ejemplo()
    
    def _crear_estudiantes_ejemplo(self):
        """Crear estudiantes de ejemplo"""
        estudiantes_ejemplo = {
            "maria_gonzalez": {
                "nombre": "María González",
                "telefono": "+1234567890",
                "email": "maria@email.com",
                "fecha_inicio": "2024-01-15",
                "sesiones": [
                    {
                        "fecha": "2024-12-01 10:00:00",
                        "consultas": [
                            {
                                "timestamp": "2024-12-01 10:15:00",
                                "fuente": "sugerencias",
                                "titulo": "¿Quién es Dios?",
                                "contenido": "Dios es el Creador del cielo y la tierra, el Ser Supremo. Su nombre es Jehová.\n\nSalmo 83:18 - 'Para que la gente sepa que tú, cuyo nombre es Jehová, tú solo eres el Altísimo sobre toda la tierra.'",
                                "idioma": "es"
                            }
                        ]
                    }
                ]
            },
            "carlos_rivera": {
                "nombre": "Carlos Rivera",
                "telefono": "+0987654321",
                "email": "carlos@email.com", 
                "fecha_inicio": "2024-02-10",
                "sesiones": [
                    {
                        "fecha": "2024-12-01 14:30:00",
                        "consultas": [
                            {
                                "timestamp": "2024-12-01 14:45:00",
                                "fuente": "temas_profundos",
                                "titulo": "¿Por qué permite Dios el sufrimiento?",
                                "contenido": "Dios permite temporalmente el sufrimiento para resolver las cuestiones planteadas en Edén.\n\nJeremías 10:23 - 'Bien sé yo, oh Jehová, que al hombre terrestre no le pertenece su camino.'",
                                "idioma": "es"
                            }
                        ]
                    }
                ]
            },
            "ana_martinez": {
                "nombre": "Ana Martínez",
                "telefono": "+1122334455",
                "email": "ana@email.com",
                "fecha_inicio": "2024-03-05",
                "sesiones": []
            }
        }
        
        self.estudiantes = estudiantes_ejemplo
        self._guardar_datos()
        print("👥 Estudiantes de ejemplo creados")
    
    def _guardar_datos(self):
        """Guardar datos en archivo"""
        try:
            data = {
                "estudiantes": self.estudiantes,
                "ultima_actualizacion": datetime.now().isoformat()
            }
            with open('estudiantes_historial.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("💾 Datos guardados correctamente")
        except Exception as e:
            print(f"Error guardando datos: {e}")
    
    def crear_estudiante(self, nombre, telefono="", email=""):
        """Crear un nuevo estudiante"""
        # Crear ID único basado en el nombre
        estudiante_id = nombre.lower().replace(" ", "_").replace(".", "")
        
        if estudiante_id in self.estudiantes:
            return False, "Ya existe un estudiante con ese nombre"
        
        self.estudiantes[estudiante_id] = {
            "nombre": nombre,
            "telefono": telefono,
            "email": email,
            "fecha_inicio": datetime.now().strftime("%Y-%m-%d"),
            "sesiones": []
        }
        
        self._guardar_datos()
        return True, estudiante_id
    
    def seleccionar_estudiante(self, estudiante_id):
        """Seleccionar estudiante actual"""
        if estudiante_id in self.estudiantes:
            self.estudiante_actual = estudiante_id
            return True
        return False
    
    def obtener_estudiantes(self):
        """Obtener lista de todos los estudiantes"""
        return {k: v["nombre"] for k, v in self.estudiantes.items()}
    
    def obtener_estudiante_actual(self):
        """Obtener datos del estudiante actual"""
        if self.estudiante_actual and self.estudiante_actual in self.estudiantes:
            return self.estudiantes[self.estudiante_actual]
        return None
    
    def iniciar_nueva_sesion(self):
        """Iniciar nueva sesión para el estudiante actual"""
        if not self.estudiante_actual:
            return False
        
        nueva_sesion = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "consultas": []
        }
        
        self.estudiantes[self.estudiante_actual]["sesiones"].append(nueva_sesion)
        self._guardar_datos()
        return True
    
    def agregar_consulta(self, fuente, titulo, contenido, idioma='es'):
        """Agregar consulta a la sesión actual del estudiante"""
        if not self.estudiante_actual:
            return False
        
        estudiante = self.estudiantes[self.estudiante_actual]
        
        # Si no hay sesiones, crear una nueva
        if not estudiante["sesiones"]:
            self.iniciar_nueva_sesion()
        
        # Agregar a la última sesión
        consulta = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fuente": fuente,
            "titulo": titulo,
            "contenido": contenido,
            "idioma": idioma
        }
        
        estudiante["sesiones"][-1]["consultas"].append(consulta)
        self._guardar_datos()
        
        print(f"📝 Consulta agregada para {estudiante['nombre']}: {titulo[:30]}...")
        return True
    
    def obtener_sesion_actual(self):
        """Obtener la sesión actual del estudiante"""
        if not self.estudiante_actual:
            return None
        
        estudiante = self.estudiantes[self.estudiante_actual]
        
        if not estudiante["sesiones"]:
            return {"fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "consultas": []}
        
        return estudiante["sesiones"][-1]
    
    def obtener_todas_sesiones(self):
        """Obtener todas las sesiones del estudiante actual"""
        if not self.estudiante_actual:
            return []
        
        return self.estudiantes[self.estudiante_actual]["sesiones"]
    
    def limpiar_sesion_actual(self):
        """Limpiar solo la sesión actual"""
        if not self.estudiante_actual:
            return False
        
        estudiante = self.estudiantes[self.estudiante_actual]
        
        if estudiante["sesiones"]:
            estudiante["sesiones"][-1]["consultas"] = []
            self._guardar_datos()
            return True
        
        return False
    
    def eliminar_estudiante(self, estudiante_id):
        """Eliminar un estudiante completamente"""
        if estudiante_id in self.estudiantes:
            del self.estudiantes[estudiante_id]
            if self.estudiante_actual == estudiante_id:
                self.estudiante_actual = None
            self._guardar_datos()
            return True
        return False


# FUNCIÓN AUXILIAR GLOBAL
def agregar_consulta_individual(fuente, titulo, contenido, idioma='es'):
    """
    Función global para agregar consultas al historial individual
    Usar desde otras pantallas para registrar consultas automáticamente
    """
    historial = HistorialIndividual()
    if historial.estudiante_actual:
        historial.agregar_consulta(fuente, titulo, contenido, idioma)
        print(f"✅ Consulta agregada al historial individual: {titulo[:30]}...")
    else:
        print("⚠️ No hay estudiante seleccionado para agregar consulta")
        
        # CONTINÚA EN EL MISMO ARCHIVO send_resume_individual.py - PARTE 2

class PantallaSendResumeIndividual(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        self.historial = HistorialIndividual()
        
        # Textos en diferentes idiomas
        self.textos = {
            'es': {
                'titulo': 'Resumen Individual de Estudio',
                'seleccionar_estudiante': 'Seleccionar Estudiante:',
                'nuevo_estudiante': '+ Nuevo',
                'gestionar_estudiantes': '👥 Gestionar',
                'estudiante_actual': 'Estudiante Actual:',
                'sin_estudiante': 'No hay estudiante seleccionado',
                'sesion_actual': 'Sesión Actual',
                'no_consultas': 'No hay consultas en esta sesión',
                'consultas_encontradas': 'consultas en esta sesión',
                'personalizar_titulo': 'Personalizar Resumen',
                'mensaje_titulo': 'Mensaje personalizado:',
                'mensaje_placeholder': 'Mensaje personal para este estudiante...',
                'incluir_timestamp': 'Incluir fecha y hora',
                'incluir_fuente': 'Incluir fuente de cada consulta',
                'incluir_todas_sesiones': 'Incluir todas las sesiones',
                'formato_titulo': 'Formato del resumen:',
                'formato_completo': 'Completo (título + contenido)',
                'formato_titulos': 'Solo títulos',
                'formato_resumido': 'Resumido',
                'enviar_titulo': 'Opciones de Envío',
                'btn_whatsapp': '📱 WhatsApp',
                'btn_email': '📧 Email',
                'btn_copiar': '📋 Copiar',
                'btn_generar': 'Generar Vista Previa',
                'btn_nueva_sesion': '🆕 Nueva Sesión',
                'btn_limpiar': '🧹 Limpiar Sesión',
                'btn_volver': 'Volver al Menú',
                'nombre_estudiante': 'Nombre del estudiante:',
                'telefono_estudiante': 'Teléfono (opcional):',
                'email_estudiante': 'Email (opcional):',
                'crear': 'Crear',
                'cancelar': 'Cancelar',
                'estudiante_creado': 'Estudiante Creado',
                'nueva_sesion_iniciada': 'Nueva Sesión Iniciada',
                'sesion_limpiada': 'Sesión Limpiada',
                'error_titulo': 'Error',
                'error_sin_estudiante': 'Debes seleccionar un estudiante primero',
                'error_sin_consultas': 'No hay consultas para incluir en el resumen',
                'confirmar_limpiar': '¿Limpiar Sesión?',
                'confirmar_limpiar_texto': '¿Estás seguro de que quieres limpiar la sesión actual?',
                'si': 'Sí',
                'no': 'No',
                'cerrar': 'Cerrar',
                'vista_previa_titulo': 'Vista Previa del Resumen',
                'resumen_copiado': 'Resumen copiado exitosamente',
                'whatsapp_exito': 'WhatsApp abierto con el resumen',
                'email_exito': 'Cliente de email abierto con el resumen',
                'desde_fuente': 'desde',
                'hora': 'Hora:',
                'fuente': 'Fuente:'
            }
        }
        
        self.construir_interfaz()
    
    def construir_interfaz(self):
        """Construir la interfaz de usuario"""
        self.clear_widgets()
        
        # Layout principal
        layout_principal = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=dp(12)
        )
        
        # Título
        titulo = Label(
            text=self.textos[self.idioma]['titulo'],
            font_size=dp(18),
            size_hint_y=None,
            height=dp(35),
            color=(0.2, 0.6, 0.9, 1)
        )
        layout_principal.add_widget(titulo)
        
        # Sección: Selección de estudiante
        self.crear_seccion_estudiante(layout_principal)
        
        # Scroll principal
        scroll_principal = ScrollView()
        contenido_scroll = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None
        )
        contenido_scroll.bind(minimum_height=contenido_scroll.setter('height'))
        
        # Sección: Historial del estudiante
        self.crear_seccion_historial_estudiante(contenido_scroll)
        
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
            height=dp(45)
        )
        
        # Botón nueva sesión
        btn_nueva_sesion = Button(
            text=self.textos[self.idioma]['btn_nueva_sesion'],
            background_color=(0.2, 0.6, 0.8, 1),
            font_size=dp(9)
        )
        btn_nueva_sesion.bind(on_press=self.iniciar_nueva_sesion)
        botones_layout.add_widget(btn_nueva_sesion)
        
        # Botón limpiar sesión
        btn_limpiar = Button(
            text=self.textos[self.idioma]['btn_limpiar'],
            background_color=(0.7, 0.4, 0.2, 1),
            font_size=dp(9)
        )
        btn_limpiar.bind(on_press=self.confirmar_limpiar_sesion)
        botones_layout.add_widget(btn_limpiar)
        
        # Botón volver
        btn_volver = Button(
            text=self.textos[self.idioma]['btn_volver'],
            background_color=(0.7, 0.3, 0.3, 1),
            font_size=dp(9)
        )
        btn_volver.bind(on_press=self.volver_menu)
        botones_layout.add_widget(btn_volver)
        
        layout_principal.add_widget(botones_layout)
        self.add_widget(layout_principal)
    
    def crear_seccion_estudiante(self, parent_layout):
        """Crear sección de selección de estudiante"""
        estudiante_container = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(100)
        )
        
        # Título
        titulo_estudiante = Label(
            text=self.textos[self.idioma]['seleccionar_estudiante'],
            font_size=dp(14),
            size_hint_y=None,
            height=dp(25),
            color=(1, 1, 0.8, 1)
        )
        estudiante_container.add_widget(titulo_estudiante)
        
        # Spinner con estudiantes + botones
        estudiante_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(35)
        )
        
        # Actualizar lista de estudiantes
        estudiantes = self.historial.obtener_estudiantes()
        estudiantes_list = list(estudiantes.values())
        
        self.estudiante_spinner = Spinner(
            text='Seleccionar...' if not estudiantes_list else estudiantes_list[0],
            values=estudiantes_list,
            font_size=dp(11)
        )
        self.estudiante_spinner.bind(text=self.on_estudiante_seleccionado)
        estudiante_row.add_widget(self.estudiante_spinner)
        
        # Botón nuevo estudiante
        btn_nuevo = Button(
            text=self.textos[self.idioma]['nuevo_estudiante'],
            size_hint_x=None,
            width=dp(80),
            background_color=(0.2, 0.7, 0.2, 1),
            font_size=dp(9)
        )
        btn_nuevo.bind(on_press=self.mostrar_crear_estudiante)
        estudiante_row.add_widget(btn_nuevo)
        
        estudiante_container.add_widget(estudiante_row)
        
        # Mostrar estudiante actual
        self.estudiante_actual_label = Label(
            text=self.obtener_texto_estudiante_actual(),
            font_size=dp(11),
            size_hint_y=None,
            height=dp(25),
            color=(0.8, 1, 0.8, 1)
        )
        estudiante_container.add_widget(self.estudiante_actual_label)
        
        parent_layout.add_widget(estudiante_container)
        
        # Auto-seleccionar primer estudiante si existe
        if estudiantes_list:
            self.seleccionar_primer_estudiante()
    
    def crear_seccion_historial_estudiante(self, parent_layout):
        """Crear sección de historial del estudiante"""
        # Título de sección
        titulo_historial = Label(
            text=self.textos[self.idioma]['sesion_actual'],
            font_size=dp(14),
            size_hint_y=None,
            height=dp(25),
            color=(1, 1, 0.8, 1)
        )
        parent_layout.add_widget(titulo_historial)
        
        # Contenedor del historial
        historial_scroll = ScrollView(
            size_hint_y=None,
            height=dp(100)
        )
        
        self.historial_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(3),
            size_hint_y=None
        )
        self.historial_layout.bind(minimum_height=self.historial_layout.setter('height'))
        
        historial_scroll.add_widget(self.historial_layout)
        parent_layout.add_widget(historial_scroll)
        
        # Actualizar historial
        self.actualizar_historial_estudiante()
    
    def crear_seccion_personalizacion(self, parent_layout):
        """Crear la sección de personalización"""
        # Título de sección
        titulo_personalizacion = Label(
            text=self.textos[self.idioma]['personalizar_titulo'],
            font_size=dp(14),
            size_hint_y=None,
            height=dp(25),
            color=(1, 1, 0.8, 1)
        )
        parent_layout.add_widget(titulo_personalizacion)
        
        # Mensaje personalizado
        mensaje_label = Label(
            text=self.textos[self.idioma]['mensaje_titulo'],
            font_size=dp(12),
            size_hint_y=None,
            height=dp(20),
            halign='left'
        )
        mensaje_label.bind(size=mensaje_label.setter('text_size'))
        parent_layout.add_widget(mensaje_label)
        
        self.mensaje_input = TextInput(
            hint_text=self.textos[self.idioma]['mensaje_placeholder'],
            multiline=True,
            size_hint_y=None,
            height=dp(50),
            font_size=dp(11)
        )
        parent_layout.add_widget(self.mensaje_input)
        
        # Opciones con checkboxes
        opciones_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(3),
            size_hint_y=None,
            height=dp(75)
        )
        
        # Checkbox incluir timestamp
        timestamp_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(22)
        )
        self.checkbox_timestamp = CheckBox(
            active=True,
            size_hint_x=None,
            width=dp(25)
        )
        timestamp_label = Label(
            text=self.textos[self.idioma]['incluir_timestamp'],
            font_size=dp(11),
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
            height=dp(22)
        )
        self.checkbox_fuente = CheckBox(
            active=True,
            size_hint_x=None,
            width=dp(25)
        )
        fuente_label = Label(
            text=self.textos[self.idioma]['incluir_fuente'],
            font_size=dp(11),
            halign='left'
        )
        fuente_label.bind(size=fuente_label.setter('text_size'))
        fuente_layout.add_widget(self.checkbox_fuente)
        fuente_layout.add_widget(fuente_label)
        opciones_layout.add_widget(fuente_layout)
        
        # Checkbox incluir todas las sesiones
        todas_sesiones_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(22)
        )
        self.checkbox_todas_sesiones = CheckBox(
            active=False,
            size_hint_x=None,
            width=dp(25)
        )
        todas_sesiones_label = Label(
            text=self.textos[self.idioma]['incluir_todas_sesiones'],
            font_size=dp(11),
            halign='left'
        )
        todas_sesiones_label.bind(size=todas_sesiones_label.setter('text_size'))
        todas_sesiones_layout.add_widget(self.checkbox_todas_sesiones)
        todas_sesiones_layout.add_widget(todas_sesiones_label)
        opciones_layout.add_widget(todas_sesiones_layout)
        
        parent_layout.add_widget(opciones_layout)
        
        # Formato del resumen
        formato_label = Label(
            text=self.textos[self.idioma]['formato_titulo'],
            font_size=dp(12),
            size_hint_y=None,
            height=dp(20),
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
            height=dp(30),
            font_size=dp(11)
        )
        parent_layout.add_widget(self.formato_spinner)
    
    def crear_seccion_envio(self, parent_layout):
        """Crear la sección de envío"""
        # Título de sección
        titulo_envio = Label(
            text=self.textos[self.idioma]['enviar_titulo'],
            font_size=dp(14),
            size_hint_y=None,
            height=dp(25),
            color=(1, 1, 0.8, 1)
        )
        parent_layout.add_widget(titulo_envio)
        
        # Botón generar vista previa
        btn_generar = Button(
            text=self.textos[self.idioma]['btn_generar'],
            size_hint_y=None,
            height=dp(35),
            background_color=(0.2, 0.7, 0.2, 1),
            font_size=dp(12)
        )
        btn_generar.bind(on_press=self.generar_vista_previa)
        parent_layout.add_widget(btn_generar)
        
        # Botones de envío
        envio_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(40)
        )
        
        # WhatsApp
        btn_whatsapp = Button(
            text=self.textos[self.idioma]['btn_whatsapp'],
            background_color=(0.1, 0.7, 0.1, 1),
            font_size=dp(11)
        )
        btn_whatsapp.bind(on_press=self.enviar_whatsapp)
        envio_layout.add_widget(btn_whatsapp)
        
        # Email
        btn_email = Button(
            text=self.textos[self.idioma]['btn_email'],
            background_color=(0.1, 0.4, 0.7, 1),
            font_size=dp(11)
        )
        btn_email.bind(on_press=self.enviar_email)
        envio_layout.add_widget(btn_email)
        
        # Copiar
        btn_copiar = Button(
            text=self.textos[self.idioma]['btn_copiar'],
            background_color=(0.6, 0.6, 0.2, 1),
            font_size=dp(11)
        )
        btn_copiar.bind(on_press=self.copiar_resumen)
        envio_layout.add_widget(btn_copiar)
        
        parent_layout.add_widget(envio_layout)
    
    def seleccionar_primer_estudiante(self):
        """Auto-seleccionar el primer estudiante disponible"""
        estudiantes = self.historial.obtener_estudiantes()
        if estudiantes:
            primer_id = list(estudiantes.keys())[0]
            self.historial.seleccionar_estudiante(primer_id)
            self.actualizar_estudiante_actual_label()
            self.actualizar_historial_estudiante()
    
    def obtener_texto_estudiante_actual(self):
        """Obtener texto para mostrar el estudiante actual"""
        estudiante = self.historial.obtener_estudiante_actual()
        if estudiante:
            return f"{self.textos[self.idioma]['estudiante_actual']} {estudiante['nombre']}"
        else:
            return self.textos[self.idioma]['sin_estudiante']
    
    def on_estudiante_seleccionado(self, spinner, text):
        """Cuando se selecciona un estudiante del spinner"""
        estudiantes = self.historial.obtener_estudiantes()
        
        # Buscar el ID del estudiante por nombre
        for estudiante_id, nombre in estudiantes.items():
            if nombre == text:
                self.historial.seleccionar_estudiante(estudiante_id)
                self.actualizar_estudiante_actual_label()
                self.actualizar_historial_estudiante()
                break
    
    def actualizar_estudiante_actual_label(self):
        """Actualizar el label del estudiante actual"""
        if hasattr(self, 'estudiante_actual_label'):
            self.estudiante_actual_label.text = self.obtener_texto_estudiante_actual()
    
    def actualizar_historial_estudiante(self):
        """Actualizar la visual"""	
        # AGREGAR ESTE CÓDIGO AL FINAL DE TU ARCHIVO send_resume_individual.py
# CONTINÚA DESPUÉS DE "def actualizar_historial_estudiante(self):"

    def actualizar_historial_estudiante(self):
        """Actualizar la visualización del historial del estudiante"""
        self.historial_layout.clear_widgets()
        
        sesion = self.historial.obtener_sesion_actual()
        
        if not sesion or not sesion['consultas']:
            # No hay consultas
            no_consultas_label = Label(
                text=self.textos[self.idioma]['no_consultas'],
                font_size=dp(11),
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=None,
                height=dp(25)
            )
            self.historial_layout.add_widget(no_consultas_label)
        else:
            # Mostrar número de consultas
            info_label = Label(
                text=f"{len(sesion['consultas'])} {self.textos[self.idioma]['consultas_encontradas']}",
                font_size=dp(11),
                color=(0.8, 0.8, 1, 1),
                size_hint_y=None,
                height=dp(20)
            )
            self.historial_layout.add_widget(info_label)
            
            # Mostrar últimas 4 consultas
            for i, consulta in enumerate(sesion['consultas'][-4:]):
                consulta_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=dp(20),
                    spacing=dp(3)
                )
                
                # Número
                num_label = Label(
                    text=f"{len(sesion['consultas']) - 3 + i}.",
                    font_size=dp(9),
                    size_hint_x=None,
                    width=dp(20)
                )
                consulta_layout.add_widget(num_label)
                
                # Título truncado
                titulo_truncado = consulta['titulo'][:30] + "..." if len(consulta['titulo']) > 30 else consulta['titulo']
                titulo_label = Label(
                    text=titulo_truncado,
                    font_size=dp(9),
                    halign='left',
                    color=(0.9, 0.9, 0.9, 1)
                )
                titulo_label.bind(size=titulo_label.setter('text_size'))
                consulta_layout.add_widget(titulo_label)
                
                # Fuente
                fuente_label = Label(
                    text=f"({consulta['fuente']})",
                    font_size=dp(8),
                    size_hint_x=None,
                    width=dp(70),
                    color=(0.7, 0.7, 1, 1)
                )
                consulta_layout.add_widget(fuente_label)
                
                self.historial_layout.add_widget(consulta_layout)
    
    def mostrar_crear_estudiante(self, instance):
        """Mostrar popup para crear nuevo estudiante"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # Campo nombre
        nombre_label = Label(
            text=self.textos[self.idioma]['nombre_estudiante'],
            size_hint_y=None,
            height=dp(25),
            font_size=dp(12)
        )
        content.add_widget(nombre_label)
        
        nombre_input = TextInput(
            hint_text="Ej: Juan Pérez",
            size_hint_y=None,
            height=dp(35),
            font_size=dp(12)
        )
        content.add_widget(nombre_input)
        
        # Campo teléfono
        telefono_label = Label(
            text=self.textos[self.idioma]['telefono_estudiante'],
            size_hint_y=None,
            height=dp(25),
            font_size=dp(12)
        )
        content.add_widget(telefono_label)
        
        telefono_input = TextInput(
            hint_text="Ej: +1234567890",
            size_hint_y=None,
            height=dp(35),
            font_size=dp(12)
        )
        content.add_widget(telefono_input)
        
        # Campo email
        email_label = Label(
            text=self.textos[self.idioma]['email_estudiante'],
            size_hint_y=None,
            height=dp(25),
            font_size=dp(12)
        )
        content.add_widget(email_label)
        
        email_input = TextInput(
            hint_text="Ej: juan@email.com",
            size_hint_y=None,
            height=dp(35),
            font_size=dp(12)
        )
        content.add_widget(email_input)
        
        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(45)
        )
        
        btn_crear = Button(
            text=self.textos[self.idioma]['crear'],
            background_color=(0.2, 0.7, 0.2, 1)
        )
        
        btn_cancelar = Button(
            text=self.textos[self.idioma]['cancelar'],
            background_color=(0.7, 0.3, 0.3, 1)
        )
        
        botones_layout.add_widget(btn_crear)
        botones_layout.add_widget(btn_cancelar)
        content.add_widget(botones_layout)
        
        popup = Popup(
            title='Nuevo Estudiante',
            content=content,
            size_hint=(0.9, 0.7),
            auto_dismiss=False
        )
        
        def crear_estudiante_action(instance):
            nombre = nombre_input.text.strip()
            if nombre:
                exito, resultado = self.historial.crear_estudiante(
                    nombre=nombre,
                    telefono=telefono_input.text.strip(),
                    email=email_input.text.strip()
                )
                
                if exito:
                    # Actualizar spinner
                    estudiantes = self.historial.obtener_estudiantes()
                    self.estudiante_spinner.values = list(estudiantes.values())
                    self.estudiante_spinner.text = nombre
                    
                    # Seleccionar nuevo estudiante
                    self.historial.seleccionar_estudiante(resultado)
                    self.actualizar_estudiante_actual_label()
                    self.actualizar_historial_estudiante()
                    
                    popup.dismiss()
                    self.mostrar_info(
                        self.textos[self.idioma]['estudiante_creado'],
                        f"Estudiante '{nombre}' creado exitosamente"
                    )
                else:
                    self.mostrar_error(resultado)
            else:
                self.mostrar_error("El nombre es requerido")
        
        btn_crear.bind(on_press=crear_estudiante_action)
        btn_cancelar.bind(on_press=lambda x: popup.dismiss())
        
        popup.open()
    
    def mostrar_gestionar_estudiantes(self, instance):
        """Mostrar popup para gestionar estudiantes"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        info_label = Label(
            text="Funcionalidad de gestión en desarrollo",
            size_hint_y=None,
            height=dp(40),
            font_size=dp(14)
        )
        content.add_widget(info_label)
        
        btn_cerrar = Button(
            text=self.textos[self.idioma]['cerrar'],
            size_hint_y=None,
            height=dp(40),
            background_color=(0.7, 0.3, 0.3, 1)
        )
        content.add_widget(btn_cerrar)
        
        popup = Popup(
            title='Gestionar Estudiantes',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()
    
    def iniciar_nueva_sesion(self, instance):
        """Iniciar nueva sesión para el estudiante actual"""
        if not self.historial.estudiante_actual:
            self.mostrar_error(self.textos[self.idioma]['error_sin_estudiante'])
            return
        
        self.historial.iniciar_nueva_sesion()
        self.actualizar_historial_estudiante()
        
        self.mostrar_info(
            self.textos[self.idioma]['nueva_sesion_iniciada'],
            "Nueva sesión iniciada para el estudiante"
        )
    
    def confirmar_limpiar_sesion(self, instance):
        """Confirmar antes de limpiar la sesión"""
        if not self.historial.estudiante_actual:
            self.mostrar_error(self.textos[self.idioma]['error_sin_estudiante'])
            return
        
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
        
        btn_si = Button(
            text=self.textos[self.idioma]['si'],
            background_color=(0.7, 0.2, 0.2, 1)
        )
        btn_no = Button(
            text=self.textos[self.idioma]['no'],
            background_color=(0.2, 0.7, 0.2, 1)
        )
        
        botones_layout.add_widget(btn_si)
        botones_layout.add_widget(btn_no)
        content.add_widget(botones_layout)
        
        popup = Popup(
            title=self.textos[self.idioma]['confirmar_limpiar'],
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        def limpiar_confirmado(instance):
            self.historial.limpiar_sesion_actual()
            self.actualizar_historial_estudiante()
            popup.dismiss()
            self.mostrar_info(
                self.textos[self.idioma]['sesion_limpiada'],
                "Sesión limpiada correctamente"
            )
        
        btn_si.bind(on_press=limpiar_confirmado)
        btn_no.bind(on_press=lambda x: popup.dismiss())
        
        popup.open()
    
    def generar_resumen_texto(self):
        """Generar el texto del resumen según las opciones seleccionadas"""
        if not self.historial.estudiante_actual:
            return ""
        
        estudiante = self.historial.obtener_estudiante_actual()
        
        # Decidir qué sesiones incluir
        if self.checkbox_todas_sesiones.active:
            sesiones = self.historial.obtener_todas_sesiones()
        else:
            sesion_actual = self.historial.obtener_sesion_actual()
            sesiones = [sesion_actual] if sesion_actual['consultas'] else []
        
        if not sesiones or not any(s['consultas'] for s in sesiones):
            return ""
        
        # Encabezado
        lineas = []
        lineas.append("📋 RESUMEN DE ESTUDIO INDIVIDUAL")
        lineas.append("=" * 45)
        lineas.append("")
        
        # Información del estudiante
        lineas.append(f"👤 ESTUDIANTE: {estudiante['nombre']}")
        if estudiante.get('telefono'):
            lineas.append(f"📱 Teléfono: {estudiante['telefono']}")
        if estudiante.get('email'):
            lineas.append(f"📧 Email: {estudiante['email']}")
        
        if self.checkbox_timestamp.active:
            lineas.append(f"📅 Fecha inicio: {estudiante['fecha_inicio']}")
            lineas.append(f"🕐 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        lineas.append("")
        
        # Mensaje personalizado
        mensaje_personalizado = self.mensaje_input.text.strip()
        if mensaje_personalizado:
            lineas.append("💭 MENSAJE PERSONAL:")
            lineas.append(mensaje_personalizado)
            lineas.append("")
        
        # Procesar sesiones
        total_consultas = sum(len(s['consultas']) for s in sesiones)
        
        if self.checkbox_todas_sesiones.active and len(sesiones) > 1:
            lineas.append(f"📊 Total: {len(sesiones)} sesiones, {total_consultas} consultas")
        else:
            lineas.append(f"📊 Total: {total_consultas} consultas")
        
        lineas.append("")
        
        # Contenido según formato
        formato = self.formato_spinner.text
        
        contador_global = 1
        
        for idx_sesion, sesion in enumerate(sesiones):
            if not sesion['consultas']:
                continue
            
            if self.checkbox_todas_sesiones.active and len(sesiones) > 1:
                lineas.append(f"📅 SESIÓN {idx_sesion + 1} - {sesion['fecha']}")
                lineas.append("-" * 35)
                lineas.append("")
            
            for consulta in sesion['consultas']:
                if formato == self.textos[self.idioma]['formato_titulos']:
                    # Solo títulos
                    titulo_line = f"{contador_global}. {consulta['titulo']}"
                    if self.checkbox_fuente.active:
                        titulo_line += f" ({self.textos[self.idioma]['desde_fuente']} {consulta['fuente']})"
                    lineas.append(titulo_line)
                
                elif formato == self.textos[self.idioma]['formato_resumido']:
                    # Formato resumido
                    lineas.append(f"{contador_global}. {consulta['titulo']}")
                    contenido_resumido = consulta['contenido'][:120] + "..." if len(consulta['contenido']) > 120 else consulta['contenido']
                    lineas.append(f"   💡 {contenido_resumido}")
                    
                    if self.checkbox_fuente.active:
                        lineas.append(f"   📍 {self.textos[self.idioma]['fuente']} {consulta['fuente']}")
                    
                    if self.checkbox_timestamp.active:
                        lineas.append(f"   ⏰ {consulta['timestamp']}")
                    
                    lineas.append("")
                
                else:
                    # Formato completo
                    lineas.append(f"{contador_global}. {consulta['titulo']}")
                    lineas.append("─" * 30)
                    lineas.append("")
                    lineas.append(consulta['contenido'])
                    lineas.append("")
                    
                    if self.checkbox_fuente.active:
                        lineas.append(f"📍 {self.textos[self.idioma]['fuente']} {consulta['fuente']}")
                    
                    if self.checkbox_timestamp.active:
                        lineas.append(f"⏰ {consulta['timestamp']}")
                    
                    lineas.append("")
                    lineas.append("=" * 40)
                    lineas.append("")
                
                contador_global += 1
            
            if self.checkbox_todas_sesiones.active and len(sesiones) > 1 and idx_sesion < len(sesiones) - 1:
                lineas.append("")
                lineas.append("*" * 45)
                lineas.append("")
        
        # Pie del resumen
        lineas.append("")
        lineas.append("📱 Generado con Asistente de Predicación")
        lineas.append(f"👤 Para: {estudiante['nombre']}")
        
        return "\n".join(lineas)
    
    def generar_vista_previa(self, instance):
        """Mostrar vista previa del resumen"""
        if not self.historial.estudiante_actual:
            self.mostrar_error(self.textos[self.idioma]['error_sin_estudiante'])
            return
        
        texto_resumen = self.generar_resumen_texto()
        
        if not texto_resumen:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        # Crear popup de vista previa
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # ScrollView con el contenido
        scroll = ScrollView()
        
        contenido_label = Label(
            text=texto_resumen,
            text_size=(dp(350), None),
            halign='left',
            valign='top',
            font_size=dp(10),
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
            height=dp(45)
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
        popup.open()
    
    def enviar_whatsapp(self, instance):
        """Enviar por WhatsApp usando WhatsApp Web"""
        if not self.historial.estudiante_actual:
            self.mostrar_error(self.textos[self.idioma]['error_sin_estudiante'])
            return
        
        texto_resumen = self.generar_resumen_texto()
        
        if not texto_resumen:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        try:
            import webbrowser
            import urllib.parse
            
            estudiante = self.historial.obtener_estudiante_actual()
            telefono = estudiante.get('telefono', '').replace('+', '').replace(' ', '').replace('-', '')
            
            # Preparar texto para WhatsApp
            texto_whatsapp = f"🙏 *Resumen de Estudio Bíblico*\n\n{texto_resumen}"
            texto_encoded = urllib.parse.quote(texto_whatsapp)
            
            # URL de WhatsApp
            if telefono and telefono.isdigit():
                whatsapp_url = f"https://wa.me/{telefono}?text={texto_encoded}"
            else:
                whatsapp_url = f"https://wa.me/?text={texto_encoded}"
            
            webbrowser.open(whatsapp_url)
            self.mostrar_info("📱 WhatsApp", self.textos[self.idioma]['whatsapp_exito'])
            
        except Exception as e:
            print(f"❌ Error con WhatsApp: {e}")
            self.mostrar_error("Error abriendo WhatsApp")
    
    def enviar_email(self, instance):
        """Enviar por Email usando mailto"""
        if not self.historial.estudiante_actual:
            self.mostrar_error(self.textos[self.idioma]['error_sin_estudiante'])
            return
        
        texto_resumen = self.generar_resumen_texto()
        
        if not texto_resumen:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        try:
            import webbrowser
            import urllib.parse
            
            estudiante = self.historial.obtener_estudiante_actual()
            email_estudiante = estudiante.get('email', '')
            
            subject = f"📋 Resumen de Estudio - {estudiante['nombre']}"
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(texto_resumen)
            
            if email_estudiante:
                mailto_url = f"mailto:{email_estudiante}?subject={subject_encoded}&body={body_encoded}"
            else:
                mailto_url = f"mailto:?subject={subject_encoded}&body={body_encoded}"
            
            webbrowser.open(mailto_url)
            self.mostrar_info("📧 Email", self.textos[self.idioma]['email_exito'])
            
        except Exception as e:
            print(f"❌ Error con email: {e}")
            self.mostrar_error("Error abriendo email")
    
    def copiar_resumen(self, instance):
        """Copiar resumen al portapapeles"""
        if not self.historial.estudiante_actual:
            self.mostrar_error(self.textos[self.idioma]['error_sin_estudiante'])
            return
        
        texto_resumen = self.generar_resumen_texto()
        
        if not texto_resumen:
            self.mostrar_error(self.textos[self.idioma]['error_sin_consultas'])
            return
        
        self.copiar_texto(texto_resumen)
    
    def copiar_texto(self, texto):
        """Copiar texto al portapapeles"""
        try:
            from kivy.utils import platform
            if platform == 'android':
                print("📋 Texto copiado (funcionalidad limitada en Android)")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(texto)
                    print("📋 Texto copiado al portapapeles")
                except ImportError:
                    print("📋 pyperclip no disponible")
            
            self.mostrar_info(
                "Resumen Generado",
                self.textos[self.idioma]['resumen_copiado']
            )
            
        except Exception as e:
            print(f"Error copiando: {e}")
    
    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        error_label = Label(
            text=mensaje,
            text_size=(dp(250), None),
            halign='center',
            font_size=dp(12)
        )
        content.add_widget(error_label)
        
        btn_ok = Button(
            text="OK",
            size_hint_y=None,
            height=dp(35),
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
            font_size=dp(12)
        )
        content.add_widget(info_label)
        
        btn_ok = Button(
            text="OK",
            size_hint_y=None,
            height=dp(35),
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
        self.actualizar_historial_estudiante()
    
    def volver_menu(self, instance):
        """Volver al menú principal"""
        if self.volver_callback:
            self.volver_callback()
        else:
            print("⚠️ volver_callback no definido en PantallaSendResumeIndividual")


# FUNCIÓN PARA OBTENER ESTADÍSTICAS DEL HISTORIAL INDIVIDUAL
def obtener_estadisticas_individual():
    """Retorna estadísticas del historial individual"""
    historial = HistorialIndividual()
    
    if not historial.estudiante_actual:
        return None
    
    estudiante = historial.obtener_estudiante_actual()
    sesiones = historial.obtener_todas_sesiones()
    
    total_consultas = sum(len(s['consultas']) for s in sesiones)
    
    fuentes = {'sugerencias': 0, 'temas_profundos': 0, 'buscar': 0}
    for sesion in sesiones:
        for consulta in sesion['consultas']:
            fuente = consulta.get('fuente', 'otros')
            if fuente in fuentes:
                fuentes[fuente] += 1
    
    return {
        'estudiante': estudiante['nombre'],
        'total_sesiones': len(sesiones),
        'total_consultas': total_consultas,
        'fecha_inicio': estudiante['fecha_inicio'],
        'fuentes': fuentes
    }