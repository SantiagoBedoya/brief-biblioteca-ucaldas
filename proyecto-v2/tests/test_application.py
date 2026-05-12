from datetime import date, timedelta
import pytest

from src.domain.entities import Prestamo, Multa
from src.domain.enums import EstadoEjemplar, EstadoPrestamo, EstadoMulta, Programa
from src.application.use_cases import NotFoundError, ConflictError


class TestListarLibros:
    def test_sin_filtros(self, service):
        libros = service.listar_libros()
        assert len(libros) == 5

    def test_filtro_titulo(self, service):
        libros = service.listar_libros(titulo="clean")
        assert len(libros) == 1
        assert libros[0].id == "L002"

    def test_filtro_autor(self, service):
        libros = service.listar_libros(autor="cervantes")
        assert len(libros) == 1

    def test_filtro_sala(self, service):
        libros = service.listar_libros(sala="Sala A")
        assert len(libros) == 2

    def test_filtro_disponible(self, service):
        libros = service.listar_libros(disponible=True)
        # All books have at least one available copy initially
        assert len(libros) >= 1


class TestObtenerLibro:
    def test_existente(self, service):
        libro, ejemplares = service.obtener_libro("L001")
        assert libro.id == "L001"
        assert len(ejemplares) == 2

    def test_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.obtener_libro("INVALIDO")


class TestCrearPrestamo:
    def test_exitoso_pregrado(self, service):
        prestamo = service.crear_prestamo("S001", "E001")
        assert prestamo.estudiante_id == "S001"
        assert prestamo.ejemplar_id == "E001"
        assert prestamo.estado == EstadoPrestamo.ACTIVO
        assert prestamo.fecha_prestamo == date.today()
        assert prestamo.fecha_devolucion_esperada == date.today() + timedelta(days=3)  # alta demanda

    def test_exitoso_estandar(self, service):
        prestamo = service.crear_prestamo("S001", "E003")
        assert prestamo.fecha_devolucion_esperada == date.today() + timedelta(days=15)

    def test_ejemplar_no_disponible(self, service):
        service.crear_prestamo("S001", "E001")
        with pytest.raises(ConflictError) as exc:
            service.crear_prestamo("S002", "E001")
        assert exc.value.detalle["error"] == "ejemplar_no_disponible"

    def test_ejemplar_danado(self, service):
        with pytest.raises(ConflictError) as exc:
            service.crear_prestamo("S001", "E008")
        assert exc.value.detalle["error"] == "ejemplar_no_disponible"

    def test_estudiante_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.crear_prestamo("INVALIDO", "E001")

    def test_ejemplar_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.crear_prestamo("S001", "INVALIDO")

    def test_limite_pregrado(self, service):
        service.crear_prestamo("S001", "E001")
        service.crear_prestamo("S001", "E003")
        service.crear_prestamo("S001", "E004")
        with pytest.raises(ConflictError) as exc:
            service.crear_prestamo("S001", "E006")
        assert exc.value.detalle["error"] == "limite_prestamos_alcanzado"
        assert exc.value.detalle["limite"] == 3

    def test_limite_posgrado(self, service, repos):
        lr, er, esr, pr, mr = repos
        # Seed allows more than 3 loans for posgrado
        service.crear_prestamo("S002", "E001")
        service.crear_prestamo("S002", "E003")
        service.crear_prestamo("S002", "E004")
        service.crear_prestamo("S002", "E006")
        service.crear_prestamo("S002", "E007")
        with pytest.raises(ConflictError) as exc:
            service.crear_prestamo("S002", "E002")
        assert exc.value.detalle["error"] == "limite_prestamos_alcanzado"
        assert exc.value.detalle["limite"] == 5

    def test_multas_pendientes_bloquea(self, service, repos):
        lr, er, esr, pr, mr = repos
        prestamo = service.crear_prestamo("S002", "E001")
        # Add a pending fine manually
        multa = Multa(id="MX", prestamo_id=prestamo.id, monto=2000)
        mr.guardar(multa)
        with pytest.raises(ConflictError) as exc:
            service.crear_prestamo("S002", "E003")
        assert exc.value.detalle["error"] == "multa_pendiente"

    def test_prestamo_vencido_bloquea(self, service, repos):
        lr, er, esr, pr, mr = repos
        prestamo = service.crear_prestamo("S002", "E001")
        prestamo.fecha_devolucion_esperada = date.today() - timedelta(days=1)
        prestamo.estado = EstadoPrestamo.VENCIDO
        pr.guardar(prestamo)
        with pytest.raises(ConflictError) as exc:
            service.crear_prestamo("S002", "E003")
        assert exc.value.detalle["error"] == "prestamo_vencido_pendiente"


