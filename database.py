import os
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# El GPS definitivo: obliga a guardar la base de datos exactamente en esta carpeta
carpeta_actual = pathlib.Path(__file__).parent.absolute()
ruta_db = os.path.join(carpeta_actual, "clinica.db")

engine = create_engine(f"sqlite:///{ruta_db}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()