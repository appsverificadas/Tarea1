import flet as ft
from database import SessionLocal
from models import Insumo, Movimiento, Empleado
from datetime import datetime

def vista_egresos(page):
    # --- 1. Elementos de Interfaz ---
    dropdown_insumo = ft.Dropdown(
        label="Seleccionar Insumo", 
        prefix_icon=ft.icons.MEDICAL_SERVICES,
        border_radius=10,
        expand=True
    )
    
    dropdown_empleado = ft.Dropdown(
        label="Profesional Responsable", 
        prefix_icon=ft.icons.BADGE,
        border_radius=10,
        expand=True
    )
    
    cantidad_input = ft.TextField(
        label="Cantidad a retirar", 
        prefix_icon=ft.icons.NUMBERS,
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        width=200
    )
    
    paciente_input = ft.TextField(
        label="Nombre del Paciente (Opcional)", 
        prefix_icon=ft.icons.PERSON_OUTLINE,
        border_radius=10,
        expand=True
    )

    # --- 2. Lógica y Validaciones ---
    def mostrar_mensaje(texto, color, icono):
        page.snack_bar = ft.SnackBar(
            content=ft.Row([ft.Icon(icono, color=ft.colors.WHITE), ft.Text(texto, color=ft.colors.WHITE)]),
            bgcolor=color,
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=20,
            shape=ft.RoundedRectangleBorder(radius=8)
        )
        page.snack_bar.open = True
        page.update()

    def cargar_listas():
        db = SessionLocal()
        try:
            # Llenar dropdown de insumos
            insumos = db.query(Insumo).all()
            dropdown_insumo.options = [ft.dropdown.Option(key=str(i.id), text=i.nombre) for i in insumos]
            
            # Llenar dropdown de empleados
            empleados = db.query(Empleado).all()
            dropdown_empleado.options = [ft.dropdown.Option(key=e.nombre, text=e.nombre) for e in empleados]
        finally:
            db.close()

    def registrar_egreso(e):
        # Validación 1: Campos incompletos
        if not dropdown_insumo.value or not dropdown_empleado.value or not cantidad_input.value:
            mostrar_mensaje("Faltan completar campos obligatorios.", ft.colors.RED_700, ft.icons.ERROR)
            return
        
        # Validación 2: Cantidad no válida
        try:
            cantidad = int(cantidad_input.value)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            mostrar_mensaje("La cantidad debe ser un número mayor a cero.", ft.colors.RED_700, ft.icons.ERROR)
            return

        db = SessionLocal()
        try:
            insumo_id = int(dropdown_insumo.value)
            insumo_db = db.query(Insumo).filter(Insumo.id == insumo_id).first()
            
            # Validación 3: Lógica de Stock (Calculamos el stock actual sumando y restando movimientos)
            total_ingresos = sum(m.cantidad for m in insumo_db.movimientos if m.tipo == "INGRESO")
            total_egresos = sum(m.cantidad for m in insumo_db.movimientos if m.tipo == "EGRESO")
            stock_actual = insumo_db.stock_inicial + total_ingresos - total_egresos

            if cantidad > stock_actual:
                mostrar_mensaje(f"Stock insuficiente. Solo quedan {stock_actual} unidades.", ft.colors.ORANGE_700, ft.icons.WARNING)
                return

            # Si pasa todas las validaciones, guardamos
            nuevo_egreso = Movimiento(
                tipo="EGRESO",
                cantidad=cantidad,
                paciente=paciente_input.value.strip() if paciente_input.value else "-",
                responsable=dropdown_empleado.value, # Toma el nombre exacto de la lista
                insumo_id=insumo_id,
                fecha=datetime.now()
            )
            
            db.add(nuevo_egreso)
            db.commit()
            
            mostrar_mensaje("Egreso registrado correctamente.", ft.colors.GREEN_700, ft.icons.CHECK_CIRCLE)
            
            # Limpiar campos
            dropdown_insumo.value = None
            dropdown_empleado.value = None
            cantidad_input.value = ""
            paciente_input.value = ""
            page.update()

        except Exception as ex:
            db.rollback()
            mostrar_mensaje("Error crítico al guardar.", ft.colors.RED_900, ft.icons.DANGEROUS)
        finally:
            db.close()

    # Botón de acción principal
    boton_registrar = ft.ElevatedButton(
        "Registrar Egreso", 
        on_click=registrar_egreso, 
        icon=ft.icons.REMOVE_CIRCLE_OUTLINE,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.RED_600, # Rojo porque es un egreso (salida)
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=20
        )
    )

    # Inicializar listas antes de mostrar la pantalla
    cargar_listas()

    # --- 3. Maquetado Profesional ---
    tarjeta_formulario = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=30,
            content=ft.Column([
                ft.Text("Registrar Consumo de Material", size=20, weight="bold", color=ft.colors.BLUE_GREY_900),
                ft.Text("Seleccioná el insumo, el profesional a cargo y la cantidad utilizada.", color=ft.colors.GREY_600),
                ft.Divider(height=30, color=ft.colors.BLUE_GREY_100),
                
                ft.Row([dropdown_insumo, cantidad_input]),
                ft.Container(height=10),
                ft.Row([dropdown_empleado, paciente_input]),
                ft.Container(height=20),
                
                ft.Row([boton_registrar], alignment=ft.MainAxisAlignment.END)
            ])
        )
    )

    return ft.Column([
        ft.Row([
            ft.Icon(ft.icons.PERSON_REMOVE, size=40, color=ft.colors.RED_600),
            ft.Text("Salida de Insumos", size=32, weight="bold")
        ], alignment=ft.MainAxisAlignment.START),
        ft.Container(height=20),
        tarjeta_formulario
    ], expand=True)