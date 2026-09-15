from sqlalchemy.orm import Session
from models import Insumo, Movimiento

def obtener_stock_actual(db: Session, insumo_id: int):
    # Buscamos el insumo en la base de datos
    insumo = db.query(Insumo).filter(Insumo.id == insumo_id).first()
    if not insumo:
        return 0
    
    # Calculamos todos los ingresos y egresos
    total_ingresos = sum(mov.cantidad for mov in insumo.movimientos if mov.tipo == "INGRESO")
    total_egresos = sum(mov.cantidad for mov in insumo.movimientos if mov.tipo == "EGRESO")
    
    # La formula de oro del inventario
    stock_real = insumo.stock_inicial + total_ingresos - total_egresos
    
    return stock_real

def registrar_movimiento(db: Session, insumo_id: int, tipo: str, cantidad: int, responsable: str, paciente: str = None):
    # Creamos el registro de la transaccion
    nuevo_movimiento = Movimiento(
        insumo_id=insumo_id,
        tipo=tipo.upper(),
        cantidad=cantidad,
        responsable=responsable,
        paciente=paciente
    )
    db.add(nuevo_movimiento)
    db.commit()
    db.refresh(nuevo_movimiento)
    return nuevo_movimiento
