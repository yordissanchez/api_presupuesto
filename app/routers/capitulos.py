from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import TCapitulos

router = APIRouter(prefix="/capitulos", tags=["Capítulos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_capitulos(db: Session = Depends(get_db)):
    return db.query(TCapitulos).all()

@router.get("/{capitulo_id}")
def obtener_capitulo(capitulo_id: int, db: Session = Depends(get_db)):
    return db.query(TCapitulos).filter(TCapitulos.id_capitulo == capitulo_id).first()
