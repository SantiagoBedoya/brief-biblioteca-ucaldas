# Las 6 Etapas del Taller — Tu Hoja de Ruta

**Lee esto antes de empezar.** Es tu mapa de las próximas 4 horas.

---

## Etapa 1 — De brief a especificación (40 minutos)

**Inicio:** ya leíste el brief de la cliente. Ahora lo conviertes en un documento técnico.

**Lo que NO debes hacer todavía:** abrir tu IA. Ni siquiera para preguntarle "ayúdame con la especificación". Si saltas este paso, todo lo demás se cae.

**Lo que SÍ debes hacer:**

1. **Léelo dos veces.** En la primera lectura, anota qué entiendes. En la segunda, anota qué te queda dudoso.

2. **Identifica entidades y relaciones.** ¿Qué objetos del mundo real aparecen? Libro, ejemplar, estudiante, préstamo, multa... ¿Cómo se relacionan? Un libro tiene varios ejemplares. Un estudiante tiene varios préstamos.

3. **Convierte cada frase del correo en una regla de negocio numerada.** Por ejemplo:

   - Frase del correo: "Los estudiantes pueden tener máximo 3 libros prestados al mismo tiempo."
   - Regla técnica: "RN1. Un estudiante de pregrado no puede tener más de 3 préstamos con `estado = activo` simultáneamente. Si lo intenta, la API devuelve 409 Conflict."

4. **Lista las ambigüedades.** Son tus preguntas para la cliente. Mínimo 3, idealmente 5 o más. Por ejemplo:

   - "¿La multa por día se cobra incluyendo días no hábiles (sábados, domingos, festivos) o solo días hábiles?"
   - "Cuando un estudiante de pregrado pasa a posgrado, ¿su límite de préstamos cambia automáticamente o requiere algún proceso?"
   - "Si un libro tiene 5 ejemplares y 3 están prestados, ¿el catálogo lo muestra como 'disponible' o como 'parcialmente disponible'?"

5. **Toma decisiones documentadas.** Como la cliente no está disponible, tienes que decidir tú. Pero **declaras qué decidiste y por qué**. Por ejemplo:

   - "DECISIÓN D1: Asumimos que los días de retraso para multa se cuentan como días calendario, no hábiles. Razón: el correo no precisa, y es la interpretación más simple."
   - "DECISIÓN D2: Si un estudiante intenta renovar y otro estudiante está esperando, devolvemos código 409 con mensaje 'no_renovable_lista_espera'. Razón: el correo dice que no se puede renovar, pero no especifica el código HTTP."

6. **Define los endpoints.** Lista cada ruta REST con método HTTP, parámetros y respuestas. Sé específico.

**Entregable de esta etapa:** `especificacion.md` lista para usar como input de la IA.

**Cómo saber si está bien:** dale a un compañero tu especificación y pídele que te diga si podría construir el sistema solo con eso. Si te pregunta "¿y qué hago si...?", probablemente te falta cubrir ese caso.

---

## Etapa 2 — Generación con IA agéntica (50 minutos)

**Inicio:** tienes tu `especificacion.md` lista.

**Lo que NO debes hacer:** copiar y pegar todo el correo de la cliente como prompt. La IA va a tomar 100 decisiones implícitas.

**Lo que SÍ debes hacer:**

1. **Prepara el prompt inicial.** Antes de mandar nada, escríbelo en un editor. El prompt debe contener:

   - **Stack técnico:** "Node.js + Express, datos en memoria, sin base de datos, sin TypeScript."
   - **Estructura del proyecto:** carpetas y archivos esperados.
   - **Endpoints exactos:** copia-pega de tu especificación.
   - **Modelo de datos:** copia-pega de tu especificación.
   - **Reglas de negocio numeradas:** copia-pega de tu especificación.
   - **Restricciones explícitas:** lo que la IA **no** debe hacer ("no generes tests todavía", "no agregues dependencias adicionales", "no uses base de datos").
   - **Rendición de cuentas:** "al terminar, lista qué reglas implementaste y cómo."

2. **Guarda este prompt** como `prompts/01-generacion-inicial.md` antes de enviarlo.

3. **Envía el prompt y deja trabajar a la IA.** Si es Claude Code, Cursor o Copilot Workspace en modo agente, va a crear archivos por ti. Si es ChatGPT o similar, te va a dar bloques de código que copies a archivos.

4. **Verifica que el proyecto arranca.**

   ```bash
   npm install
   npm start
   ```

   Si hay errores, **antes** de pedir corrección a la IA: léelos y entiende qué dicen.

5. **Haz 3 llamados básicos** con `curl` o Postman para confirmar que la API responde:

   - Crear un libro o consultar el catálogo.
   - Crear un préstamo.
   - Listar préstamos.

