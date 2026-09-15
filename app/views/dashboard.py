import flet as ft
from database import SessionLocal
from models import Insumo
from controllers import obtener_stock_actual

def vista_dashboard():
    # Abrimos una sesion de lectura con la base de datos local
    db = SessionLocal()
    
    # Traemos todos los insumos (agujas, punch, clips, etc.)
    insumos = db.query(Insumo).all()
    
    # Armamos las filas de la tabla dinamicamente
    filas = []
    for insumo in insumos:
        stock_real = obtener_stock_actual(db, insumo.id)
        
        # Alerta visual: si hay menos de 5 unidades, el numero se pone rojo
        color_texto = ft.colors.RED_700 if stock_real < 5 else ft.colors.BLACK
        
        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(insumo.id))),
                    ft.DataCell(ft.Text(insumo.nombre, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(str(stock_real), color=color_texto, weight=ft.FontWeight.BOLD)),
                ]
            )
        )
    
    db.close() # Cerramos la conexion por seguridad

    # Construimos la tabla estetica de Flet
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.W_900)),
            ft.DataColumn(ft.Text("Artículo", weight=ft.FontWeight.W_900)),
            ft.DataColumn(ft.Text("Stock Actual", color=ft.colors.BLUE_700, weight=ft.FontWeight.W_900)),
        ],
        rows=filas,
        border=ft.border.all(1, ft.colors.GREY_300),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_200),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_200),
    )
    
    # Empaquetamos todo en una columna scrolleable
    return ft.Column([
        ft.Text("Inventario en Tiempo Real", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("El stock se calcula automáticamente en base a ingresos y egresos.", color=ft.colors.GREY_500),
        ft.Container(content=tabla, padding=ft.padding.only(top=20))
    ], scroll=ft.ScrollMode.ADAPTIVE)
