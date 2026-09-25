import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# El GPS real para PyInstaller / Flet Pack
if getattr(sys, 'frozen', False):
    # Si está corriendo el .exe compilado, usa la ruta del ejecutable
    carpeta_actual = os.path.dirname(sys.executable)
else:
    # Si lo corrés vos desde tu editor de código
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))

ruta_db = os.path.join(carpeta_actual, "clinica.db")

engine = create_engine(f"sqlite:///{ruta_db}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
