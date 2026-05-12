import pytest
from datetime import date, timedelta

from src.domain.entities import Libro, Ejemplar, Estudiante, Prestamo, Multa
from src.domain.enums import Programa, EstadoEjemplar, EstadoPrestamo, EstadoMulta
from src.infrastructure.memory_repository import (
    MemoryLibroRepository,
    MemoryEjemplarRepository,
    MemoryEstudianteRepository,
    MemoryPrestamoRepository,
    MemoryMultaRepository,
    seed_repositorios,
)
from src.application.use_cases import BibliotecaService


@pytest.fixture
def repos():
    lr = MemoryLibroRepository()
    er = MemoryEjemplarRepository()
    esr = MemoryEstudianteRepository()
    pr = MemoryPrestamoRepository()
    mr = MemoryMultaRepository()
    seed_repositorios(lr, er, esr)
    return lr, er, esr, pr, mr


@pytest.fixture
def service(repos):
    lr, er, esr, pr, mr = repos
    return BibliotecaService(libro_repo=lr, ejemplar_repo=er, estudiante_repo=esr, prestamo_repo=pr, multa_repo=mr)


@pytest.fixture
def client(service):
    from src.presentation.routes import crear_router
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(crear_router(service))
    return TestClient(app)
