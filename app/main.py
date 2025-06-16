from fastapi import FastAPI
from .database import Base, engine
from .routers import obras, presupuestos, capitulos, partidas

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(obras.router)
app.include_router(presupuestos.router)
app.include_router(capitulos.router)
app.include_router(partidas.router)
