import flet as ft
from database import SessionLocal
from models import Insumo

def vista_nuevos_insumos(page: ft.Page):
    # Cajas de texto
    input_nombre = ft.TextField(label="Nombre del Artículo (Ej: Arpón 20x20)", width=300)
    # Por defecto arranca en 0, pero pueden ponerle el stock inicial que quieran
    input_stock = ft.TextField(label="Stock Inicial", width=150, keyboard_type=ft.KeyboardType.NUMBER, value="0")
    
    texto_resultado = ft.Text(weight=ft.FontWeight.BOLD)

    # Lógica para crear el artículo
    def guardar_insumo(e):
        if not input_nombre.value or not input_stock.value:
            texto_resultado.value = "⚠️ Error: Completá el nombre y el stock."
            texto_resultado.color = ft.colors.RED_700
            page.update()
            return

        # Limpiamos el texto y lo pasamos a mayúsculas para mantener orden
        nombre_insumo = input_nombre.value.strip().upper()
        stock_inicial = int(input_stock.value)

        db = SessionLocal()
        
        # Revisamos que no hayan cargado este insumo antes
        existe = db.query(Insumo).filter(Insumo.nombre == nombre_insumo).first()
        if existe:
            texto_resultado.value = "❌ Error: Este artículo ya existe en el sistema."
            texto_resultado.color = ft.colors.RED_700
        else:
            # Lo creamos y lo guardamos
            nuevo_insumo = Insumo(nombre=nombre_insumo, stock_inicial=stock_inicial)
            db.add(nuevo_insumo)
            db.commit()
            
            texto_resultado.value = f"✅ Artículo '{nombre_insumo}' creado con {stock_inicial} unidades."
            texto_resultado.color = ft.colors.GREEN_700
            
            # Limpiamos los campos para cargar otro
            input_nombre.value = ""
            input_stock.value = "0"
        
        db.close()
        page.update()

    # Botón estético (Violeta para diferenciarlo de ingresos/egresos)
    boton_guardar = ft.ElevatedButton(
        "Crear Nuevo Artículo", 
        on_click=guardar_insumo, 
        color=ft.colors.WHITE, 
        bgcolor=ft.colors.PURPLE_700,
        height=45
    )

    # Empaquetamos
    return ft.Column([
        ft.Text("Alta de Nuevos Artículos", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Registrá un insumo que no exista en la base de datos y su stock inicial.", color=ft.colors.GREY_500),
        ft.Divider(height=20),
        input_nombre,
        input_stock,
        ft.Container(height=10),
        boton_guardar,
        texto_resultado
    ], spacing=10)
