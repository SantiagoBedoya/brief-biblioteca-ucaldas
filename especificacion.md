# Especificación Formal — Sistema de Préstamo de Libros

> **Autor:** Santiago Bedoya, Cristian Gonzalez
> **Fecha:** 05 de mayo de 2026
> **Versión:** 1.0
> **Brief de origen:** Correo de Diana Restrepo, Coordinadora de Biblioteca

---

## 1. Propósito del sistema

Sistema de gestión de préstamos de libros de la Biblioteca de la Universidad de Caldas que expone una API REST para consultar el catálogo, gestionar préstamos, devoluciones, renovaciones y multas, así como consultar historiales de estudiantes, inicialmente orientado a estudiantes de pregrado y posgrado.

---

## 2. Alcance

**Incluido en esta versión:**

- Consulta de catálogo de libros con filtros por disponibilidad, título, autor o sala.
- Registro de préstamos de ejemplares a estudiantes de pregrado y posgrado.
- Registro de devoluciones con cálculo automático de multas por retraso.
- Renovación de préstamos vigentes según disponibilidad del ejemplar.
- Consulta de préstamos vigentes, vencidos e historial de estudiantes.
- Gestión de multas acumuladas por estudiante.

**Explícitamente fuera del alcance:**

- Préstamos a profesores investigadores.
- Autenticación de usuarios.
- Interfaz frontend o integración con app móvil/portal de estudiantes.
- Persistencia en base de datos (datos en memoria).
- Gestión de otros recursos físicos de la biblioteca.

---

## 3. Modelo de datos

### Entidad: Libro

| Campo             | Tipo    | Obligatorio | Descripción                                  |
|-------------------|---------|-------------|----------------------------------------------|
| id                | string  | sí          | Código único de identificación del libro     |
| titulo            | string  | sí          | Título del libro                             |
| autor             | string  | sí          | Autor del libro                               |
| sala              | string  | sí          | Sala donde se ubica el libro en la biblioteca |
| es_alta_demanda   | boolean | sí          | Indica si el libro es de alta demanda (sala de reserva) |

### Entidad: Ejemplar

| Campo     | Tipo    | Obligatorio | Descripción                                  |
|-----------|---------|-------------|----------------------------------------------|
| id        | string  | sí          | Código único de inventario del ejemplar       |
| libro_id  | string  | sí          | Identificador del libro al que pertenece      |
| estado    | enum    | sí          | disponible, prestado, dañado                  |

### Entidad: Estudiante

| Campo     | Tipo    | Obligatorio | Descripción                                  |
|-----------|---------|-------------|----------------------------------------------|
| id        | string  | sí          | Código único del estudiante                   |
| nombre    | string  | sí          | Nombre completo del estudiante                |
| programa  | enum    | sí          | pregrado, posgrado                            |
| semestre  | number  | sí          | Semestre actual del estudiante                |

### Entidad: Préstamo

| Campo                | Tipo    | Obligatorio | Descripción                                  |
|----------------------|---------|-------------|----------------------------------------------|
| id                   | string  | sí          | Identificador único del préstamo              |
| estudiante_id        | string  | sí          | Identificador del estudiante                  |
| ejemplar_id          | string  | sí          | Identificador del ejemplar prestado           |
| fecha_prestamo       | date    | sí          | Fecha del préstamo                            |
| fecha_devolucion_esperada | date | sí      | Fecha máxima de devolución                    |
| fecha_devolucion_real| date    | no          | Fecha real de devolución                      |
| estado               | enum    | sí          | activo, devuelto, vencido                     |

### Entidad: Multa

| Campo             | Tipo    | Obligatorio | Descripción                                  |
|-------------------|---------|-------------|----------------------------------------------|
| id                | string  | sí          | Identificador único de la multa               |
| prestamo_id       | string  | sí          | Identificador del préstamo asociado           |
| monto             | number  | sí          | Monto total (2000 * días de retraso)          |
| estado            | enum    | sí          | pendiente, pagada                             |
| fecha_generacion  | date    | sí          | Fecha de generación de la multa                |

### Diagrama de relaciones

```
Libro 1 --- N Ejemplar
Estudiante 1 --- N Préstamo
Ejemplar 1 --- N Préstamo (a lo largo del tiempo)
Préstamo 1 --- 0..1 Multa
Préstamo N --- 1 Estudiante
Préstamo N --- 1 Ejemplar
```

---

## 4. Endpoints REST

| Método | Ruta | Propósito | Body / Query | Respuesta éxito | Códigos error posibles |
|---|---|---|---|---|---|
| `GET` | `/libros` | Listar catálogo | filtros opcionales: titulo, autor, sala, disponible | `200` con lista | - |
| `GET` | `/libros/:id` | Detalle de libro con ejemplares | - | `200` con objeto | `404` |
| `POST` | `/prestamos` | Crear préstamo | `{estudiante_id, ejemplar_id}` | `201` con préstamo | `400`, `404`, `409` |
| `POST` | `/prestamos/:id/devolucion` | Registrar devolución | - | `200` con préstamo y multa si aplica | `404`, `409` |
| `POST` | `/prestamos/:id/renovacion` | Renovar préstamo vigente | - | `200` con préstamo actualizado | `404`, `409` |
| `GET` | `/estudiantes/:id/prestamos` | Préstamos de estudiante | query: `activo=true/false` | `200` con lista | `404` |
| `GET` | `/prestamos/vencidos` | Listar préstamos vencidos | - | `200` con lista | - |
| `GET` | `/estudiantes/:id/multas` | Multas de estudiante | - | `200` con lista | `404` |
| `GET` | `/estudiantes/:id/historial` | Historial de préstamos | - | `200` con lista histórica | `404` |

