import flet as ft
from database import SessionLocal
from models import Insumo
from controllers import registrar_movimiento, obtener_stock_actual

def vista_ingresos(page: ft.Page):
    # 1. Traemos los insumos para el menú
    db = SessionLocal()
    insumos_db = db.query(Insumo).all()
    db.close()

    if not insumos_db:
        return ft.Text("Primero debés registrar insumos en el sistema.", color=ft.colors.RED_500)

    opciones_insumos = [ft.dropdown.Option(key=str(i.id), text=i.nombre) for i in insumos_db]

    # 2. Cajas de texto (UI)
    dropdown_insumo = ft.Dropdown(label="Artículo Comprado", options=opciones_insumos, width=300)
    input_cantidad = ft.TextField(label="Cantidad que ingresa", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    input_responsable = ft.TextField(label="Responsable de la carga", width=300)
    
    texto_resultado = ft.Text(color=ft.colors.GREEN_700, weight=ft.FontWeight.BOLD)

    # 3. Lógica para sumar stock
    def guardar_ingreso(e):
        # Validación básica
        if not dropdown_insumo.value or not input_cantidad.value or not input_responsable.value:
            texto_resultado.value = "⚠️ Error: Faltan completar datos."
            texto_resultado.color = ft.colors.RED_700
            page.update()
            return
        
        insumo_id = int(dropdown_insumo.value)
        cantidad = int(input_cantidad.value)
        responsable = input_responsable.value

        # Grabamos el ingreso
        db = SessionLocal()
        registrar_movimiento(
            db=db, 
            insumo_id=insumo_id, 
            tipo="INGRESO", 
            cantidad=cantidad, 
            responsable=responsable
        )
        
        # Calculamos cómo quedó el stock para mostrarlo en el mensaje
        stock_nuevo = obtener_stock_actual(db, insumo_id)
        db.close()

        texto_resultado.value = f"✅ ¡Mercadería ingresada! El stock actual subió a: {stock_nuevo}"
        texto_resultado.color = ft.colors.GREEN_700
        input_cantidad.value = ""
        page.update()

    # 4. Botón estético (Azul para diferenciarlo del rojo de Egresos)
    boton_guardar = ft.ElevatedButton(
        "Cargar Mercadería", 
        on_click=guardar_ingreso, 
        color=ft.colors.WHITE, 
        bgcolor=ft.colors.BLUE_700,
        height=45
    )

    # 5. Empaquetamos
    return ft.Column([
        ft.Text("Ingreso de Mercadería", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Registrá acá las compras o reposiciones de insumos.", color=ft.colors.GREY_500),
        ft.Divider(height=20),
        dropdown_insumo,
        input_cantidad,
        input_responsable,
        ft.Container(height=10),
        boton_guardar,
        texto_resultado
    ], spacing=10)
