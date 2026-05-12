from fastapi import APIRouter, HTTPException, Query

from src.application.use_cases import BibliotecaService, NotFoundError, ConflictError
from src.presentation.schemas import (
    LibroResponse,
    LibroDetalleResponse,
    EjemplarResponse,
    PrestamoCreateRequest,
    PrestamoResponse,
    MultaResponse,
    DevolucionResponse,
)


def crear_router(service: BibliotecaService) -> APIRouter:
    router = APIRouter()

    # ------------------------------------------------------------------
    # GET /libros
    # ------------------------------------------------------------------
    @router.get("/libros", response_model=list[LibroResponse])
    def listar_libros(
        titulo: str | None = Query(None),
        autor: str | None = Query(None),
        sala: str | None = Query(None),
        disponible: bool | None = Query(None),
    ):
        return service.listar_libros(titulo=titulo, autor=autor, sala=sala, disponible=disponible)

    # ------------------------------------------------------------------
    # GET /libros/{id}
    # ------------------------------------------------------------------
    @router.get("/libros/{libro_id}", response_model=LibroDetalleResponse)
    def obtener_libro(libro_id: str):
        try:
            libro, ejemplares = service.obtener_libro(libro_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail={"error": "libro_no_encontrado"})
        return LibroDetalleResponse(
            id=libro.id,
            titulo=libro.titulo,
            autor=libro.autor,
            sala=libro.sala,
            es_alta_demanda=libro.es_alta_demanda,
            ejemplares=[EjemplarResponse(id=e.id, libro_id=e.libro_id, estado=e.estado.value) for e in ejemplares],
        )

    # ------------------------------------------------------------------
    # POST /prestamos
    # ------------------------------------------------------------------
    @router.post("/prestamos", response_model=PrestamoResponse, status_code=201)
    def crear_prestamo(body: PrestamoCreateRequest):
        try:
            prestamo = service.crear_prestamo(body.estudiante_id, body.ejemplar_id)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail={"error": f"{e.tipo}_no_encontrado"})
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=e.detalle)
        return _prestamo_to_response(prestamo)

    # ------------------------------------------------------------------
    # POST /prestamos/{id}/devolucion
    # ------------------------------------------------------------------
    @router.post("/prestamos/{prestamo_id}/devolucion", response_model=DevolucionResponse)
    def devolucion(prestamo_id: str):
        try:
            prestamo, multa = service.devolucion(prestamo_id)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail={"error": f"{e.tipo}_no_encontrado"})
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=e.detalle)
        return DevolucionResponse(
            prestamo=_prestamo_to_response(prestamo),
            multa=_multa_to_response(multa) if multa else None,
        )

    # ------------------------------------------------------------------
    # POST /prestamos/{id}/renovacion
    # ------------------------------------------------------------------
    @router.post("/prestamos/{prestamo_id}/renovacion", response_model=PrestamoResponse)
    def renovacion(prestamo_id: str):
        try:
            prestamo = service.renovacion(prestamo_id)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail={"error": f"{e.tipo}_no_encontrado"})
        except ConflictError as e:
            raise HTTPException(status_code=409, detail=e.detalle)
        return _prestamo_to_response(prestamo)

    # ------------------------------------------------------------------
    # GET /estudiantes/{id}/prestamos
    # ------------------------------------------------------------------
    @router.get("/estudiantes/{estudiante_id}/prestamos", response_model=list[PrestamoResponse])
    def prestamos_estudiante(estudiante_id: str, activo: bool | None = Query(None)):
        try:
            prestamos = service.listar_prestamos_estudiante(estudiante_id, activo)
        except NotFoundError:
            raise HTTPException(status_code=404, detail={"error": "estudiante_no_encontrado"})
        return [_prestamo_to_response(p) for p in prestamos]

    # ------------------------------------------------------------------
    # GET /prestamos/vencidos
    # ------------------------------------------------------------------
    @router.get("/prestamos/vencidos", response_model=list[PrestamoResponse])
    def listar_vencidos():
        return [_prestamo_to_response(p) for p in service.listar_vencidos()]

    # ------------------------------------------------------------------
    # GET /estudiantes/{id}/multas
    # ------------------------------------------------------------------
    @router.get("/estudiantes/{estudiante_id}/multas", response_model=list[MultaResponse])
    def multas_estudiante(estudiante_id: str):
        try:
            multas = service.listar_multas_estudiante(estudiante_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail={"error": "estudiante_no_encontrado"})
        return [_multa_to_response(m) for m in multas]

    # ------------------------------------------------------------------
    # GET /estudiantes/{id}/historial
    # ------------------------------------------------------------------
    @router.get("/estudiantes/{estudiante_id}/historial", response_model=list[PrestamoResponse])
    def historial_estudiante(estudiante_id: str):
        try:
            prestamos = service.listar_historial_estudiante(estudiante_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail={"error": "estudiante_no_encontrado"})
        return [_prestamo_to_response(p) for p in prestamos]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _prestamo_to_response(p):
        return PrestamoResponse(
            id=p.id,
            estudiante_id=p.estudiante_id,
            ejemplar_id=p.ejemplar_id,
            fecha_prestamo=p.fecha_prestamo,
            fecha_devolucion_esperada=p.fecha_devolucion_esperada,
            fecha_devolucion_real=p.fecha_devolucion_real,
            estado=p.estado.value,
        )

    def _multa_to_response(m):
        return MultaResponse(
            id=m.id,
            prestamo_id=m.prestamo_id,
            monto=m.monto,
            estado=m.estado.value,
            fecha_generacion=m.fecha_generacion,
        )

    return router