6. **Si algo falla**, prepara un prompt de corrección. Específico, acotado, con la línea o endpoint afectado. Guárdalo como `prompts/02-correccion-XXX.md`.

**Cuándo terminar:** el proyecto arranca y los 3 llamados básicos funcionan. No esperes que esté perfecto. La perfección viene en la siguiente etapa.

---

## Etapa 3 — Auditoría humana (35 minutos)

**Inicio:** tienes un proyecto que arranca. Hora de leerlo con desconfianza profesional.

**Lo que NO debes hacer:** asumir que el código está bien porque la IA dijo que sí. **Asumir** que está mal hasta probar lo contrario.

**Lo que SÍ debes hacer:**

1. **Vuelta de inventario (5 min):** ¿qué archivos creó la IA? ¿qué dependencias instaló? ¿hay archivos o dependencias que no pediste? Lista en tu bitácora.

2. **Vuelta regla por regla (15 min):** abre tu `especificacion.md` en una pantalla y el código en otra. Para cada regla RN1, RN2, RN3..., busca dónde se aplica en el código.

   Llena esta tabla en tu `bitacora.md`:

   | Regla | Archivo y línea donde se aplica | ¿Aplica correctamente? | Notas |
   |---|---|---|---|
   | RN1 — máx 3 préstamos pregrado | rutas/prestamos.js línea X | Sí / No / Parcial | |
   | RN2 — plazo según tipo libro | | | |
   | RN... | | | |

   **Si una regla no aparece en el código**, esa regla no está implementada. Anótalo.

3. **Vuelta adversarial (10 min):** para cada función/endpoint, pregúntate:

   - ¿Qué pasa si la entrada es `null`?
   - ¿Qué pasa con valores de borde? (cantidad 0, fecha en el pasado, plazo negativo)
   - ¿La operación es idempotente?
   - ¿Los códigos HTTP son correctos?

4. **Vuelta con IA como auditora (5 min):** ahora le pides a la misma IA que generó el código que **se audite a sí misma**:

   ```
   Te paso este código que generaste hace un rato. Audítalo desde
   la perspectiva de un QA senior adversarial.

   Especificación de referencia:
   [pegar tus reglas RN1, RN2... ]

   Código:
   [pegar archivos relevantes]

   INSTRUCCIONES:
   - No me sugieras correcciones todavía. Solo el diagnóstico.
   - Para cada hallazgo: archivo, línea, tipo de problema, escenario que lo dispara.
   - Si una función está bien, dilo: "Función X no presenta hallazgos."
   - No inventes problemas que no existen.
   ```

   Guarda el prompt en `prompts/03-auditoria-con-ia.md`.

5. **Validación cruzada:** la IA te devuelve hallazgos. Tu trabajo: ¿cuáles son reales? ¿cuáles son inventados? ¿cuáles ya tenías tú? ¿cuáles te faltaron?

**Entregable de esta etapa:** sección de hallazgos completa en tu `bitacora.md`.

---

## Etapa 4 — Tests con IA (35 minutos)

**Inicio:** tienes el código auditado y una lista de hallazgos. Ahora vienen los tests.

**Lo que NO debes hacer:** decirle "genérame tests para el código". Va a generar tests confirmatorios que pasen al 100% sin detectar nada.

**Lo que SÍ debes hacer:**

1. **Prompt anclado a la especificación, no al código.**

   ```
   Voy a generar tests de integración con [Jest+Supertest / pytest+httpx / etc.]
   para una API que cumple esta especificación:

   REGLAS:
   RN1. [tu regla 1]
   RN2. [tu regla 2]
   ...

   CONTEXTO TÉCNICO:
   - [tu stack]
   - El servidor exporta una instancia en [archivo]
   - Datos en memoria; necesito resetear entre tests

   INSTRUCCIONES:
   - UN test por cada regla de negocio.
   - Patrón AAA en cada uno.
   - Nombra cada test referenciando la regla:
     test_RN1_estudiante_pregrado_no_puede_tener_4_prestamos_activos
   - Cada test debe ANCLAR a la regla, no al código. Es decir, debe pasar
     contra cualquier implementación correcta de la regla.
   - No me sugieras tests adicionales fuera de las reglas.
   - Pruebas de integración contra el servidor real, sin mocks.

   Lista al final qué regla cubre cada test.
   ```

   Guárdalo como `prompts/04-tests-reglas-negocio.md`.

2. **Ejecuta los tests.** Lo más probable es que **algunos fallen**. Cada fallo es:

   - **Fallo legítimo:** el código no cumple esa regla → es un bug real → anótalo en `bitacora.md`.
   - **Fallo del test:** el test está mal escrito → corrige el test.

   Distinguir entre ambos es lo que un QA senior hace. Lee el `AssertionError`, entiende qué se esperaba, qué pasó. Decide cuál de las dos categorías aplica.

