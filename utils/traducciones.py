# Variable global para el idioma actual
_idioma_actual = 'es'

def traducir(clave, idioma='es'):
    traducciones = {
        'es': {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'telefono': 'Teléfono',
            'correo': 'Correo electrónico',
            'usuario': 'Nombre de usuario',
            'contrasena': 'Contraseña',
            'crear_usuario': 'Crear usuario',
            'volver': 'Volver',
            'campos_obligatorios': 'Faltan campos obligatorios',
            'usuario_creado': '¡Usuario creado con éxito!',
            'error': 'Error',
            'exito': 'Éxito',
            'asistente_predicacion': 'Asistente de Predicación',
            'sugerencias': 'Sugerencias',
            'temas_profundos': 'Temas Profundos',
            'buscar': 'Buscar',
            'cerrar_sesion': 'Cerrar sesión',
            'continuar': 'Entrar',
            'idioma': 'Idioma',
            'espanol': 'Español',
            'ingles': 'Inglés',
            'login': 'Iniciar sesión',
            'iniciar_sesion': 'Iniciar sesión',
            'buscar_actualizaciones': 'Buscar actualizaciones',
            'recordar_usuario': 'Recordar usuario',
            'buscar_titulo': 'Buscar temas',
            'buscar_hint': 'Escribe una palabra clave...',
            'resultados': 'Resultados',
            'sin_resultados': 'No se encontraron coincidencias.',
            'titulo_login': 'Inicio de sesión',
            'titulo_menu': 'Menú principal',
            'titulo_temas_profundos': 'Temas Profundos',
            'actualizacion_disponible_confirmar': 'Nueva versión disponible: {version_nueva} (actual: {version_actual}). ¿Desea descargarla?',
            'confirmar_actualizacion': 'Confirmar Actualización',
            'si': 'Sí',
            'no': 'No',
            'error_actualizacion': 'Error de actualización',
            'actualizacion_completada': 'Actualización completada a la versión {version}.',
            'reiniciar_aplicacion': 'Por favor, reinicie la aplicación para aplicar los cambios.',
            'informacion': 'Información',
            'error_descarga_archivos': 'Error al descargar algunos archivos:',
            'aviso_legal_texto': (
                'Esta aplicación es un asistente personal diseñado para apoyar la predicación. '
                'No representa ni sustituye al sitio oficial jw.org. Toda la información presentada '
                'se basa en publicaciones públicas y recursos disponibles al público. El uso de esta aplicación '
                'es voluntario y bajo la responsabilidad personal del usuario. Esta herramienta no almacena ni distribuye '
                'contenido oficial, solo organiza referencias útiles para el estudio y la predicación.'
            ),
            'aceptar': 'Aceptar'
        },
        'en': {
            'nombre': 'First Name',
            'apellido': 'Last Name',
            'telefono': 'Phone',
            'correo': 'Email',
            'usuario': 'Username',
            'contrasena': 'Password',
            'crear_usuario': 'Create user',
            'volver': 'Back',
            'campos_obligatorios': 'Missing required fields',
            'usuario_creado': 'User created successfully!',
            'error': 'Error',
            'exito': 'Success',
            'asistente_predicacion': 'Preaching Assistant',
            'sugerencias': 'Suggestions',
            'temas_profundos': 'Deep Topics',
            'buscar': 'Search',
            'cerrar_sesion': 'Log out',
            'continuar': 'Enter',
            'idioma': 'Language',
            'espanol': 'Spanish',
            'ingles': 'English',
            'login': 'Login',
            'iniciar_sesion': 'Sign in',
            'buscar_actualizaciones': 'Check for updates',
            'recordar_usuario': 'Remember user',
            'buscar_titulo': 'Search Topics',
            'buscar_hint': 'Type a keyword...',
            'resultados': 'Results',
            'sin_resultados': 'No matches found.',
            'titulo_login': 'Login',
            'titulo_menu': 'Main Menu',
            'titulo_temas_profundos': 'Deep Topics',
            'actualizacion_disponible_confirmar': 'New version available: {version_nueva} (current: {version_actual}). Do you want to download it?',
            'confirmar_actualizacion': 'Confirm Update',
            'si': 'Yes',
            'no': 'No',
            'error_actualizacion': 'Update Error',
            'actualizacion_completada': 'Update completed to version {version}.',
            'reiniciar_aplicacion': 'Please restart the application to apply changes.',
            'informacion': 'Information',
            'error_descarga_archivos': 'Error downloading some files:',
            'aviso_legal_texto': (
                'This application is a personal assistant designed to support preaching activities. '
                'It does not represent or replace the official website jw.org. All information presented '
                'is based on publicly available publications and resources. Use of this application is voluntary '
                'and under the personal responsibility of the user. This tool does not store or distribute official content; '
                'it only organizes useful references for study and preaching.'
            ),
            'aceptar': 'Accept'
        }
    }

    return traducciones.get(idioma, traducciones['es']).get(clave, clave)

def obtener_texto(clave):
    """
    Obtiene el texto traducido usando el idioma actual global
    """
    return traducir(clave, _idioma_actual)

def cambiar_idioma(nuevo_idioma):
    """
    Cambia el idioma actual globalmente
    """
    global _idioma_actual
    if nuevo_idioma in ['es', 'en']:
        _idioma_actual = nuevo_idioma
        return True
    return False

def obtener_idioma_actual():
    """
    Retorna el idioma actual
    """
    return _idioma_actual