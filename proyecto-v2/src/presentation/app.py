from fastapi import FastAPI

from src.infrastructure.memory_repository import (
    MemoryLibroRepository,
    MemoryEjemplarRepository,
    MemoryEstudianteRepository,
    MemoryPrestamoRepository,
    MemoryMultaRepository,
    seed_repositorios,
)
from src.application.use_cases import BibliotecaService
from src.presentation.routes import crear_router


def create_app() -> FastAPI:
    libro_repo = MemoryLibroRepository()
    ejemplar_repo = MemoryEjemplarRepository()
    estudiante_repo = MemoryEstudianteRepository()
    prestamo_repo = MemoryPrestamoRepository()
    multa_repo = MemoryMultaRepository()

    seed_repositorios(libro_repo, ejemplar_repo, estudiante_repo)

    service = BibliotecaService(
        libro_repo=libro_repo,
        ejemplar_repo=ejemplar_repo,
        estudiante_repo=estudiante_repo,
        prestamo_repo=prestamo_repo,
        multa_repo=multa_repo,
    )

    app = FastAPI(title="Biblioteca UCaldas — API de Préstamos", version="2.0.0")
    app.include_router(crear_router(service))
    return app


app = create_app()
