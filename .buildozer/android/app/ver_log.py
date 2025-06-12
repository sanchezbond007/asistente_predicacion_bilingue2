import os

ruta_log = "/data/user/0/ru.iiec.pydroid3/app_HOME/.kivy/logs"

# Buscar los archivos de log ordenados por fecha
archivos_log = sorted(
    [f for f in os.listdir(ruta_log) if f.endswith(".txt")],
    reverse=True
)

if not archivos_log:
    print("❌ No se encontraron archivos de log.")
else:
    ultimo_log = archivos_log[0]
    ruta_completa = os.path.join(ruta_log, ultimo_log)
    print(f"📄 Mostrando log: {ultimo_log}\n")
    with open(ruta_completa, 'r', encoding='utf-8') as f:
        print(f.read())