import flet as ft
from database import engine, Base

# Importamos las 4 vistas que creamos
from views.dashboard import vista_dashboard
from views.egresos import vista_egresos
from views.ingresos import vista_ingresos
from views.nuevos_insumos import vista_nuevos_insumos

# Inicializamos la base de datos
Base.metadata.create_all(bind=engine)

def main(page: ft.Page):
    # Configuración de la ventana principal
    page.title = "Gestor de Stock - Clínica"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1100
    page.window_height = 700
    page.padding = 0 # Quitamos los márgenes para que el menú ocupe todo el borde

    # Este es el cuadro derecho donde va a ir cambiando el contenido.
    # Arranca mostrando la vista_dashboard() por defecto.
    contenedor_principal = ft.Container(
        expand=True,
        padding=30,
        content=vista_dashboard()
    )

    # La lógica para cambiar de pestaña
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
        page.update()

    # El menú lateral
    menu_lateral = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        group_alignment=-0.9, # Tira los botones hacia arriba
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.DASHBOARD_OUTLINED, selected_icon=ft.icons.DASHBOARD, label="Inventario"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PERSON_REMOVE_OUTLINED, selected_icon=ft.icons.PERSON_REMOVE, label="Consumos"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ADD_SHOPPING_CART_OUTLINED, selected_icon=ft.icons.ADD_SHOPPING_CART, label="Ingresos"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LIBRARY_ADD_OUTLINED, selected_icon=ft.icons.LIBRARY_ADD, label="Catálogo"
            ),
        ],
        on_change=cambiar_pantalla,
    )

    # Armamos la estructura final: Una fila con el menú a la izquierda y el contenedor a la derecha
    layout = ft.Row(
        [
            menu_lateral,
            ft.VerticalDivider(width=1),
            contenedor_principal
        ],
        expand=True,
    )

    page.add(layout)

# Le decimos a Flet que arranque la aplicación
ft.app(target=main)
