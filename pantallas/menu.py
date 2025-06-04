# menu.py - TU DISEÑO ORIGINAL + BOTÓN RECORDATORIOS + SEND RESUME FUNCIONAL
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
import datetime
import json
import os

class PantallaMenu(Screen):
    def __init__(self, **kwargs):
        # EXTRAER CALLBACKS ANTES DE PASAR A SUPER() - SOLUCIÓN DEL ERROR
        self.navegacion_callback = kwargs.pop('navegacion_callback', None)
        self.programar_recordatorio_callback = kwargs.pop('programar_recordatorio_callback', None)
        self.buscar_callback = kwargs.pop('buscar_callback', None)
        self.profundos_callback = kwargs.pop('profundos_callback', None)
        self.sugerencias_callback = kwargs.pop('sugerencias_callback', None)
        self.volver_callback = kwargs.pop('volver_callback', None)
        self.idioma = kwargs.pop('idioma', 'es')
        
        # AHORA SÍ LLAMAR A SUPER() SIN PROPIEDADES INVÁLIDAS
        super().__init__(**kwargs)
        
        self.construir_interfaz()
    
    def construir_interfaz(self):
        self.clear_widgets()
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=dp(20), padding=dp(20))
        
        # Título principal
        titulo = Label(
            text='🏠 ASISTENTE PREDICACIÓN' if self.idioma == 'es' else '🏠 PREACHING ASSISTANT',
            font_size=dp(26),
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.6, 0.9, 1),
            bold=True
        )
        layout.add_widget(titulo)
        
        # ESTADÍSTICAS DE RECORDATORIOS (NUEVA LÍNEA)
        self.stats_label = Label(
            text='Cargando estadísticas...',
            font_size=dp(12),
            size_hint_y=None,
            height=dp(30),
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.stats_label)
        
        # Grid de botones principales (3x2)
        grid = GridLayout(cols=2, spacing=dp(15), size_hint_y=None, height=dp(300))
        
        # Botón 1: Programar Recordatorio
        btn_recordatorio = Button(
            text='⏰\nProgramar\nRecordatorio' if self.idioma == 'es' else '⏰\nSchedule\nReminder',
            background_color=(0.6, 0.2, 0.8, 1),
            font_size=dp(14)
        )
        btn_recordatorio.bind(on_press=self.ir_a_programar_recordatorio)
        grid.add_widget(btn_recordatorio)
        
        # Botón 2: Ver Mis Recordatorios (NUEVO BOTÓN)
        btn_mis_recordatorios = Button(
            text='📋\nMis\nRecordatorios' if self.idioma == 'es' else '📋\nMy\nReminders',
            background_color=(0.2, 0.6, 0.9, 1),
            font_size=dp(14)
        )
        btn_mis_recordatorios.bind(on_press=self.ir_a_mis_recordatorios)
        grid.add_widget(btn_mis_recordatorios)
        
        # Botón 3: Casa en Casa
        btn_casa_casa = Button(
            text='🏠\nCasa en\nCasa' if self.idioma == 'es' else '🏠\nHouse to\nHouse',
            background_color=(0.2, 0.7, 0.3, 1),
            font_size=dp(14)
        )
        btn_casa_casa.bind(on_press=self.ir_a_casa_en_casa)
        grid.add_widget(btn_casa_casa)
        
        # Botón 4: Send Resume - VERSIÓN FINAL
        btn_send_resume = Button(
            text='📄\nEnviar\nResumen' if self.idioma == 'es' else '📄\nSend\nResume',
            background_color=(0.3, 0.5, 0.7, 1),
            font_size=dp(14)
        )
        btn_send_resume.bind(on_press=self.ir_a_send_resume)
        grid.add_widget(btn_send_resume)
        
        # Botón 5: Búsqueda
        btn_busqueda = Button(
            text='🔍\nBúsqueda de\nEscrituras' if self.idioma == 'es' else '🔍\nScripture\nSearch',
            background_color=(0.7, 0.3, 0.5, 1),
            font_size=dp(14)
        )
        btn_busqueda.bind(on_press=self.ir_a_busqueda)
        grid.add_widget(btn_busqueda)
        
        # Botón 6: Temas Profundos
        btn_profundos = Button(
            text='📚\nTemas\nProfundos' if self.idioma == 'es' else '📚\nDeep\nTopics',
            background_color=(0.5, 0.7, 0.3, 1),
            font_size=dp(14)
        )
        btn_profundos.bind(on_press=self.ir_a_profundos)
        grid.add_widget(btn_profundos)
        
        layout.add_widget(grid)
        
        # Botón de sugerencias
        btn_sugerencias = Button(
            text='💡 Sugerencias para Hoy' if self.idioma == 'es' else '💡 Today\'s Suggestions',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.9, 0.6, 0.2, 1),
            font_size=dp(14)
        )
        btn_sugerencias.bind(on_press=self.ir_a_sugerencias)
        layout.add_widget(btn_sugerencias)
        
        # Botón de idioma
        texto_idioma = 'English' if self.idioma == 'es' else 'Español'
        btn_idioma = Button(
            text=f'🌐 {texto_idioma}',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.5, 0.5, 0.5, 1),
            font_size=dp(12)
        )
        btn_idioma.bind(on_press=self.cambiar_idioma)
        layout.add_widget(btn_idioma)
        
        # AVISO LEGAL (RESTAURADO)
        if self.idioma == 'es':
            aviso_text = "⚖️ Aviso Legal: Esta aplicación es una herramienta de ayuda personal para la predicación. " \
                        "Los usuarios son responsables del uso de la información bíblica proporcionada. " \
                        "Consulte siempre las publicaciones oficiales de los Testigos de Jehová."
        else:
            aviso_text = "⚖️ Legal Notice: This application is a personal aid tool for preaching. " \
                        "Users are responsible for the use of the biblical information provided. " \
                        "Always consult official publications of Jehovah's Witnesses."
        
        aviso_legal = Label(
            text=aviso_text,
            font_size=dp(8),
            text_size=(dp(300), None),
            halign='center',
            size_hint_y=None,
            height=dp(40),
            color=(0.6, 0.6, 0.6, 1)
        )
        layout.add_widget(aviso_legal)
        
        self.add_widget(layout)
        
        # CARGAR ESTADÍSTICAS INICIALES
        self.actualizar_estadisticas()
        
        # Programar actualización automática cada 30 segundos
        Clock.schedule_interval(self.actualizar_estadisticas, 30)
    
    def cargar_estadisticas_recordatorios(self):
        """Cargar estadísticas de recordatorios"""
        try:
            filename = "recordatorios_predicacion.json"
            if not os.path.exists(filename):
                return {'total': 0, 'hoy': 0, 'vencidos': 0, 'futuros': 0}
            
            with open(filename, 'r', encoding='utf-8') as f:
                recordatorios = json.load(f)
            
            ahora = datetime.datetime.now()
            hoy = ahora.date()
            
            stats = {'total': len(recordatorios), 'hoy': 0, 'vencidos': 0, 'futuros': 0}
            
            for rec in recordatorios:
                try:
                    if rec.get('completado', False):
                        continue
                    
                    fecha_rec = datetime.datetime.fromisoformat(rec['fecha_hora'])
                    
                    if fecha_rec.date() < hoy:
                        stats['vencidos'] += 1
                    elif fecha_rec.date() == hoy:
                        stats['hoy'] += 1
                    else:
                        stats['futuros'] += 1
                        
                except Exception as e:
                    print(f"Error procesando recordatorio: {e}")
            
            return stats
            
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
            return {'total': 0, 'hoy': 0, 'vencidos': 0, 'futuros': 0}
    
    def actualizar_estadisticas(self, dt=None):
        """Actualizar las estadísticas mostradas"""
        try:
            stats = self.cargar_estadisticas_recordatorios()
            
            if stats['total'] == 0:
                texto = "📋 No tienes recordatorios - ¡Crea tu primer recordatorio!"
            else:
                texto = f"📊 Total: {stats['total']} | 🔴 Vencidos: {stats['vencidos']} | 🟡 Hoy: {stats['hoy']} | 🟢 Futuros: {stats['futuros']}"
            
            self.stats_label.text = texto
            
            # Cambiar color según urgencia
            if stats['hoy'] > 0:
                self.stats_label.color = (1, 0.7, 0.2, 1)  # Naranja
            elif stats['vencidos'] > 0:
                self.stats_label.color = (0.8, 0.5, 0.5, 1)  # Rojo suave
            else:
                self.stats_label.color = (0.7, 0.7, 0.7, 1)  # Gris normal
                
        except Exception as e:
            print(f"Error actualizando estadísticas: {e}")
            self.stats_label.text = "📊 Error cargando estadísticas"
    
    # ===== NUEVA FUNCIÓN: FORZAR IDIOMA SIN RECREAR INTERFAZ =====
    def forzar_idioma(self, nuevo_idioma):
        """Forzar actualización de idioma sin recrear interfaz completa"""
        print(f"🔧 Forzando idioma del menú a: {nuevo_idioma}")
        self.idioma = nuevo_idioma
        # No llamar construir_interfaz() aquí para evitar perder callbacks
        self.actualizar_estadisticas()
    
    # FUNCIONES DE NAVEGACIÓN (TU CÓDIGO ORIGINAL)
    def ir_a_programar_recordatorio(self, instance):
        print("🎯 Botón 'Programar Recordatorio' presionado")
        if self.programar_recordatorio_callback:
            self.programar_recordatorio_callback()
        else:
            print("⚠️ programar_recordatorio_callback no está configurado")
    
    def ir_a_mis_recordatorios(self, instance):
        """NUEVA FUNCIÓN - Ir a Mis Recordatorios"""
        print("🎯 Botón 'Mis Recordatorios' presionado")
        if self.navegacion_callback:
            self.navegacion_callback('mis_recordatorios')
        else:
            print("⚠️ navegacion_callback no está configurado")
    
    def ir_a_casa_en_casa(self, instance):
        print("🎯 Botón 'Casa en Casa' presionado")
        if self.navegacion_callback:
            self.navegacion_callback('casa_en_casa')
        else:
            print("⚠️ navegacion_callback no está configurado")
    
    # ===== FUNCIÓN SEND RESUME FINAL (SIN PRUEBA VISUAL) =====
    def ir_a_send_resume(self, instance):
        print("🎯 Botón 'Send Resume' presionado")
        
        if self.navegacion_callback:
            print("🔧 Llamando navegacion_callback('send_resume')")
            self.navegacion_callback('send_resume')
        else:
            print("⚠️ navegacion_callback no está configurado")
    
    def ir_a_busqueda(self, instance):
        print("🎯 Botón 'Búsqueda' presionado")
        if self.buscar_callback:
            self.buscar_callback()
        else:
            print("⚠️ buscar_callback no está configurado")
    
    def ir_a_profundos(self, instance):
        print("🎯 Botón 'Temas Profundos' presionado")
        if self.profundos_callback:
            self.profundos_callback()
        else:
            print("⚠️ profundos_callback no está configurado")
    
    def ir_a_sugerencias(self, instance):
        print("🎯 Botón 'Sugerencias' presionado")
        if self.sugerencias_callback:
            self.sugerencias_callback()
        else:
            print("⚠️ sugerencias_callback no está configurado")
    
    def cambiar_idioma(self, instance):
        """Cambiar idioma"""
        self.idioma = 'en' if self.idioma == 'es' else 'es'
        self.construir_interfaz()
        print(f"🌐 Idioma cambiado a: {self.idioma}")
    
    def on_enter(self):
        """Cuando se entra a la pantalla del menú"""
        self.actualizar_estadisticas()