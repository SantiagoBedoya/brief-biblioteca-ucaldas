from enum import Enum


class Programa(str, Enum):
    PREGRADO = "pregrado"
    POSGRADO = "posgrado"


class EstadoEjemplar(str, Enum):
    DISPONIBLE = "disponible"
    PRESTADO = "prestado"
    DANADO = "dañado"


class EstadoPrestamo(str, Enum):
    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    VENCIDO = "vencido"


class EstadoMulta(str, Enum):
    PENDIENTE = "pendiente"
    PAGADA = "pagada"
