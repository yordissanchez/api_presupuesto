from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from .database import Base

class TObras(Base):
    __tablename__ = "TObras"

    id_obra = Column(Integer, primary_key=True)
    referencia = Column(String)
    nombre = Column(String)
    direccion = Column(String)

class TPresupuestos(Base):
    __tablename__ = "TPresupuestos"

    id_presupuesto = Column(Integer, primary_key=True)
    id_obra = Column(Integer, ForeignKey("TObras.id_obra"))
    nombre_presupuesto = Column(String)

class TCapitulos(Base):
    __tablename__ = "TCapitulos"

    id_capitulo = Column(Integer, primary_key=True)
    codigo = Column(String)
    descripcion = Column(String)

class TPartidas(Base):
    __tablename__ = "TPartidas"

    id_partida = Column(Integer, primary_key=True)
    codigo = Column(String)
    descripcion = Column(String)
