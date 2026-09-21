import flet as ft
from database import engine, Base

from views.dashboard import vista_dashboard
from views.egresos import vista_egresos
from views.ingresos import vista_ingresos
from views.nuevos_insumos import vista_nuevos_insumos
from views.historial import vista_historial
from views.empleados import vista_empleados

# Inicializamos la base de datos
Base.metadata.create_all(bind=engine)

def main(page: ft.Page):
    page.title = "Gestión de Inventario"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # --- DISEÑO CLÍNICA PRIVADA (Sobrio y Corporativo) ---
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap"}
    page.theme = ft.Theme(font_family="Roboto", color_scheme_seed="#12233A") 
    
    page.bgcolor = "#ECEFF1" 
    page.window_width = 1200
    page.window_height = 800
    page.padding = 0

    # Barra superior corregida (sin el letter_spacing que causaba el error)
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.LOCAL_HOSPITAL_OUTLINED, color=ft.colors.WHITE70, size=26),
        leading_width=60,
        title=ft.Text("GESTIÓN DE INVENTARIO", color=ft.colors.WHITE, weight=ft.FontWeight.W_500, size=16),
        bgcolor="#12233A", 
        elevation=2, 
    )

    contenedor_principal = ft.Container(
        expand=True,
        padding=40,
        bgcolor=ft.colors.WHITE,
        border_radius=ft.border_radius.only(top_left=15), 
        shadow=ft.BoxShadow(
            spread_radius=0, 
            blur_radius=10, 
            color=ft.colors.with_opacity(0.05, ft.colors.BLACK)
        ),
        content=vista_dashboard()
    )

    def cambiar_pantalla(e):
        indice = e.control.selected_index
        if indice == 0:
            contenedor_principal.content = vista_dashboard()
        elif indice == 1:
            contenedor_principal.content = vista_egresos(page)
        elif indice == 2:
            contenedor_principal.content = vista_ingresos(page)
        elif indice == 3:
            contenedor_principal.content = vista_nuevos_insumos(page)
        elif indice == 4:
            contenedor_principal.content = vista_historial()
        elif indice == 5:
            contenedor_principal.content = vista_empleados(page)
        page.update()

    menu_lateral = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        bgcolor="#ECEFF1", 
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.DASHBOARD_OUTLINED, selected_icon=ft.icons.DASHBOARD, label="Resumen"),
            ft.NavigationRailDestination(icon=ft.icons.PERSON_REMOVE_OUTLINED, selected_icon=ft.icons.PERSON_REMOVE, label="Egresos"),
            ft.NavigationRailDestination(icon=ft.icons.ADD_SHOPPING_CART_OUTLINED, selected_icon=ft.icons.ADD_SHOPPING_CART, label="Ingresos"),
            ft.NavigationRailDestination(icon=ft.icons.LIBRARY_ADD_OUTLINED, selected_icon=ft.icons.LIBRARY_ADD, label="Catálogo"),
            ft.NavigationRailDestination(icon=ft.icons.HISTORY_OUTLINED, selected_icon=ft.icons.HISTORY, label="Historial"),
            ft.NavigationRailDestination(icon=ft.icons.BADGE_OUTLINED, selected_icon=ft.icons.BADGE, label="Personal"),
        ],
        on_change=cambiar_pantalla,
    )

    layout = ft.Row([menu_lateral, contenedor_principal], expand=True)
    page.add(layout)

ft.app(target=main)