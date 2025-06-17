from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import SessionLocal
from ..models import TObras

router = APIRouter(prefix="/obras", tags=["Obras"])

# Esquemas Pydantic para validación
class ObraBase(BaseModel):
    referencia: Optional[str] = None
    nombre: Optional[str] = None
    direccion: Optional[str] = None

class ObraCreate(ObraBase):
    referencia: str
    nombre: str
    direccion: str

class ObraUpdate(ObraBase):
    pass

class ObraResponse(ObraBase):
    id_obra: int
    
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# READ - Listar todas las obras
@router.get("/", response_model=list[ObraResponse])
def listar_obras(db: Session = Depends(get_db)):
    return db.query(TObras).all()

# READ - Obtener una obra específica
@router.get("/{obra_id}", response_model=ObraResponse)
def obtener_obra(obra_id: int, db: Session = Depends(get_db)):
    obra = db.query(TObras).filter(TObras.id_obra == obra_id).first()
    if not obra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Obra con ID {obra_id} no encontrada"
        )
    return obra

# CREATE - Crear nueva obra
@router.post("/", response_model=ObraResponse, status_code=status.HTTP_201_CREATED)
def crear_obra(obra: ObraCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe una obra con la misma referencia
    existing_obra = db.query(TObras).filter(TObras.referencia == obra.referencia).first()
    if existing_obra:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una obra con la referencia '{obra.referencia}'"
        )
    
    db_obra = TObras(
        referencia=obra.referencia,
        nombre=obra.nombre,
        direccion=obra.direccion
    )
    
    db.add(db_obra)
    db.commit()
    db.refresh(db_obra)
    
    return db_obra

# UPDATE - Actualizar obra existente
@router.put("/{obra_id}", response_model=ObraResponse)
def actualizar_obra(obra_id: int, obra_update: ObraUpdate, db: Session = Depends(get_db)):
    # Buscar la obra existente
    db_obra = db.query(TObras).filter(TObras.id_obra == obra_id).first()
    if not db_obra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Obra con ID {obra_id} no encontrada"
        )
    
    # Actualizar solo los campos que se envían
    update_data = obra_update.dict(exclude_unset=True)
    
    # Si se está actualizando la referencia, verificar que no exista otra obra con la misma
    if "referencia" in update_data:
        existing_obra = db.query(TObras).filter(
            TObras.referencia == update_data["referencia"],
            TObras.id_obra != obra_id
        ).first()
        if existing_obra:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otra obra con la referencia '{update_data['referencia']}'"
            )
    
    # Aplicar las actualizaciones
    for field, value in update_data.items():
        setattr(db_obra, field, value)
    
    db.commit()
    db.refresh(db_obra)
    
    return db_obra

# DELETE - Eliminar obra
@router.delete("/{obra_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_obra(obra_id: int, db: Session = Depends(get_db)):
    # Buscar la obra existente
    db_obra = db.query(TObras).filter(TObras.id_obra == obra_id).first()
    if not db_obra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Obra con ID {obra_id} no encontrada"
        )
    
    # Verificar si hay presupuestos asociados (opcional - para integridad referencial)
    # Descomenta estas líneas si quieres evitar eliminar obras que tienen presupuestos
    # from ..models import TPresupuestos
    # presupuestos_asociados = db.query(TPresupuestos).filter(TPresupuestos.id_obra == obra_id).first()
    # if presupuestos_asociados:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="No se puede eliminar la obra porque tiene presupuestos asociados"
    #     )
    
    db.delete(db_obra)
    db.commit()
    
    return None
