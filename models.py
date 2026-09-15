from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Insumo(Base):
    __tablename__ = "insumos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    stock_inicial = Column(Integer, default=0)

    # Relacion para ver todos los movimientos de este insumo
    movimientos = relationship("Movimiento", back_populates="insumo")

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now)
    tipo = Column(String, nullable=False) # Puede ser "INGRESO" o "EGRESO"
    cantidad = Column(Integer, nullable=False)
    paciente = Column(String, nullable=True)     # Solo si es egreso
    responsable = Column(String, nullable=False) # Quien retira/ingresa
    
    insumo_id = Column(Integer, ForeignKey("insumos.id"))
    
    # Relacion inversa
    insumo = relationship("Insumo", back_populates="movimientos")
