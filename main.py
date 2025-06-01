import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Asegura acceso al directorio base del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from pantallas.menu import PantallaMenu
from pantallas.sugerencias import PantallaSugerencias
from pantallas.temas_profundos import PantallaTemasProfundos
from pantallas.login import PantallaLogin
from pantallas.crear_usuario import PantallaCrearUsuario
from pantallas.aviso_legal import PantallaAvisoLegal
from pantallas.buscar import PantallaBuscar  # ← NUEVA pantalla añadida

class AsistentePredicacionApp(App):
    def build(self):
        self.idioma = 'es'  # Idioma predeterminado
        self.sm = ScreenManager(transition=FadeTransition())

        # Pantalla Aviso Legal
        self.pantalla_aviso = PantallaAvisoLegal(
            name='aviso_legal',
            continuar_callback=self.ir_a_login
        )
        self.sm.add_widget(self.pantalla_aviso)

        # Pantalla Login
        self.pantalla_login = PantallaLogin(
            name='login',
            idioma_callback=self.cambiar_idioma,
            continuar_callback=self.ir_a_menu,
            crear_usuario_callback=self.ir_a_crear_usuario,
            actualizar_callback=self.buscar_actualizacion,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_login)

        # Pantalla Crear Usuario
        self.pantalla_crear_usuario = PantallaCrearUsuario(
            name='crear_usuario',
            volver_callback=self.ir_a_login,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_crear_usuario)

        # Pantalla Menú principal
        self.pantalla_menu = PantallaMenu(
            name='menu',
            sugerencias_callback=self.ir_a_sugerencias,
            profundos_callback=self.ir_a_profundos,
            buscar_callback=self.ir_a_busqueda,  # ← ACTIVADO
            volver_callback=self.ir_a_login,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_menu)

        # Pantalla Sugerencias
        self.pantalla_sugerencias = PantallaSugerencias(
            name='sugerencias',
            volver_callback=self.ir_a_menu,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_sugerencias)

        # Pantalla Temas Profundos
        self.pantalla_profundos = PantallaTemasProfundos(
            name='temas_profundos',
            volver_callback=self.ir_a_menu,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_profundos)

        # Pantalla Buscar
        self.pantalla_buscar = PantallaBuscar(
            name='buscar',
            volver_callback=self.ir_a_menu,
            idioma=self.idioma
        )
        self.sm.add_widget(self.pantalla_buscar)

        # Mostrar primero el aviso legal
        self.sm.current = 'aviso_legal'
        return self.sm

    def cambiar_idioma(self, nuevo_idioma):
        self.idioma = nuevo_idioma
        self.pantalla_login.idioma = nuevo_idioma
        self.pantalla_crear_usuario.idioma = nuevo_idioma
        self.pantalla_menu.idioma = nuevo_idioma
        self.pantalla_sugerencias.idioma = nuevo_idioma
        self.pantalla_profundos.idioma = nuevo_idioma
        self.pantalla_buscar.idioma = nuevo_idioma

    def ir_a_login(self, *args):
        self.sm.current = 'login'

    def ir_a_crear_usuario(self, *args):
        self.sm.current = 'crear_usuario'

    def ir_a_menu(self, *args):
        self.sm.current = 'menu'

    def ir_a_sugerencias(self, *args):
        self.sm.current = 'sugerencias'

    def ir_a_profundos(self, *args):
        self.sm.current = 'temas_profundos'

    def ir_a_busqueda(self, *args):
        print("🔍 Cambiando a pantalla de búsqueda")
        self.sm.current = 'buscar'

    def buscar_actualizacion(self, *args):
        print("🔄 Verificando actualizaciones...")

if __name__ == '__main__':
    AsistentePredicacionApp().run()