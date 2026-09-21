from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Empleado(Base):
    __tablename__ = 'empleados'
    id = Column(Integer, primary_key=True, index=True)
    # unique=True evita que carguen a la misma persona dos veces
    nombre = Column(String, unique=True, index=True)

class Insumo(Base):
    __tablename__ = 'insumos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    stock_inicial = Column(Integer, default=0)
    movimientos = relationship("Movimiento", back_populates="insumo")

class Movimiento(Base):
    __tablename__ = 'movimientos'
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now)
    tipo = Column(String)  # "INGRESO" o "EGRESO"
    cantidad = Column(Integer)
    paciente = Column(String, default="-")
    responsable = Column(String)  # Acá guardaremos el nombre exacto elegido de la lista
    insumo_id = Column(Integer, ForeignKey("insumos.id"))
    insumo = relationship("Insumo", back_populates="movimientos")