---

## 5. Reglas de negocio

### RN1 — Límite de préstamos por tipo de estudiante

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:**
  - Estudiante de pregrado: máximo 3 préstamos con `estado = "activo"`.
  - Estudiante de posgrado: máximo 5 préstamos con `estado = "activo"`.
- **Acción si cumple:** continuar con el flujo de creación.
- **Acción si no cumple:** retornar `409 Conflict` con `{error: "limite_prestamos_alcanzado", limite: N, actuales: M}`.

### RN2 — Plazo de préstamo según tipo de libro

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:**
  - Libro de alta demanda: plazo de 3 días.
  - Libro estándar: plazo de 15 días.
- **Acción si cumple:** calcular `fecha_devolucion_esperada` sumando el plazo a `fecha_prestamo`.
- **Acción si no cumple:** no aplica.

### RN3 — No préstamo si tiene préstamos vencidos

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:** el estudiante no tiene préstamos con `estado = "vencido"`.
- **Acción si cumple:** continuar con el flujo.
- **Acción si no cumple:** retornar `409 Conflict` con `{error: "prestamo_vencido_pendiente"}`.

### RN4 — Ejemplar debe estar disponible

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:** el ejemplar tiene `estado = "disponible"`.
- **Acción si cumple:** marcar ejemplar como `prestado`.
- **Acción si no cumple:** retornar `409 Conflict` con `{error: "ejemplar_no_disponible"}`.

### RN5 — Renovación de préstamo condicionada

- **Trigger:** al recibir `POST /prestamos/:id/renovacion`.
- **Condición:**
  - Préstamo tiene `estado = "activo"` y no está vencido.
  - No hay solicitudes pendientes para el ejemplar asociado.
- **Acción si cumple:** extender `fecha_devolucion_esperada` según plazo original (3 o 15 días).
- **Acción si no cumple:** retornar `409 Conflict` con `{error: "renovacion_no_permitida", motivo: "..."}`.

### RN6 — Cálculo de multas por retraso

- **Trigger:** al recibir `POST /prestamos/:id/devolucion`.
- **Condición:** `fecha_devolucion_real` > `fecha_devolucion_esperada`.
- **Acción si cumple:** generar multa con monto `2000 * días de retraso`.
- **Acción si no cumple:** no generar multa.

### RN7 — No préstamo si tiene multas pendientes

- **Trigger:** al recibir `POST /prestamos`.
- **Condición:** el estudiante no tiene multas con `estado = "pendiente"`.
- **Acción si cumple:** continuar con el flujo.
- **Acción si no cumple:** retornar `409 Conflict` con `{error: "multa_pendiente"}`.

---

## 6. Decisiones tomadas (lo que el correo no dice)

### D1 — Cálculo de días para multa

- **Contexto:** el correo no precisa si los días de retraso son calendario o hábiles.
- **Decisión:** usar días calendario.
- **Justificación:** interpretación más simple, alineada con estándares de bibliotecas.

### D2 — Estado de ejemplares dañados

- **Contexto:** el correo no cubre ejemplares no aptos para préstamo.
- **Decisión:** añadir estado `dañado` a la entidad Ejemplar.
- **Justificación:** permite gestionar ejemplares temporalmente no prestables.

### D3 — Renovación conserva plazo original

- **Contexto:** el correo indica que la renovación da 15 o 3 días según tipo, pero no especifica si usa el plazo original.
- **Decisión:** la renovación extiende la fecha esperada con el mismo plazo del préstamo original.
- **Justificación:** evita confusiones y mantiene consistencia.

### D4 — Multas asociadas a préstamo específico

- **Contexto:** el correo dice que la multa se acumula al historial del estudiante, pero no especifica estructura.
- **Decisión:** cada multa se asocia a un único préstamo.
- **Justificación:** facilita trazabilidad y cobro por préstamo.

### D5 — Sin autenticación en esta versión

- **Contexto:** el correo no menciona autenticación.
- **Decisión:** no implementar autenticación.
- **Justificación:** alineado con alcance reducido y tiempo límite de una semana.

### D6 — Persistencia en memoria

- **Contexto:** el correo especifica explícitamente manejar datos en memoria.
- **Decisión:** usar estructuras en memoria (arrays/objetos).
- **Justificación:** requisito explícito del cliente hasta obtener presupuesto para base de datos.

---

## 7. Códigos HTTP usados

| Código | Significado | Cuándo se usa |
|---|---|---|
| 200 | OK | GET exitosos |
| 201 | Created | POST exitosos que crean recursos |
| 400 | Bad Request | Body malformado o validación fallida |
| 404 | Not Found | Recurso no existe |
| 409 | Conflict | Reglas de negocio violadas |
| 500 | Internal Server Error | Error no controlado del servidor |

---

## 8. Restricciones técnicas

- **Stack:** Python + FastAPI
- **Persistencia:** datos en memoria. No usar base de datos.
- **Sin autenticación** en esta versión.
- **Sin frontend** en esta versión. Solo API REST.