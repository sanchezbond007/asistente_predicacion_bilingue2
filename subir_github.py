import os
import shutil
import subprocess

# CONFIGURACIÓN
carpeta_origen = "/storage/emulated/0/prueba_asistente_predicacion_bilingüe"
repositorio_local = "/storage/emulated/0/asistente_predicacion_bilingue2"
repositorio_git = "https://github.com/sanchezbond007/asistente_predicacion_bilingue2.git"

# Paso 1: Clonar si no existe
if not os.path.exists(repositorio_local):
    print("🔽 Clonando repositorio...")
    subprocess.run(["git", "clone", repositorio_git, repositorio_local])

# Paso 2: Copiar archivos desde la carpeta de origen
print("📂 Copiando archivos...")
for item in os.listdir(carpeta_origen):
    src = os.path.join(carpeta_origen, item)
    dst = os.path.join(repositorio_local, item)
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

# Paso 3: Subir a GitHub
print("📤 Subiendo a GitHub...")
os.chdir(repositorio_local)
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "🚀 Subida automática desde Pydroid 3"])
subprocess.run(["git", "push", "origin", "main"])

print("✅ ¡Proceso completado!")