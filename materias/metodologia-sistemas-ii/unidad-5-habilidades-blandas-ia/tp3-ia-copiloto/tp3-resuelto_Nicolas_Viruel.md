# TP3 – IA como copiloto

**Materia:** Metodología de Sistemas II  
**Unidad 5:** Habilidades blandas + IA  
**Alumno:** Nicolás Viruel

En este práctico la IA me sirvió de copiloto. Los prompts los escribí yo. Cuando le pedí una tabla, ya traía el orden y el recorte definidos. Lo que devolvió lo leí y taché lo que el cliente no había pedido.

---

## Parte 1. Prompts que armé

El cliente dijo: "Necesitamos un sistema para gestionar las reservas del gimnasio. Que los usuarios puedan reservar clases, cancelar si no pueden ir y que el instructor vea quiénes confirmaron. También queremos que envíe recordatorios."

**Prompt flojo, para comparar**

"Dame los requerimientos del sistema."

Así no sirve. No digo qué sistema es, para quién, ni cómo lo quiero de vuelta. Me puede devolver cualquier lista.

**Prompt que sí usaría**

"Contexto: un gimnasio con clases presenciales. El socio reserva y cancela su lugar. El instructor ve quién confirmó. Hay que avisar antes de la clase. No agregues pagos ni una app de entrenamiento: el cliente no lo pidió.

Tarea: pasá esa descripción a requerimientos, separados en funcionales y no funcionales.

Formato: tabla con ID, requisito, actor y prioridad (alta, media o baja).

Criterio: cada fila se tiene que poder probar. Si algo queda ambiguo, como los recordatorios, ponelo en una fila Aclarar. No lo completes vos."

**Prompt para el requisito "el sistema debe ser rápido"**

"Tomá esta frase del cliente: 'El sistema debe ser rápido.'

Seguí este orden y mostrame cada paso: (1) por qué no se puede probar así; (2) qué acción del gimnasio es la que importa, por ejemplo reservar una clase; (3) qué medirías, tiempo o cantidad de pasos; (4) una sola frase verificable, con un número, y un ejemplo de cómo la probaría. No inventes servidores ni hardware."

La frase que yo aceptaría, después de leer la respuesta, es concreta: al confirmar una reserva, el socio ve el resultado en menos de 3 segundos. "Rápido" solo no entra al documento.

---

## Parte 2. Lo que no le acepté a la IA

Me trajo estas cuatro frases para una biblioteca escolar. No las copié.

| Frase de la IA | ¿Se puede probar? | ¿Alcanza? | Cómo la dejaría yo |
|----------------|-------------------|-----------|--------------------|
| Buscar libros | No | No dice quién ni por qué dato | El alumno busca por título o autor y ve si está prestado |
| Consultas rápidas | No | "Rápido" no mide nada | La búsqueda por título muestra resultados en menos de 3 segundos en la red de la escuela |
| Interfaz amigable | No | No hay usuario ni tarea | El alumno anota un préstamo en no más de tres pasos |
| Guardar la información de forma segura | No | No dice qué dato ni de quién | Solo el personal de biblioteca ve los datos del alumno, y el acceso queda registrado |

Suena a requisito y no se puede aceptar ni rechazar en una prueba. Por eso las reescribí.

---

## Parte 3. Bitácora

Caso de práctica: tres requisitos de facturación de un comercio chico. El orden ya lo tenía yo (emitir, anular, ver la deuda). Le pedí al asistente que lo pase a tabla y que me marque dudas. No le pedí que priorice.

| Campo | Qué registré |
|-------|----------------|
| Fecha | 19/10/2026 |
| Tarea | Pasar a tabla un orden que yo ya había cerrado |
| Herramienta | Asistente de IA (copiloto de redacción) |
| Prompt | "Pasá a una tabla estos requisitos, en este orden, que ya definí: 1 emitir la factura, 2 anularla con motivo y con un usuario autorizado, 3 listar la deuda del cliente sin intereses. Agregá una columna de pregunta abierta. No sumes medios de pago ni cambies la prioridad." |
| Qué devolvió | La tabla en ese orden. Preguntó si la deuda incluye intereses y si cualquiera puede anular |
| Qué validé | Intereses no: el cliente no los mencionó. Lo de quién anula ya estaba en mi punto 2 |
| Decisión | Se mantiene mi orden. La deuda queda sin intereses |
| Responsable | Nicolás Viruel |

---

## Parte 4. Qué no pegaría en un chat público

| Situación | Seguro | Riesgoso |
|-----------|--------|----------|
| El código completo de un proyecto privado de la empresa | | X |
| Cómo se escribe un ordenamiento genérico | X | |
| Nombres reales de clientes y sus datos | | X |
| Un concepto de la materia, sin datos del proyecto | X | |

Lo más delicado son los datos de los clientes. No son míos y no hacen falta para aprender a redactar un requisito. Si quiero un ejemplo, invento "cliente A" y un CUIT ficticio. El código privado tampoco lo pegaría: con un fragmento genérico, sin nombres del proyecto, alcanza.

---

## Parte 5. Cómo lo citaría, y el caso del compañero

Nota para un informe de requisitos:

"Usé un asistente de IA como copiloto para revisar la redacción y para pasar a tabla requisitos que yo ya había definido y ordenado. Leí el resultado, saqué lo que el cliente no pidió y las decisiones quedan a mi cargo."

Si un compañero entrega un informe entero generado por IA, sin leerlo y sin citarlo, el problema es que figura como análisis suyo algo que no puede explicar. El riesgo es concreto: una fila inventada puede llegar a desarrollo, y en la corrección o frente al cliente no va a saber defenderla. La IA puede ayudar a redactar. El contraste con lo que dijo el cliente, y la cita, los tiene que hacer la persona.

---

## Cierre

Los prompts de arriba los armé con contexto, tarea y formato. Las cuatro frases de la biblioteca no las copié. En la bitácora se ve qué pedí, qué taché y qué decisión dejé. La IA ordena y propone texto. Qué entra al sistema lo sigo decidiendo yo.
