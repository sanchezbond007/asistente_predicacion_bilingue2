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

# ===== IMPORTACIONES PARA RECORDATORIOS =====
try:
    from pantallas.schedule_reminder import PantallaScheduleReminder
    SCHEDULE_REMINDER_DISPONIBLE = True
    print("✅ PantallaScheduleReminder importada correctamente")
except ImportError as e:
    SCHEDULE_REMINDER_DISPONIBLE = False
    print(f"⚠️ PantallaScheduleReminder no disponible: {e}")

# ===== IMPORTACIÓN: MIS RECORDATORIOS =====
try:
    from pantallas.mis_recordatorios import PantallaMisRecordatorios
    MIS_RECORDATORIOS_DISPONIBLE = True
    print("✅ PantallaMisRecordatorios importada correctamente")
except ImportError as e:
    MIS_RECORDATORIOS_DISPONIBLE = False
    print(f"⚠️ PantallaMisRecordatorios no disponible: {e}")

# ===== NUEVA IMPORTACIÓN: SEND RESUME =====
try:
    from pantallas.datos_interesado import PantallaDatosInteresado
    SEND_RESUME_DISPONIBLE = True
    print("✅ PantallaDatosInteresado (Send Resume) importada correctamente")
except ImportError as e:
    SEND_RESUME_DISPONIBLE = False
    print(f"⚠️ PantallaDatosInteresado no disponible: {e}")

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
            login_callback=self.manejar_login_exitoso,
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
            buscar_callback=self.ir_a_busqueda,
            programar_recordatorio_callback=self.ir_a_schedule_reminder,
            volver_callback=self.ir_a_login,
            # ===== CALLBACK PARA NAVEGACIÓN GENERAL =====
            navegacion_callback=self.navegar_a,
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

        # Pantalla Schedule Reminder
        if SCHEDULE_REMINDER_DISPONIBLE:
            self.pantalla_schedule_reminder = PantallaScheduleReminder(
                name='schedule_reminder',
                volver_callback=self.ir_a_menu,
                idioma=self.idioma
            )
            self.sm.add_widget(self.pantalla_schedule_reminder)
            print("✅ Pantalla Schedule Reminder agregada")
        else:
            self.pantalla_schedule_reminder = None
            print("⚠️ Pantalla Schedule Reminder no disponible")

        # Pantalla Mis Recordatorios
        if MIS_RECORDATORIOS_DISPONIBLE:
            self.pantalla_mis_recordatorios = PantallaMisRecordatorios(
                name='mis_recordatorios',
                volver_callback=self.ir_a_menu
            )
            self.sm.add_widget(self.pantalla_mis_recordatorios)
            print("✅ Pantalla Mis Recordatorios agregada")
        else:
            self.pantalla_mis_recordatorios = None
            print("⚠️ Pantalla Mis Recordatorios no disponible")

        # ===== NUEVA PANTALLA: SEND RESUME =====
        if SEND_RESUME_DISPONIBLE:
            self.pantalla_send_resume = PantallaDatosInteresado(
                name='send_resume',
                volver_callback=self.ir_a_menu,
                idioma=self.idioma
            )
            self.sm.add_widget(self.pantalla_send_resume)
            print("✅ Pantalla Send Resume (Datos Interesado) agregada")
        else:
            self.pantalla_send_resume = None
            print("⚠️ Pantalla Send Resume no disponible")

        # Mostrar primero el aviso legal
        self.sm.current = 'aviso_legal'
        return self.sm

    def cambiar_idioma(self, nuevo_idioma):
        """Método mejorado para cambiar idioma en toda la aplicación"""
        print(f"🌍 === CAMBIO GLOBAL DE IDIOMA ===")
        print(f"🌍 De: '{self.idioma}' a '{nuevo_idioma}'")
        
        self.idioma = nuevo_idioma
        
        # Actualizar todas las pantallas CORRECTAMENTE
        self.pantalla_login.idioma = nuevo_idioma
        self.pantalla_crear_usuario.idioma = nuevo_idioma
        self.pantalla_menu.idioma = nuevo_idioma
        
        # CORREGIDO: Actualizar PantallaSugerencias correctamente
        self.pantalla_sugerencias.idioma_usuario = nuevo_idioma
        self.pantalla_sugerencias.idioma_inicial = nuevo_idioma
        print(f"✅ Sugerencias actualizada: idioma_usuario='{self.pantalla_sugerencias.idioma_usuario}', idioma_inicial='{self.pantalla_sugerencias.idioma_inicial}'")
        
        # CORREGIDO: Actualizar PantallaTemasProfundos
        if hasattr(self.pantalla_profundos, 'idioma_usuario'):
            self.pantalla_profundos.idioma_usuario = nuevo_idioma
            self.pantalla_profundos.idioma_inicial = nuevo_idioma
        else:
            self.pantalla_profundos.idioma = nuevo_idioma
        
        # Actualizar Schedule Reminder
        if self.pantalla_schedule_reminder:
            self.pantalla_schedule_reminder.idioma = nuevo_idioma
            if hasattr(self.pantalla_schedule_reminder, 'cambiar_idioma'):
                self.pantalla_schedule_reminder.cambiar_idioma(nuevo_idioma)
        
        # Actualizar Mis Recordatorios
        if self.pantalla_mis_recordatorios:
            if hasattr(self.pantalla_mis_recordatorios, 'idioma'):
                self.pantalla_mis_recordatorios.idioma = nuevo_idioma
        
        # ===== NUEVO: Actualizar Send Resume =====
        if self.pantalla_send_resume:
            if hasattr(self.pantalla_send_resume, 'idioma'):
                self.pantalla_send_resume.idioma = nuevo_idioma
            if hasattr(self.pantalla_send_resume, 'cambiar_idioma'):
                self.pantalla_send_resume.cambiar_idioma(nuevo_idioma)
        
        # Forzar actualización del menú si es la pantalla actual
        if self.sm.current == 'menu':
            print("🔄 Actualizando menú inmediatamente...")
            self.pantalla_menu.forzar_idioma(nuevo_idioma)
        
        print(f"🌍 === CAMBIO DE IDIOMA COMPLETADO ===")

    def manejar_login_exitoso(self, datos_login):
        """Maneja el login exitoso y navega al menú con idioma correcto"""
        print(f"✅ === LOGIN EXITOSO ===")
        print(f"✅ Usuario: {datos_login.get('usuario', 'N/A')}")
        print(f"✅ Idioma actual: '{self.idioma}'")
        
        # Asegurar que el menú tenga el idioma correcto ANTES de navegar
        print(f"🔧 Configurando idioma del menú: '{self.idioma}'")
        self.pantalla_menu.idioma = self.idioma
        if hasattr(self.pantalla_menu, 'forzar_idioma'):
            self.pantalla_menu.forzar_idioma(self.idioma)
        
        # Navegar al menú
        print("🔄 Navegando al menú...")
        self.sm.current = 'menu'
        print(f"✅ === NAVEGACIÓN AL MENÚ COMPLETADA ===")

    # ===== FUNCIÓN DE NAVEGACIÓN GENERAL =====
    def navegar_a(self, destino):
        """Función de navegación general para el menú"""
        print(f"🎯 Navegando a: {destino}")
        
        if destino == 'mis_recordatorios':
            self.ir_a_mis_recordatorios()
        elif destino == 'send_resume':
            self.ir_a_send_resume()  # ← NUEVA FUNCIÓN
        elif destino == 'casa_en_casa':
            print("🚧 Casa en Casa - En desarrollo")
        elif destino == 'configuracion':
            print("🚧 Configuración - En desarrollo")
        elif destino == 'acerca_de':
            print("🚧 Acerca de - En desarrollo")
        else:
            print(f"⚠️ Destino no reconocido: {destino}")

    def ir_a_login(self, *args):
        print("🔙 Navegando a login...")
        self.sm.current = 'login'

    def ir_a_crear_usuario(self, *args):
        print("👤 Navegando a crear usuario...")
        # Asegurar idioma correcto antes de navegar
        self.pantalla_crear_usuario.idioma = self.idioma
        self.sm.current = 'crear_usuario'

    def ir_a_menu(self, *args):
        print(f"🏠 Navegando a menú con idioma: '{self.idioma}'")
        # CRÍTICO: Actualizar idioma del menú antes de navegar
        self.pantalla_menu.idioma = self.idioma
        if hasattr(self.pantalla_menu, 'forzar_idioma'):
            self.pantalla_menu.forzar_idioma(self.idioma)
        self.sm.current = 'menu'

    def ir_a_sugerencias(self, *args):
        print(f"📋 === NAVEGANDO A SUGERENCIAS ===")
        print(f"📋 Idioma actual de la app: '{self.idioma}'")
        
        # CORREGIDO: Asegurar idioma correcto antes de navegar
        self.pantalla_sugerencias.idioma_usuario = self.idioma
        self.pantalla_sugerencias.idioma_inicial = self.idioma
        
        print(f"📋 Idioma asignado a sugerencias:")
        print(f"   - idioma_usuario: '{self.pantalla_sugerencias.idioma_usuario}'")
        print(f"   - idioma_inicial: '{self.pantalla_sugerencias.idioma_inicial}'")
        
        # Forzar actualización de la interfaz
        if hasattr(self.pantalla_sugerencias, 'actualizar_idioma'):
            self.pantalla_sugerencias.actualizar_idioma()
        
        self.sm.current = 'sugerencias'
        print(f"📋 === NAVEGACIÓN A SUGERENCIAS COMPLETADA ===")

    def ir_a_profundos(self, *args):
        print("📚 Navegando a temas profundos...")
        # CORREGIDO: Asegurar idioma correcto antes de navegar
        if hasattr(self.pantalla_profundos, 'idioma_usuario'):
            self.pantalla_profundos.idioma_usuario = self.idioma
            self.pantalla_profundos.idioma_inicial = self.idioma
        else:
            self.pantalla_profundos.idioma = self.idioma
        self.sm.current = 'temas_profundos'

    def ir_a_busqueda(self, *args):
        print("🔍 Función de búsqueda aún no implementada.")
        # Aquí puedes agregar una pantalla real en el futuro:
        # self.pantalla_busqueda.idioma = self.idioma
        # self.sm.current = 'busqueda'

    def ir_a_schedule_reminder(self, *args):
        """Navegar a la pantalla de programar recordatorio"""
        print("⏰ === NAVEGANDO A SCHEDULE REMINDER ===")
        
        if self.pantalla_schedule_reminder:
            print(f"⏰ Idioma actual de la app: '{self.idioma}'")
            
            # Asegurar idioma correcto antes de navegar
            self.pantalla_schedule_reminder.idioma = self.idioma
            if hasattr(self.pantalla_schedule_reminder, 'cambiar_idioma'):
                self.pantalla_schedule_reminder.cambiar_idioma(self.idioma)
            
            self.sm.current = 'schedule_reminder'
            print("✅ Navegación a Schedule Reminder completada")
        else:
            print("❌ Schedule Reminder no está disponible")
            print("🔧 Asegúrate de que el archivo pantallas/schedule_reminder.py existe")

    def ir_a_mis_recordatorios(self, *args):
        """Navegar a la pantalla de ver mis recordatorios"""
        print("📋 === NAVEGANDO A MIS RECORDATORIOS ===")
        
        if self.pantalla_mis_recordatorios:
            print(f"📋 Idioma actual de la app: '{self.idioma}'")
            
            # Asegurar idioma correcto antes de navegar
            if hasattr(self.pantalla_mis_recordatorios, 'idioma'):
                self.pantalla_mis_recordatorios.idioma = self.idioma
            
            self.sm.current = 'mis_recordatorios'
            print("✅ Navegación a Mis Recordatorios completada")
        else:
            print("❌ Mis Recordatorios no está disponible")
            print("🔧 Asegúrate de que el archivo pantallas/mis_recordatorios.py existe")

    # ===== NUEVA FUNCIÓN: NAVEGAR A SEND RESUME =====
    def ir_a_send_resume(self, *args):
        """Navegar a la pantalla de enviar resumen al interesado"""
        print("📧 === NAVEGANDO A SEND RESUME ===")
        
        if self.pantalla_send_resume:
            print(f"📧 Idioma actual de la app: '{self.idioma}'")
            
            # Asegurar idioma correcto antes de navegar
            if hasattr(self.pantalla_send_resume, 'idioma'):
                self.pantalla_send_resume.idioma = self.idioma
            if hasattr(self.pantalla_send_resume, 'cambiar_idioma'):
                self.pantalla_send_resume.cambiar_idioma(self.idioma)
            
            self.sm.current = 'send_resume'
            print("✅ Navegación a Send Resume completada")
        else:
            print("❌ Send Resume no está disponible")
            print("🔧 Asegúrate de que el archivo pantallas/datos_interesado.py existe")

    def buscar_actualizacion(self, *args):
        print("🔄 Verificando actualizaciones...")

if __name__ == '__main__':
    print("🚀 Iniciando Asistente de Predicación...")
    print("📱 Funcionalidades disponibles:")
    if SCHEDULE_REMINDER_DISPONIBLE:
        print("   ✅ Programar Recordatorios")
    else:
        print("   ❌ Programar Recordatorios (archivo faltante)")
    
    if MIS_RECORDATORIOS_DISPONIBLE:
        print("   ✅ Ver Mis Recordatorios")
    else:
        print("   ❌ Ver Mis Recordatorios (archivo faltante)")
    
    if SEND_RESUME_DISPONIBLE:
        print("   ✅ Send Resume (Datos Interesado)")
    else:
        print("   ❌ Send Resume (archivo faltante)")
    
    print("=" * 50)
    
    AsistentePredicacionApp().run()