# Biblioteca UCaldas — API de Préstamos

Sistema de gestión de préstamos de libros para la Biblioteca de la Universidad de Caldas.

## Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- Datos en memoria
- pytest

## Requisitos

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn src.presentation.app:app --reload --port 8000
```

Documentación interactiva en `http://localhost:8000/docs`.

## Ejecutar tests

```bash
pytest -v
```

## Endpoints

| Método | Ruta | Propósito |
|--------|------|-----------|
| GET | `/libros` | Listar catálogo (filtros: titulo, autor, sala, disponible) |
| GET | `/libros/{id}` | Detalle de libro con ejemplares |
| POST | `/prestamos` | Crear préstamo |
| POST | `/prestamos/{id}/devolucion` | Registrar devolución |
| POST | `/prestamos/{id}/renovacion` | Renovar préstamo |
| GET | `/estudiantes/{id}/prestamos` | Préstamos de estudiante |
| GET | `/prestamos/vencidos` | Listar vencidos |
| GET | `/estudiantes/{id}/multas` | Multas de estudiante |
| GET | `/estudiantes/{id}/historial` | Historial de préstamos |
