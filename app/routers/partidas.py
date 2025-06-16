from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import TPartidas

router = APIRouter(prefix="/partidas", tags=["Partidas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_partidas(db: Session = Depends(get_db)):
    return db.query(TPartidas).all()

@router.get("/{partida_id}")
def obtener_partida(partida_id: int, db: Session = Depends(get_db)):
    return db.query(TPartidas).filter(TPartidas.id_partida == partida_id).first()
