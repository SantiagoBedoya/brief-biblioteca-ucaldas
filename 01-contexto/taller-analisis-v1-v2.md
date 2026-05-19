**Requisitos previos:** Haber explorado los proyectos `proyecto-v1` y `proyecto-v2` del repositorio

---

## Contexto

Durante este taller trabajarás con dos versiones de la misma API REST para gestión de préstamos de una biblioteca universitaria.

- **`proyecto-v1`** — Implementación simple en JavaScript con Express o . Sin validaciones formales, sin arquitectura en capas, sin tests.
- **`proyecto-v2`** — Implementación en TypeScript con Clean Architecture, validaciones con Zod, manejo de errores tipado y suite completa de tests unitarios e integración.

El objetivo no es determinar cuál versión es "mejor", sino comprender qué impacto tiene la estructura del código sobre la capacidad de probarlo.

---

## Antes de empezar

Levanta ambos servidores en terminales separadas:

```bash
# Terminal 1
cd proyecto-v1
node src/index.js
```

```bash
# Terminal 2
cd proyecto-v2
npm run dev
```

Verifica que ambos respondan:

```bash
curl http://localhost:3000/
curl http://localhost:3001/
```

---

## Bloque 1 — Lectura y comparación estructural

### Ejercicio 1.1 — Inventario de diferencias

Recorre ambos proyectos y completa la siguiente tabla en tu bitácora:

| Dimensión | v1 | v2 |
|---|---|---|
| Lenguaje | | |
| Validación de entradas al servidor | | |
| Manejo de errores HTTP | | |
| Arquitectura (número de capas) | | |
| Tests incluidos | | |
| Tipado de datos | | |
| Forma de iniciar la aplicación | | |

### Ejercicio 1.2 — Rastreo de una regla de negocio

Localiza la **RN1: límite de préstamos simultáneos por tipo de estudiante** en ambas versiones y responde:

1. ¿En qué archivo está en v1? ¿En cuántas líneas se implementa?
   - La IA no implemento la regla de negocio 1
2. ¿En qué archivo(s) está en v2? ¿Qué capas atraviesa?
   - Version 2: La regla de negocio se encuentra en el archivo `src/application/use_cases.py:110`, va de la linea 110 a 118, ocupa 9 lineas en total
   - Atraviesa las rama de infraestructura.persistencia para obtener el estudiante y obtener información del prestamos, la capa de aplicación para el caso de uso `crear_prestamo` (contiene la logica de esta regla) y la capa de dominio, este evalua los atributos de las entidades (programa, estado del prestamo)
3. Si el cliente pide cambiar el límite de pregrado de 3 a 4, ¿cuántos archivos hay que modificar en cada versión?
   - Version 1: Implementar toda la regla de negocio
   - Version 2: Hay que modificar 2 archivos: `src/application/use_cases.py:112` — la lógica de negocio y `tests/test_application.py:83` — el test que afirma
4. ¿Cómo sabrías que el cambio no rompió nada en cada versión?
   - Como primera medida, ejecutar los unit tests, esto indicaria que los componentes hacen lo esperado, pero mas que los unit tests, lo mejor seria realizar pruebas funcionales o pruebas E2E, para revisar que el sistema en funcionamiento si haga lo que se pide

---

## Bloque 2 — Análisis de calidad y comportamiento ante errores

**Modalidad:** Parejas
**Tiempo:** 30 minutos

### Ejercicio 2.1 — El request que no debería funcionar

Ejecuta el siguiente comando contra **v1**:

```bash
curl -s -X POST http://localhost:3000/api/prestamos \
  -H "Content-Type: application/json" \
  -d '{"estudianteId": "NO-EXISTE", "ejemplarId": "abc"}' | jq
```

Luego ejecuta el mismo request contra **v2** (ajusta el puerto si es necesario).

Responde en tu bitácora:

1. ¿Qué código HTTP devuelve cada versión?
   - En la version 1: Retorna un status 404 not found.
   - En la version 2: Retorno un status 404 not found
2. ¿Qué información contiene el cuerpo de la respuesta en cada caso?
   - Version 1:
     ```
     {
       "detail": "Not Found"
     }
     ```
   - Version 2:
     ```
     {
       "detail": "Not Found"
     }
     ```
3. ¿Cuál respuesta es más útil para un cliente que consume la API?
   - Ambas respuestas son validas, aunque sean un poco ambiguas y no diga exactamente que es lo que no encuentra (estudiante o ejemplar), sigue indicando cual es la causa raiz de que falla.
4. ¿Qué pasa en v1 si `ejemplarId` llega como string en lugar de número? ¿Y en v2?
   - En version 1: La respuesta sigue siendo igual, un status 404 not found con el mismo cuerpo de respuesta
   - En version 2: La respuesta sigue siendo igual, un status 404 not found con el mismo cuerpo de respuesta

### Ejercicio 2.2 — Comparar errores de dominio

Provoca el mismo error de negocio en ambas versiones: intenta prestar un ejemplar que ya está prestado.

Pasos sugeridos:
1. Crea un préstamo con el ejemplar 1
2. Intenta crear otro préstamo con el mismo ejemplar 1

> Para la version 1, no se cuenta con prestamos a nivel de ejemplares, solo a nivel de libros. Por lo que haremos el ejercicio con este funcionamiento

Registra y compara:

| Aspecto | v1 | v2 |
|---|---|---|
| Código HTTP | 409 Conflict | 409 Conflict |
| Campo `error` en la respuesta | `{"detail":"El libro no está disponible para préstamo"}` | `{"detail":{"error":"ejemplar_no_disponible"}}` |
| Mensaje legible | SI | SI |
| Información adicional (detalles) | SI | Si, dice el detalle del error |
| ¿Expone información interna del servidor? | NO | NO |

---

## Bloque 3 — Análisis de los tests de v2

### Ejercicio 3.1 — Lectura de un test unitario

Abre el archivo `proyecto-v2/tests/unit/CrearPrestamo.test.ts` y responde:

1. ¿Qué técnica de aislamiento se usa? (mocks, stubs, fakes, spies)
2. ¿Se levanta algún servidor HTTP para ejecutar este test? ¿Por qué importa esto?
4. Identifica en qué línea(s) del archivo se prueba la **RN4** (multa pendiente) y la **RN3** (préstamos vencidos pendientes).
5. ¿Cuánto tiempo tarda en ejecutarse este test? Corre `npm

---

## Bloque 4 — Escritura de tests


### Ejercicio 4.1 — Un test que v1 no puede tener con la misma velocidad

En `proyecto-v2`, escribe un test unitario para `CrearPrestamo` que verifique que un estudiante de **posgrado** puede tener hasta 5 préstamos simultáneos pero falla al intentar el sexto.

Plantilla de inicio:

```typescript
it('RN1 — posgrado falla al intentar el sexto préstamo', async () => {
  const vigentes: Prestamo[] = Array.from({ length: 5 }, (_, i) => ({
    // completa los campos necesarios
  }));
  // construye el caso de uso con los repos mockeados
  // verifica que lanza LimitePrestamosAlcanzado
});
```

Una vez terminado, reflexiona: ¿por qué sería más lento o difícil escribir este test en v1?
