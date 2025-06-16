from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import TPresupuestos

router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_presupuestos(db: Session = Depends(get_db)):
    return db.query(TPresupuestos).all()

@router.get("/{presupuesto_id}")
def obtener_presupuesto(presupuesto_id: int, db: Session = Depends(get_db)):
    return db.query(TPresupuestos).filter(TPresupuestos.id_presupuesto == presupuesto_id).first()
