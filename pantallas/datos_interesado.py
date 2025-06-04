from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp
import datetime
import json
import os
import webbrowser
import urllib.parse
from gestor_temas import gestor_temas, obtener_mensaje_completo_para_envio, establecer_interesado_para_captura

class PantallaDatosInteresado(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        self.temas_automaticos = []
        self.temas_seleccionados = set()
        self.mensaje_personalizado = ""
        
        self.textos = {
            'es': {
                'titulo': '📧 ENVIAR RESUMEN POR INTERESADO',
                'nombre_label': '👤 Nombre del interesado: *',
                'nombre_hint': 'Ej: María González',
                'buscar_btn': '🔍 Buscar Temas de este Interesado',
                'email_label': '📧 Email:',
                'email_hint': 'maria.gonzalez@email.com',
                'telefono_label': '📱 Teléfono:',
                'telefono_hint': '+1 407-590-6349',
                'temas_titulo': '📚 TEMAS TRATADOS',
                'agregar_tema_label': '➕ Agregar tema manualmente:',
                'agregar_tema_hint': 'Ej: Reino de Dios - Mateo 6:9',
                'agregar_btn': '➕ Agregar',
                'vista_previa_label': '👁️ VISTA PREVIA:',
                'editar_btn': '✏️ Editar Mensaje',
                'copiar_btn': '📋 Copiar Todo',
                'email_btn': '📧 Email',
                'whatsapp_btn': '💬 WhatsApp',
                'sms_btn': '📱 SMS',
                'jw_library_btn': '📖 JW Library',
                'curso_btn': '🎓 Curso Gratis',
                'volver_btn': '🔙 Volver al Menú',
                'buscar_placeholder': 'Ingresa el nombre y busca sus temas...',
                'nombre_requerido': 'Nombre Requerido',
                'nombre_requerido_msg': 'Ingresa el nombre del interesado para buscar sus temas',
                'temas_encontrados': 'Temas Encontrados',
                'sin_temas': 'Sin Temas',
                'sin_temas_msg': 'No se encontraron temas previos para {nombre}.',
                'tema_requerido': 'Tema Requerido',
                'tema_requerido_msg': 'Ingresa el texto del tema a agregar',
                'tema_agregado': 'Tema Agregado',
                'email_requerido': 'Email Requerido',
                'email_requerido_msg': 'El email es necesario para enviar por correo',
                'telefono_requerido': 'Teléfono Requerido',
                'telefono_requerido_msg': 'El teléfono es necesario para enviar SMS',
                'mensaje_copiado': 'Mensaje Copiado',
                'mensaje_copiado_msg': 'El mensaje ha sido copiado al portapapeles',
                'seleccionar_todos': 'Seleccionar Todos',
                'deseleccionar_todos': 'Deseleccionar Todos'
            },
            'en': {
                'titulo': '📧 SEND RESUME BY INTERESTED PERSON',
                'nombre_label': '👤 Interested person name: *',
                'nombre_hint': 'E.g: Maria Gonzalez',
                'buscar_btn': '🔍 Search Topics for this Person',
                'email_label': '📧 Email:',
                'email_hint': 'maria.gonzalez@email.com',
                'telefono_label': '📱 Phone:',
                'telefono_hint': '+1 407-590-6349',
                'temas_titulo': '📚 TOPICS COVERED',
                'agregar_tema_label': '➕ Add topic manually:',
                'agregar_tema_hint': 'E.g: Kingdom of God - Matthew 6:9',
                'agregar_btn': '➕ Add',
                'vista_previa_label': '👁️ PREVIEW:',
                'editar_btn': '✏️ Edit Message',
                'copiar_btn': '📋 Copy All',
                'email_btn': '📧 Email',
                'whatsapp_btn': '💬 WhatsApp',
                'sms_btn': '📱 SMS',
                'jw_library_btn': '📖 JW Library',
                'curso_btn': '🎓 Free Course',
                'volver_btn': '🔙 Back to Menu',
                'buscar_placeholder': 'Enter the name and search for their topics...',
                'nombre_requerido': 'Name Required',
                'nombre_requerido_msg': 'Enter the name to search for their topics',
                'temas_encontrados': 'Topics Found',
                'sin_temas': 'No Topics',
                'sin_temas_msg': 'No previous topics found for {nombre}.',
                'tema_requerido': 'Topic Required',
                'tema_requerido_msg': 'Enter the topic text to add',
                'tema_agregado': 'Topic Added',
                'email_requerido': 'Email Required',
                'email_requerido_msg': 'Email is required to send by mail',
                'telefono_requerido': 'Phone Required',
                'telefono_requerido_msg': 'Phone is required to send SMS',
                'mensaje_copiado': 'Message Copied',
                'mensaje_copiado_msg': 'The message has been copied to clipboard',
                'seleccionar_todos': 'Select All',
                'deseleccionar_todos': 'Deselect All'
            }
        }
        
        self.construir_interfaz()
        self.cargar_datos_previos()
    
    def get_texto(self, clave, **kwargs):
        texto = self.textos.get(self.idioma, self.textos['es']).get(clave, clave)
        if kwargs:
            return texto.format(**kwargs)
        return texto
    
    def cambiar_idioma(self, nuevo_idioma):
        self.idioma = nuevo_idioma
        self.construir_interfaz()
        self.actualizar_vista_previa()
    
    def cargar_temas_por_interesado(self, nombre_interesado):
        if not nombre_interesado or len(nombre_interesado.strip()) < 2:
            return []
        
        establecer_interesado_para_captura(nombre_interesado)
        temas_guardados = gestor_temas.obtener_temas_por_interesado(nombre_interesado)
        
        print(f"🔍 Temas del gestor para {nombre_interesado}: {len(temas_guardados)}")
        
        temas_procesados = []
        
        for tema in temas_guardados:
            temas_procesados.append({
                'texto': f"{tema.get('titulo', 'Sin título')} - {tema.get('fecha', 'Sin fecha')}",
                'respuesta_completa': tema.get('respuesta', 'Sin respuesta'),
                'titulo_original': tema.get('titulo', 'Sin título'),
                'fecha': tema.get('fecha', ''),
                'origen': tema.get('origen', 'gestor'),
                'seleccionado': True
            })
        
        if len(temas_procesados) < 3:
            ejemplos_demo = [
                {
                    'titulo': f'Primera conversación con {nombre_interesado}',
                    'respuesta': f'Conocí a {nombre_interesado} en el servicio del campo. Mostramos interés en temas bíblicos.',
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y'),
                    'origen': 'demo'
                },
                {
                    'titulo': 'Reino de Dios - Mateo 6:9-10',
                    'respuesta': 'El Reino de Dios es un gobierno real establecido por Jehová en los cielos. Jesús enseñó a orar por este reino en el Padrenuestro.',
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y'),
                    'origen': 'demo'
                },
                {
                    'titulo': 'Esperanza de la resurrección - Juan 5:28-29',
                    'respuesta': 'La Biblia enseña que habrá una resurrección tanto de justos como de injustos. Esto da esperanza para el futuro.',
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y'),
                    'origen': 'demo'
                },
                {
                    'titulo': 'Vida eterna en la Tierra - Salmo 37:29',
                    'respuesta': 'Los justos heredarán la tierra y vivirán en ella para siempre. Esta es la esperanza bíblica original.',
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y'),
                    'origen': 'demo'
                },
                {
                    'titulo': 'Nombre de Dios - Éxodo 6:3',
                    'respuesta': 'El nombre personal de Dios es Jehová (YHWH en hebreo). Este nombre aparece cerca de 7,000 veces en la Biblia.',
                    'fecha': datetime.datetime.now().strftime('%d/%m/%Y'),
                    'origen': 'demo'
                }
            ]
            
            for ejemplo in ejemplos_demo:
                if len(temas_procesados) >= 5:
                    break
                    
                temas_procesados.append({
                    'texto': f"{ejemplo['titulo']} - {ejemplo['fecha']}",
                    'respuesta_completa': ejemplo['respuesta'],
                    'titulo_original': ejemplo['titulo'],
                    'fecha': ejemplo['fecha'],
                    'origen': ejemplo['origen'],
                    'seleccionado': True
                })
                
                gestor_temas.capturar_tema_seleccionado(
                    titulo_tema=ejemplo['titulo'],
                    respuesta_completa=ejemplo['respuesta'],
                    origen=ejemplo['origen'],
                    nombre_interesado=nombre_interesado
                )
        
        print(f"📋 Total temas procesados: {len(temas_procesados)}")
        return temas_procesados
    
    def guardar_tema_para_interesado(self, nombre_interesado, tema_texto):
        try:
            return gestor_temas.capturar_tema_seleccionado(
                titulo_tema=tema_texto,
                respuesta_completa=f"Tema agregado manualmente: {tema_texto}",
                origen="manual",
                nombre_interesado=nombre_interesado
            )
        except Exception as e:
            print(f"❌ Error guardando tema: {e}")
            return False
    
    def construir_interfaz(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', spacing=dp(8), padding=dp(12))
        
        titulo = Label(text=self.get_texto('titulo'), font_size=dp(16), bold=True, color=(0.2, 0.6, 0.9, 1), size_hint_y=None, height=dp(35), halign='center')
        main_layout.add_widget(titulo)
        
        nombre_label = Label(text=self.get_texto('nombre_label'), size_hint_y=None, height=dp(20), font_size=dp(12), halign='left', color=(1, 0.8, 0.8, 1))
        main_layout.add_widget(nombre_label)
        
        self.nombre_input = TextInput(hint_text=self.get_texto('nombre_hint'), size_hint_y=None, height=dp(35), font_size=dp(13), multiline=False, background_color=(0.95, 0.95, 0.95, 1))
        self.nombre_input.bind(text=self.on_nombre_change)
        main_layout.add_widget(self.nombre_input)
        
        btn_buscar = Button(text=self.get_texto('buscar_btn'), background_color=(0.3, 0.8, 0.3, 1), size_hint_y=None, height=dp(35), font_size=dp(11))
        btn_buscar.bind(on_press=self.buscar_temas_interesado)
        main_layout.add_widget(btn_buscar)
        
        email_label = Label(text=self.get_texto('email_label'), size_hint_y=None, height=dp(18), font_size=dp(11), halign='left', color=(0.9, 0.9, 0.9, 1))
        main_layout.add_widget(email_label)
        
        self.email_input = TextInput(hint_text=self.get_texto('email_hint'), size_hint_y=None, height=dp(30), font_size=dp(12), multiline=False, background_color=(0.95, 0.95, 0.95, 1))
        main_layout.add_widget(self.email_input)
        
        telefono_label = Label(text=self.get_texto('telefono_label'), size_hint_y=None, height=dp(18), font_size=dp(11), halign='left', color=(0.9, 0.9, 0.9, 1))
        main_layout.add_widget(telefono_label)
        
        self.telefono_input = TextInput(hint_text=self.get_texto('telefono_hint'), size_hint_y=None, height=dp(30), font_size=dp(12), multiline=False, background_color=(0.95, 0.95, 0.95, 1))
        main_layout.add_widget(self.telefono_input)
        
        self.temas_seccion = Label(text=f'{self.get_texto("temas_titulo")} (0):', font_size=dp(12), bold=True, color=(0.3, 0.8, 0.3, 1), size_hint_y=None, height=dp(25), halign='left')
        main_layout.add_widget(self.temas_seccion)
        
        seleccion_grid = GridLayout(cols=2, spacing=dp(4), size_hint_y=None, height=dp(30))
        
        btn_seleccionar_todos = Button(text=self.get_texto('seleccionar_todos'), background_color=(0.2, 0.7, 0.2, 1), size_hint_y=None, height=dp(30), font_size=dp(9))
        btn_seleccionar_todos.bind(on_press=self.seleccionar_todos_temas)
        seleccion_grid.add_widget(btn_seleccionar_todos)
        
        btn_deseleccionar_todos = Button(text=self.get_texto('deseleccionar_todos'), background_color=(0.7, 0.2, 0.2, 1), size_hint_y=None, height=dp(30), font_size=dp(9))
        btn_deseleccionar_todos.bind(on_press=self.deseleccionar_todos_temas)
        seleccion_grid.add_widget(btn_deseleccionar_todos)
        
        main_layout.add_widget(seleccion_grid)
        
        self.scroll_temas = ScrollView(size_hint_y=None, height=dp(120))
        self.temas_layout = BoxLayout(orientation='vertical', spacing=dp(2), size_hint_y=None)
        self.temas_layout.bind(minimum_height=self.temas_layout.setter('height'))
        
        self.scroll_temas.add_widget(self.temas_layout)
        main_layout.add_widget(self.scroll_temas)
        
        agregar_label = Label(text=self.get_texto('agregar_tema_label'), size_hint_y=None, height=dp(18), font_size=dp(10), halign='left', color=(0.8, 0.8, 0.9, 1))
        main_layout.add_widget(agregar_label)
        
        agregar_grid = GridLayout(cols=2, spacing=dp(4), size_hint_y=None, height=dp(30))
        
        self.nuevo_tema_input = TextInput(hint_text=self.get_texto('agregar_tema_hint'), size_hint_y=None, height=dp(30), font_size=dp(10), multiline=False, background_color=(0.9, 0.9, 1, 1))
        agregar_grid.add_widget(self.nuevo_tema_input)
        
        btn_agregar_tema = Button(text=self.get_texto('agregar_btn'), background_color=(0.6, 0.3, 0.8, 1), size_hint_y=None, height=dp(30), font_size=dp(9))
        btn_agregar_tema.bind(on_press=self.agregar_tema_manual)
        agregar_grid.add_widget(btn_agregar_tema)
        
        main_layout.add_widget(agregar_grid)
        
        vista_label = Label(text=self.get_texto('vista_previa_label'), font_size=dp(11), bold=True, color=(0.6, 0.3, 0.9, 1), size_hint_y=None, height=dp(20), halign='left')
        main_layout.add_widget(vista_label)
        
        self.vista_previa = Label(text=self.get_texto('buscar_placeholder'), size_hint_y=None, height=dp(40), font_size=dp(8), color=(0.8, 0.8, 0.8, 1), text_size=(dp(300), None), halign='left', valign='top')
        main_layout.add_widget(self.vista_previa)
        
        edicion_grid = GridLayout(cols=2, spacing=dp(4), size_hint_y=None, height=dp(35))
        
        btn_editar = Button(text=self.get_texto('editar_btn'), background_color=(0.8, 0.6, 0.2, 1), font_size=dp(9))
        btn_editar.bind(on_press=self.abrir_editor_mensaje)
        edicion_grid.add_widget(btn_editar)
        
        # CONTINUACIÓN DESDE LÍNEA 292 - datos_interesado.py

        btn_copiar = Button(text=self.get_texto('copiar_btn'), background_color=(0.2, 0.8, 0.6, 1), font_size=dp(9))
        btn_copiar.bind(on_press=self.copiar_mensaje)
        edicion_grid.add_widget(btn_copiar)
        
        main_layout.add_widget(edicion_grid)
        
        botones_grid = GridLayout(cols=3, spacing=dp(4), size_hint_y=None, height=dp(45))
        
        btn_email = Button(text=self.get_texto('email_btn'), background_color=(0.2, 0.5, 0.8, 1), font_size=dp(9))
        btn_email.bind(on_press=self.enviar_por_email)
        botones_grid.add_widget(btn_email)
        
        btn_whatsapp = Button(text=self.get_texto('whatsapp_btn'), background_color=(0.3, 0.7, 0.3, 1), font_size=dp(9))
        btn_whatsapp.bind(on_press=self.enviar_por_whatsapp)
        botones_grid.add_widget(btn_whatsapp)
        
        btn_sms = Button(text=self.get_texto('sms_btn'), background_color=(0.8, 0.5, 0.2, 1), font_size=dp(9))
        btn_sms.bind(on_press=self.enviar_por_sms)
        botones_grid.add_widget(btn_sms)
        
        main_layout.add_widget(botones_grid)
        
        links_grid = GridLayout(cols=2, spacing=dp(4), size_hint_y=None, height=dp(35))
        
        btn_jw_library = Button(text=self.get_texto('jw_library_btn'), background_color=(0.5, 0.3, 0.7, 1), font_size=dp(9))
        btn_jw_library.bind(on_press=self.abrir_jw_library)
        links_grid.add_widget(btn_jw_library)
        
        btn_curso = Button(text=self.get_texto('curso_btn'), background_color=(0.7, 0.5, 0.3, 1), font_size=dp(9))
        btn_curso.bind(on_press=self.solicitar_curso_biblico)
        links_grid.add_widget(btn_curso)
        
        main_layout.add_widget(links_grid)
        
        btn_volver = Button(text=self.get_texto('volver_btn'), background_color=(0.7, 0.3, 0.3, 1), size_hint_y=None, height=dp(30), font_size=dp(10))
        btn_volver.bind(on_press=self.volver)
        main_layout.add_widget(btn_volver)
        
        self.add_widget(main_layout)
        self.actualizar_vista_previa()
    
    def seleccionar_todos_temas(self, instance):
        for tema in self.temas_automaticos:
            tema['seleccionado'] = True
        self.actualizar_lista_temas()
        self.actualizar_vista_previa()
    
    def deseleccionar_todos_temas(self, instance):
        for tema in self.temas_automaticos:
            tema['seleccionado'] = False
        self.actualizar_lista_temas()
        self.actualizar_vista_previa()
    
    def on_checkbox_active(self, checkbox, value, tema_index):
        if 0 <= tema_index < len(self.temas_automaticos):
            self.temas_automaticos[tema_index]['seleccionado'] = value
            temas_seleccionados = sum(1 for tema in self.temas_automaticos if tema.get('seleccionado', False))
            if hasattr(self, 'temas_seccion') and self.temas_seccion:
                self.temas_seccion.text = f'{self.get_texto("temas_titulo")} ({temas_seleccionados}/{len(self.temas_automaticos)}):'
            self.actualizar_vista_previa()
    
    def buscar_temas_interesado(self, instance):
        nombre = self.nombre_input.text.strip()
        if not nombre:
            self.mostrar_popup(self.get_texto('nombre_requerido'), self.get_texto('nombre_requerido_msg'))
            return
        
        self.temas_automaticos = self.cargar_temas_por_interesado(nombre)
        self.actualizar_lista_temas()
        self.actualizar_vista_previa()
        
        if self.temas_automaticos:
            mensaje = f"Se encontraron {len(self.temas_automaticos)} temas para {nombre}"
            self.mostrar_popup(self.get_texto('temas_encontrados'), mensaje)
        else:
            self.mostrar_popup(self.get_texto('sin_temas'), self.get_texto('sin_temas_msg', nombre=nombre))
    
    def actualizar_lista_temas(self):
        self.temas_layout.clear_widgets()
        
        temas_seleccionados = sum(1 for tema in self.temas_automaticos if tema.get('seleccionado', False))
        
        if hasattr(self, 'temas_seccion') and self.temas_seccion:
            self.temas_seccion.text = f'{self.get_texto("temas_titulo")} ({temas_seleccionados}/{len(self.temas_automaticos)}):'
        
        def crear_callback_checkbox(indice):
            return lambda checkbox, value: self.on_checkbox_active(checkbox, value, indice)
        
        for i, tema_info in enumerate(self.temas_automaticos):
            tema_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(25))
            
            checkbox = CheckBox(active=tema_info.get('seleccionado', True), size_hint_x=None, width=dp(30))
            checkbox.bind(active=crear_callback_checkbox(i))
            tema_layout.add_widget(checkbox)
            
            tema_texto = tema_info.get('texto', 'Tema sin texto')
            tema_label = Label(text=f"• {tema_texto[:80]}{'...' if len(tema_texto) > 80 else ''}", font_size=dp(8), color=(0.9, 0.9, 0.9, 1), text_size=(dp(250), None), halign='left', valign='middle')
            tema_layout.add_widget(tema_label)
            
            self.temas_layout.add_widget(tema_layout)
    
    def on_nombre_change(self, instance, value):
        self.actualizar_vista_previa()
    
    def agregar_tema_manual(self, instance):
        tema_texto = self.nuevo_tema_input.text.strip()
        if not tema_texto:
            self.mostrar_popup(self.get_texto('tema_requerido'), self.get_texto('tema_requerido_msg'))
            return
        
        nuevo_tema = {
            'texto': tema_texto,
            'respuesta_completa': f"Tema agregado manualmente: {tema_texto}",
            'titulo_original': tema_texto,
            'fecha': datetime.datetime.now().strftime('%d/%m/%Y'),
            'origen': 'manual',
            'seleccionado': True
        }
        self.temas_automaticos.append(nuevo_tema)
        
        nombre = self.nombre_input.text.strip()
        if nombre:
            self.guardar_tema_para_interesado(nombre, tema_texto)
        
        self.nuevo_tema_input.text = ''
        self.actualizar_lista_temas()
        self.actualizar_vista_previa()
        
        self.mostrar_popup(self.get_texto('tema_agregado'), f"✅ {tema_texto}")
    
    def actualizar_vista_previa(self):
        if self.mensaje_personalizado:
            texto = self.mensaje_personalizado[:200] + "..." if len(self.mensaje_personalizado) > 200 else self.mensaje_personalizado
            self.vista_previa.text = texto
        else:
            mensaje = self.generar_mensaje_completo()
            self.vista_previa.text = mensaje[:200] + "..." if len(mensaje) > 200 else mensaje
    
    def generar_mensaje_completo(self):
        nombre = self.nombre_input.text.strip()
        
        if not nombre:
            return "Ingresa el nombre del interesado para generar el mensaje"
        
        if self.mensaje_personalizado:
            return self.mensaje_personalizado
        
        return obtener_mensaje_completo_para_envio(nombre, self.idioma)
    
    def abrir_editor_mensaje(self, instance):
        mensaje_actual = self.generar_mensaje_completo()
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        editor = TextInput(text=mensaje_actual, multiline=True, font_size=dp(11), background_color=(0.95, 0.95, 0.95, 1))
        content.add_widget(editor)
        
        botones = GridLayout(cols=2, spacing=dp(5), size_hint_y=None, height=dp(40))
        
        btn_guardar = Button(text="💾 Guardar", background_color=(0.3, 0.7, 0.3, 1))
        btn_cancelar = Button(text="❌ Cancelar", background_color=(0.7, 0.3, 0.3, 1))
        
        botones.add_widget(btn_guardar)
        botones.add_widget(btn_cancelar)
        
        content.add_widget(botones)
        
        popup = Popup(title="✏️ Editar Mensaje", content=content, size_hint=(0.9, 0.8))
        
        def guardar_mensaje(btn_instance):
            self.mensaje_personalizado = editor.text
            self.actualizar_vista_previa()
            popup.dismiss()
        
        def cancelar_edicion(btn_instance):
            popup.dismiss()
        
        btn_guardar.bind(on_press=guardar_mensaje)
        btn_cancelar.bind(on_press=cancelar_edicion)
        
        popup.open()
    
    def copiar_mensaje(self, instance):
        mensaje = self.generar_mensaje_completo()
        print(f"📋 MENSAJE COPIADO:\n{mensaje}")
        self.mostrar_popup(self.get_texto('mensaje_copiado'), self.get_texto('mensaje_copiado_msg'))
    
    def enviar_por_email(self, instance):
        email = self.email_input.text.strip()
        if not email:
            self.mostrar_popup(self.get_texto('email_requerido'), self.get_texto('email_requerido_msg'))
            return
        
        nombre = self.nombre_input.text.strip()
        asunto = f"Resumen de temas bíblicos - {nombre}" if self.idioma == 'es' else f"Biblical topics summary - {nombre}"
        mensaje = self.generar_mensaje_completo()
        
        try:
            mensaje_encoded = urllib.parse.quote(mensaje)
            asunto_encoded = urllib.parse.quote(asunto)
            email_url = f"mailto:{email}?subject={asunto_encoded}&body={mensaje_encoded}"
            webbrowser.open(email_url)
        except Exception as e:
            print(f"❌ Error abriendo email: {e}")
    
    def enviar_por_whatsapp(self, instance):
        telefono = self.telefono_input.text.strip()
        mensaje = self.generar_mensaje_completo()
        
        try:
            mensaje_encoded = urllib.parse.quote(mensaje)
            if telefono:
                telefono_limpio = ''.join(filter(str.isdigit, telefono))
                whatsapp_url = f"https://wa.me/{telefono_limpio}?text={mensaje_encoded}"
            else:
                whatsapp_url = f"https://wa.me/?text={mensaje_encoded}"
            webbrowser.open(whatsapp_url)
        except Exception as e:
            print(f"❌ Error abriendo WhatsApp: {e}")
    
    def enviar_por_sms(self, instance):
        telefono = self.telefono_input.text.strip()
        if not telefono:
            self.mostrar_popup(self.get_texto('telefono_requerido'), self.get_texto('telefono_requerido_msg'))
            return
        
        mensaje = self.generar_mensaje_completo()
        
        try:
            telefono_limpio = ''.join(filter(str.isdigit, telefono))
            mensaje_encoded = urllib.parse.quote(mensaje)
            sms_url = f"sms:{telefono_limpio}?body={mensaje_encoded}"
            webbrowser.open(sms_url)
        except Exception as e:
            print(f"❌ Error abriendo SMS: {e}")
    
    def abrir_jw_library(self, instance):
        url = "https://www.jw.org/es/biblioteca-en-linea/" if self.idioma == 'es' else "https://www.jw.org/en/online-library/"
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"❌ Error abriendo JW Library: {e}")
    
    def solicitar_curso_biblico(self, instance):
        url = "https://www.jw.org/es/estudio-biblico/" if self.idioma == 'es' else "https://www.jw.org/en/bible-study/"
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"❌ Error abriendo curso bíblico: {e}")
    
    def cargar_datos_previos(self):
        try:
            if os.path.exists("datos_interesado_temp.json"):
                with open("datos_interesado_temp.json", 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                self.nombre_input.text = datos.get('nombre', '')
                self.email_input.text = datos.get('email', '')
                self.telefono_input.text = datos.get('telefono', '')
                self.mensaje_personalizado = datos.get('mensaje_personalizado', '')
                print("✅ Datos previos cargados")
        except Exception as e:
            print(f"⚠️ No se pudieron cargar datos previos: {e}")
    
    def guardar_datos_temporales(self):
        try:
            datos = {
                'nombre': self.nombre_input.text.strip(),
                'email': self.email_input.text.strip(),
                'telefono': self.telefono_input.text.strip(),
                'mensaje_personalizado': self.mensaje_personalizado,
                'fecha': datetime.datetime.now().isoformat()
            }
            with open("datos_interesado_temp.json", 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            print("✅ Datos temporales guardados")
        except Exception as e:
            print(f"❌ Error guardando datos temporales: {e}")
    
    def mostrar_popup(self, titulo, mensaje):
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        label = Label(text=mensaje, font_size=dp(12), text_size=(dp(280), None), halign='center')
        content.add_widget(label)
        btn_ok = Button(text="OK", size_hint_y=None, height=dp(40), background_color=(0.3, 0.7, 0.3, 1))
        content.add_widget(btn_ok)
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.4))
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()
    
    def volver(self, instance):
        self.guardar_datos_temporales()
        if self.volver_callback:
            self.volver_callback()