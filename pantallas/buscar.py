import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp

# Asegura acceso a la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.temas_handler import cargar_todos_los_bloques
from utils.temas_handler2 import cargar_temas_profundos
from utils.traducciones import traducir as t

# INTEGRACIÓN CON HISTORIAL
try:
    from pantallas.send_resume import agregar_consulta_al_historial
    HISTORIAL_DISPONIBLE = True
    print("✅ Integración con historial disponible")
except ImportError:
    HISTORIAL_DISPONIBLE = False
    print("⚠️ Historial no disponible")

class PantallaBuscar(Screen):
    def __init__(self, volver_callback=None, idioma='es', **kwargs):
        super().__init__(**kwargs)
        self.volver_callback = volver_callback
        self.idioma = idioma
        
        # Variables para resultados
        self.resultados_actuales = []

        self.layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        
        # Título
        titulo = Label(
            text=t("Buscar en la Biblioteca", self.idioma),
            font_size=dp(24),
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.6, 0.9, 1)
        )
        self.layout.add_widget(titulo)
        
        # Campo de búsqueda
        self.text_input = TextInput(
            hint_text=t("Buscar", self.idioma), 
            size_hint_y=None, 
            height=dp(60), 
            font_size=dp(18),
            multiline=False
        )
        # Buscar al presionar Enter
        self.text_input.bind(on_text_validate=self.realizar_busqueda)
        
        self.boton_buscar = Button(
            text=t("🔍 Buscar", self.idioma), 
            size_hint_y=None, 
            height=dp(50), 
            font_size=dp(18), 
            background_color=(0.2, 0.6, 1, 1)
        )
        self.boton_buscar.bind(on_press=self.realizar_busqueda)

        # Layout de resultados
        self.resultados_layout = GridLayout(
            cols=1, 
            spacing=dp(5), 
            size_hint_y=None
        )
        self.resultados_layout.bind(minimum_height=self.resultados_layout.setter('height'))
        
        self.scroll = ScrollView()
        self.scroll.add_widget(self.resultados_layout)

        # Botón volver
        self.boton_volver = Button(
            text=t("← Volver", self.idioma), 
            size_hint_y=None, 
            height=dp(50), 
            font_size=dp(18), 
            background_color=(0.7, 0.3, 0.3, 1)
        )
        self.boton_volver.bind(on_press=self.volver)

        # Agregar widgets
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.boton_buscar)
        
        # Label de estado
        self.estado_label = Label(
            text=t("Escribe un término para buscar", self.idioma),
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            color=(0.7, 0.7, 0.7, 1)
        )
        self.layout.add_widget(self.estado_label)
        
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.boton_volver)

        self.add_widget(self.layout)

    def realizar_busqueda(self, instancia=None):
        """Realizar búsqueda en todos los contenidos"""
        termino = self.text_input.text.strip()
        if not termino:
            self.estado_label.text = t("Por favor escribe un término para buscar", self.idioma)
            return

        print(f"🔍 Buscando: '{termino}'")
        self.estado_label.text = f"🔍 Buscando '{termino}'..."

        # Limpiar resultados anteriores
        self.resultados_layout.clear_widgets()
        self.resultados_actuales = []

        # Cargar datos
        try:
            temas_normales = cargar_todos_los_bloques()
            temas_profundos = cargar_temas_profundos(self.idioma)
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            self.estado_label.text = t("Error cargando la biblioteca", self.idioma)
            return

        resultados = []
        termino_lower = termino.lower()

        # Buscar en temas normales
        for tema in temas_normales:
            try:
                titulo = tema.get("titulo", {}).get(self.idioma, "")
                respuesta = tema.get("respuesta", {}).get(self.idioma, "")
                
                if termino_lower in titulo.lower() or termino_lower in respuesta.lower():
                    resultado = {
                        "titulo": titulo,
                        "contenido": respuesta,
                        "versiculos": [tema.get("cita", "")],
                        "fuente": "Biblioteca Básica",
                        "copyright": "",
                        "tipo": "tema_normal"
                    }
                    resultados.append(resultado)
            except Exception as e:
                print(f"⚠️ Error procesando tema normal: {e}")

        # Buscar en temas profundos
        for articulo in temas_profundos:
            try:
                titulo = articulo.get("titulo", "")
                contenido = articulo.get("contenido", "")
                
                if termino_lower in titulo.lower() or termino_lower in contenido.lower():
                    resultado = dict(articulo)
                    resultado["tipo"] = "tema_profundo"
                    if "fuente" not in resultado:
                        resultado["fuente"] = "Biblioteca Avanzada"
                    resultados.append(resultado)
            except Exception as e:
                print(f"⚠️ Error procesando tema profundo: {e}")

        # Mostrar resultados
        self.mostrar_resultados(resultados, termino)

    def mostrar_resultados(self, resultados, termino):
        """Mostrar los resultados de búsqueda"""
        self.resultados_actuales = resultados
        
        if not resultados:
            self.estado_label.text = f"❌ No se encontraron resultados para '{termino}'"
            
            # Mensaje de no resultados
            no_resultado_label = Label(
                text=t("No se encontraron resultados. Intenta con otros términos.", self.idioma),
                font_size=dp(16),
                size_hint_y=None,
                height=dp(100),
                color=(0.7, 0.7, 0.7, 1),
                halign='center'
            )
            no_resultado_label.bind(size=no_resultado_label.setter('text_size'))
            self.resultados_layout.add_widget(no_resultado_label)
            return

        # Mostrar estado de resultados
        self.estado_label.text = f"✅ {len(resultados)} resultado(s) encontrado(s)"

        # Crear botones para cada resultado
        for i, resultado in enumerate(resultados):
            titulo = resultado.get("titulo", "Sin título")[:80]
            fuente = resultado.get("fuente", "")
            
            # Crear layout para cada resultado
            resultado_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(85),
                spacing=dp(2)
            )
            
            # Botón principal
            btn = Button(
                text=titulo,
                font_size=dp(14),
                background_color=(0.3, 0.5, 0.9, 1),
                size_hint_y=None,
                height=dp(60)
            )
            btn.bind(on_press=lambda btn, idx=i: self.mostrar_detalle(idx))
            
            # Label de fuente
            fuente_label = Label(
                text=f"📚 {fuente}",
                font_size=dp(10),
                size_hint_y=None,
                height=dp(20),
                color=(0.6, 0.6, 0.8, 1)
            )
            
            resultado_layout.add_widget(btn)
            resultado_layout.add_widget(fuente_label)
            self.resultados_layout.add_widget(resultado_layout)

    def mostrar_detalle(self, indice):
        """Mostrar el detalle completo de un resultado"""
        if indice >= len(self.resultados_actuales):
            return
            
        articulo = self.resultados_actuales[indice]
        titulo = articulo.get("titulo", "Sin título")
        contenido = articulo.get("contenido", "")
        versiculos = articulo.get("versiculos", [])
        fuente = articulo.get("fuente", "")
        copyright_ = articulo.get("copyright", "")

        # Construir el texto completo
        texto_completo = self.construir_texto_completo(titulo, contenido, versiculos, fuente, copyright_)

        # AGREGAR AL HISTORIAL
        if HISTORIAL_DISPONIBLE:
            try:
                agregar_consulta_al_historial(
                    fuente='buscar',
                    titulo=f"Búsqueda: {titulo}",
                    contenido=texto_completo,
                    idioma=self.idioma
                )
                print(f"📝 Resultado de búsqueda agregado al historial: {titulo[:50]}...")
            except Exception as e:
                print(f"⚠️ Error agregando al historial: {e}")

        # Crear popup
        self.crear_popup_detalle(titulo, texto_completo)

    def construir_texto_completo(self, titulo, contenido, versiculos, fuente, copyright_):
        """Construir el texto completo del resultado"""
        texto = f"{contenido}\n\n"
        
        if versiculos and any(versiculos):
            texto += "📖 Versículos:\n"
            for v in versiculos:
                if isinstance(v, dict):
                    cita = v.get("cita", "")
                    texto_verso = v.get("texto", "")
                    if cita and texto_verso:
                        texto += f"{cita} - \"{texto_verso}\"\n"
                    elif cita:
                        texto += f"{cita}\n"
                elif isinstance(v, str) and v.strip():
                    texto += f"{v}\n"
            texto += "\n"

        if fuente:
            texto += f"📚 Fuente: {fuente}\n"
        if copyright_:
            texto += f"© {copyright_}"

        return texto

    def crear_popup_detalle(self, titulo, texto):
        """Crear popup con el detalle del resultado"""
        # Layout principal del popup
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # ScrollView con el contenido
        scroll_content = ScrollView()
        
        contenido_label = Label(
            text=texto,
            font_size=dp(14),
            size_hint_y=None,
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(1, 1, 1, 1)
        )
        
        # Configurar el ancho del texto
        def actualizar_text_size(instance, size):
            instance.text_size = (size[0] - dp(30), None)
        
        contenido_label.bind(size=actualizar_text_size)
        contenido_label.bind(texture_size=contenido_label.setter('size'))
        
        scroll_content.add_widget(contenido_label)
        content.add_widget(scroll_content)
        
        # Botones
        botones_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )
        
        # Botón copiar (si está disponible)
        try:
            btn_copiar = Button(
                text="📋 Copiar",
                background_color=(0.2, 0.7, 0.2, 1),
                font_size=dp(14)
            )
            btn_copiar.bind(on_press=lambda x: self.copiar_texto(texto))
            botones_layout.add_widget(btn_copiar)
        except:
            pass
        
        # Botón cerrar
        btn_cerrar = Button(
            text=t("Cerrar", self.idioma),
            background_color=(0.7, 0.3, 0.3, 1),
            font_size=dp(14)
        )
        botones_layout.add_widget(btn_cerrar)
        
        content.add_widget(botones_layout)
        
        # Crear y mostrar popup
        popup = Popup(
            title=titulo[:50] + ("..." if len(titulo) > 50 else ""),
            content=content,
            size_hint=(0.95, 0.8),
            auto_dismiss=False
        )
        
        btn_cerrar.bind(on_press=popup.dismiss)
        
        # Auto-scroll al tope cuando se abre
        def scroll_al_tope(*args):
            scroll_content.scroll_y = 1
        
        popup.bind(on_open=lambda *args: scroll_al_tope())
        popup.open()

    def copiar_texto(self, texto):
        """Copiar texto al portapapeles"""
        try:
            from kivy.utils import platform
            if platform == 'android':
                print("📋 Texto disponible para copiar (funcionalidad limitada en Android)")
            else:
                try:
                    import pyperclip
                    pyperclip.copy(texto)
                    print("📋 Texto copiado al portapapeles")
                except ImportError:
                    print("📋 pyperclip no disponible - instala con: pip install pyperclip")
        except Exception as e:
            print(f"Error copiando texto: {e}")

    def cambiar_idioma(self, nuevo_idioma):
        """Cambiar el idioma de la pantalla"""
        self.idioma = nuevo_idioma
        # Reconstruir la interfaz con el nuevo idioma
        self.clear_widgets()
        self.__init__(self.volver_callback, nuevo_idioma)

    def on_enter(self):
        """Al entrar a la pantalla, focus en el campo de búsqueda"""
        try:
            self.text_input.focus = True
        except:
            pass

    def volver(self, instancia):
        """Volver al menú principal"""
        print("🔙 Volviendo al menú principal desde Buscar")
        if self.volver_callback:
            self.volver_callback()
        else:
            print("⚠️ volver_callback no está definido")


