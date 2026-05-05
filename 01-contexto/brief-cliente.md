# Correo del cliente — Sistema de Préstamo de Libros

> **Para:** Equipo de Desarrollo
> **De:** Coordinadora de Biblioteca, Universidad de Caldas
> **Asunto:** Necesitamos modernizar los préstamos de libros

---

Hola equipo,

Espero que estén bien. Les escribo porque la biblioteca está colapsada con el sistema actual de préstamos. Todavía estamos llevando todo en una hoja de cálculo y eso ya no es sostenible. Necesitamos urgentemente un sistema que nos permita gestionar los préstamos de libros desde una API, para luego conectarla a la app móvil y al portal de estudiantes.

Les cuento más o menos cómo funciona la biblioteca para que entiendan:

Tenemos varios miles de libros catalogados. Cada libro tiene un código único de inventario, título, autor y se ubica en una sala. Algunos libros tienen varios ejemplares disponibles, otros solo uno. Cuando un estudiante quiere prestar un libro, viene a la biblioteca con su carnet, busca el libro y la persona en el mostrador registra el préstamo. El estudiante se lleva el libro físicamente. Después tiene que devolverlo en el plazo acordado.

Lo que necesitamos que la API permita hacer:

- Consultar el catálogo de libros y ver cuáles están disponibles para préstamo.
- Que un estudiante pueda solicitar el préstamo de un libro.
- Que registremos la devolución cuando el libro vuelve.
- Que podamos ver qué estudiantes tienen préstamos vigentes.
- Que el sistema nos avise sobre los préstamos vencidos.

Algunas reglas importantes que tenemos en la biblioteca:

Los estudiantes pueden tener máximo 3 libros prestados al mismo tiempo. Si ya tienen 3, no se les puede prestar uno más hasta que devuelvan alguno.

El plazo del préstamo depende del tipo de libro. La mayoría son por 15 días, pero los libros de la sala de reserva (los más solicitados, que están marcados como "alta demanda") solo se prestan por 3 días, porque otros estudiantes también los necesitan rápido.

Si un estudiante tiene un préstamo vencido sin devolver, no puede pedir más libros prestados. Tiene que primero ponerse al día.

Cuando un libro está en préstamo, no puede prestarse otra vez hasta que vuelva. Si el libro tiene varios ejemplares, cada ejemplar tiene su código aparte y se prestan independientemente.

Ah, importante: los estudiantes a veces piden renovar el préstamo. La renovación les da otros 15 días (o 3 días si era alta demanda). Pero la renovación solo se puede hacer si nadie más ha solicitado ese libro mientras tanto. Si otro estudiante lo está esperando, no se renueva, hay que devolverlo.

Sobre los estudiantes: cada uno tiene un código único, nombre, programa académico y semestre. Los de pregrado pueden prestar máximo 3 libros como dije. Los de posgrado pueden prestar hasta 5. Los profesores investigadores pueden prestar hasta 10 y por 30 días, pero ese caso lo manejamos aparte y por ahora no lo necesitan en la API. Solo concéntrense en estudiantes de pregrado y posgrado.

Las multas: si un estudiante devuelve tarde, la biblioteca le cobra 2.000 pesos por día de retraso por cada libro. La multa la calcula automáticamente al momento de la devolución, comparando la fecha de devolución con la fecha en que debía haberlo devuelto. La multa se acumula al historial del estudiante. Mientras tenga multas pendientes sin pagar tampoco puede prestar libros.

Necesitamos también poder consultar el historial de préstamos de un estudiante, para ver qué libros se ha llevado en el pasado. Eso nos sirve para cuando los profesores nos piden estadísticas.

Por ahora con esto está bien. Manejen los datos en memoria por ahora, después montaremos base de datos cuando tengamos presupuesto del próximo semestre. La API debe estar lista en una semana porque empiezan las clases. Estoy disponible si tienen dudas, pero por favor avancen lo más que puedan ustedes mismos porque yo tengo varias reuniones esta semana y poco tiempo.

Gracias y un abrazo.

—

Diana Restrepo
Coordinadora de Biblioteca
Universidad de Caldas

---

## Lo que tienes en este correo y lo que NO tienes

Esto es lo que recibiste. **Esto es todo.** No hay otra documentación.
- ¿Qué te queda claro?
- ¿Qué te queda ambiguo?
- ¿Qué cosas la cliente asume que tú vas a saber pero que no especifica?
- ¿Qué decisiones técnicas tienes que tomar tú porque el correo no las menciona?

**Antes de pedirle nada a una IA**, este correo se convierte en una especificación formal. 
