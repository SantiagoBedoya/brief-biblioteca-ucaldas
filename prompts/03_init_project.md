# Registro de Prompts

## Prompt #3

**Fecha y hora:** 2026-05-12 17:30

**Propósito en una línea:** Inicializar proyecto backend con Clean Architecture + FastAPI basado en la especificación formal del sistema de préstamos.

**Etapa del taller:** 2

**IA usada:** Claude Code (opencode)

---

### Prompt enviado (literal)

```
**Rol:** Actúa como un Ingeniero de Software Senior experto en Python, FastAPI y Arquitectura Limpia (Clean Architecture).

**Tarea:** Tu objetivo es inicializar y estructurar un proyecto backend basándote *exclusivamente* en los requerimientos que te proporcionaré en el documento `@especificación.md`.

**Stack Tecnológico y Restricciones:**
* **Backend:** Python con FastAPI.
* **Base de Datos:** En memoria (ej. SQLite `:memory:` o diccionarios nativos, según sea más eficiente para la especificación).
* **Testing:** `pytest`.
* **Restricciones Estrictas:** NO implementes ningún tipo de autenticación en los endpoints. NO implementes ni sirvas ningún Frontend en esta versión.

**Reglas de Desarrollo:**
1. **Arquitectura:** Aplica los principios de Arquitectura Limpia (Clean Architecture). Respeta la estructura de carpetas que definamos; si la especificación no dicta una, propón una organización modular e independiente de los frameworks.
2. **Cero Alucinaciones:** Limítate estrictamente a la especificación. No inventes, asumas, ni agregues funcionalidades o campos de base de datos que no estén explícitamente documentados.
3. **Resolución de Ambigüedades:** Si encuentras algo ambiguo, contradictorio o faltante en `especificación.md`, detente inmediatamente. Hazme una lista de preguntas claras para resolver la ambigüedad antes de escribir cualquier código de implementación.

**Flujo de Trabajo (Sigue estos pasos en orden):**
* **Paso 1 (Estructura):** Genera un árbol de archivos visual (ASCII) mostrando la estructura completa del proyecto. **Detente aquí y pregúntame si apruebo la estructura antes de continuar.**
* **Paso 2 (Configuración):** Una vez que yo apruebe el árbol, genera el contenido de los archivos de configuración iniciales: `README.md`, `.gitignore` y `.env`.
* **Paso 3 (Documentación del Prompt):** Crea un archivo dentro de la carpeta `prompts/` (ej. `prompts/01_init_project.md`) que contenga exactamente este prompt inicial para mantener el registro, siguiendo el formato estándar de prompts del proyecto. @02-tu-trabajo/plantilla-prompts.md
* **Paso 4 (Implementación):** Espera mi orden para comenzar a implementar la lógica de negocio y los endpoints.
```

---

### Resumen de la respuesta de la IA

Creó la carpeta `proyecto-v2/` con la estructura completa de Clean Architecture (domain, application, infrastructure, presentation, tests). Generó 11 archivos de configuración e inicialización: `README.md`, `.gitignore`, `.env`, `requirements.txt`, `pytest.ini`, y los `__init__.py` de cada módulo. Aceptó la corrección de mover el registro del prompt a la carpeta `prompts/` existente en lugar de dentro del proyecto. Dejó `src/domain/`, `src/application/`, `src/infrastructure/`, `src/presentation/` y `tests/` vacíos listos para implementar.

---

### Mi evaluación

**¿La respuesta cumplió con lo que pedí?**

- [ ] Completamente.
- [x] Parcialmente. Faltó: Tuve que indicar que proceediera con la Implementación
- [ ] No, se desvió. Hizo: [...]

**¿La acepté tal cual o la modifiqué?**

- [ ] Tal cual.
- [X] La modifiqué a mano. Cambios: Corregi la ruta del prompt e indique que proceediera con la Implementación
- [ ] Le pedí corrección con un prompt nuevo (ver prompt #[N+1]).
- [ ] La rechacé completamente. Razón: [...]

**¿Qué aprendí de esta interacción?**

La IA es mas precisa si pregunta lo ambiguo
