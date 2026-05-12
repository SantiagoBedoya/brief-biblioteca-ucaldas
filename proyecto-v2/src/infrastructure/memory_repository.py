from src.domain.entities import Libro, Ejemplar, Estudiante, Prestamo, Multa
from src.domain.enums import Programa, EstadoEjemplar, EstadoPrestamo, EstadoMulta
from src.domain.repositories import (
    LibroRepository,
    EjemplarRepository,
    EstudianteRepository,
    PrestamoRepository,
    MultaRepository,
)


class MemoryLibroRepository(LibroRepository):
    def __init__(self):
        self._data: dict[str, Libro] = {}

    def listar(self, titulo: str | None = None, autor: str | None = None, sala: str | None = None) -> list[Libro]:
        resultados = list(self._data.values())
        if titulo:
            resultados = [l for l in resultados if titulo.lower() in l.titulo.lower()]
        if autor:
            resultados = [l for l in resultados if autor.lower() in l.autor.lower()]
        if sala:
            resultados = [l for l in resultados if sala.lower() in l.sala.lower()]
        return resultados

    def obtener(self, id: str) -> Libro | None:
        return self._data.get(id)

    def guardar(self, libro: Libro) -> None:
        self._data[libro.id] = libro


class MemoryEjemplarRepository(EjemplarRepository):
    def __init__(self):
        self._data: dict[str, Ejemplar] = {}

    def listar_por_libro(self, libro_id: str) -> list[Ejemplar]:
        return [e for e in self._data.values() if e.libro_id == libro_id]

    def obtener(self, id: str) -> Ejemplar | None:
        return self._data.get(id)

    def actualizar(self, ejemplar: Ejemplar) -> None:
        self._data[ejemplar.id] = ejemplar

    def guardar(self, ejemplar: Ejemplar) -> None:
        self._data[ejemplar.id] = ejemplar


class MemoryEstudianteRepository(EstudianteRepository):
    def __init__(self):
        self._data: dict[str, Estudiante] = {}

    def obtener(self, id: str) -> Estudiante | None:
        return self._data.get(id)

    def guardar(self, estudiante: Estudiante) -> None:
        self._data[estudiante.id] = estudiante


class MemoryPrestamoRepository(PrestamoRepository):
    def __init__(self):
        self._data: dict[str, Prestamo] = {}

    def obtener(self, id: str) -> Prestamo | None:
        return self._data.get(id)

    def guardar(self, prestamo: Prestamo) -> None:
        self._data[prestamo.id] = prestamo

    def listar_por_estudiante(self, estudiante_id: str, activo: bool | None = None) -> list[Prestamo]:
        resultados = [p for p in self._data.values() if p.estudiante_id == estudiante_id]
        if activo is True:
            resultados = [p for p in resultados if p.estado == EstadoPrestamo.ACTIVO]
        elif activo is False:
            resultados = [p for p in resultados if p.estado != EstadoPrestamo.ACTIVO]
        return resultados

    def listar_todos(self) -> list[Prestamo]:
        return list(self._data.values())

    def listar_todos_activos(self) -> list[Prestamo]:
        return [p for p in self._data.values() if p.estado == EstadoPrestamo.ACTIVO]


class MemoryMultaRepository(MultaRepository):
    def __init__(self):
        self._data: dict[str, Multa] = {}

    def guardar(self, multa: Multa) -> None:
        self._data[multa.id] = multa

    def listar_por_prestamo(self, prestamo_id: str) -> Multa | None:
        for m in self._data.values():
            if m.prestamo_id == prestamo_id:
                return m
        return None

    def listar_por_ids_de_prestamo(self, prestamo_ids: list[str]) -> list[Multa]:
        return [m for m in self._data.values() if m.prestamo_id in prestamo_ids]


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

def seed_repositorios(
    libro_repo: MemoryLibroRepository,
    ejemplar_repo: MemoryEjemplarRepository,
    estudiante_repo: MemoryEstudianteRepository,
) -> None:
    libros = [
        Libro(id="L001", titulo="Introducción a los Algoritmos", autor="Cormen et al.", sala="Sala A", es_alta_demanda=True),
        Libro(id="L002", titulo="Clean Code", autor="Robert C. Martin", sala="Sala A", es_alta_demanda=False),
        Libro(id="L003", titulo="El Quijote", autor="Miguel de Cervantes", sala="Sala B", es_alta_demanda=False),
        Libro(id="L004", titulo="Sistemas Operativos Modernos", autor="Andrew Tanenbaum", sala="Sala B", es_alta_demanda=False),
        Libro(id="L005", titulo="Bases de Datos: Diseño e Implementación", autor="C.J. Date", sala="Sala C", es_alta_demanda=True),
    ]
    for l in libros:
        libro_repo.guardar(l)

    ejemplares = [
        Ejemplar(id="E001", libro_id="L001"),
        Ejemplar(id="E002", libro_id="L001"),
        Ejemplar(id="E003", libro_id="L002"),
        Ejemplar(id="E004", libro_id="L003"),
        Ejemplar(id="E005", libro_id="L003"),
        Ejemplar(id="E006", libro_id="L004"),
        Ejemplar(id="E007", libro_id="L005"),
        Ejemplar(id="E008", libro_id="L005", estado=EstadoEjemplar.DANADO),
    ]
    for e in ejemplares:
        ejemplar_repo.guardar(e)

    estudiantes = [
        Estudiante(id="S001", nombre="Juan Pérez", programa=Programa.PREGRADO, semestre=3),
        Estudiante(id="S002", nombre="María Gómez", programa=Programa.POSGRADO, semestre=2),
    ]
    for e in estudiantes:
        estudiante_repo.guardar(e)
