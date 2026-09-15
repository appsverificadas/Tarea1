from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Crea un archivo fisico llamado "inventario.db" en la misma carpeta
DATABASE_URL = "sqlite:///inventario.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