3. **Pide tests adicionales adversariales:**

   ```
   Ahora genera tests específicos para casos límite y entradas inválidas.
   Para cada endpoint:
   - Body vacío.
   - Campos obligatorios faltantes.
   - Tipos incorrectos (string donde se esperaba número, etc.).
   - Recurso no existente.
   - Operación con un usuario o libro inexistente.

   Cada test debe esperar un código HTTP específico (400, 404, 409).
   ```

   Guárdalo como `prompts/05-tests-validacion.md`.

4. **Ejecuta todos los tests juntos.** Anota cuántos pasan y cuántos fallan.

**Entregable de esta etapa:** carpeta `tests/` con la suite y el resultado de la última ejecución registrado en `bitacora.md`.

---

## Etapa 5 — Bugs y correcciones (30 minutos)

**Inicio:** tienes una suite de tests con algunos fallos legítimos.

**Lo que NO debes hacer:** decirle a la IA "arregla todos los bugs". Va a tocar archivos que no debería.

**Lo que SÍ debes hacer:**

1. **Para cada bug confirmado**, prepara un prompt de corrección quirúrgica:

   ```
   Tengo este bug confirmado:

   [pegar el test fallando + AssertionError]

   Y este código:
   [pegar SOLO la función afectada, no el archivo completo]

   La regla violada según la especificación es:
   [pegar la regla]

   Genera el parche mínimo para esa función. Solo la línea o líneas
   modificadas. No reescribas la función completa. No me sugieras
   refactorizaciones adicionales.
   ```

   Guarda el prompt como `prompts/06-fix-bug-X.md`.

2. **Aplica el parche.** Léelo antes de pegarlo. Si entiendes lo que hace, lo aceptas. Si no, le pides a la IA que lo explique.

3. **Re-ejecuta los tests.** El test que documentaba el bug ahora debe pasar. Si **otro** test que antes pasaba ahora falla, la corrección rompió algo (regresión). Anótalo y corrígelo.

4. **Itera hasta que la suite esté verde.** Si hay algún bug que no alcanzas a corregir, **declárelo explícitamente** en tu `bitacora.md` con justificación.

5. **Llena el `diff-de-correcciones.md`** con cada cambio aplicado: archivo, línea, descripción, hecho por IA o por ti.

**Entregable de esta etapa:** suite verde (o con fallos declarados) y `diff-de-correcciones.md` lleno.

---

## Etapa 6 — Defensa oral (15 minutos por estudiante)

**Inicio:** el docente te llama. Tu pantalla está compartida con tu proyecto.

**Lo que va a pasar:**

1. **Demostración (3 min).** Arrancas tu API y haces 2 llamados con `curl` o Postman. Muestras que funciona.

2. **Lectura crítica (5 min).** El docente señala una línea de tu código (al azar) y te pregunta:

   - ¿Qué hace esta línea?
   - ¿Por qué está aquí?
   - ¿La escribiste tú o la IA?
   - Si fue la IA, ¿la entendiste antes de aceptarla?

   Si no puedes explicar una línea, esa línea cuenta como deuda.

3. **Pregunta de reflexión (3 min).** El docente toma una de las 3 preguntas de tu `reflexion-final.md` y te pide elaborar.

4. **Hallazgos (4 min).** El docente lee tu `bitacora.md` por encima y te pregunta sobre 1 o 2 bugs que reportaste.

**Cómo lucirte:**

- Conoce los nombres de los bugs que encontraste y dónde estaban.
- Ten claro qué decisiones tomaste durante la Etapa 1 y por qué.
- Recuerda al menos 1 prompt que cambiaste a mitad del taller (qué prompt original usaste, qué prompt nuevo escribiste, qué cambió).

---

## Resumen visual

```
[00:00] Lee brief
   ↓
[00:20] Etapa 1 — Especificación (40 min)
   ↓
[01:00] Etapa 2 — Generación con IA (50 min)
   ↓
[01:50] Pausa (15 min)
   ↓
[02:05] Etapa 3 — Auditoría (35 min)
   ↓
[02:40] Etapa 4 — Tests con IA (35 min)
   ↓
[03:15] Etapa 5 — Bugs y correcciones (30 min)
   ↓
[03:45] Etapa 6 — Defensa oral (15 min)
   ↓
[04:00] FIN
```

Cada etapa que saltas, debilita la siguiente. La especificación de la Etapa 1 es lo que ancla los tests de la Etapa 4. La auditoría de la Etapa 3 es lo que detecta los bugs que la Etapa 5 corrige. **Es un sistema. No funciona en pedazos.**
