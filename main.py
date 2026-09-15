import flet as ft
from database import engine, Base

# ESTO ES MAGIA: Crea el archivo .db y todas las tablas automáticamente
Base.metadata.create_all(bind=engine)

def main(page: ft.Page):
    # Configuracion de la ventana
    page.title = "Gestor de Stock - Clínica"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 700
    page.padding = 30

    # Elementos visuales iniciales
    titulo = ft.Text("Inventario: Mama Punch", size=32, weight=ft.FontWeight.BOLD)
    subtitulo = ft.Text("El motor de base de datos está conectado y funcionando.", color=ft.colors.GREEN_700)

    # Agregamos los elementos a la pantalla
    page.add(
        ft.Column([
            titulo,
            subtitulo,
            ft.Divider(height=40),
            ft.Text("Acá va a ir la tabla dinámica con el stock real...")
        ])
    )

# Levanta la aplicacion como un programa de escritorio
ft.app(target=main)