class TestDevolucion:
    def test_devolucion_sin_multa(self, service):
        prestamo = service.crear_prestamo("S001", "E001")
        resultado, multa = service.devolucion(prestamo.id)
        assert resultado.estado == EstadoPrestamo.DEVUELTO
        assert resultado.fecha_devolucion_real == date.today()
        assert multa is None

    def test_devolucion_con_multa(self, service, repos):
        lr, er, esr, pr, mr = repos
        prestamo = service.crear_prestamo("S001", "E001")
        prestamo.fecha_devolucion_esperada = date.today() - timedelta(days=5)
        pr.guardar(prestamo)
        resultado, multa = service.devolucion(prestamo.id)
        assert multa is not None
        assert multa.monto == 10000  # 2000 * 5
        assert multa.estado == EstadoMulta.PENDIENTE

    def test_devolucion_repetida(self, service):
        prestamo = service.crear_prestamo("S001", "E001")
        service.devolucion(prestamo.id)
        with pytest.raises(ConflictError) as exc:
            service.devolucion(prestamo.id)
        assert exc.value.detalle["error"] == "prestamo_ya_devuelto"

    def test_devolucion_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.devolucion("INVALIDO")

    def test_ejemplar_vuelve_disponible(self, service):
        prestamo = service.crear_prestamo("S001", "E001")
        service.devolucion(prestamo.id)
        ejemplar = service._ejemplar_repo.obtener("E001")
        assert ejemplar.estado == EstadoEjemplar.DISPONIBLE


class TestRenovacion:
    def test_renovacion_exitosa(self, service):
        prestamo = service.crear_prestamo("S001", "E001")
        fecha_original = prestamo.fecha_devolucion_esperada
        renovado = service.renovacion(prestamo.id)
        assert renovado.fecha_devolucion_esperada == fecha_original + timedelta(days=3)

    def test_renovacion_estandar(self, service):
        prestamo = service.crear_prestamo("S001", "E003")
        fecha_original = prestamo.fecha_devolucion_esperada
        renovado = service.renovacion(prestamo.id)
        assert renovado.fecha_devolucion_esperada == fecha_original + timedelta(days=15)

    def test_renovacion_ya_devuelto(self, service):
        prestamo = service.crear_prestamo("S001", "E001")
        service.devolucion(prestamo.id)
        with pytest.raises(ConflictError) as exc:
            service.renovacion(prestamo.id)
        assert exc.value.detalle["error"] == "renovacion_no_permitida"

    def test_renovacion_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.renovacion("INVALIDO")


class TestListarPrestamosEstudiante:
    def test_sin_filtro(self, service):
        service.crear_prestamo("S001", "E001")
        prestamos = service.listar_prestamos_estudiante("S001")
        assert len(prestamos) == 1

    def test_filtro_activo_true(self, service):
        p1 = service.crear_prestamo("S001", "E001")
        p2 = service.crear_prestamo("S001", "E003")
        service.devolucion(p1.id)
        activos = service.listar_prestamos_estudiante("S001", activo=True)
        assert len(activos) == 1
        assert activos[0].id == p2.id

    def test_filtro_activo_false(self, service):
        p1 = service.crear_prestamo("S001", "E001")
        service.crear_prestamo("S001", "E003")
        service.devolucion(p1.id)
        no_activos = service.listar_prestamos_estudiante("S001", activo=False)
        assert len(no_activos) == 1

    def test_estudiante_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.listar_prestamos_estudiante("INVALIDO")


class TestListarVencidos:
    def test_sin_vencidos(self, service):
        assert service.listar_vencidos() == []

    def test_con_vencidos(self, service, repos):
        lr, er, esr, pr, mr = repos
        prestamo = service.crear_prestamo("S002", "E001")
        prestamo.fecha_devolucion_esperada = date.today() - timedelta(days=1)
        pr.guardar(prestamo)
        vencidos = service.listar_vencidos()
        assert len(vencidos) == 1
        assert vencidos[0].estado == EstadoPrestamo.VENCIDO


class TestMultasEstudiante:
    def test_sin_multas(self, service):
        assert service.listar_multas_estudiante("S001") == []

    def test_con_multa(self, service, repos):
        lr, er, esr, pr, mr = repos
        prestamo = service.crear_prestamo("S001", "E001")
        prestamo.fecha_devolucion_esperada = date.today() - timedelta(days=3)
        pr.guardar(prestamo)
        service.devolucion(prestamo.id)
        multas = service.listar_multas_estudiante("S001")
        assert len(multas) == 1
        assert multas[0].monto == 6000

    def test_estudiante_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.listar_multas_estudiante("INVALIDO")


class TestHistorial:
    def test_historial_vacio(self, service):
        assert service.listar_historial_estudiante("S001") == []

    def test_historial_con_prestamos(self, service):
        service.crear_prestamo("S001", "E001")
        service.crear_prestamo("S001", "E003")
        historial = service.listar_historial_estudiante("S001")
        assert len(historial) == 2

    def test_historial_inexistente(self, service):
        with pytest.raises(NotFoundError):
            service.listar_historial_estudiante("INVALIDO")
