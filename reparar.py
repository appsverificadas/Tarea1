import os
import pathlib

# Buscamos la ruta exacta donde estás trabajando
carpeta_base = pathlib.Path(__file__).parent.absolute()
carpeta_views = os.path.join(carpeta_base, "views")

# Nos aseguramos de que la carpeta views exista
if not os.path.exists(carpeta_views):
    os.makedirs(carpeta_views)

# Este es el código de tu pantalla
codigo = """import flet as ft
from controllers import registrar_insumo
from database import SessionLocal

def vista_nuevos_insumos(page):
    nombre_input = ft.TextField(label="Nombre del artículo", width=300)
    stock_input = ft.TextField(label="Stock Inicial", width=150, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))

    def guardar_insumo(e):
        if not nombre_input.value or not stock_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, completá todos los campos", color=ft.colors.WHITE), bgcolor=ft.colors.RED_700)
            page.snack_bar.open = True
            page.update()
            return
        
        db = SessionLocal()
        try:
            registrar_insumo(db, nombre_input.value, int(stock_input.value))
            page.snack_bar = ft.SnackBar(ft.Text("¡Insumo agregado al catálogo con éxito!", color=ft.colors.WHITE), bgcolor=ft.colors.GREEN_700)
            page.snack_bar.open = True
            nombre_input.value = ""
            stock_input.value = ""
            page.update()
        except Exception as ex:
            print(f"Error: {ex}")
        finally:
            db.close()

    boton_guardar = ft.ElevatedButton(
        "Guardar en el Catálogo", 
        on_click=guardar_insumo, 
        icon=ft.icons.SAVE,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE_700
    )

    return ft.Column([
        ft.Text("Agregar Nuevo Artículo", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Cargá acá los insumos médicos que no existían en el Excel original.", color=ft.colors.GREY_500),
        ft.Container(padding=10),
        ft.Row([nombre_input, stock_input]),
        ft.Container(padding=5),
        boton_guardar
    ], scroll=ft.ScrollMode.ADAPTIVE)
"""

# Forzamos a Windows a crear el archivo exactamente donde va, sin extensiones fantasma
ruta_archivo = os.path.join(carpeta_views, "nuevos_insumos.py")
with open(ruta_archivo, "w", encoding="utf-8") as archivo:
    archivo.write(codigo)

# También creamos el archivo __init__.py que a veces Python necesita para leer carpetas
with open(os.path.join(carpeta_views, "__init__.py"), "w", encoding="utf-8") as archivo:
    archivo.write("")

print("✅ ¡Reparación completada! El archivo 'nuevos_insumos.py' se creó a la fuerza en el lugar correcto.")