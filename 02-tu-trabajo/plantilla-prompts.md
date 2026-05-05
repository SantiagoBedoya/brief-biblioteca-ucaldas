# Plantilla — Registro de Prompts

> **Cómo usar esta plantilla:** copia este archivo y renómbralo `01-generacion-inicial.md`, `02-correccion-X.md`, etc. Llena un archivo por cada prompt que envíes a la IA.

---

## Prompt #[número]

**Fecha y hora:** [YYYY-MM-DD HH:MM]

**Propósito en una línea:** [Por ejemplo: "Generar la estructura inicial del proyecto" o "Corregir la validación de fechas en el endpoint POST /prestamos"]

**Etapa del taller:** [1 / 2 / 3 / 4 / 5]

**IA usada:** [Claude Code / Cursor / Copilot Workspace / ChatGPT / etc.]

---

### Prompt enviado (literal)

```
[Pega aquí el prompt EXACTO que enviaste a la IA. No lo edites para que se vea mejor. Pega lo que escribiste, errores de tipeo incluidos.]
```

---

### Resumen de la respuesta de la IA

[En 3 a 5 líneas, describe qué hizo la IA. NO pegues toda la respuesta. Solo:

- Qué archivos creó o modificó.
- Qué dependencias instaló (si hubo).
- Qué decisiones tomó que tú no le pediste.
- Si dijo "todo está funcionando" o si admitió alguna limitación.

Ejemplo:
> Creó 3 archivos: app.js, modelos/prestamo.js, rutas/prestamos.js. Instaló express y body-parser. Tomó la decisión de usar moment.js para manejar fechas (no se lo pedí). Dijo que todo está funcionando.]

---

### Mi evaluación

**¿La respuesta cumplió con lo que pedí?**

- [ ] Completamente.
- [ ] Parcialmente. Faltó: [...]
- [ ] No, se desvió. Hizo: [...]

**¿La acepté tal cual o la modifiqué?**

- [ ] Tal cual.
- [ ] La modifiqué a mano. Cambios: [...]
- [ ] Le pedí corrección con un prompt nuevo (ver prompt #[N+1]).
- [ ] La rechacé completamente. Razón: [...]

**¿Qué aprendí de esta interacción?**

[Una línea sobre qué te llevaste de este prompt. Por ejemplo:

> "Si no le digo explícitamente 'no instales dependencias adicionales', la IA siempre mete una librería de fechas sin preguntar."

> "El prompt era demasiado corto. La IA tuvo que adivinar el modelo de datos y se equivocó."]

---

## Plantilla en blanco (copiar para cada prompt nuevo)

Crea un archivo nuevo cada vez que mandes un prompt. No acumules todos los prompts en un solo archivo.

```
01-generacion-inicial.md
02-correccion-validacion-fechas.md
03-tests-reglas-negocio.md
04-correccion-bug-cupo.md
05-...
```

El docente va a leer esta carpeta para ver tu evolución como vibecoder consciente.
