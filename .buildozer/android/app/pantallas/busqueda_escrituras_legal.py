# busqueda_escrituras_legal.py - SISTEMA LEGAL DE BÚSQUEDA

import requests
import urllib.parse

class BuscadorEscriturasLegal:
    """Buscador de escrituras usando solo fuentes legales y gratuitas"""
    
    def __init__(self):
        self.fuentes_legales = {
            'jw_org': {
                'nombre': 'JW.org (Oficial)',
                'base_url': 'https://www.jw.org/finder',
                'parametros': {'wtlocale': 'S', 'pub-filter': 'bi12'},
                'legal': True,
                'gratuita': True
            },
            'bible_gateway_rvr': {
                'nombre': 'Bible Gateway (RVR1960)',
                'base_url': 'https://www.biblegateway.com/passage/',
                'version': 'RVR1960',
                'legal': True,
                'gratuita': True
            },
            'bible_gateway_kjv': {
                'nombre': 'Bible Gateway (KJV)',
                'base_url': 'https://www.biblegateway.com/passage/',
                'version': 'KJV',
                'legal': True,
                'gratuita': True
            }
        }
    
    def buscar_escritura_jw_org(self, texto_busqueda):
        """Buscar en JW.org - 100% legal y oficial"""
        try:
            url = "https://www.jw.org/finder"
            params = {
                'wtlocale': 'S',  # Español
                'pub-filter': 'bi12',  # Biblia
                'q': texto_busqueda
            }
            
            # Solo construir URL, no hacer request directo
            url_completa = f"{url}?{urllib.parse.urlencode(params)}"
            
            return {
                'fuente': 'JW.org',
                'url': url_completa,
                'legal': True,
                'metodo': 'redireccion_web',
                'descripcion': f'Búsqueda de "{texto_busqueda}" en JW.org'
            }
            
        except Exception as e:
            print(f"❌ Error en búsqueda JW.org: {e}")
            return None
    
    def buscar_escritura_bible_gateway(self, referencia, version='RVR1960'):
        """Buscar en Bible Gateway - Versiones libres de copyright"""
        try:
            # Versiones completamente libres
            versiones_libres = ['RVR1960', 'KJV', 'ASV', 'WEB', 'YLT']
            
            if version not in versiones_libres:
                version = 'RVR1960'  # Default seguro
            
            url_completa = f"https://www.biblegateway.com/passage/?search={urllib.parse.quote(referencia)}&version={version}"
            
            return {
                'fuente': f'Bible Gateway ({version})',
                'url': url_completa,
                'legal': True,
                'version': version,
                'metodo': 'redireccion_web',
                'descripcion': f'Búsqueda de "{referencia}" en Bible Gateway'
            }
            
        except Exception as e:
            print(f"❌ Error en búsqueda Bible Gateway: {e}")
            return None
    
    def generar_opciones_busqueda(self, texto_busqueda):
        """Generar múltiples opciones de búsqueda legal"""
        opciones = []
        
        # Opción 1: JW.org
        jw_result = self.buscar_escritura_jw_org(texto_busqueda)
        if jw_result:
            opciones.append(jw_result)
        
        # Opción 2: Bible Gateway RVR1960
        bg_result = self.buscar_escritura_bible_gateway(texto_busqueda, 'RVR1960')
        if bg_result:
            opciones.append(bg_result)
        
        # Opción 3: Bible Gateway KJV (inglés)
        if texto_busqueda:
            bg_kjv = self.buscar_escritura_bible_gateway(texto_busqueda, 'KJV')
            if bg_kjv:
                opciones.append(bg_kjv)
        
        return opciones
    
    def abrir_busqueda_segura(self, texto_busqueda, fuente_preferida='jw_org'):
        """Abrir búsqueda en navegador usando fuente legal"""
        import webbrowser
        
        try:
            if fuente_preferida == 'jw_org':
                resultado = self.buscar_escritura_jw_org(texto_busqueda)
            else:
                resultado = self.buscar_escritura_bible_gateway(texto_busqueda)
            
            if resultado:
                webbrowser.open(resultado['url'])
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error abriendo búsqueda: {e}")
            return False

# DATOS DE ESCRITURAS PRE-CARGADAS (sin copyright)
ESCRITURAS_REFERENCIAS_LIBRES = {
    'esperanza': [
        'Juan 5:28-29',
        '1 Tesalonicenses 4:13-14',
        'Apocalipsis 21:3-4'
    ],
    'reino': [
        'Mateo 6:9-10',
        'Daniel 2:44',
        'Mateo 24:14'
    ],
    'vida_eterna': [
        'Juan 3:16',
        'Salmo 37:29',
        'Mateo 5:5'
    ],
    'nombre_dios': [
        'Éxodo 6:3',
        'Salmo 83:18',
        'Isaías 42:8'
    ],
    'resurrección': [
        'Juan 5:28-29',
        'Hechos 24:15',
        '1 Corintios 15:42-44'
    ]
}

# FUNCIÓN PARA INTEGRAR EN LA APP
def buscar_escritura_legal(termino_busqueda, idioma='es'):
    """
    Función principal para buscar escrituras de forma legal
    
    Uso:
    resultado = buscar_escritura_legal("Juan 3:16")
    """
    buscador = BuscadorEscriturasLegal()
    
    # Generar opciones de búsqueda
    opciones = buscador.generar_opciones_busqueda(termino_busqueda)
    
    # Buscar en referencias pre-cargadas
    referencias_encontradas = []
    termino_lower = termino_busqueda.lower()
    
    for tema, refs in ESCRITURAS_REFERENCIAS_LIBRES.items():
        if tema in termino_lower or any(palabra in termino_lower for palabra in tema.split('_')):
            referencias_encontradas.extend(refs)
    
    return {
        'opciones_web': opciones,
        'referencias_sugeridas': referencias_encontradas,
        'legal': True,
        'fuentes_usadas': ['JW.org', 'Bible Gateway (versiones libres)']
    }

# EJEMPLO DE USO
if __name__ == "__main__":
    # Ejemplo de búsqueda legal
    resultado = buscar_escritura_legal("esperanza resurrección")
    print("Opciones web:", resultado['opciones_web'])
    print("Referencias sugeridas:", resultado['referencias_sugeridas'])