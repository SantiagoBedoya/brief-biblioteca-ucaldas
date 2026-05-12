import uuid
from datetime import date, timedelta

from src.domain.entities import Prestamo, Multa
from src.domain.enums import EstadoEjemplar, EstadoPrestamo, EstadoMulta, Programa
from src.domain.repositories import (
    LibroRepository,
    EjemplarRepository,
    EstudianteRepository,
    PrestamoRepository,
    MultaRepository,
)


class NotFoundError(Exception):
    def __init__(self, tipo: str, id: str):
        self.tipo = tipo
        self.id = id


class ConflictError(Exception):
    def __init__(self, detalle: dict):
        self.detalle = detalle


class BibliotecaService:
    def __init__(
        self,
        libro_repo: LibroRepository,
        ejemplar_repo: EjemplarRepository,
        estudiante_repo: EstudianteRepository,
        prestamo_repo: PrestamoRepository,
        multa_repo: MultaRepository,
    ):
        self._libro_repo = libro_repo
        self._ejemplar_repo = ejemplar_repo
        self._estudiante_repo = estudiante_repo
        self._prestamo_repo = prestamo_repo
        self._multa_repo = multa_repo

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _marcar_vencidos(self) -> None:
        for p in self._prestamo_repo.listar_todos_activos():
            if p.fecha_devolucion_esperada < date.today():
                p.estado = EstadoPrestamo.VENCIDO
                self._prestamo_repo.guardar(p)

    def _tiene_ejemplares_disponibles(self, libro_id: str) -> bool:
        return any(
            e.estado == EstadoEjemplar.DISPONIBLE
            for e in self._ejemplar_repo.listar_por_libro(libro_id)
        )

    # ------------------------------------------------------------------
    # Libros
    # ------------------------------------------------------------------

    def listar_libros(
        self,
        titulo: str | None = None,
        autor: str | None = None,
        sala: str | None = None,
        disponible: bool | None = None,
    ) -> list:
        libros = self._libro_repo.listar(titulo=titulo, autor=autor, sala=sala)
        if disponible is not None:
            libros = [l for l in libros if self._tiene_ejemplares_disponibles(l.id) == disponible]
        return libros

    def obtener_libro(self, libro_id: str):
        libro = self._libro_repo.obtener(libro_id)
        if not libro:
            raise NotFoundError("libro", libro_id)
        ejemplares = self._ejemplar_repo.listar_por_libro(libro_id)
        return libro, ejemplares

    # ------------------------------------------------------------------
    # Préstamos
    # ------------------------------------------------------------------

    def crear_prestamo(self, estudiante_id: str, ejemplar_id: str):
        estudiante = self._estudiante_repo.obtener(estudiante_id)
        if not estudiante:
            raise NotFoundError("estudiante", estudiante_id)

        ejemplar = self._ejemplar_repo.obtener(ejemplar_id)
        if not ejemplar:
            raise NotFoundError("ejemplar", ejemplar_id)

        # RN4 — Ejemplar debe estar disponible
        if ejemplar.estado != EstadoEjemplar.DISPONIBLE:
            raise ConflictError({"error": "ejemplar_no_disponible"})

        self._marcar_vencidos()

        # RN3 — No préstamo si tiene préstamos vencidos
        prestamos_est = self._prestamo_repo.listar_por_estudiante(estudiante_id)
        if any(p.estado == EstadoPrestamo.VENCIDO for p in prestamos_est):
            raise ConflictError({"error": "prestamo_vencido_pendiente"})

        # RN7 — No préstamo si tiene multas pendientes
        ids_prestamos = [p.id for p in prestamos_est]
        multas = self._multa_repo.listar_por_ids_de_prestamo(ids_prestamos)
        if any(m.estado == EstadoMulta.PENDIENTE for m in multas):
            raise ConflictError({"error": "multa_pendiente"})

        # RN1 — Límite de préstamos por tipo de estudiante
        activos = [p for p in prestamos_est if p.estado == EstadoPrestamo.ACTIVO]
        limite = 3 if estudiante.programa == Programa.PREGRADO else 5
        if len(activos) >= limite:
            raise ConflictError({
                "error": "limite_prestamos_alcanzado",
                "limite": limite,
                "actuales": len(activos),
            })

        # RN2 — Plazo de préstamo según tipo de libro
        libro = self._libro_repo.obtener(ejemplar.libro_id)
        plazo = 3 if libro.es_alta_demanda else 15

        prestamo = Prestamo(
            id=uuid.uuid4().hex[:8].upper(),
            estudiante_id=estudiante_id,
            ejemplar_id=ejemplar_id,
            fecha_prestamo=date.today(),
            fecha_devolucion_esperada=date.today() + timedelta(days=plazo),
        )

        ejemplar.estado = EstadoEjemplar.PRESTADO
        self._ejemplar_repo.actualizar(ejemplar)
        self._prestamo_repo.guardar(prestamo)

        return prestamo

    def devolucion(self, prestamo_id: str):
        prestamo = self._prestamo_repo.obtener(prestamo_id)
        if not prestamo:
            raise NotFoundError("prestamo", prestamo_id)

        if prestamo.estado == EstadoPrestamo.DEVUELTO:
            raise ConflictError({"error": "prestamo_ya_devuelto"})

        hoy = date.today()
        prestamo.fecha_devolucion_real = hoy
        prestamo.estado = EstadoPrestamo.DEVUELTO

        ejemplar = self._ejemplar_repo.obtener(prestamo.ejemplar_id)
        ejemplar.estado = EstadoEjemplar.DISPONIBLE
        self._ejemplar_repo.actualizar(ejemplar)
        self._prestamo_repo.guardar(prestamo)

        # RN6 — Cálculo de multas por retraso
        multa = None
        if hoy > prestamo.fecha_devolucion_esperada:
            dias_retraso = (hoy - prestamo.fecha_devolucion_esperada).days
            multa = Multa(
                id=uuid.uuid4().hex[:8].upper(),
                prestamo_id=prestamo.id,
                monto=2000 * dias_retraso,
            )
            self._multa_repo.guardar(multa)

        return prestamo, multa

    def renovacion(self, prestamo_id: str):
        prestamo = self._prestamo_repo.obtener(prestamo_id)
        if not prestamo:
            raise NotFoundError("prestamo", prestamo_id)

        self._marcar_vencidos()

        # RN5 — Renovación condicionada
        if prestamo.estado != EstadoPrestamo.ACTIVO:
            raise ConflictError({
                "error": "renovacion_no_permitida",
                "motivo": "el préstamo no está activo",
            })

        if prestamo.fecha_devolucion_esperada < date.today():
            raise ConflictError({
                "error": "renovacion_no_permitida",
                "motivo": "el préstamo ya está vencido",
            })

        ejemplar = self._ejemplar_repo.obtener(prestamo.ejemplar_id)
        libro = self._libro_repo.obtener(ejemplar.libro_id)
        plazo = 3 if libro.es_alta_demanda else 15

        prestamo.fecha_devolucion_esperada += timedelta(days=plazo)
        self._prestamo_repo.guardar(prestamo)

        return prestamo

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def listar_prestamos_estudiante(self, estudiante_id: str, activo: bool | None = None):
        if not self._estudiante_repo.obtener(estudiante_id):
            raise NotFoundError("estudiante", estudiante_id)
        return self._prestamo_repo.listar_por_estudiante(estudiante_id, activo)

    def listar_vencidos(self):
        self._marcar_vencidos()
        return [p for p in self._prestamo_repo.listar_todos() if p.estado == EstadoPrestamo.VENCIDO]

    def listar_multas_estudiante(self, estudiante_id: str):
        if not self._estudiante_repo.obtener(estudiante_id):
            raise NotFoundError("estudiante", estudiante_id)
        prestamos = self._prestamo_repo.listar_por_estudiante(estudiante_id)
        ids = [p.id for p in prestamos]
        return self._multa_repo.listar_por_ids_de_prestamo(ids)

    def listar_historial_estudiante(self, estudiante_id: str):
        if not self._estudiante_repo.obtener(estudiante_id):
            raise NotFoundError("estudiante", estudiante_id)
        return self._prestamo_repo.listar_por_estudiante(estudiante_id)