# FUNCIÓN DE UTILIDAD PARA BÚSQUEDA EXTERNA
def buscar_contenido(termino, idioma='es'):
    """
    Función de utilidad para buscar contenido desde otras pantallas
    
    Args:
        termino (str): Término de búsqueda
        idioma (str): Idioma de búsqueda
    
    Returns:
        list: Lista de resultados encontrados
    """
    try:
        temas_normales = cargar_todos_los_bloques()
        temas_profundos = cargar_temas_profundos(idioma)
        
        resultados = []
        termino_lower = termino.lower()
        
        # Buscar en temas normales
        for tema in temas_normales:
            titulo = tema.get("titulo", {}).get(idioma, "")
            respuesta = tema.get("respuesta", {}).get(idioma, "")
            
            if termino_lower in titulo.lower() or termino_lower in respuesta.lower():
                resultado = {
                    "titulo": titulo,
                    "contenido": respuesta,
                    "versiculos": [tema.get("cita", "")],
                    "fuente": "Biblioteca Básica",
                    "tipo": "tema_normal"
                }
                resultados.append(resultado)
        
        # Buscar en temas profundos
        for articulo in temas_profundos:
            titulo = articulo.get("titulo", "")
            contenido = articulo.get("contenido", "")
            
            if termino_lower in titulo.lower() or termino_lower in contenido.lower():
                resultado = dict(articulo)
                resultado["tipo"] = "tema_profundo"
                if "fuente" not in resultado:
                    resultado["fuente"] = "Biblioteca Avanzada"
                resultados.append(resultado)
        
        return resultados
        
    except Exception as e:
        print(f"❌ Error en búsqueda externa: {e}")
        return []