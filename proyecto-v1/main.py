from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date, timedelta
import uuid

app = FastAPI(title="Biblioteca UCALDAS - API de Préstamos", version="1.0.0")

# ---------------------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------------------

class Libro(BaseModel):
    id: str
    titulo: str
    autor: str
    isbn: str
    disponible: bool = True


class PrestamoCreate(BaseModel):
    libro_id: str
    usuario_id: str
    nombre_usuario: str
    dias_prestamo: int = 7


class Prestamo(BaseModel):
    id: str
    libro_id: str
    titulo_libro: str
    usuario_id: str
    nombre_usuario: str
    fecha_prestamo: date
    fecha_devolucion_esperada: date
    fecha_devolucion_real: Optional[date] = None
    activo: bool = True


# ---------------------------------------------------------------------------
# Datos en memoria
# ---------------------------------------------------------------------------

libros: dict[str, Libro] = {
    "L001": Libro(id="L001", titulo="Introducción a los Algoritmos", autor="Cormen et al.", isbn="978-0-262-03384-8"),
    "L002": Libro(id="L002", titulo="Clean Code", autor="Robert C. Martin", isbn="978-0-13-235088-4"),
    "L003": Libro(id="L003", titulo="El Quijote", autor="Miguel de Cervantes", isbn="978-84-376-0494-7"),
    "L004": Libro(id="L004", titulo="Sistemas Operativos Modernos", autor="Andrew Tanenbaum", isbn="978-607-32-2377-5"),
    "L005": Libro(id="L005", titulo="Bases de Datos: Diseño e Implementación", autor="C.J. Date", isbn="978-970-26-0876-8"),
}

prestamos: dict[str, Prestamo] = {}


# ---------------------------------------------------------------------------
# Endpoints — Libros
# ---------------------------------------------------------------------------

@app.get("/libros", response_model=list[Libro], summary="Listar todos los libros")
def listar_libros():
    return list(libros.values())


@app.get("/libros/disponibles", response_model=list[Libro], summary="Listar libros disponibles")
def listar_libros_disponibles():
    return [l for l in libros.values() if l.disponible]


@app.get("/libros/{libro_id}", response_model=Libro, summary="Obtener un libro por ID")
def obtener_libro(libro_id: str):
    if libro_id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libros[libro_id]


# ---------------------------------------------------------------------------
# Endpoints — Préstamos
# ---------------------------------------------------------------------------

@app.post("/prestamos", response_model=Prestamo, status_code=201, summary="Crear un préstamo")
def crear_prestamo(datos: PrestamoCreate):
    if datos.libro_id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro = libros[datos.libro_id]
    if not libro.disponible:
        raise HTTPException(status_code=409, detail="El libro no está disponible para préstamo")

    if datos.dias_prestamo < 1 or datos.dias_prestamo > 30:
        raise HTTPException(status_code=422, detail="Los días de préstamo deben estar entre 1 y 30")

    hoy = date.today()
    prestamo = Prestamo(
        id=str(uuid.uuid4())[:8].upper(),
        libro_id=datos.libro_id,
        titulo_libro=libro.titulo,
        usuario_id=datos.usuario_id,
        nombre_usuario=datos.nombre_usuario,
        fecha_prestamo=hoy,
        fecha_devolucion_esperada=hoy + timedelta(days=datos.dias_prestamo),
    )

    prestamos[prestamo.id] = prestamo
    libros[datos.libro_id].disponible = False
    return prestamo


@app.get("/prestamos/vigentes", response_model=list[Prestamo], summary="Consultar préstamos vigentes")
def prestamos_vigentes():
    return [p for p in prestamos.values() if p.activo]


@app.get("/prestamos", response_model=list[Prestamo], summary="Listar todos los préstamos")
def listar_prestamos():
    return list(prestamos.values())


@app.get("/prestamos/{prestamo_id}", response_model=Prestamo, summary="Obtener un préstamo por ID")
def obtener_prestamo(prestamo_id: str):
    if prestamo_id not in prestamos:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamos[prestamo_id]


@app.put("/prestamos/{prestamo_id}/devolver", response_model=Prestamo, summary="Registrar devolución de un libro")
def devolver_libro(prestamo_id: str):
    if prestamo_id not in prestamos:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    prestamo = prestamos[prestamo_id]
    if not prestamo.activo:
        raise HTTPException(status_code=409, detail="Este préstamo ya fue cerrado")

    prestamo.fecha_devolucion_real = date.today()
    prestamo.activo = False
    libros[prestamo.libro_id].disponible = True
    return prestamo
