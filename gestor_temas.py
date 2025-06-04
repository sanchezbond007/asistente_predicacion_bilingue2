# gestor_temas.py - SISTEMA COMPLETO DE CAPTURA Y ALMACENAMIENTO
import json
import os
import datetime

class GestorTemas:
    def __init__(self):
        self.archivo_sesion = "temas_sesion_actual.json"
        self.directorio_historiales = "historiales_interesados"
        self.crear_directorio_si_no_existe()
    
    def crear_directorio_si_no_existe(self):
        if not os.path.exists(self.directorio_historiales):
            os.makedirs(self.directorio_historiales)
    
    def capturar_tema_seleccionado(self, titulo_tema, respuesta_completa, origen, nombre_interesado=None):
        tema_capturado = {
            'titulo': titulo_tema,
            'respuesta': respuesta_completa,
            'origen': origen,
            'fecha': datetime.datetime.now().strftime('%d/%m/%Y'),
            'hora': datetime.datetime.now().strftime('%H:%M'),
            'timestamp': datetime.datetime.now().isoformat(),
            'nombre_interesado': nombre_interesado
        }
        
        self.guardar_en_sesion_actual(tema_capturado)
        
        if nombre_interesado:
            self.guardar_en_historial_personal(nombre_interesado, tema_capturado)
        
        print(f"📚 TEMA CAPTURADO: {titulo_tema} -> {origen}")
        return True
    
    def guardar_en_sesion_actual(self, tema):
        try:
            sesion_actual = []
            if os.path.exists(self.archivo_sesion):
                with open(self.archivo_sesion, 'r', encoding='utf-8') as f:
                    sesion_actual = json.load(f)
            
            sesion_actual = [t for t in sesion_actual if t.get('titulo', '') != tema['titulo']]
            sesion_actual.append(tema)
            sesion_actual = sesion_actual[-20:]
            
            with open(self.archivo_sesion, 'w', encoding='utf-8') as f:
                json.dump(sesion_actual, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error guardando en sesión: {e}")
            return False
    
    def guardar_en_historial_personal(self, nombre_interesado, tema):
        try:
            nombre_archivo = self.normalizar_nombre_archivo(nombre_interesado)
            archivo_personal = os.path.join(self.directorio_historiales, f"{nombre_archivo}.json")
            
            historial_personal = []
            if os.path.exists(archivo_personal):
                with open(archivo_personal, 'r', encoding='utf-8') as f:
                    historial_personal = json.load(f)
            
            historial_personal = [t for t in historial_personal if t.get('titulo', '') != tema['titulo']]
            historial_personal.append(tema)
            
            with open(archivo_personal, 'w', encoding='utf-8') as f:
                json.dump(historial_personal, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Error guardando en historial personal: {e}")
            return False
    
    def obtener_temas_sesion_actual(self):
        try:
            if os.path.exists(self.archivo_sesion):
                with open(self.archivo_sesion, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error cargando sesión actual: {e}")
            return []
    
    def obtener_temas_por_interesado(self, nombre_interesado):
        try:
            nombre_archivo = self.normalizar_nombre_archivo(nombre_interesado)
            archivo_personal = os.path.join(self.directorio_historiales, f"{nombre_archivo}.json")
            
            if os.path.exists(archivo_personal):
                with open(archivo_personal, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error cargando historial de {nombre_interesado}: {e}")
            return []
    
    def establecer_interesado_actual(self, nombre_interesado):
        try:
            config = {'interesado_actual': nombre_interesado, 'timestamp': datetime.datetime.now().isoformat()}
            with open("interesado_actual.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"👤 Interesado actual establecido: {nombre_interesado}")
            return True
        except Exception as e:
            print(f"❌ Error estableciendo interesado actual: {e}")
            return False
    
    def obtener_interesado_actual(self):
        try:
            if os.path.exists("interesado_actual.json"):
                with open("interesado_actual.json", 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return config.get('interesado_actual', None)
            return None
        except Exception as e:
            print(f"❌ Error obteniendo interesado actual: {e}")
            return None
    
    def generar_mensaje_completo_con_respuestas(self, nombre_interesado, idioma='es'):
        temas = self.obtener_temas_por_interesado(nombre_interesado)
        
        if not temas:
            return self.mensaje_sin_temas(nombre_interesado, idioma)
        
        mensaje_partes = []
        
        saludo = f"Hola {nombre_interesado}," if idioma == 'es' else f"Hello {nombre_interesado},"
        mensaje_partes.append(saludo)
        mensaje_partes.append("")
        
        intro = "Te envío un resumen de los temas bíblicos que hemos tratado:" if idioma == 'es' else "I'm sending you a summary of the biblical topics we have covered:"
        mensaje_partes.append(intro)
        mensaje_partes.append("")
        
        for i, tema in enumerate(temas, 1):
            titulo = tema.get('titulo', 'Tema sin título')
            respuesta = tema.get('respuesta', 'Sin respuesta disponible')
            
            mensaje_partes.append(f"{i}. {titulo}")
            mensaje_partes.append(f"   {respuesta}")
            mensaje_partes.append("")
        
        recursos = "📖 Recursos adicionales:" if idioma == 'es' else "📖 Additional resources:"
        jw_link = "• JW Library: https://www.jw.org/es/biblioteca-en-linea/" if idioma == 'es' else "• JW Library: https://www.jw.org/en/online-library/"
        curso_link = "• Curso bíblico gratuito: https://www.jw.org/es/estudio-biblico/" if idioma == 'es' else "• Free Bible course: https://www.jw.org/en/bible-study/"
        
        mensaje_partes.extend([recursos, jw_link, curso_link, ""])
        
        despedida = "Espero que esta información te sea útil para tu estudio personal.\nSi tienes alguna pregunta, no dudes en contactarme.\n\n¡Que tengas un excelente día!" if idioma == 'es' else "I hope this information is useful for your personal study.\nIf you have any questions, don't hesitate to contact me.\n\nHave a great day!"
        mensaje_partes.append(despedida)
        mensaje_partes.append("")
        mensaje_partes.append("Enviado desde Preaching Assistant" if idioma == 'es' else "Sent from Preaching Assistant")
        
        return '\n'.join(mensaje_partes)
    
    def mensaje_sin_temas(self, nombre_interesado, idioma='es'):
        if idioma == 'es':
            return f"""Hola {nombre_interesado},

Espero que te encuentres bien.

📖 Recursos para tu estudio bíblico:
• JW Library: https://www.jw.org/es/biblioteca-en-linea/
• Curso bíblico gratuito: https://www.jw.org/es/estudio-biblico/

Si tienes alguna pregunta bíblica, no dudes en contactarme.

¡Que tengas un excelente día!

Enviado desde Preaching Assistant"""
        else:
            return f"""Hello {nombre_interesado},

I hope you are doing well.

📖 Resources for your Bible study:
• JW Library: https://www.jw.org/en/online-library/
• Free Bible course: https://www.jw.org/en/bible-study/

If you have any Bible questions, don't hesitate to contact me.

Have a great day!

Sent from Preaching Assistant"""
    
    def limpiar_sesion_actual(self):
        try:
            if os.path.exists(self.archivo_sesion):
                os.remove(self.archivo_sesion)
            print("🧹 Sesión actual limpiada")
            return True
        except Exception as e:
            print(f"❌ Error limpiando sesión: {e}")
            return False
    
    @staticmethod
    def normalizar_nombre_archivo(nombre):
        return nombre.strip().lower().replace(' ', '_').replace('.', '').replace(',', '')

gestor_temas = GestorTemas()

def capturar_tema_desde_boton(titulo_tema, respuesta_completa, origen):
    nombre_interesado = gestor_temas.obtener_interesado_actual()
    return gestor_temas.capturar_tema_seleccionado(titulo_tema, respuesta_completa, origen, nombre_interesado)

def establecer_interesado_para_captura(nombre):
    return gestor_temas.establecer_interesado_actual(nombre)

def obtener_mensaje_completo_para_envio(nombre_interesado, idioma='es'):
    return gestor_temas.generar_mensaje_completo_con_respuestas(nombre_interesado, idioma)