import flet as ft
from database import SessionLocal
from models import Empleado, Movimiento  # <-- Sumamos Movimiento para poder revisar el historial

def vista_empleados(page):
    nombre_input = ft.TextField(
        label="Nombre del Profesional", 
        prefix_icon=ft.icons.PERSON,
        border_radius=8,
        expand=True
    )
    
    tabla_empleados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight="bold")),
            ft.DataColumn(ft.Text("Nombre", weight="bold")),
            ft.DataColumn(ft.Text("Acciones", weight="bold")),
        ],
        rows=[]
    )

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

    def abrir_editar(emp_id, nombre_actual):
        input_editar = ft.TextField(value=nombre_actual, label="Nuevo Nombre", border_radius=8)
        
        def guardar_edicion(e):
            db = SessionLocal()
            try:
                emp = db.query(Empleado).filter(Empleado.id == emp_id).first()
                if emp and input_editar.value.strip():
                    emp.nombre = input_editar.value.strip().title()
                    db.commit()
                    mostrar_mensaje("Nombre actualizado correctamente.", ft.colors.GREEN_700, ft.icons.CHECK)
                    dialogo.open = False
                    cargar_datos()
            finally:
                db.close()
                page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Editar Profesional"),
            content=input_editar,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dialogo)),
                ft.ElevatedButton("Guardar", on_click=guardar_edicion, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE),
            ]
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    def abrir_eliminar(emp_id, nombre_actual):
        def confirmar_borrado(e):
            db = SessionLocal()
            try:
                # --- ESCUDO DE SEGURIDAD ---
                # Buscamos si el empleado tiene al menos un movimiento registrado
                tiene_movimientos = db.query(Movimiento).filter(Movimiento.responsable == nombre_actual).first()
                
                if tiene_movimientos:
                    mostrar_mensaje("Bloqueado: Esta persona tiene registros en el historial.", ft.colors.RED_700, ft.icons.BLOCK)
                    dialogo.open = False
                    return

                # Si pasa el escudo, lo eliminamos
                emp = db.query(Empleado).filter(Empleado.id == emp_id).first()
                if emp:
                    db.delete(emp)
                    db.commit()
                    mostrar_mensaje("Profesional eliminado del sistema.", ft.colors.GREEN_700, ft.icons.DELETE_SWEEP)
                    dialogo.open = False
                    cargar_datos()
            finally:
                db.close()
                page.update()

        dialogo = ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.icons.WARNING, color=ft.colors.RED_600), ft.Text("Confirmar Borrado")]),
            content=ft.Text(f"¿Estás seguro que deseas eliminar a {nombre_actual}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dialogo)),
                ft.ElevatedButton("Eliminar", on_click=confirmar_borrado, bgcolor=ft.colors.RED_600, color=ft.colors.WHITE),
            ]
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    def cerrar_dialogo(dlg):
        dlg.open = False
        page.update()

    def cargar_datos():
        db = SessionLocal()
        try:
            empleados = db.query(Empleado).all()
            tabla_empleados.rows.clear()
            for emp in empleados:
                botones_accion = ft.Row([
                    ft.IconButton(icon=ft.icons.EDIT, icon_color=ft.colors.BLUE_600, tooltip="Editar", on_click=lambda e, id=emp.id, nom=emp.nombre: abrir_editar(id, nom)),
                    ft.IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.RED_500, tooltip="Eliminar", on_click=lambda e, id=emp.id, nom=emp.nombre: abrir_eliminar(id, nom)),
                ])
                
                tabla_empleados.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(emp.id))),
                        ft.DataCell(ft.Text(emp.nombre, weight="w500")),
                        ft.DataCell(botones_accion)
                    ])
                )
            page.update()
        finally:
            db.close()

    def guardar_empleado(e):
        if not nombre_input.value or not nombre_input.value.strip():
            mostrar_mensaje("El nombre no puede estar vacío.", ft.colors.RED_700, ft.icons.ERROR)
            return
        
        db = SessionLocal()
        try:
            nuevo_nombre = nombre_input.value.strip().title()
            if db.query(Empleado).filter(Empleado.nombre == nuevo_nombre).first():
                mostrar_mensaje("Este profesional ya está registrado.", ft.colors.ORANGE_700, ft.icons.WARNING)
                return

            db.add(Empleado(nombre=nuevo_nombre))
            db.commit()
            mostrar_mensaje("Personal registrado con éxito.", ft.colors.GREEN_700, ft.icons.CHECK_CIRCLE)
            nombre_input.value = ""
            cargar_datos() 
        finally:
            db.close()

    boton_guardar = ft.ElevatedButton(
        "Registrar", 
        on_click=guardar_empleado, 
        icon=ft.icons.ADD,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_800, padding=15)
    )

    cargar_datos()

    tarjeta_ingreso = ft.Card(
        elevation=2,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Alta de Profesional", size=18, weight="bold", color=ft.colors.BLUE_GREY_900),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Row([nombre_input, boton_guardar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )
    )

    tarjeta_lista = ft.Card(
        elevation=2,
        expand=True, 
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Directorio Activo", size=18, weight="bold", color=ft.colors.BLUE_GREY_900),
                ft.Divider(height=20, color=ft.colors.BLUE_GREY_100),
                ft.Column([tabla_empleados], scroll=ft.ScrollMode.ADAPTIVE, expand=True)
            ])
        )
    )

    return ft.Column([
        ft.Row([
            ft.Icon(ft.icons.BADGE, size=32, color=ft.colors.BLUE_800),
            ft.Text("Gestión de Personal", size=28, weight="bold", color=ft.colors.BLUE_GREY_900)
        ]),
        ft.Container(height=10),
        tarjeta_ingreso,
        tarjeta_lista
    ], expand=True)