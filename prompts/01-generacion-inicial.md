# Registro de Prompts

## Prompt #1

**Fecha y hora:** 2026-05-12 17:23

**Propósito en una línea:** Generar la estructura inicial del proyecto con una API REST en FastAPI para gestionar préstamos de libros.

**Etapa del taller:** 1

**IA usada:** Claude Code

---

### Prompt enviado (literal)

```
crea una carpeta proyecto-v1  en la raíz de la carpeta brief-biblioteca-ucaldas , construye una API REST en python con fastApi para gestionar préstamos de libros en una biblioteca universitaria.
Necesito endpoints para listar libros, crear préstamos, devolver libros y consultar préstamos vigentes. Usa datos en memoria.
```

---

### Resumen de la respuesta de la IA

Creó 3 archivos: `proyecto-v1/main.py`, `proyecto-v1/run.py`, `proyecto-v1/requirements.txt`. No instaló dependencias nuevas (ya estaban en el sistema). Tomó la decisión de agregar endpoints extra no pedidos explícitamente: `GET /libros/disponibles`, `GET /libros/{id}`, `GET /prestamos`, `GET /prestamos/{id}`. Populó la base de datos en memoria con 5 libros de ejemplo. Verificó que el servidor arrancaba y el endpoint `/libros` respondía correctamente antes de reportar éxito.

---

### Mi evaluación

**¿La respuesta cumplió con lo que pedí?**

- [X] Completamente.
- [ ] Parcialmente. Faltó: [...]
- [ ] No, se desvió. Hizo: [...]

**¿La acepté tal cual o la modifiqué?**

- [X] Tal cual.
- [ ] La modifiqué a mano. Cambios: [...]
- [ ] Le pedí corrección con un prompt nuevo (ver prompt #[N+1]).
- [ ] La rechacé completamente. Razón: [...]

**¿Qué aprendí de esta interacción?**

[Una línea sobre qué te llevaste de este prompt.]
