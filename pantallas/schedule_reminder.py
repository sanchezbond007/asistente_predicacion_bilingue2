# schedule_reminder.py SIMPLIFICADO - Solo funciones esenciales
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
import datetime
import json
import os

class PantallaScheduleReminder(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        
        # Datos del recordatorio
        self.fecha_seleccionada = None
        self.hora_seleccionada = None
        
        self.construir_interfaz()
    
    def construir_interfaz(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        # TÍTULO
        titulo = Label(
            text='📅 PROGRAMAR RECORDATORIO',
            font_size=dp(24),
            bold=True,
            color=(0.6, 0.3, 0.9, 1),
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(titulo)
        
        # ESTADO SIMPLE
        self.estado_label = Label(
            text='Estado: ✅ Listo para crear recordatorio',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(12),
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.estado_label)
        
        # CAMPOS DE ENTRADA
        
        # Título del recordatorio
        layout.add_widget(Label(
            text='📝 Título del recordatorio:',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(14),
            halign='left'
        ))
        
        self.titulo_input = TextInput(
            hint_text='Ej: Visita a Juan',
            size_hint_y=None,
            height=dp(40),
            font_size=dp(14),
            multiline=False
        )
        layout.add_widget(self.titulo_input)
        
        # Descripción
        layout.add_widget(Label(
            text='📋 Descripción:',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(14),
            halign='left'
        ))
        
        self.descripcion_input = TextInput(
            hint_text='Ej: Revisita - Mostrar Apocalipsis 21:3-4',
            size_hint_y=None,
            height=dp(60),
            font_size=dp(14),
            multiline=True
        )
        layout.add_widget(self.descripcion_input)
        
        # Ubicación
        layout.add_widget(Label(
            text='📍 Ubicación:',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(14),
            halign='left'
        ))
        
        self.ubicacion_input = TextInput(
            hint_text='Dirección o referencia',
            size_hint_y=None,
            height=dp(40),
            font_size=dp(14),
            multiline=False
        )
        layout.add_widget(self.ubicacion_input)
        
        # BOTONES DE FECHA Y HORA
        fecha_hora_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        self.btn_fecha = Button(
            text='📅 Seleccionar Fecha',
            background_color=(0.2, 0.5, 0.7, 1),
            font_size=dp(14)
        )
        self.btn_fecha.bind(on_press=self.seleccionar_fecha)
        fecha_hora_layout.add_widget(self.btn_fecha)
        
        self.btn_hora = Button(
            text='⏰ Seleccionar Hora',
            background_color=(0.3, 0.6, 0.3, 1),
            font_size=dp(14)
        )
        self.btn_hora.bind(on_press=self.seleccionar_hora)
        fecha_hora_layout.add_widget(self.btn_hora)
        
        layout.add_widget(fecha_hora_layout)
        
        # ESPACIADOR
        layout.add_widget(Label(size_hint_y=None, height=dp(20)))
        
        # BOTÓN PRINCIPAL - GUARDAR
        self.btn_guardar = Button(
            text='💾 Guardar Recordatorio',
            background_color=(0.5, 0.2, 0.8, 1),
            size_hint_y=None,
            height=dp(60),
            font_size=dp(16),
            bold=True
        )
        self.btn_guardar.bind(on_press=self.guardar_recordatorio)
        layout.add_widget(self.btn_guardar)
        
        # ESPACIADOR
        layout.add_widget(Label(size_hint_y=None, height=dp(10)))
        
        # BOTÓN VOLVER
        btn_volver = Button(
            text='🔙 Volver al Menú',
            background_color=(0.7, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        btn_volver.bind(on_press=self.volver)
        layout.add_widget(btn_volver)
        
        self.add_widget(layout)
    
    def seleccionar_fecha(self, instance):
        """Selector de fecha simple"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # Título
        content.add_widget(Label(
            text='Selecciona una fecha:',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(16)
        ))
        
        # Botones de fechas rápidas
        fechas_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        hoy = datetime.date.today()
        
        # Hoy
        btn_hoy = Button(
            text=f'📅 Hoy ({hoy.strftime("%d/%m/%Y")})',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        btn_hoy.bind(on_press=lambda x: self.fecha_seleccionada_callback(hoy))
        fechas_layout.add_widget(btn_hoy)
        
        # Mañana
        manana = hoy + datetime.timedelta(days=1)
        btn_manana = Button(
            text=f'📅 Mañana ({manana.strftime("%d/%m/%Y")})',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_manana.bind(on_press=lambda x: self.fecha_seleccionada_callback(manana))
        fechas_layout.add_widget(btn_manana)
        
        # Próxima semana
        semana = hoy + datetime.timedelta(days=7)
        btn_semana = Button(
            text=f'📅 En una semana ({semana.strftime("%d/%m/%Y")})',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.6, 0.4, 0.2, 1)
        )
        btn_semana.bind(on_press=lambda x: self.fecha_seleccionada_callback(semana))
        fechas_layout.add_widget(btn_semana)
        
        content.add_widget(fechas_layout)
        
        # Botón cancelar
        btn_cancelar = Button(
            text='❌ Cancelar',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.7, 0.3, 0.3, 1)
        )
        content.add_widget(btn_cancelar)
        
        # Crear popup
        self.popup_fecha = Popup(
            title='Seleccionar Fecha',
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        btn_cancelar.bind(on_press=self.popup_fecha.dismiss)
        self.popup_fecha.open()
    
    def fecha_seleccionada_callback(self, fecha):
        """Callback cuando se selecciona una fecha"""
        self.fecha_seleccionada = fecha
        self.btn_fecha.text = f'📅 {fecha.strftime("%d/%m/%Y")}'
        self.btn_fecha.background_color = (0.3, 0.7, 0.3, 1)
        self.popup_fecha.dismiss()
        self.actualizar_estado()
    
    def seleccionar_hora(self, instance):
        """Selector de hora simple"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # Título
        content.add_widget(Label(
            text='Selecciona una hora:',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(16)
        ))
        
        # Botones de horas comunes
        horas_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        horas_comunes = [
            ('09:00', '🌅 9:00 AM'),
            ('10:00', '☀️ 10:00 AM'),
            ('14:00', '🌞 2:00 PM'),
            ('16:00', '🌇 4:00 PM'),
            ('19:00', '🌆 7:00 PM')
        ]
        
        for hora_valor, hora_texto in horas_comunes:
            btn_hora = Button(
                text=hora_texto,
                size_hint_y=None,
                height=dp(35),
                background_color=(0.4, 0.6, 0.8, 1)
            )
            btn_hora.bind(on_press=lambda x, h=hora_valor: self.hora_seleccionada_callback(h))
            horas_layout.add_widget(btn_hora)
        
        content.add_widget(horas_layout)
        
        # Botón cancelar
        btn_cancelar = Button(
            text='❌ Cancelar',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.7, 0.3, 0.3, 1)
        )
        content.add_widget(btn_cancelar)
        
        # Crear popup
        self.popup_hora = Popup(
            title='Seleccionar Hora',
            content=content,
            size_hint=(0.8, 0.7),
            auto_dismiss=False
        )
        
        btn_cancelar.bind(on_press=self.popup_hora.dismiss)
        self.popup_hora.open()
    
    def hora_seleccionada_callback(self, hora):
        """Callback cuando se selecciona una hora"""
        self.hora_seleccionada = hora
        self.btn_hora.text = f'⏰ {hora}'
        self.btn_hora.background_color = (0.3, 0.7, 0.3, 1)
        self.popup_hora.dismiss()
        self.actualizar_estado()
    
    def actualizar_estado(self):
        """Actualizar el estado de la interfaz"""
        if self.fecha_seleccionada and self.hora_seleccionada:
            self.estado_label.text = f'✅ Fecha: {self.fecha_seleccionada.strftime("%d/%m/%Y")} | Hora: {self.hora_seleccionada}'
            self.estado_label.color = (0.3, 0.8, 0.3, 1)
        elif self.fecha_seleccionada:
            self.estado_label.text = f'⏳ Fecha seleccionada: {self.fecha_seleccionada.strftime("%d/%m/%Y")} | Falta hora'
            self.estado_label.color = (0.8, 0.6, 0.2, 1)
        elif self.hora_seleccionada:
            self.estado_label.text = f'⏳ Hora seleccionada: {self.hora_seleccionada} | Falta fecha'
            self.estado_label.color = (0.8, 0.6, 0.2, 1)
        else:
            self.estado_label.text = '⏳ Selecciona fecha y hora'
            self.estado_label.color = (0.7, 0.7, 0.7, 1)
    
    def guardar_recordatorio(self, instance):
        """Guardar el recordatorio"""
        # Validaciones
        if not self.titulo_input.text.strip():
            self.mostrar_popup("Error", "❌ El título es obligatorio")
            return
        
        if not self.fecha_seleccionada:
            self.mostrar_popup("Error", "❌ Debes seleccionar una fecha")
            return
        
        if not self.hora_seleccionada:
            self.mostrar_popup("Error", "❌ Debes seleccionar una hora")
            return
        
        try:
            # Crear fecha y hora completa
            fecha_hora = datetime.datetime.combine(
                self.fecha_seleccionada,
                datetime.time.fromisoformat(self.hora_seleccionada)
            )
            
            # Crear recordatorio
            recordatorio = {
                'titulo': self.titulo_input.text.strip(),
                'descripcion': self.descripcion_input.text.strip(),
                'ubicacion': self.ubicacion_input.text.strip(),
                'fecha_hora': fecha_hora.isoformat(),
                'creado': datetime.datetime.now().isoformat(),
                'completado': False
            }
            
            # Cargar recordatorios existentes
            filename = "recordatorios_predicacion.json"
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    recordatorios = json.load(f)
            else:
                recordatorios = []
            
            # Agregar nuevo recordatorio
            recordatorios.append(recordatorio)
            
            # Guardar
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(recordatorios, f, ensure_ascii=False, indent=2)
            
            # Mostrar confirmación
            mensaje = f"✅ Recordatorio guardado:\n\n📝 {recordatorio['titulo']}\n📅 {fecha_hora.strftime('%d/%m/%Y %H:%M')}"
            self.mostrar_popup("Guardado", mensaje)
            
            # Limpiar formulario
            self.limpiar_formulario()
            
        except Exception as e:
            self.mostrar_popup("Error", f"❌ Error guardando: {str(e)}")
    
    def limpiar_formulario(self):
        """Limpiar todos los campos"""
        self.titulo_input.text = ''
        self.descripcion_input.text = ''
        self.ubicacion_input.text = ''
        self.fecha_seleccionada = None
        self.hora_seleccionada = None
        
        self.btn_fecha.text = '📅 Seleccionar Fecha'
        self.btn_fecha.background_color = (0.2, 0.5, 0.7, 1)
        
        self.btn_hora.text = '⏰ Seleccionar Hora'
        self.btn_hora.background_color = (0.3, 0.6, 0.3, 1)
        
        self.actualizar_estado()
    
    def mostrar_popup(self, titulo, mensaje):
        """Mostrar popup informativo"""
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        label = Label(
            text=mensaje,
            text_size=(dp(250), None),
            halign='center',
            font_size=dp(14),
            size_hint_y=None
        )
        label.bind(texture_size=label.setter('size'))
        content.add_widget(label)
        
        btn_ok = Button(
            text='OK',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.6, 0.9, 1)
        )
        content.add_widget(btn_ok)
        
        popup = Popup(
            title=titulo,
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()
    
    def volver(self, instance=None):
        """Volver al menú principal"""
        if self.volver_callback:
            self.volver_callback()
    
    def cambiar_idioma(self, nuevo_idioma):
        """Cambiar idioma (placeholder)"""
        self.idioma = nuevo_idioma
        # Aquí podrías actualizar los textos según el idioma