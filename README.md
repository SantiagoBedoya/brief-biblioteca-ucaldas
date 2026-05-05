# Taller: De Cero con IA Agéntica — Construye, Audita, Valida

El brief tiene ambigüedades y suposiciones implícitas, igual que cualquier brief profesional.

Tu trabajo es recorrer todo el ciclo:

1. Convertir el brief en una especificación formal (escrita por ti, en Markdown).
2. Diseñar prompts para que una IA agéntica genere el proyecto desde cero.
3. Auditar el código que la IA generó.
4. Pedir tests con IA, sin caer en el círculo cerrado.
5. Detectar bugs y corregirlos iterando.

Al final del taller, sales con **un proyecto que tú mismo construiste con IA, pero entiendes línea por línea**. Esa es la diferencia entre un junior que vibe-codea y un Quality Guardian.

---

## Duración y modalidad

| Aspecto      | Detalle                                                                                                         |
|--------------|-----------------------------------------------------------------------------------------------------------------|
| Trabajo      | Individual                                                                                                      |
| Stack libre  | Tú decides el lenguaje y framework, entre las opciones: Node.js + Express, Python + FastAPI, Java + Spring Boot |
| IA agéntica libre | Claude Code, Cursor agent mode, Copilot Workspace, Windsurf                                                |

---

## Sistema de Préstamo de Libros — Biblioteca UCaldas

Tu cliente es la Biblioteca de la Universidad de Caldas. Te entrega un correo con un brief informal.

**El brief completo está en `01-contexto/brief-cliente.md`.** Léelo primero.

No te entregamos especificación formal. La especificación la vas a escribir tú interpretando el brief, identificando ambigüedades, tomando decisiones documentadas, y dejando claro qué le preguntarías al cliente real si tuvieras la oportunidad.

---

## Estructura del taller

```
taller-qa-agentico/
├── README.md                        ← este documento
├── 01-contexto/
│   ├── brief-cliente.md             El correo del cliente con su problema
│   └── instrucciones-entrega.md     Cómo debe quedar tu entrega final
├── 02-tu-trabajo/
│   ├── paso-a-paso.md               Las 6 etapas que vas a recorrer
│   ├── plantilla-especificacion.md  Esqueleto para que TÚ lo llenes
│   ├── plantilla-prompts.md         Para registrar los prompts que uses
│   └── plantilla-bitacora.md        Para registrar tus hallazgos
```

---

## Cronograma de las 2 horas

| Tiempo        | Etapa                                              | Entregable parcial                 |
|---------------|----------------------------------------------------|------------------------------------|
| 04:00 – 04:20 | Lectura del brief                                  | Brief leído y dudas planteadas     |
| 04:20 – 04:40 | Etapa 1 — Convertir el brief en especificación     | `especificacion.md` escrita        |
| 04:40 – 05:20 | Etapa 2 — Diseñar prompts y generar el proyecto con IA | Proyecto generado y arrancando |
| 05:20 – 05:40 | Etapa 3 — Auditoría humana del código generado     | Hallazgos                          |
| 05:40 – 06:00 | Etapa 4 — Generar tests con IA + auditarlos        | Suite de tests ejecutada           |
| 06:00 – 07:00 | Etapa 5 — Detectar y corregir bugs                 | Suite verde + diff de cambios      |

---

## Lo que tienes que entregar al final

Una carpeta con:

```
mi-entrega/
├── especificacion.md           Tu interpretación formal del brief
├── prompts/                    Cada prompt que usaste (numerado)
│   ├── 01-generacion-inicial.md
│   ├── 02-correccion-X.md
│   └── ...
├── proyecto/                   Código generado por la IA
│   └── (todos los archivos del proyecto)
├── tests/                      Tests generados por la IA
├── bitacora.md                 Hallazgos de auditoría y bugs encontrados
├── diff-de-correcciones.md     Qué cambiaste tú a mano vs qué te corrigió la IA
└── reflexion-final.md          Tres preguntas respondidas
```

El detalle de cada documento está en `01-contexto/instrucciones-entrega.md`.

---

## Las 3 reglas no negociables del taller

**Regla 1.** No copies código de la IA sin entenderlo. 

**Regla 2.** Cada prompt que uses queda registrado en la carpeta `prompts/`. Numerados, con fecha y propósito. Esto es **parte de la calificación**.

**Regla 3.** Si la IA te dice "todo está funcionando", lo verificas tú.

---

## Continúa en `01-contexto/brief-cliente.md`.
