import flet as ft
from database import SessionLocal
from models import Insumo
from controllers import registrar_movimiento, obtener_stock_actual

def vista_egresos(page: ft.Page):
    # 1. Buscamos los insumos para armar la lista desplegable
    db = SessionLocal()
    insumos_db = db.query(Insumo).all()
    db.close()

    # Si todavía no hay insumos, mostramos un mensaje
    if not insumos_db:
        return ft.Text("Primero debés registrar insumos en el sistema.", color=ft.colors.RED_500)

    # Creamos las opciones visuales del desplegable
    opciones_insumos = [ft.dropdown.Option(key=str(i.id), text=i.nombre) for i in insumos_db]

    # 2. Cajas de texto y selectores (UI)
    dropdown_insumo = ft.Dropdown(label="Seleccionar Artículo", options=opciones_insumos, width=300)
    input_cantidad = ft.TextField(label="Cantidad usada", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    input_paciente = ft.TextField(label="Nombre del Paciente", width=300)
    input_responsable = ft.TextField(label="Responsable (Ej: Valentina, Maru)", width=300)
    
    texto_resultado = ft.Text(color=ft.colors.GREEN_700, weight=ft.FontWeight.BOLD)

    # 3. Lógica del botón de guardar
    def guardar_consumo(e):
        # Validamos que no dejen campos clave en blanco
        if not dropdown_insumo.value or not input_cantidad.value or not input_responsable.value:
            texto_resultado.value = "⚠️ Error: Faltan completar datos obligatorios."
            texto_resultado.color = ft.colors.RED_700
            page.update()
            return
        
        insumo_id = int(dropdown_insumo.value)
        cantidad = int(input_cantidad.value)
        paciente = input_paciente.value
        responsable = input_responsable.value

        db = SessionLocal()
        stock_actual = obtener_stock_actual(db, insumo_id)
        
        # Validamos que no usen stock fantasma
        if cantidad > stock_actual:
            texto_resultado.value = f"❌ Error: No hay suficiente stock. Stock actual: {stock_actual}"
            texto_resultado.color = ft.colors.RED_700
            db.close()
            page.update()
            return

        # Grabamos la operación en la base de datos
        registrar_movimiento(
            db=db, 
            insumo_id=insumo_id, 
            tipo="EGRESO", 
            cantidad=cantidad, 
            responsable=responsable, 
            paciente=paciente
        )
        db.close()

        # Éxito y limpieza de los campos
        texto_resultado.value = "✅ ¡Consumo registrado con éxito y stock descontado!"
        texto_resultado.color = ft.colors.GREEN_700
        input_cantidad.value = ""
        input_paciente.value = ""
        page.update()

    # 4. El botón estético
    boton_guardar = ft.ElevatedButton(
        "Registrar Uso en Paciente", 
        on_click=guardar_consumo, 
        color=ft.colors.WHITE, 
        bgcolor=ft.colors.RED_700,
        height=45
    )

    # 5. Empaquetamos todo en una columna
    return ft.Column([
        ft.Text("Registrar Nuevo Consumo", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Completá los datos cada vez que se utilice material en consultorio.", color=ft.colors.GREY_500),
        ft.Divider(height=20),
        dropdown_insumo,
        input_cantidad,
        input_paciente,
        input_responsable,
        ft.Container(height=10),
        boton_guardar,
        texto_resultado
    ], spacing=10)
