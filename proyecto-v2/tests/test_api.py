from datetime import date, timedelta


class TestLibrosAPI:
    def test_listar_libros(self, client):
        r = client.get("/libros")
        assert r.status_code == 200
        data = r.json()
        assert len(data) >= 1
        assert "id" in data[0]
        assert "titulo" in data[0]

    def test_listar_con_filtro(self, client):
        r = client.get("/libros?titulo=clean")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_obtener_libro(self, client):
        r = client.get("/libros/L001")
        assert r.status_code == 200
        data = r.json()
        assert data["id"] == "L001"
        assert "ejemplares" in data
        assert len(data["ejemplares"]) == 2

    def test_obtener_libro_404(self, client):
        r = client.get("/libros/INVALIDO")
        assert r.status_code == 404

    def test_filtro_disponible(self, client):
        r = client.get("/libros?disponible=true")
        assert r.status_code == 200


class TestPrestamosAPI:
    def test_crear_prestamo(self, client):
        r = client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        assert r.status_code == 201
        data = r.json()
        assert data["estudiante_id"] == "S001"
        assert data["ejemplar_id"] == "E001"
        assert data["estado"] == "activo"

    def test_crear_prestamo_ejemplar_no_disponible(self, client):
        client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        r = client.post("/prestamos", json={"estudiante_id": "S002", "ejemplar_id": "E001"})
        assert r.status_code == 409
        assert r.json()["detail"]["error"] == "ejemplar_no_disponible"

    def test_crear_prestamo_estudiante_404(self, client):
        r = client.post("/prestamos", json={"estudiante_id": "INVALIDO", "ejemplar_id": "E001"})
        assert r.status_code == 404

    def test_crear_prestamo_ejemplar_404(self, client):
        r = client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "INVALIDO"})
        assert r.status_code == 404

    def test_limite_prestamos(self, client):
        client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E003"})
        client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E004"})
        r = client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E006"})
        assert r.status_code == 409
        assert r.json()["detail"]["error"] == "limite_prestamos_alcanzado"

    def test_devolucion(self, client):
        r1 = client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        prestamo_id = r1.json()["id"]
        r2 = client.post(f"/prestamos/{prestamo_id}/devolucion")
        assert r2.status_code == 200
        data = r2.json()
        assert data["prestamo"]["estado"] == "devuelto"
        assert data["multa"] is None

    def test_devolucion_404(self, client):
        r = client.post("/prestamos/INVALIDO/devolucion")
        assert r.status_code == 404

    def test_renovacion(self, client):
        r1 = client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E003"})
        prestamo_id = r1.json()["id"]
        fecha_original = r1.json()["fecha_devolucion_esperada"]
        r2 = client.post(f"/prestamos/{prestamo_id}/renovacion")
        assert r2.status_code == 200
        from datetime import datetime
        assert datetime.strptime(r2.json()["fecha_devolucion_esperada"], "%Y-%m-%d").date() == datetime.strptime(fecha_original, "%Y-%m-%d").date() + timedelta(days=15)

    def test_renovacion_ya_devuelto(self, client):
        r1 = client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        pid = r1.json()["id"]
        client.post(f"/prestamos/{pid}/devolucion")
        r2 = client.post(f"/prestamos/{pid}/renovacion")
        assert r2.status_code == 409

    def test_renovacion_404(self, client):
        r = client.post("/prestamos/INVALIDO/renovacion")
        assert r.status_code == 404

    def test_prestamos_vencidos(self, client):
        r = client.get("/prestamos/vencidos")
        assert r.status_code == 200
        assert isinstance(r.json(), list)


class TestEstudiantesAPI:
    def test_prestamos_estudiante(self, client):
        client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        r = client.get("/estudiantes/S001/prestamos")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_prestamos_estudiante_filtro_activo(self, client):
        r1 = client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E003"})
        pid = r1.json()["id"]
        client.post(f"/prestamos/{pid}/devolucion")
        r2 = client.get("/estudiantes/S001/prestamos?activo=true")
        assert len(r2.json()) == 1
        r3 = client.get("/estudiantes/S001/prestamos?activo=false")
        assert len(r3.json()) == 1

    def test_prestamos_estudiante_404(self, client):
        r = client.get("/estudiantes/INVALIDO/prestamos")
        assert r.status_code == 404

    def test_multas_estudiante(self, client):
        r = client.get("/estudiantes/S001/multas")
        assert r.status_code == 200
        assert r.json() == []

    def test_multas_estudiante_404(self, client):
        r = client.get("/estudiantes/INVALIDO/multas")
        assert r.status_code == 404

    def test_historial_estudiante(self, client):
        client.post("/prestamos", json={"estudiante_id": "S001", "ejemplar_id": "E001"})
        r = client.get("/estudiantes/S001/historial")
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_historial_estudiante_404(self, client):
        r = client.get("/estudiantes/INVALIDO/historial")
        assert r.status_code == 404
