from datetime import date
from typing import Optional

from pydantic import BaseModel


class LibroResponse(BaseModel):
    id: str
    titulo: str
    autor: str
    sala: str
    es_alta_demanda: bool


class EjemplarResponse(BaseModel):
    id: str
    libro_id: str
    estado: str


class LibroDetalleResponse(BaseModel):
    id: str
    titulo: str
    autor: str
    sala: str
    es_alta_demanda: bool
    ejemplares: list[EjemplarResponse]


class PrestamoCreateRequest(BaseModel):
    estudiante_id: str
    ejemplar_id: str


class PrestamoResponse(BaseModel):
    id: str
    estudiante_id: str
    ejemplar_id: str
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    fecha_devolucion_real: Optional[date] = None
    estado: str


class MultaResponse(BaseModel):
    id: str
    prestamo_id: str
    monto: int
    estado: str
    fecha_generacion: date


class DevolucionResponse(BaseModel):
    prestamo: PrestamoResponse
    multa: Optional[MultaResponse] = None
