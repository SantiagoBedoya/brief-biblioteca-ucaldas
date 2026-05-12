from dataclasses import dataclass, field
from datetime import date

from src.domain.enums import Programa, EstadoEjemplar, EstadoPrestamo, EstadoMulta


@dataclass
class Libro:
    id: str
    titulo: str
    autor: str
    sala: str
    es_alta_demanda: bool


@dataclass
class Ejemplar:
    id: str
    libro_id: str
    estado: EstadoEjemplar = EstadoEjemplar.DISPONIBLE


@dataclass
class Estudiante:
    id: str
    nombre: str
    programa: Programa
    semestre: int


@dataclass
class Prestamo:
    id: str
    estudiante_id: str
    ejemplar_id: str
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    fecha_devolucion_real: date | None = None
    estado: EstadoPrestamo = EstadoPrestamo.ACTIVO


@dataclass
class Multa:
    id: str
    prestamo_id: str
    monto: int
    estado: EstadoMulta = EstadoMulta.PENDIENTE
    fecha_generacion: date = field(default_factory=date.today)
