from datetime import date
from src.domain.entities import Libro, Ejemplar, Estudiante, Prestamo, Multa
from src.domain.enums import Programa, EstadoEjemplar, EstadoPrestamo, EstadoMulta


class TestLibro:
    def test_crear_libro(self):
        l = Libro(id="L001", titulo="Clean Code", autor="Martin", sala="A", es_alta_demanda=False)
        assert l.id == "L001"
        assert not l.es_alta_demanda


class TestEjemplar:
    def test_estado_default(self):
        e = Ejemplar(id="E001", libro_id="L001")
        assert e.estado == EstadoEjemplar.DISPONIBLE


class TestEstudiante:
    def test_crear_estudiante(self):
        e = Estudiante(id="S001", nombre="Juan", programa=Programa.PREGRADO, semestre=3)
        assert e.programa == Programa.PREGRADO


class TestPrestamo:
    def test_estado_default(self):
        p = Prestamo(id="P001", estudiante_id="S001", ejemplar_id="E001", fecha_prestamo=date.today(), fecha_devolucion_esperada=date.today())
        assert p.estado == EstadoPrestamo.ACTIVO

    def test_con_devolucion(self):
        p = Prestamo(id="P001", estudiante_id="S001", ejemplar_id="E001", fecha_prestamo=date.today(), fecha_devolucion_esperada=date.today(), fecha_devolucion_real=date.today(), estado=EstadoPrestamo.DEVUELTO)
        assert p.estado == EstadoPrestamo.DEVUELTO


class TestMulta:
    def test_monto_mult(self):
        m = Multa(id="M001", prestamo_id="P001", monto=6000)
        assert m.monto == 6000
        assert m.estado == EstadoMulta.PENDIENTE
