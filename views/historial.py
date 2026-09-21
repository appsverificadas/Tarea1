import flet as ft
from database import SessionLocal
from models import Movimiento, Insumo, Empleado
from datetime import datetime

def vista_historial():
    filtro_tipo = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option(key="Todos", text="Todos"),
            ft.dropdown.Option(key="INGRESO", text="Ingresos (Altas)"),
            ft.dropdown.Option(key="EGRESO", text="Egresos (Consumos)")
        ],
        value="Todos",
        expand=1,
        border_radius=8
    )
    
    filtro_insumo = ft.Dropdown(label="Filtrar por Insumo", expand=2, border_radius=8)
    filtro_responsable = ft.Dropdown(label="Filtrar por Responsable", expand=2, border_radius=8)

    tabla_historial = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha", weight="bold")),
            ft.DataColumn(ft.Text("Operación", weight="bold")),
            ft.DataColumn(ft.Text("Insumo", weight="bold")),
            ft.DataColumn(ft.Text("Cant.", weight="bold"), numeric=True),
            ft.DataColumn(ft.Text("Responsable", weight="bold")),
            ft.DataColumn(ft.Text("Paciente", weight="bold")),
        ],
        rows=[]
    )

    contenedor_tabla = ft.Column([tabla_historial], scroll=ft.ScrollMode.ADAPTIVE, expand=True)

    def cargar_filtros():
        db = SessionLocal()
        try:
            insumos = db.query(Insumo).all()
            opciones_insumo = [ft.dropdown.Option(key="Todos", text="Todos los insumos")]
            opciones_insumo.extend([ft.dropdown.Option(key=str(i.id), text=i.nombre) for i in insumos])
            filtro_insumo.options = opciones_insumo
            filtro_insumo.value = "Todos"

            empleados = db.query(Empleado).all()
            opciones_resp = [ft.dropdown.Option(key="Todos", text="Todos los responsables")]
            opciones_resp.extend([ft.dropdown.Option(key=e.nombre, text=e.nombre) for e in empleados])
            filtro_responsable.options = opciones_resp
            filtro_responsable.value = "Todos"
        finally:
            db.close()

    def aplicar_filtros(e=None):
        db = SessionLocal()
        try:
            query = db.query(Movimiento).order_by(Movimiento.fecha.desc())
            
            if filtro_tipo.value != "Todos":
                query = query.filter(Movimiento.tipo == filtro_tipo.value)
            
            if filtro_insumo.value != "Todos":
                query = query.filter(Movimiento.insumo_id == int(filtro_insumo.value))
            
            if filtro_responsable.value != "Todos":
                query = query.filter(Movimiento.responsable == filtro_responsable.value)
            
            movimientos = query.all()
            tabla_historial.rows.clear()
            
            for m in movimientos:
                # Código blindado para fechas
                if isinstance(m.fecha, datetime):
                    fecha_str = m.fecha.strftime("%d/%m/%Y %H:%M")
                else:
                    fecha_str = str(m.fecha)[:16] if m.fecha else "-"
                
                # Código blindado por si eliminan un insumo
                nombre_insumo = m.insumo.nombre if m.insumo else "Insumo Borrado"
                
                es_ingreso = (m.tipo == "INGRESO")
                color_texto = ft.colors.GREEN_700 if es_ingreso else ft.colors.RED_700
                icono = ft.icons.ARROW_CIRCLE_UP if es_ingreso else ft.icons.ARROW_CIRCLE_DOWN
                
                # ARREGLO DEL COLOR: Pasamos el color directo, compatible con Flet 0.23.2
                fondo_fila = ft.colors.GREEN_50 if es_ingreso else ft.colors.RED_50

                tabla_historial.rows.append(
                    ft.DataRow(
                        color=fondo_fila,
                        cells=[
                            ft.DataCell(ft.Text(fecha_str)),
                            ft.DataCell(ft.Row([ft.Icon(icono, color=color_texto, size=18), ft.Text(m.tipo, color=color_texto, weight="bold")])),
                            ft.DataCell(ft.Text(nombre_insumo, weight="w500")),
                            ft.DataCell(ft.Text(str(m.cantidad), size=16)),
                            ft.DataCell(ft.Text(m.responsable)),
                            ft.DataCell(ft.Text(m.paciente)),
                        ]
                    )
                )
            
            if e:
                tabla_historial.update()
        finally:
            db.close()

    filtro_tipo.on_change = aplicar_filtros
    filtro_insumo.on_change = aplicar_filtros
    filtro_responsable.on_change = aplicar_filtros

    cargar_filtros()
    aplicar_filtros()

    tarjeta_filtros = ft.Card(
        elevation=2,
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Filtros de Búsqueda", weight="bold", color=ft.colors.BLUE_GREY_700),
                ft.Row([filtro_tipo, filtro_insumo, filtro_responsable])
            ])
        )
    )

    tarjeta_tabla = ft.Card(
        elevation=4,
        expand=True,
        content=ft.Container(
            padding=10,
            content=contenedor_tabla
        )
    )

    return ft.Column([
        ft.Row([
            ft.Icon(ft.icons.HISTORY, size=40, color=ft.colors.BLUE_GREY_800),
            ft.Text("Historial de Movimientos", size=32, weight="bold")
        ], alignment=ft.MainAxisAlignment.START),
        ft.Container(height=10),
        tarjeta_filtros,
        ft.Container(height=10),
        tarjeta_tabla
    ], expand=True)