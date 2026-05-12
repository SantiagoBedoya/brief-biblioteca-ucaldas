from abc import ABC, abstractmethod

from src.domain.entities import Libro, Ejemplar, Estudiante, Prestamo, Multa


class LibroRepository(ABC):
    @abstractmethod
    def listar(self, titulo: str | None = None, autor: str | None = None, sala: str | None = None) -> list[Libro]:
        ...

    @abstractmethod
    def obtener(self, id: str) -> Libro | None:
        ...


class EjemplarRepository(ABC):
    @abstractmethod
    def listar_por_libro(self, libro_id: str) -> list[Ejemplar]:
        ...

    @abstractmethod
    def obtener(self, id: str) -> Ejemplar | None:
        ...

    @abstractmethod
    def actualizar(self, ejemplar: Ejemplar) -> None:
        ...


class EstudianteRepository(ABC):
    @abstractmethod
    def obtener(self, id: str) -> Estudiante | None:
        ...


class PrestamoRepository(ABC):
    @abstractmethod
    def obtener(self, id: str) -> Prestamo | None:
        ...

    @abstractmethod
    def guardar(self, prestamo: Prestamo) -> None:
        ...

    @abstractmethod
    def listar_por_estudiante(self, estudiante_id: str, activo: bool | None = None) -> list[Prestamo]:
        ...

    @abstractmethod
    def listar_todos(self) -> list[Prestamo]:
        ...

    @abstractmethod
    def listar_todos_activos(self) -> list[Prestamo]:
        ...


class MultaRepository(ABC):
    @abstractmethod
    def guardar(self, multa: Multa) -> None:
        ...

    @abstractmethod
    def listar_por_prestamo(self, prestamo_id: str) -> Multa | None:
        ...

    @abstractmethod
    def listar_por_ids_de_prestamo(self, prestamo_ids: list[str]) -> list[Multa]:
        ...
