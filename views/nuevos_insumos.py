import flet as ft
from database import SessionLocal
from models import Insumo, Movimiento # <-- Sumamos Movimiento para el escudo

def vista_nuevos_insumos(page):
    nombre_input = ft.TextField(
        label="Nombre del Nuevo Insumo", 
        prefix_icon=ft.icons.VACCINES,
        border_radius=8,
        expand=True
    )
    
    tabla_insumos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight="bold")),
            ft.DataColumn(ft.Text("Nombre del Insumo", weight="bold")),
            ft.DataColumn(ft.Text("Stock Inicial", weight="bold")),
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

    def abrir_editar(insumo_id, nombre_actual):
        input_editar = ft.TextField(value=nombre_actual, label="Corregir Nombre", border_radius=8)
        
        def guardar_edicion(e):
            db = SessionLocal()
            try:
                ins = db.query(Insumo).filter(Insumo.id == insumo_id).first()
                if ins and input_editar.value.strip():
                    ins.nombre = input_editar.value.strip().title()
                    db.commit()
                    mostrar_mensaje("Nombre del insumo corregido.", ft.colors.GREEN_700, ft.icons.CHECK)
                    dialogo.open = False
                    cargar_datos()
            finally:
                db.close()
                page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Editar Insumo"),
            content=input_editar,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dialogo)),
                ft.ElevatedButton("Guardar", on_click=guardar_edicion, bgcolor="#0F172A", color=ft.colors.WHITE),
            ]
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    def abrir_eliminar(insumo_id, nombre_actual):
        def confirmar_borrado(e):
            db = SessionLocal()
            try:
                # --- ESCUDO DE SEGURIDAD ---
                # Buscamos si el insumo ya tiene un movimiento en el historial
                tiene_movimientos = db.query(Movimiento).filter(Movimiento.insumo_id == insumo_id).first()
                
                if tiene_movimientos:
                    mostrar_mensaje("Bloqueado: El insumo ya tiene consumos históricos.", ft.colors.RED_700, ft.icons.BLOCK)
                    dialogo.open = False
                    return

                # Si pasa el escudo, lo eliminamos
                ins = db.query(Insumo).filter(Insumo.id == insumo_id).first()
                if ins:
                    db.delete(ins)
                    db.commit()
                    mostrar_mensaje("Insumo eliminado del catálogo.", ft.colors.GREEN_700, ft.icons.DELETE_SWEEP)
                    dialogo.open = False
                    cargar_datos()
            finally:
                db.close()
                page.update()

        dialogo = ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.icons.WARNING, color=ft.colors.RED_600), ft.Text("Confirmar Borrado")]),
            content=ft.Text(f"¿Deseas eliminar '{nombre_actual}' del catálogo definitivo?"),
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
            insumos = db.query(Insumo).all()
            tabla_insumos.rows.clear()
            for ins in insumos:
                botones_accion = ft.Row([
                    ft.IconButton(icon=ft.icons.EDIT, icon_color=ft.colors.BLUE_600, tooltip="Editar Nombre", on_click=lambda e, id=ins.id, nom=ins.nombre: abrir_editar(id, nom)),
                    ft.IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.RED_500, tooltip="Eliminar", on_click=lambda e, id=ins.id, nom=ins.nombre: abrir_eliminar(id, nom)),
                ])
                
                tabla_insumos.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(ins.id))),
                        ft.DataCell(ft.Text(ins.nombre, weight="w500")),
                        ft.DataCell(ft.Text(str(ins.stock_inicial))),
                        ft.DataCell(botones_accion)
                    ])
                )
            page.update()
        finally:
            db.close()

    def guardar_insumo(e):
        if not nombre_input.value or not nombre_input.value.strip():
            mostrar_mensaje("El nombre no puede estar vacío.", ft.colors.RED_700, ft.icons.ERROR)
            return
        
        db = SessionLocal()
        try:
            nuevo_nombre = nombre_input.value.strip().title()
            if db.query(Insumo).filter(Insumo.nombre == nuevo_nombre).first():
                mostrar_mensaje("Este insumo ya existe.", ft.colors.ORANGE_700, ft.icons.WARNING)
                return

            db.add(Insumo(nombre=nuevo_nombre, stock_inicial=0))
            db.commit()
            mostrar_mensaje("Insumo registrado con éxito.", ft.colors.GREEN_700, ft.icons.CHECK_CIRCLE)
            nombre_input.value = ""
            cargar_datos() 
        finally:
            db.close()

    boton_guardar = ft.ElevatedButton(
        "Añadir Insumo", 
        on_click=guardar_insumo, 
        icon=ft.icons.ADD,
        style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor="#0F172A", padding=15)
    )

    cargar_datos()

    tarjeta_ingreso = ft.Card(
        elevation=1,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Ingresar Nuevo Insumo", size=18, weight="bold", color="#0F172A"),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Row([nombre_input, boton_guardar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )
    )

    tarjeta_lista = ft.Card(
        elevation=1,
        expand=True, 
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Catálogo Actual", size=18, weight="bold", color="#0F172A"),
                ft.Divider(height=20, color=ft.colors.BLUE_GREY_100),
                ft.Column([tabla_insumos], scroll=ft.ScrollMode.ADAPTIVE, expand=True)
            ])
        )
    )

    return ft.Column([
        ft.Row([
            ft.Icon(ft.icons.LIBRARY_ADD, size=32, color="#0F172A"),
            ft.Text("Catálogo de Insumos", size=28, weight="bold", color="#0F172A")
        ]),
        ft.Container(height=10),
        tarjeta_ingreso,
        tarjeta_lista
    ], expand=True)