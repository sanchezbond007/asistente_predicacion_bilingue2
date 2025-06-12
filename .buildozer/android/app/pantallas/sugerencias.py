# pantallas/sugerencias.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.metrics import dp
import json
import os
import random

class PantallaSugerencias(Screen):
    def __init__(self, **kwargs):
        # Extraer parámetros personalizados antes de llamar al super()
        self.volver_callback = kwargs.pop('volver_callback', None)
        self.idioma_inicial = kwargs.pop('idioma', 'es')
        
        print(f"🏁 CONSTRUCTOR PantallaSugerencias:")
        print(f"   - idioma_inicial recibido: {repr(self.idioma_inicial)}")
        print(f"   - Tipo: {type(self.idioma_inicial)}")
        
        super(PantallaSugerencias, self).__init__(**kwargs)
        self.usuario_actual = None
        self.idioma_usuario = self.idioma_inicial
        self.todos_los_temas = []  # Cache de todos los temas
        self.temas_mostrados = []  # Temas ya mostrados
        self.temas_por_pagina = 10  # Cantidad de temas por página
        
        print(f"   - idioma_usuario asignado: {repr(self.idioma_usuario)}")
        
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        # Botón para generar nuevas sugerencias
        self.btn_nuevas_sugerencias = Button(
            text='Nuevas Sugerencias',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.3, 0.6, 0.3, 1)
        )
        self.btn_nuevas_sugerencias.bind(on_press=self.generar_nuevas_sugerencias)
        main_layout.add_widget(self.btn_nuevas_sugerencias)
        
        # Botón para buscar temas
        self.btn_buscar = Button(
            text='Buscar',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.6, 0.3, 0.6, 1)
        )
        self.btn_buscar.bind(on_press=self.mostrar_busqueda)
        main_layout.add_widget(self.btn_buscar)
        
        scroll = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', spacing=dp(5), size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        scroll.add_widget(self.content_layout)
        main_layout.add_widget(scroll)
        
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
        print(f"🎬 ON_ENTER PantallaSugerencias:")
        print(f"   - idioma_inicial: {repr(self.idioma_inicial)}")
        print(f"   - idioma_usuario antes: {repr(self.idioma_usuario)}")
        
        # FORZAR el uso del idioma inicial siempre
        self.idioma_usuario = self.idioma_inicial
        
        # Actualizar archivo para persistir el idioma correcto
        self.actualizar_archivo_idioma()
        
        print(f"   - idioma_usuario FINAL: {repr(self.idioma_usuario)}")
        
        self.actualizar_idioma()
        self.cargar_todos_los_temas()
        self.cargar_sugerencias_iniciales()
        print(f"🌐 PANTALLA SUGERENCIAS - Idioma detectado: '{self.idioma_usuario}'")

    def actualizar_archivo_idioma(self):
        """Actualiza el archivo usuario_actual.json con el idioma correcto"""
        try:
            datos_usuario = {
                "usuario": self.usuario_actual or "usuario_auto",
                "idioma": self.idioma_inicial  # Usar idioma inicial
            }
            
            with open('usuario_actual.json', 'w', encoding='utf-8') as file:
                json.dump(datos_usuario, file, ensure_ascii=False, indent=2)
            
            print(f"✅ Archivo actualizado con idioma: {self.idioma_inicial}")
            
        except Exception as e:
            print(f"❌ Error actualizando archivo: {e}")

    def debug_a_archivo(self, mensaje):
        """Guarda mensajes de debug en un archivo para Android"""
        try:
            with open('debug_sugerencias.txt', 'a', encoding='utf-8') as f:
                f.write(f"{mensaje}\n")
        except:
            pass

    def cargar_usuario_actual(self):
        try:
            self.debug_a_archivo("=== INICIANDO CARGA DE USUARIO ===")
            
            if os.path.exists('usuario_actual.json'):
                with open('usuario_actual.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.usuario_actual = data.get('usuario')
                    idioma_cargado = data.get('idioma', 'es')
                    
                    debug_info = f"""
📁 ARCHIVO USUARIO_ACTUAL.JSON:
   - Contenido completo: {data}
   - Usuario: {self.usuario_actual}
   - Idioma raw: {repr(idioma_cargado)}
   - Tipo idioma: {type(idioma_cargado)}
"""
                    print(debug_info)
                    self.debug_a_archivo(debug_info)
                    
                    # Asegurar que el idioma sea una cadena válida
                    if isinstance(idioma_cargado, str) and idioma_cargado.strip():
                        self.idioma_usuario = idioma_cargado.strip().lower()
                    else:
                        self.idioma_usuario = 'es'
                    
                    resultado = f"""
🎯 RESULTADO FINAL:
   - Usuario: {self.usuario_actual}
   - Idioma procesado: '{self.idioma_usuario}'
"""
                    print(resultado)
                    self.debug_a_archivo(resultado)
                    
            else:
                # CREAR ARCHIVO AUTOMÁTICAMENTE
                error_msg = "❌ Archivo usuario_actual.json NO EXISTE - CREANDO AUTOMÁTICAMENTE"
                print(error_msg)
                self.debug_a_archivo(error_msg)
                
                # Crear archivo con idioma por defecto
                self.crear_archivo_usuario_automatico()
                
        except Exception as e:
            error_completo = f"❌ ERROR CARGANDO USUARIO: {e}"
            print(error_completo)
            self.debug_a_archivo(error_completo)
            import traceback
            traceback.print_exc()
            self.idioma_usuario = 'es'

    def crear_archivo_usuario_automatico(self):
        """Crea automáticamente el archivo usuario_actual.json"""
        try:
            # USAR EL IDIOMA INICIAL PASADO DESDE EL MENÚ
            idioma_a_usar = self.idioma_inicial if hasattr(self, 'idioma_inicial') else 'es'
            
            print(f"🔧 CREANDO ARCHIVO AUTOMÁTICO:")
            print(f"   - idioma_inicial disponible: {self.idioma_inicial}")
            print(f"   - idioma_a_usar: {idioma_a_usar}")
            
            datos_usuario = {
                "usuario": "usuario_auto",
                "idioma": idioma_a_usar  # USAR EL IDIOMA PASADO, NO 'es'
            }
            
            with open('usuario_actual.json', 'w', encoding='utf-8') as file:
                json.dump(datos_usuario, file, ensure_ascii=False, indent=2)
            
            self.usuario_actual = "usuario_auto"
            self.idioma_usuario = idioma_a_usar.lower().strip()
            
            mensaje = f"""
✅ ARCHIVO CREADO AUTOMÁTICAMENTE:
   - Usuario: {self.usuario_actual}
   - Idioma: {self.idioma_usuario}
   - Archivo: usuario_actual.json
   - Idioma original: {self.idioma_inicial}
"""
            print(mensaje)
            self.debug_a_archivo(mensaje)
            
        except Exception as e:
            error_msg = f"❌ Error creando archivo automático: {e}"
            print(error_msg)
            self.debug_a_archivo(error_msg)
            self.idioma_usuario = self.idioma_inicial if hasattr(self, 'idioma_inicial') else 'es'

    def actualizar_idioma(self):
        print(f"🔄 === ACTUALIZANDO IDIOMA ===")
        print(f"   - self.idioma_usuario: {repr(self.idioma_usuario)}")
        print(f"   - self.idioma_inicial: {repr(self.idioma_inicial)}")
        
        traducciones = {
            'volver': {'es': 'Volver', 'en': 'Back'},
            'nuevas_sugerencias': {'es': 'Nuevas Sugerencias', 'en': 'New Suggestions'},
            'buscar': {'es': 'Buscar', 'en': 'Search'}
        }
        
        # FORZAR idioma a inglés para testing
        idioma_para_usar = self.idioma_usuario.lower().strip()
        print(f"   - idioma_para_usar: {repr(idioma_para_usar)}")
        
        # Obtener textos
        texto_volver = traducciones['volver'].get(idioma_para_usar, 'Volver')
        texto_nuevas = traducciones['nuevas_sugerencias'].get(idioma_para_usar, 'Nuevas Sugerencias')
        texto_buscar = traducciones['buscar'].get(idioma_para_usar, 'Buscar')
        
        print(f"   - Textos obtenidos:")
        print(f"     * Volver: {repr(texto_volver)}")
        print(f"     * Nuevas: {repr(texto_nuevas)}")
        print(f"     * Buscar: {repr(texto_buscar)}")
        
        # Aplicar textos
        self.btn_volver.text = texto_volver
        self.btn_nuevas_sugerencias.text = texto_nuevas
        self.btn_buscar.text = texto_buscar
        
        print(f"📝 Textos aplicados a botones:")
        print(f"   - btn_volver.text: {repr(self.btn_volver.text)}")
        print(f"   - btn_nuevas_sugerencias.text: {repr(self.btn_nuevas_sugerencias.text)}")
        print(f"   - btn_buscar.text: {repr(self.btn_buscar.text)}")
        print(f"=== FIN ACTUALIZAR IDIOMA ===\n")

    def cargar_temas_desde_json(self):
        """Carga todos los temas desde múltiples archivos bloque_X.json"""
        try:
            directorio_temas = os.path.join('datos', 'temas')
            print(f"🔍 Buscando archivos JSON en: {directorio_temas}")
            
            if not os.path.exists(directorio_temas):
                print(f"❌ No se encontró el directorio: {directorio_temas}")
                return []
            
            # Buscar todos los archivos bloque_X.json
            archivos_bloque = []
            try:
                archivos_en_directorio = os.listdir(directorio_temas)
                print(f"📁 Archivos encontrados: {archivos_en_directorio}")
                
                for archivo in archivos_en_directorio:
                    if archivo.startswith('bloque_') and archivo.endswith('.json'):
                        archivos_bloque.append(archivo)
                
                archivos_bloque.sort()  # Ordenar para procesar en orden
                print(f"📋 Archivos de bloques encontrados: {archivos_bloque}")
                
            except Exception as e:
                print(f"❌ Error listando directorio: {e}")
                return []
            
            if not archivos_bloque:
                print(f"❌ No se encontraron archivos bloque_*.json en {directorio_temas}")
                return []
            
            todos_los_temas = []
            
            # Cargar cada archivo de bloque
            for archivo_bloque in archivos_bloque:
                try:
                    ruta_archivo = os.path.join(directorio_temas, archivo_bloque)
                    print(f"📖 Cargando archivo: {archivo_bloque}")
                    
                    with open(ruta_archivo, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    
                    # Procesar los temas del bloque
                    if isinstance(data, dict) and 'temas' in data:
                        temas_en_bloque = len(data['temas'])
                        print(f"   ✅ {archivo_bloque}: {temas_en_bloque} temas")
                        for tema in data['temas']:
                            todos_los_temas.append(tema)
                    elif isinstance(data, list):
                        # Si el archivo contiene una lista de temas directamente
                        temas_en_bloque = len(data)
                        print(f"   ✅ {archivo_bloque}: {temas_en_bloque} temas (lista directa)")
                        for tema in data:
                            todos_los_temas.append(tema)
                    else:
                        print(f"   ⚠️ {archivo_bloque}: Estructura no reconocida")
                        
                except Exception as e:
                    print(f"   ❌ Error cargando {archivo_bloque}: {e}")
                    continue
            
            print(f"🎯 Total de temas cargados desde archivos JSON: {len(todos_los_temas)}")
            
            # Mostrar una muestra de los primeros temas para verificar estructura
            if todos_los_temas:
                print(f"📋 Muestra del primer tema:")
                primer_tema = todos_los_temas[0]
                print(f"   Estructura: {list(primer_tema.keys()) if isinstance(primer_tema, dict) else type(primer_tema)}")
                if isinstance(primer_tema, dict) and 'titulo' in primer_tema:
                    titulo = primer_tema['titulo']
                    if isinstance(titulo, dict):
                        print(f"   Idiomas disponibles en título: {list(titulo.keys())}")
                        print(f"   Ejemplo ES: {titulo.get('es', 'N/A')}")
                        print(f"   Ejemplo EN: {titulo.get('en', 'N/A')}")
            
            return todos_los_temas
            
        except Exception as e:
            print(f"❌ Error general cargando temas desde JSON: {e}")
            import traceback
            traceback.print_exc()
            return []

    def cargar_todos_los_temas(self):
        """Carga todos los temas disponibles una sola vez"""
        self.todos_los_temas = self.cargar_temas_desde_json()
        print(f"🎯 Total de temas disponibles: {len(self.todos_los_temas)}")
        
        # Actualizar estado del botón mostrar más
        self.actualizar_boton_mostrar_mas()

    def obtener_temas_no_mostrados(self, cantidad):
        """Obtiene temas que no han sido mostrados aún"""
        if not self.todos_los_temas:
            return []
        
        # Filtrar temas que no han sido mostrados
        temas_disponibles = [tema for tema in self.todos_los_temas if tema not in self.temas_mostrados]
        
        # Si no hay suficientes temas nuevos, mezclar todos y reiniciar
        if len(temas_disponibles) < cantidad:
            print(f"📋 Pocos temas nuevos disponibles ({len(temas_disponibles)}), mezclando todos...")
            random.shuffle(self.todos_los_temas)
            self.temas_mostrados = []
            temas_disponibles = self.todos_los_temas
        
        # Seleccionar la cantidad solicitada
        temas_seleccionados = temas_disponibles[:cantidad]
        
        # Agregar a la lista de mostrados
        self.temas_mostrados.extend(temas_seleccionados)
        
        return temas_seleccionados

    def actualizar_boton_mostrar_mas(self):
        """Esta función ya no se usa pero se mantiene para compatibilidad"""
        pass

    def cargar_sugerencias_iniciales(self):
        """Carga las primeras sugerencias (reinicia la paginación)"""
        self.content_layout.clear_widgets()
        self.temas_mostrados = []  # Reiniciar temas mostrados
        
        print(f"🌐 Idioma actual del usuario: {self.idioma_usuario}")
        
        # Obtener primeros temas
        if not self.todos_los_temas:
            # Usar temas predeterminados si no hay archivo JSON
            temas_a_mostrar = self.obtener_preguntas_predeterminadas()[:self.temas_por_pagina]
        else:
            temas_a_mostrar = self.obtener_temas_no_mostrados(self.temas_por_pagina)
        
        self.agregar_temas_a_layout(temas_a_mostrar)
        
        # Actualizar estado del botón "Nuevas Sugerencias" para mostrar cuántos temas quedan
        temas_restantes = len(self.todos_los_temas) - len(self.temas_mostrados)
        if temas_restantes > 0:
            if self.idioma_usuario == 'en':
                texto_boton = f"New Suggestions ({temas_restantes} more available)"
            else:
                texto_boton = f"Nuevas Sugerencias ({temas_restantes} más disponibles)"
        else:
            if self.idioma_usuario == 'en':
                texto_boton = "New Suggestions"
            else:
                texto_boton = "Nuevas Sugerencias"
        
        # Actualizar texto del botón (esto es opcional, para mostrar cuántos temas quedan)
        # self.btn_nuevas_sugerencias.text = texto_boton

    def mostrar_busqueda(self, instance):
        """Muestra un popup para buscar temas por palabra clave"""
        print(f"🔍 ¡BOTÓN 'BUSCAR' PRESIONADO!")
        
        # Crear el contenido del popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Texto de instrucciones
        instrucciones = {
            'es': 'Escriba una palabra clave para buscar temas:',
            'en': 'Enter a keyword to search topics:'
        }
        idioma_normalizado = self.idioma_usuario.lower().strip()
        texto_instrucciones = instrucciones.get(idioma_normalizado, instrucciones['es'])
        
        label_instrucciones = Label(
            text=texto_instrucciones,
            size_hint_y=None,
            height=dp(40),
            text_size=(dp(300), None),
            halign='center'
        )
        content.add_widget(label_instrucciones)
        
        # Campo de texto para la búsqueda
        self.input_busqueda = TextInput(
            hint_text='Palabra clave...' if idioma_normalizado == 'es' else 'Keyword...',
            size_hint_y=None,
            height=dp(40),
            multiline=False
        )
        content.add_widget(self.input_busqueda)
        
        # Botones del popup
        botones_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        # Botón buscar
        btn_buscar_popup = Button(
            text='Buscar' if idioma_normalizado == 'es' else 'Search',
            background_color=(0.3, 0.6, 0.3, 1)
        )
        btn_buscar_popup.bind(on_press=self.ejecutar_busqueda)
        botones_layout.add_widget(btn_buscar_popup)
        
        # Botón cancelar
        btn_cancelar = Button(
            text='Cancelar' if idioma_normalizado == 'es' else 'Cancel',
            background_color=(0.6, 0.3, 0.3, 1)
        )
        btn_cancelar.bind(on_press=self.cerrar_popup_busqueda)
        botones_layout.add_widget(btn_cancelar)
        
        content.add_widget(botones_layout)
        
        # Crear y mostrar el popup
        titulo_popup = 'Buscar Temas' if idioma_normalizado == 'es' else 'Search Topics'
        self.popup_busqueda = Popup(
            title=titulo_popup,
            content=content,
            size_hint=(0.9, 0.4),
            auto_dismiss=False
        )
        self.popup_busqueda.open()

    def ejecutar_busqueda(self, instance):
        """Ejecuta la búsqueda de temas"""
        palabra_clave = self.input_busqueda.text.strip().lower()
        print(f"🔍 Buscando temas con palabra clave: '{palabra_clave}'")
        
        if not palabra_clave:
            print("❌ No se ingresó palabra clave")
            return
        
        # Cerrar el popup
        self.popup_busqueda.dismiss()
        
        # Buscar temas que contengan la palabra clave
        temas_encontrados = self.buscar_temas_por_palabra_clave(palabra_clave)
        
        # Mostrar resultados
        self.mostrar_resultados_busqueda(temas_encontrados, palabra_clave)

    def buscar_temas_por_palabra_clave(self, palabra_clave):
        """Busca temas que contengan la palabra clave en título o respuesta"""
        temas_encontrados = []
        idioma_normalizado = self.idioma_usuario.lower().strip()
        
        print(f"🔍 Buscando en {len(self.todos_los_temas)} temas...")
        
        for tema in self.todos_los_temas:
            try:
                encontrado = False
                
                # Buscar en el título
                titulo = tema.get('titulo', {})
                if isinstance(titulo, dict):
                    texto_titulo = titulo.get(idioma_normalizado, titulo.get('es', ''))
                else:
                    texto_titulo = str(titulo)
                
                if palabra_clave in texto_titulo.lower():
                    encontrado = True
                    print(f"   ✅ Encontrado en título: '{texto_titulo}'")
                
                # Buscar en la respuesta
                if not encontrado:
                    respuesta = tema.get('respuesta', {})
                    if isinstance(respuesta, dict):
                        texto_respuesta = respuesta.get(idioma_normalizado, respuesta.get('es', ''))
                    else:
                        texto_respuesta = str(respuesta)
                    
                    if palabra_clave in texto_respuesta.lower():
                        encontrado = True
                        print(f"   ✅ Encontrado en respuesta: '{texto_titulo}'")
                
                # Buscar en la cita bíblica
                if not encontrado:
                    cita = tema.get('cita', '')
                    if palabra_clave in cita.lower():
                        encontrado = True
                        print(f"   ✅ Encontrado en cita: '{texto_titulo}'")
                
                if encontrado:
                    temas_encontrados.append(tema)
                    
            except Exception as e:
                print(f"❌ Error procesando tema en búsqueda: {e}")
                continue
        
        print(f"🎯 Búsqueda completada: {len(temas_encontrados)} temas encontrados")
        return temas_encontrados

    def mostrar_resultados_busqueda(self, temas_encontrados, palabra_clave):
        """Muestra los resultados de la búsqueda"""
        self.content_layout.clear_widgets()
        
        idioma_normalizado = self.idioma_usuario.lower().strip()
        
        # Agregar título de resultados
        if temas_encontrados:
            texto_resultados = f"Resultados para '{palabra_clave}': {len(temas_encontrados)} temas" if idioma_normalizado == 'es' else f"Results for '{palabra_clave}': {len(temas_encontrados)} topics"
        else:
            texto_resultados = f"No se encontraron temas para '{palabra_clave}'" if idioma_normalizado == 'es' else f"No topics found for '{palabra_clave}'"
        
        label_resultados = Label(
            text=texto_resultados,
            size_hint_y=None,
            height=dp(50),
            text_size=(dp(300), None),
            halign='center',
            color=(1, 1, 0, 1)  # Amarillo para destacar
        )
        self.content_layout.add_widget(label_resultados)
        
        # Mostrar los temas encontrados
        if temas_encontrados:
            self.agregar_temas_a_layout(temas_encontrados)
        
        print(f"📱 Resultados mostrados en pantalla")

    def cerrar_popup_busqueda(self, instance):
        """Cierra el popup de búsqueda"""
        self.popup_busqueda.dismiss()

    def agregar_temas_a_layout(self, temas):
        """Agrega una lista de temas al layout"""
        if not temas:
            if len(self.content_layout.children) == 0:
                # Solo mostrar mensaje de error si no hay ningún tema
                mensaje_error = {
                    'es': "No se pudieron cargar los temas. Verifique el archivo de datos.",
                    'en': "Could not load themes. Please check the data file."
                }
                idioma_normalizado = self.idioma_usuario.lower().strip()
                texto_error = mensaje_error.get(idioma_normalizado, mensaje_error['es'])
                
                label_error = Label(
                    text=texto_error,
                    size_hint_y=None,
                    height=dp(50),
                    text_size=(dp(300), None),
                    halign='center'
                )
                self.content_layout.add_widget(label_error)
            return
        
        for i, tema in enumerate(temas):
            try:
                posicion_actual = len(self.content_layout.children) + 1
                print(f"\n🔍 ========== PROCESANDO TEMA #{posicion_actual} ==========")
                print(f"📋 Estructura completa del tema: {tema}")
                
                # Obtener el título en el idioma apropiado
                titulo = tema.get('titulo', {})
                idioma_normalizado = self.idioma_usuario.lower().strip()
                
                print(f"🌐 Idioma solicitado (normalizado): '{idioma_normalizado}'")
                print(f"📝 Estructura del título: {titulo}")
                print(f"📝 Tipo del título: {type(titulo)}")
                
                if isinstance(titulo, dict):
                    print(f"📚 Idiomas disponibles en título: {list(titulo.keys())}")
                    
                    # Intentar múltiples variaciones del idioma
                    texto_boton = None
                    
                    # Primero intentar el idioma exacto
                    if idioma_normalizado in titulo:
                        texto_boton = titulo[idioma_normalizado]
                        print(f"✅ Encontrado idioma exacto '{idioma_normalizado}': {texto_boton}")
                    
                    # Si no, buscar variaciones comunes
                    elif idioma_normalizado == 'en':
                        for variacion in ['en', 'english', 'eng', 'EN', 'English']:
                            if variacion in titulo:
                                texto_boton = titulo[variacion]
                                print(f"✅ Encontrado variación inglés '{variacion}': {texto_boton}")
                                break
                    
                    elif idioma_normalizado == 'es':
                        for variacion in ['es', 'español', 'spanish', 'esp', 'ES', 'Español']:
                            if variacion in titulo:
                                texto_boton = titulo[variacion]
                                print(f"✅ Encontrado variación español '{variacion}': {texto_boton}")
                                break
                    
                    # Si aún no encuentra nada, usar español como fallback
                    if not texto_boton:
                        # Intentar cualquier clave que contenga 'es' o sea el primer valor
                        for key, value in titulo.items():
                            if 'es' in key.lower() or 'esp' in key.lower():
                                texto_boton = value
                                print(f"✅ Fallback español encontrado '{key}': {texto_boton}")
                                break
                        
                        # Si no encuentra nada con 'es', usar el primer valor disponible
                        if not texto_boton and titulo:
                            primera_clave = list(titulo.keys())[0]
                            texto_boton = titulo[primera_clave]
                            print(f"⚠️ Usando primer valor disponible '{primera_clave}': {texto_boton}")
                    
                    if not texto_boton:
                        texto_boton = 'Tema sin título'
                        print(f"❌ No se encontró título, usando fallback: {texto_boton}")
                        
                else:
                    texto_boton = str(titulo)
                    print(f"📝 Título no es diccionario, usando como string: {texto_boton}")
                
                print(f"🎯 TÍTULO FINAL SELECCIONADO: '{texto_boton}'")
                
                # Agregar bullet point
                texto_boton = f"• {texto_boton}"
                
                btn = Button(
                    text=texto_boton,
                    size_hint_y=None,
                    height=dp(60),
                    background_color=(0.2, 0.4, 0.6, 1),
                    text_size=(dp(280), None),
                    halign='left',
                    valign='middle'
                )
                btn.bind(on_press=lambda x, t=tema: self.procesar_pregunta(t))
                self.content_layout.add_widget(btn)
                
                print(f"✅ Botón #{posicion_actual} creado exitosamente")
                print(f"========================================\n")
                
            except Exception as e:
                print(f"❌ Error procesando tema: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"🎯 RESUMEN FINAL:")
        print(f"   - Total de botones en pantalla: {len(self.content_layout.children)}")
        print(f"   - Idioma usado: '{self.idioma_usuario}'")
        print(f"   - Archivo usuario_actual.json existe: {os.path.exists('usuario_actual.json')}")

    def obtener_preguntas_predeterminadas(self):
        """Preguntas de respaldo en caso de que no se pueda cargar el JSON"""
        preguntas_predeterminadas = [
            {"titulo": {"es": "¿Quién es Dios?", "en": "Who is God?"}, "respuesta": {"es": "Dios es el Creador del cielo y la tierra, el Ser Supremo. Su nombre es Jehová.", "en": "God is the Creator of heaven and earth, the Supreme Being. His name is Jehovah."}, "cita": "Salmo 83:18"},
            {"titulo": {"es": "¿Quién es Jesucristo?", "en": "Who is Jesus Christ?"}, "respuesta": {"es": "Jesucristo es el Hijo de Dios, el Mesías prometido, y el primero de toda la creación.", "en": "Jesus Christ is the Son of God, the promised Messiah, and the first of all creation."}, "cita": "Juan 3:16"},
            {"titulo": {"es": "¿Qué es el Reino de Dios?", "en": "What is God's Kingdom?"}, "respuesta": {"es": "Es un gobierno celestial establecido por Jehová que reemplazará los gobiernos humanos.", "en": "It is a heavenly government established by Jehovah that will replace human governments."}, "cita": "Mateo 6:9-10"},
            {"titulo": {"es": "¿Por qué sufrimos?", "en": "Why do we suffer?"}, "respuesta": {"es": "Por vivir en un mundo gobernado por Satanás, bajo pecado heredado y condiciones injustas.", "en": "Because we live in a world ruled by Satan, affected by inherited sin and injustice."}, "cita": "1 Juan 5:19"},
            {"titulo": {"es": "¿Qué esperanza hay para los muertos?", "en": "What hope is there for the dead?"}, "respuesta": {"es": "La resurrección. Jehová devolverá la vida a los que han muerto.", "en": "The resurrection. Jehovah will restore life to those who have died."}, "cita": "Juan 5:28-29"},
            {"titulo": {"es": "¿Qué es la Biblia?", "en": "What is the Bible?"}, "respuesta": {"es": "Es la Palabra inspirada de Dios para guiar a la humanidad.", "en": "It is God's inspired Word to guide humanity."}, "cita": "2 Timoteo 3:16"},
            {"titulo": {"es": "¿Por qué debemos orar a Dios?", "en": "Why should we pray to God?"}, "respuesta": {"es": "Jehová desea que nos comuniquemos con Él como un Padre amoroso.", "en": "Jehovah wants us to communicate with Him as a loving Father."}, "cita": "Filipenses 4:6"},
            {"titulo": {"es": "¿Qué hará Dios por la humanidad?", "en": "What will God do for humanity?"}, "respuesta": {"es": "Eliminará el sufrimiento y hará de la Tierra un paraíso.", "en": "He will eliminate suffering and turn Earth into a paradise."}, "cita": "Apocalipsis 21:3-4"},
            {"titulo": {"es": "¿Qué propósito tiene la vida?", "en": "What is the purpose of life?"}, "respuesta": {"es": "Conocer a Jehová y vivir para siempre en una Tierra paradisíaca.", "en": "To know Jehovah and live forever in a paradise Earth."}, "cita": "Juan 17:3"},
            {"titulo": {"es": "¿Quién es Satanás?", "en": "Who is Satan?"}, "respuesta": {"es": "Un ángel rebelde que se convirtió en el enemigo de Dios.", "en": "A rebellious angel who became God's enemy."}, "cita": "Apocalipsis 12:9"},
            {"titulo": {"es": "¿Cómo podemos ser felices?", "en": "How can we be happy?"}, "respuesta": {"es": "Siguiendo los principios bíblicos y confiando en Jehová.", "en": "By following biblical principles and trusting in Jehovah."}, "cita": "Salmo 144:15"},
            {"titulo": {"es": "¿Qué es el amor verdadero?", "en": "What is true love?"}, "respuesta": {"es": "El amor que viene de Dios y se basa en principios, no en emociones.", "en": "Love that comes from God and is based on principles, not emotions."}, "cita": "1 Juan 4:8"}
        ]
        
        print(f"📚 Usando preguntas predeterminadas ({len(preguntas_predeterminadas)} disponibles)")
        return preguntas_predeterminadas

    def cargar_sugerencias(self):
        """Método de compatibilidad - redirige a cargar_sugerencias_iniciales"""
        self.cargar_sugerencias_iniciales()

    def generar_nuevas_sugerencias(self, instance):
        """Genera un nuevo conjunto de sugerencias aleatorias (reinicia todo)"""
        print(f"🔄 Generando nuevas sugerencias...")
        
        # Mezclar todos los temas para obtener un orden diferente
        if self.todos_los_temas:
            random.shuffle(self.todos_los_temas)
        
        # Reiniciar la paginación y mostrar nuevos temas
        self.temas_mostrados = []
        self.cargar_sugerencias_iniciales()
        
        print(f"🎯 Nuevas sugerencias cargadas con idioma: {self.idioma_usuario}")

    def mostrar_debug_popup(self):
        """Muestra un popup con información de debug para Android"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.scrollview import ScrollView
        
        # Recopilar información de debug
        info_debug = f"""INFORMACIÓN DE DEBUG:

🏁 CONSTRUCTOR:
idioma_inicial: {repr(self.idioma_inicial)}
Tipo inicial: {type(self.idioma_inicial)}

🌐 IDIOMA ACTUAL: '{self.idioma_usuario}'
Tipo actual: {type(self.idioma_usuario)}

📁 ARCHIVO usuario_actual.json existe: {os.path.exists('usuario_actual.json')}

📊 DATOS DEL USUARIO:
Usuario actual: {self.usuario_actual}

📋 TEMAS CARGADOS:
Total de temas: {len(self.todos_los_temas)}
Archivos JSON encontrados: {len([f for f in os.listdir('datos/temas/') if f.startswith('bloque_') and f.endswith('.json')]) if os.path.exists('datos/temas') else 0}

📚 PRIMER TEMA (si existe):"""

        # Agregar información del primer tema
        if self.todos_los_temas:
            primer_tema = self.todos_los_temas[0]
            info_debug += f"""
Estructura: {list(primer_tema.keys()) if isinstance(primer_tema, dict) else 'No es diccionario'}

Título completo: {primer_tema.get('titulo', 'Sin título')}

Idiomas en título: {list(primer_tema.get('titulo', {}).keys()) if isinstance(primer_tema.get('titulo'), dict) else 'No es diccionario'}
"""
        else:
            info_debug += "\n¡NO HAY TEMAS CARGADOS!"

        # Verificar archivo usuario_actual.json
        try:
            if os.path.exists('usuario_actual.json'):
                with open('usuario_actual.json', 'r', encoding='utf-8') as f:
                    contenido = json.load(f)
                info_debug += f"\n\n📄 CONTENIDO usuario_actual.json:\n{contenido}"
            else:
                info_debug += "\n\n❌ usuario_actual.json NO EXISTE"
        except Exception as e:
            info_debug += f"\n\n❌ ERROR leyendo usuario_actual.json: {e}"

        # Crear el popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        scroll = ScrollView()
        label_info = Label(
            text=info_debug,
            text_size=(dp(350), None),
            halign='left',
            valign='top'
        )
        scroll.add_widget(label_info)
        content.add_widget(scroll)
        
        # Botones del popup
        botones_layout = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(50))
        
        # Botón para cambiar a inglés
        btn_ingles = Button(
            text='🇺🇸 English',
            background_color=(0.3, 0.6, 0.3, 1)
        )
        btn_ingles.bind(on_press=lambda x: self.cambiar_idioma('en'))
        botones_layout.add_widget(btn_ingles)
        
        # Botón para cambiar a español  
        btn_espanol = Button(
            text='🇪🇸 Español',
            background_color=(0.6, 0.6, 0.3, 1)
        )
        btn_espanol.bind(on_press=lambda x: self.cambiar_idioma('es'))
        botones_layout.add_widget(btn_espanol)
        
        # Botón cerrar
        btn_cerrar = Button(
            text='Cerrar',
            background_color=(0.6, 0.3, 0.3, 1)
        )
        botones_layout.add_widget(btn_cerrar)
        
        content.add_widget(botones_layout)
        
        popup = Popup(
            title='🔍 DEBUG - Información del Idioma',
            content=content,
            size_hint=(0.9, 0.8)
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        popup.open()

    def cambiar_idioma(self, nuevo_idioma):
        """Cambia el idioma y actualiza la interfaz"""
        try:
            # Actualizar variable
            self.idioma_usuario = nuevo_idioma
            
            # Crear/actualizar archivo
            datos_usuario = {
                "usuario": self.usuario_actual or "usuario_manual",
                "idioma": nuevo_idioma
            }
            
            with open('usuario_actual.json', 'w', encoding='utf-8') as file:
                json.dump(datos_usuario, file, ensure_ascii=False, indent=2)
            
            # Actualizar interfaz
            self.actualizar_idioma()
            self.cargar_sugerencias_iniciales()
            
            print(f"✅ Idioma cambiado a: {nuevo_idioma}")
            
        except Exception as e:
            print(f"❌ Error cambiando idioma: {e}")

    def procesar_pregunta(self, tema):
        """Procesa la selección de un tema y muestra su información completa"""
        try:
            titulo = tema.get('titulo', {})
            if isinstance(titulo, dict):
                titulo_texto = titulo.get(self.idioma_usuario, titulo.get('es', 'Tema'))
            else:
                titulo_texto = str(titulo)
            
            print(f"🔍 Tema seleccionado: {titulo_texto}")
            
            # Mostrar popup con información completa del tema
            self.mostrar_detalle_tema(tema)
            
        except Exception as e:
            print(f"❌ Error procesando pregunta: {e}")

    def mostrar_detalle_tema(self, tema):
        """Muestra un popup con toda la información del tema"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.scrollview import ScrollView
        
        # Extraer información del tema
        idioma_normalizado = self.idioma_usuario.lower().strip()
        
        # Título
        titulo = tema.get('titulo', {})
        if isinstance(titulo, dict):
            titulo_texto = titulo.get(idioma_normalizado, titulo.get('es', 'Sin título'))
        else:
            titulo_texto = str(titulo)
        
        # Respuesta
        respuesta = tema.get('respuesta', {})
        if isinstance(respuesta, dict):
            respuesta_texto = respuesta.get(idioma_normalizado, respuesta.get('es', 'Sin respuesta'))
        else:
            respuesta_texto = str(respuesta)
        
        # Cita bíblica
        cita = tema.get('cita', 'Sin cita bíblica')
        
        # Categoría (si existe)
        categoria = tema.get('categoria', '')
        if isinstance(categoria, dict):
            categoria_texto = categoria.get(idioma_normalizado, categoria.get('es', ''))
        else:
            categoria_texto = str(categoria) if categoria else ''
        
        # Línea adicional (si existe)
        linea = tema.get('linea', '')
        if isinstance(linea, dict):
            linea_texto = linea.get(idioma_normalizado, linea.get('es', ''))
        else:
            linea_texto = str(linea) if linea else ''
        
        # Construir texto completo con formato simple y claro
        lineas = []
        
        # Título 
        lineas.append(titulo_texto)
        lineas.append("")  # Línea vacía
        
        if categoria_texto:
            categoria_label = "Category:" if idioma_normalizado == 'en' else "Categoría:"
            lineas.append(f"{categoria_label} {categoria_texto}")
            lineas.append("")
        
        respuesta_label = "Answer:" if idioma_normalizado == 'en' else "Respuesta:"
        lineas.append(respuesta_label)
        lineas.append("")
        lineas.append(respuesta_texto)
        lineas.append("")
        
        if linea_texto:
            additional_label = "Additional Information:" if idioma_normalizado == 'en' else "Información Adicional:"
            lineas.append(additional_label)
            lineas.append("")
            lineas.append(linea_texto)
            lineas.append("")
        
        cita_label = "Bible Citation:" if idioma_normalizado == 'en' else "Cita Bíblica:"
        lineas.append(f"{cita_label} {cita}")
        
        texto_completo = "\n".join(lineas)
        
    def mostrar_detalle_tema(self, tema):
        """Muestra un popup con toda la información del tema"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.scrollview import ScrollView
        from kivy.clock import Clock
        
        # Extraer información del tema
        idioma_normalizado = self.idioma_usuario.lower().strip()
        
        # Título
        titulo = tema.get('titulo', {})
        if isinstance(titulo, dict):
            titulo_texto = titulo.get(idioma_normalizado, titulo.get('es', 'Sin título'))
        else:
            titulo_texto = str(titulo)
        
        # Respuesta
        respuesta = tema.get('respuesta', {})
        if isinstance(respuesta, dict):
            respuesta_texto = respuesta.get(idioma_normalizado, respuesta.get('es', 'Sin respuesta'))
        else:
            respuesta_texto = str(respuesta)
        
        # Cita bíblica
        cita = tema.get('cita', 'Sin cita bíblica')
        
        # Categoría (si existe)
        categoria = tema.get('categoria', '')
        if isinstance(categoria, dict):
            categoria_texto = categoria.get(idioma_normalizado, categoria.get('es', ''))
        else:
            categoria_texto = str(categoria) if categoria else ''
        
        # Línea adicional (si existe)
        linea = tema.get('linea', '')
        if isinstance(linea, dict):
            linea_texto = linea.get(idioma_normalizado, linea.get('es', ''))
        else:
            linea_texto = str(linea) if linea else ''
        
        # Construir texto completo con formato simple y claro
        lineas = []
        
        # Título 
        lineas.append(titulo_texto)
        lineas.append("")  # Línea vacía
        
        if categoria_texto:
            categoria_label = "Category:" if idioma_normalizado == 'en' else "Categoría:"
            lineas.append(f"{categoria_label} {categoria_texto}")
            lineas.append("")
        
        respuesta_label = "Answer:" if idioma_normalizado == 'en' else "Respuesta:"
        lineas.append(respuesta_label)
        lineas.append("")
        lineas.append(respuesta_texto)
        lineas.append("")
        
        if linea_texto:
            additional_label = "Additional Information:" if idioma_normalizado == 'en' else "Información Adicional:"
            lineas.append(additional_label)
            lineas.append("")
            lineas.append(linea_texto)
            lineas.append("")
        
        cita_label = "Bible Citation:" if idioma_normalizado == 'en' else "Cita Bíblica:"
        lineas.append(f"{cita_label} {cita}")
        
        texto_completo = "\n".join(lineas)
        
        # Crear el contenido del popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # CLAVE: Layout container que mantenga el contenido en la parte superior
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        container.bind(minimum_height=container.setter('height'))
        
        # Label con el contenido
        label_contenido = Label(
            text=texto_completo,
            text_size=(dp(300), None),
            halign='left',
            valign='top',
            markup=False,
            color=(1, 1, 1, 1),
            font_size='15sp',
            size_hint_y=None
        )
        label_contenido.bind(texture_size=label_contenido.setter('size'))
        
        # Agregar el label al container
        container.add_widget(label_contenido)
        
        # ScrollView que contenga el container
        scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True
        )
        scroll.add_widget(container)
        content.add_widget(scroll)
        
        # Botones del popup
        botones_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        # Botón copiar
        btn_copiar = Button(
            text='📋 Copy' if idioma_normalizado == 'en' else '📋 Copiar',
            background_color=(0.3, 0.6, 0.3, 1)
        )
        btn_copiar.bind(on_press=lambda x: self.copiar_tema(texto_completo))
        botones_layout.add_widget(btn_copiar)
        
        # Botón cerrar
        btn_cerrar = Button(
            text='Close' if idioma_normalizado == 'en' else 'Cerrar',
            background_color=(0.6, 0.3, 0.3, 1)
        )
        botones_layout.add_widget(btn_cerrar)
        
        content.add_widget(botones_layout)
        
        # Crear el popup
        popup_titulo = titulo_texto if len(titulo_texto) < 30 else titulo_texto[:27] + "..."
        popup = Popup(
            title=popup_titulo,
            content=content,
            size_hint=(0.92, 0.75),
            auto_dismiss=True,
            separator_color=[0.2, 0.4, 0.6, 1],
            title_color=[1, 1, 1, 1],
            title_size='16sp'
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        
        # CLAVE: Forzar el scroll al tope cuando se abra el popup
        def scroll_al_tope(*args):
            scroll.scroll_y = 1  # 1 = arriba, 0 = abajo
        
        # Programar el scroll al tope para después de que se renderice
        popup.bind(on_open=lambda *args: Clock.schedule_once(scroll_al_tope, 0.1))
        
        popup.open()

    def copiar_tema(self, texto):
        """Copia el texto del tema al portapapeles (funcionalidad básica)"""
        try:
            # En Android, esto puede no funcionar, pero intentamos
            from kivy.utils import platform
            if platform == 'android':
                print("📋 Texto copiado (funcionalidad limitada en Android)")
                print(f"Texto: {texto[:100]}...")
            else:
                # En desktop se puede usar el clipboard
                import pyperclip
                pyperclip.copy(texto)
                print("📋 Texto copiado al portapapeles")
        except Exception as e:
            print(f"❌ Error copiando texto: {e}")
            print("📋 Puedes copiar manualmente el texto del popup")

    def ir_al_menu(self, instance):
        if self.volver_callback:
            self.volver_callback()
        else:
            self.manager.current = 'menu'