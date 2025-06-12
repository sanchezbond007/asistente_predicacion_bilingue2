# mis_recordatorios.py - PANTALLA VER RECORDATORIOS COMPLETA
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.clock import Clock
import datetime
import json
import os

class PantallaMisRecordatorios(Screen):
    def __init__(self, volver_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.recordatorios = []
        
        self.construir_interfaz()
        self.cargar_recordatorios()
        
        # Auto-refresh cada 30 segundos
        Clock.schedule_interval(self.actualizar_lista, 30)
    
    def construir_interfaz(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # HEADER CORREGIDO CON TEXTO CLARO
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        titulo = Label(
            text='📋 MIS RECORDATORIOS',
            font_size=dp(22),
            bold=True,
            color=(0.2, 0.6, 0.9, 1),
            size_hint_x=0.6
        )
        header.add_widget(titulo)
        
        # BOTÓN REFRESCAR - TEXTO CLARO
        btn_actualizar = Button(
            text='🔄 Refrescar',
            size_hint_x=0.2,
            background_color=(0.3, 0.7, 0.3, 1),
            font_size=dp(11)
        )
        btn_actualizar.bind(on_press=self.actualizar_lista)
        header.add_widget(btn_actualizar)
        
        # BOTÓN LIMPIAR VENCIDOS - TEXTO ESPECÍFICO
        btn_limpiar = Button(
            text='🗑️ Vencidos',
            size_hint_x=0.2,
            background_color=(0.7, 0.3, 0.3, 1),
            font_size=dp(11)
        )
        btn_limpiar.bind(on_press=self.limpiar_vencidos)
        header.add_widget(btn_limpiar)
        
        layout.add_widget(header)
        
        # ESTADÍSTICAS
        self.stats_label = Label(
            text='Cargando estadísticas...',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(12),
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.stats_label)
        
        # ÁREA DE SCROLL PARA RECORDATORIOS
        scroll = ScrollView()
        self.recordatorios_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            padding=[0, dp(5)]
        )
        self.recordatorios_layout.bind(minimum_height=self.recordatorios_layout.setter('height'))
        
        scroll.add_widget(self.recordatorios_layout)
        layout.add_widget(scroll)
        
        # BOTONES INFERIORES
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        btn_hoy = Button(
            text='📅 Solo Hoy',
            background_color=(0.9, 0.6, 0.2, 1)
        )
        btn_hoy.bind(on_press=self.filtrar_hoy)
        botones_layout.add_widget(btn_hoy)
        
        btn_todos = Button(
            text='📋 Todos',
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_todos.bind(on_press=self.mostrar_todos)
        botones_layout.add_widget(btn_todos)
        
        btn_volver = Button(
            text='🔙 Volver',
            background_color=(0.7, 0.3, 0.3, 1)
        )
        btn_volver.bind(on_press=self.volver)
        botones_layout.add_widget(btn_volver)
        
        layout.add_widget(botones_layout)
        
        self.add_widget(layout)
    
    def cargar_recordatorios(self):
        """Cargar recordatorios desde el archivo JSON"""
        try:
            filename = "recordatorios_predicacion.json"
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    self.recordatorios = json.load(f)
            else:
                self.recordatorios = []
                
            # Ordenar por fecha
            self.recordatorios.sort(key=lambda x: x.get('fecha_hora', ''))
            
        except Exception as e:
            print(f"Error cargando recordatorios: {e}")
            self.recordatorios = []
        
        self.actualizar_interfaz()
    
    def actualizar_lista(self, dt=None):
        """Actualizar la lista de recordatorios"""
        self.cargar_recordatorios()
    
    def actualizar_interfaz(self):
        """Actualizar la interfaz con los recordatorios"""
        self.recordatorios_layout.clear_widgets()
        
        ahora = datetime.datetime.now()
        hoy = ahora.date()
        
        # ESTADÍSTICAS
        total = len(self.recordatorios)
        vencidos = 0
        hoy_count = 0
        futuros = 0
        
        for rec in self.recordatorios:
            try:
                fecha_rec = datetime.datetime.fromisoformat(rec['fecha_hora']).date()
                if fecha_rec < hoy:
                    vencidos += 1
                elif fecha_rec == hoy:
                    hoy_count += 1
                else:
                    futuros += 1
            except:
                pass
        
        self.stats_label.text = f"Total: {total} | 🔴 Vencidos: {vencidos} | 🟡 Hoy: {hoy_count} | 🟢 Futuros: {futuros}"
        
        if not self.recordatorios:
            # NO HAY RECORDATORIOS
            mensaje = Label(
                text='📋 No tienes recordatorios guardados\n\n'
                     '💡 Ve a "Programar Recordatorio" para crear uno',
                text_size=(dp(300), None),
                halign='center',
                font_size=dp(16),
                color=(0.6, 0.6, 0.6, 1),
                size_hint_y=None,
                height=dp(100)
            )
            self.recordatorios_layout.add_widget(mensaje)
            return
        
        # MOSTRAR RECORDATORIOS
        for i, recordatorio in enumerate(self.recordatorios):
            card = self.crear_card_recordatorio(recordatorio, i)
            self.recordatorios_layout.add_widget(card)
    
    def crear_card_recordatorio(self, recordatorio, index):
        """Crear una tarjeta para mostrar un recordatorio"""
        
        # Determinar el color según la fecha
        try:
            fecha_hora = datetime.datetime.fromisoformat(recordatorio['fecha_hora'])
            ahora = datetime.datetime.now()
            
            if fecha_hora.date() < ahora.date():
                color = (0.8, 0.3, 0.3, 1)  # Rojo - Vencido
                estado = "🔴 VENCIDO"
            elif fecha_hora.date() == ahora.date():
                if fecha_hora.time() < ahora.time():
                    color = (0.9, 0.5, 0.2, 1)  # Naranja - Vencido hoy
                    estado = "🟠 PASADO"
                else:
                    color = (0.9, 0.8, 0.2, 1)  # Amarillo - Hoy
                    estado = "🟡 HOY"
            else:
                color = (0.3, 0.7, 0.3, 1)  # Verde - Futuro
                estado = "🟢 PRÓXIMO"
                
            fecha_str = fecha_hora.strftime('%d/%m/%Y %H:%M')
            
        except:
            color = (0.5, 0.5, 0.5, 1)  # Gris - Error
            estado = "❓ ERROR"
            fecha_str = "Fecha inválida"
        
        # CARD PRINCIPAL
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(100),
            spacing=dp(5)
        )
        
        # CONTENIDO DE LA CARD
        main_btn = Button(
            background_color=color,
            size_hint_y=None,
            height=dp(80)
        )
        
        # Texto del botón
        titulo = recordatorio.get('titulo', 'Sin título')[:25]
        ubicacion = recordatorio.get('ubicacion', '')
        ubicacion_text = f"\n📍 {ubicacion}" if ubicacion else ""
        
        main_btn.text = f"{estado}\n📝 {titulo}\n📅 {fecha_str}{ubicacion_text}"
        main_btn.font_size = dp(11)
        main_btn.text_size = (dp(280), None)
        main_btn.halign = 'center'
        main_btn.valign = 'center'
        
        # Bind para mostrar detalles
        main_btn.bind(on_press=lambda x, idx=index: self.mostrar_detalles(idx))
        
        card.add_widget(main_btn)
        
        # BOTONES DE ACCIÓN
        acciones = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(15),
            spacing=dp(2)
        )
        
        btn_completar = Button(
            text='✅',
            background_color=(0.2, 0.7, 0.2, 1),
            font_size=dp(10),
            size_hint_x=0.25
        )
        btn_completar.bind(on_press=lambda x, idx=index: self.marcar_completado(idx))
        acciones.add_widget(btn_completar)
        
        btn_posponer = Button(
            text='⏰',
            background_color=(0.7, 0.5, 0.2, 1),
            font_size=dp(10),
            size_hint_x=0.25
        )
        btn_posponer.bind(on_press=lambda x, idx=index: self.posponer(idx))
        acciones.add_widget(btn_posponer)
        
        btn_editar = Button(
            text='✏️',
            background_color=(0.2, 0.5, 0.7, 1),
            font_size=dp(10),
            size_hint_x=0.25
        )
        btn_editar.bind(on_press=lambda x, idx=index: self.editar(idx))
        acciones.add_widget(btn_editar)
        
        btn_eliminar = Button(
            text='🗑️',
            background_color=(0.7, 0.2, 0.2, 1),
            font_size=dp(10),
            size_hint_x=0.25
        )
        btn_eliminar.bind(on_press=lambda x, idx=index: self.eliminar(idx))
        acciones.add_widget(btn_eliminar)
        
        card.add_widget(acciones)
        
        return card
    
    def mostrar_detalles(self, index):
        """Mostrar detalles completos del recordatorio"""
        try:
            rec = self.recordatorios[index]
            
            content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
            
            scroll = ScrollView()
            detalles_text = f"""📝 TÍTULO: {rec.get('titulo', 'Sin título')}

📅 FECHA Y HORA: {datetime.datetime.fromisoformat(rec['fecha_hora']).strftime('%d/%m/%Y %H:%M')}

📍 UBICACIÓN: {rec.get('ubicacion', 'No especificada')}

📋 DESCRIPCIÓN: {rec.get('descripcion', 'Sin descripción')}

🕒 CREADO: {datetime.datetime.fromisoformat(rec['creado']).strftime('%d/%m/%Y %H:%M')}"""
            
            label = Label(
                text=detalles_text,
                text_size=(dp(280), None),
                halign='left',
                valign='top',
                font_size=dp(13),
                size_hint_y=None
            )
            label.bind(texture_size=label.setter('size'))
            scroll.add_widget(label)
            content.add_widget(scroll)
            
            btn_cerrar = Button(
                text='Cerrar',
                size_hint_y=None,
                height=dp(40),
                background_color=(0.2, 0.6, 0.9, 1)
            )
            content.add_widget(btn_cerrar)
            
            popup = Popup(
                title=f"Recordatorio #{index + 1}",
                content=content,
                size_hint=(0.9, 0.7),
                auto_dismiss=False
            )
            
            btn_cerrar.bind(on_press=popup.dismiss)
            popup.open()
            
        except Exception as e:
            self.mostrar_popup("Error", f"No se pudo mostrar el recordatorio: {e}")
    
    def marcar_completado(self, index):
        """Marcar recordatorio como completado"""
        try:
            # Agregar marca de completado
            self.recordatorios[index]['completado'] = True
            self.recordatorios[index]['fecha_completado'] = datetime.datetime.now().isoformat()
            
            self.guardar_recordatorios()
            self.actualizar_interfaz()
            
            self.mostrar_popup("Completado", "✅ Recordatorio marcado como completado")
            
        except Exception as e:
            self.mostrar_popup("Error", f"No se pudo marcar como completado: {e}")
    
    def posponer(self, index):
        """Posponer recordatorio por 1 hora"""
        try:
            fecha_actual = datetime.datetime.fromisoformat(self.recordatorios[index]['fecha_hora'])
            nueva_fecha = fecha_actual + datetime.timedelta(hours=1)
            
            self.recordatorios[index]['fecha_hora'] = nueva_fecha.isoformat()
            self.recordatorios[index]['pospuesto'] = True
            
            self.guardar_recordatorios()
            self.actualizar_interfaz()
            
            self.mostrar_popup("Pospuesto", f"⏰ Recordatorio pospuesto hasta:\n{nueva_fecha.strftime('%d/%m/%Y %H:%M')}")
            
        except Exception as e:
            self.mostrar_popup("Error", f"No se pudo posponer: {e}")
    
    def editar(self, index):
        """Editar recordatorio (placeholder)"""
        self.mostrar_popup("Editar", "🚧 Función de edición próximamente...\n\nPor ahora puedes eliminarlo y crear uno nuevo.")
    
    def eliminar(self, index):
        """Eliminar recordatorio con confirmación"""
        try:
            rec = self.recordatorios[index]
            titulo = rec.get('titulo', 'Sin título')
            
            # Popup de confirmación
            content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
            
            label = Label(
                text=f"¿Eliminar este recordatorio?\n\n📝 {titulo}\n📅 {datetime.datetime.fromisoformat(rec['fecha_hora']).strftime('%d/%m/%Y %H:%M')}",
                text_size=(dp(250), None),
                halign='center',
                font_size=dp(14),
                size_hint_y=None,
                height=dp(100)
            )
            content.add_widget(label)
            
            botones = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
            
            btn_si = Button(text='🗑️ Sí, Eliminar', background_color=(0.8, 0.3, 0.3, 1))
            btn_no = Button(text='❌ Cancelar', background_color=(0.3, 0.6, 0.3, 1))
            
            botones.add_widget(btn_si)
            botones.add_widget(btn_no)
            content.add_widget(botones)
            
            popup = Popup(
                title="Confirmar Eliminación",
                content=content,
                size_hint=(0.8, 0.5),
                auto_dismiss=False
            )
            
            def confirmar_eliminar(instance):
                try:
                    del self.recordatorios[index]
                    self.guardar_recordatorios()
                    self.actualizar_interfaz()
                    popup.dismiss()
                    self.mostrar_popup("Eliminado", "🗑️ Recordatorio eliminado correctamente")
                except Exception as e:
                    popup.dismiss()
                    self.mostrar_popup("Error", f"No se pudo eliminar: {e}")
            
            btn_si.bind(on_press=confirmar_eliminar)
            btn_no.bind(on_press=popup.dismiss)
            
            popup.open()
            
        except Exception as e:
            self.mostrar_popup("Error", f"Error al eliminar: {e}")
    
    def filtrar_hoy(self, instance):
        """Mostrar solo recordatorios de hoy"""
        hoy = datetime.date.today()
        recordatorios_hoy = []
        
        for rec in self.recordatorios:
            try:
                fecha_rec = datetime.datetime.fromisoformat(rec['fecha_hora']).date()
                if fecha_rec == hoy:
                    recordatorios_hoy.append(rec)
            except:
                pass
        
        # Temporalmente mostrar solo los de hoy
        self.recordatorios_temp = self.recordatorios.copy()
        self.recordatorios = recordatorios_hoy
        self.actualizar_interfaz()
    
    def mostrar_todos(self, instance):
        """Mostrar todos los recordatorios"""
        if hasattr(self, 'recordatorios_temp'):
            self.recordatorios = self.recordatorios_temp
            delattr(self, 'recordatorios_temp')
        self.cargar_recordatorios()
    
    def limpiar_vencidos(self, instance):
        """Eliminar recordatorios vencidos"""
        try:
            hoy = datetime.date.today()
            antes = len(self.recordatorios)
            
            self.recordatorios = [
                rec for rec in self.recordatorios
                if datetime.datetime.fromisoformat(rec['fecha_hora']).date() >= hoy
            ]
            
            despues = len(self.recordatorios)
            eliminados = antes - despues
            
            if eliminados > 0:
                self.guardar_recordatorios()
                self.actualizar_interfaz()
                self.mostrar_popup("Limpieza", f"🗑️ {eliminados} recordatorios vencidos eliminados")
            else:
                self.mostrar_popup("Limpieza", "✅ No hay recordatorios vencidos para eliminar")
                
        except Exception as e:
            self.mostrar_popup("Error", f"Error limpiando recordatorios: {e}")
    
    def guardar_recordatorios(self):
        """Guardar recordatorios en el archivo"""
        try:
            filename = "recordatorios_predicacion.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.recordatorios, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando recordatorios: {e}")
    
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
    
    def volver(self, instance):
        """Volver al menú principal"""
        if self.volver_callback:
            self.volver_callback()
        else:
            print("No hay callback para volver")