from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import TObras

router = APIRouter(prefix="/obras", tags=["Obras"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_obras(db: Session = Depends(get_db)):
    return db.query(TObras).all()

@router.get("/{obra_id}")
def obtener_obra(obra_id: int, db: Session = Depends(get_db)):
    return db.query(TObras).filter(TObras.id_obra == obra_id).first()
