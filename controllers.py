from models import Insumo, Movimiento
from datetime import datetime

def obtener_stock_actual(db, insumo_id):
    insumo = db.query(Insumo).filter(Insumo.id == insumo_id).first()
    if not insumo:
        return 0
    
    stock_calculado = insumo.stock_inicial
    movimientos = db.query(Movimiento).filter(Movimiento.insumo_id == insumo_id).all()
    
    for movimiento in movimientos:
        if movimiento.tipo == "INGRESO":
            stock_calculado += movimiento.cantidad
        elif movimiento.tipo == "EGRESO":
            stock_calculado -= movimiento.cantidad
            
    return stock_calculado

def registrar_movimiento(db, insumo_id, tipo, cantidad, paciente, responsable):
    nuevo_movimiento = Movimiento(
        fecha=datetime.now(),
        tipo=tipo,
        cantidad=cantidad,
        paciente=paciente if paciente else "",
        responsable=responsable if responsable else "No registrado",
        insumo_id=insumo_id
    )
    db.add(nuevo_movimiento)
    db.commit()

def registrar_insumo(db, nombre, stock_inicial):
    nuevo_insumo = Insumo(nombre=nombre, stock_inicial=stock_inicial)
    db.add(nuevo_insumo)
    db.commit()