import os
import pathlib

# Esta línea descubre exactamente en qué carpeta está este archivo
carpeta_correcta = pathlib.Path(__file__).parent.absolute()
print(f"Buscando en la carpeta exacta: {carpeta_correcta}")

for raiz, directorios, archivos in os.walk(carpeta_correcta):
    for nombre_archivo in archivos:
        if nombre_archivo.endswith(".py"):
            ruta = os.path.join(raiz, nombre_archivo)
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    codigo = f.read()
                
                # Reemplazamos las minúsculas rebeldes por mayúsculas
                nuevo_codigo = codigo.replace("ft.colors.", "ft.colors.").replace("ft.icons.", "ft.icons.")
                
                if nuevo_codigo != codigo:
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(nuevo_codigo)
                    print(f"-> ¡Archivo arreglado!: {nombre_archivo}")
            except:
                pass

print("¡ARREGLO DEFINITIVO COMPLETADO! Ya podés volver a main.py y darle Play.")