# TRABAJO PRÁCTICO — Actuación profesional y pericia informática

**Materia:** Legislación  
**Unidad 11:** Actuación profesional y procesos judiciales  
**Alumno:** Nicolás Viruel — Legajo 100634  
**Comisión:** TUPaD  
**Fecha:** 14 de octubre de 2026

---

## Caso

Juan Ignacio Veltri, desarrollador informático, está procesado en la causa que tramita el juez federal Sebastián Casanello, con intervención del fiscal Guillermo Marijuan. Según las dos noticias del material de jurisprudencia, entre diciembre de 2023 y enero de 2025 se alteraron los parámetros del sistema de compra de millas de Aerolíneas Plus: se modificaban el monto a pagar y la cantidad de millas acreditadas. La descripción técnica del expediente habla de interceptar y cambiar cantidad o precio cuando la web enviaba los datos al servidor.

A Veltri se le atribuyen 16.595.000 millas y un perjuicio de alrededor de USD 495.000. La fiscalía pidió indagar a otras 53 personas y estimó el daño total en USD 1.320.479,10. Hubo secuestro de dispositivos. El encuadre que recoge el material es la defraudación por manipulación informática en perjuicio de la administración pública.

---

## 1. Figuras penales (Ley 26.388)

La conducta que describen las noticias no es “romper” el sistema: es usar conocimiento técnico para cambiar los parámetros de una compra (precio y cantidad de millas) y obtener un patrimonio que no correspondía. Esa acción encaja, en primer lugar, en la **defraudación mediante manipulación informática**.

La Ley 26.388 incorporó al Código Penal el **art. 173, inciso 16**: comete defraudación quien defrauda a otro mediante cualquier técnica de manipulación informática que altere el normal funcionamiento de un sistema informático o la transmisión de datos. “Manipular códigos” o, con más precisión técnica, alterar los parámetros que viajan de la web al servidor, es exactamente eso: la transmisión deja de reflejar el precio oficial y el sistema acredita millas por un valor irrisorio. El perjuicio es patrimonial (las millas y los pasajes), no la destrucción del sitio.

Como Aerolíneas Argentinas integra la administración pública, el material de la cátedra agrega el **art. 174, inciso 5**, que agrava el fraude cuando el damnificado es una administración pública. Ese es el encuadre central que señala la jurisprudencia del aula. El mismo texto aclara que el encuadre puede modificarse si la investigación avanza.

Cabe distinguir otras figuras de la 26.388 que la noticia roza, pero que no reemplazan a la defraudación:

- **Art. 153 bis** (acceso ilegítimo a un sistema o dato de acceso restringido). La fiscalía habla de “acceso indebido”. Habría que probar que entró a un sector restringido y no solo que usó la web pública de compra alterando su propio pedido. Si la maniobra fue cambiar parámetros en el tránsito cliente-servidor, el núcleo es la manipulación de la transmisión (173 inc. 16), no necesariamente un acceso clandestino al servidor.
- **Daño informático** (alterar o destruir datos, en la línea del art. 183). Acá el sistema siguió funcionando y el daño denunciado es el patrimonio de la empresa. La figura propia del resultado económico es la defraudación, no el daño.

En síntesis: la imputación principal que se sostiene con las noticias y con la Ley 26.388 es **defraudación por manipulación informática (art. 173 inc. 16), agravada por el perjuicio a la administración pública (art. 174 inc. 5)**.

---

## 2. Principios éticos vulnerados

El apunte dice que el software —y quien lo desarrolla— debe ser **útil, seguro, confiable y justo**. Veltri hizo lo contrario: detectó una falla y la explotó para beneficio propio, en lugar de reportarla.

Del Código de ética que trabaja la unidad, se vulneran sobre todo estos principios:

- **Evitar el daño.** El daño incluye el perjuicio injustificado a la propiedad. El apunte obliga, además, a **informar cualquier signo de riesgo** del sistema. Explotar la vulnerabilidad es la conducta opuesta a dar la voz de alarma.
- **Ser honesto y confiable.** La maniobra es engañosa: el sistema muestra una compra que no se corresponde con la tarifa real. Fabricar un resultado falso es una infracción directa de ese principio.
- **Integridad.** El apunte la define como mantener la integridad del sistema y evitar el uso no autorizado. Alterar parámetros de precio y cantidad quiebra esa integridad.
- **Contribuir al bienestar y responsabilidad social.** El conocimiento técnico se usó en contra del patrimonio de una empresa pública y de la confianza de quienes compran millas por el canal oficial.
- **Calidad y competencia.** Saber encontrar la falla imponía corregirla o advertirla, no aprovecharla. La competencia técnica agrava la falta ética: no fue un error involuntario.

El deber del apunte es claro: si aparece un riesgo, se informa y se mitiga. Usar la falla para comprar millas a precio irrisorio rompe honestidad, integridad y el deber de evitar el daño.

---

## 3. Tres puntos de pericia y adelanto de gastos

Si el juez Casanello me designara perito oficial, el dictamen tiene que servirle para decidir si hubo manipulación y si puede atribuirse a los dispositivos y cuentas investigados. Propondría estos tres puntos:

1. **Reconstrucción de la operatoria de compra.** Comparar, operación por operación, el precio y la cantidad de millas que debían regir según la tarifa oficial con lo que efectivamente se debitó y se acreditó. Determinar si los parámetros se modificaron entre el navegador y el servidor. Base: logs, la planilla aportada por la empresa y los registros del programa de millas.
2. **Análisis forense de los dispositivos secuestrados.** Buscar herramientas, scripts o historial que permitan alterar pedidos HTTP (proxies, interceptores), y correlacionar fechas, cuentas y operaciones con las compras cuestionadas, sin modificar los originales.
3. **Evaluación de la vulnerabilidad y de la integridad de los registros.** Verificar si el servidor confiaba en el precio enviado por el cliente (falta de validación del lado servidor) y si los logs de Aerolíneas Plus se conservaron sin alteraciones posteriores. Este punto separa la falla de diseño de la conducta de quien la explotó.

**Adelanto de gastos.** No es un pago a cuenta de honorarios. Es un derecho del perito para cubrir costos operativos mientras dura el proceso: licencias de software forense, discos de almacenamiento, tiempo de máquina. Lo pediría al juzgado al aceptar el cargo, con un presupuesto escrito de esas herramientas. Como dice el cierre del apunte, una licencia forense o un disco de alta capacidad los asume el proceso, no el profesional. En una causa con muchos dispositivos y operaciones entre 2023 y 2025, ese adelanto es lo que permite trabajar sin adelantar de su bolsillo el costo de la prueba.

---

## 4. Integridad de la evidencia digital

Se secuestraron dispositivos y se analiza la web de Aerolíneas. Si esa evidencia se modifica, se copia mal o se pierde el rastro de quién la tuvo, la defensa puede pedir la **nulidad** de la prueba: sostener que lo que el juez ve ya no es lo que se secuestró, y que no puede condenarse con un elemento contaminado.

Por eso la integridad no es un formalismo. Hace falta trabajar sobre copias, calcular y registrar hashes, documentar la cadena de custodia (quién recibió cada dispositivo, cuándo y en qué estado) y no alterar originales ni logs. Lo mismo vale para la planilla y los registros de la web: si no se puede demostrar que no fueron editados después del hecho, el peritaje pierde fuerza y el proceso queda expuesto a un planteo de nulidad.

---

## 5. Honorarios del consultor técnico de parte

Un consultor técnico de parte es el perito que contrata una de las partes —en este supuesto, Aerolíneas— para analizar el caso y sostener su posición. No reemplaza al perito oficial, que debe ser imparcial e independiente. Igual tiene que ser competente, justificar lo que cobra y guardar confidencialidad.

Los honorarios se fijan de manera **justa y transparente**, por escrito, según la complejidad, el tiempo, la especialización y los gastos de software. Puede ser un monto fijo, por hora o por proyecto. En un expediente de esta magnitud (millones de millas, decenas de imputados, dispositivos y una investigación que sigue en 2026) el presupuesto tiene que contemplar esa carga, no una tarifa genérica de un informe corto.

El **JUS** evita que esos honorarios se licúen. Es una unidad ligada a un porcentaje del sueldo de un juez de primera instancia y se actualiza. El juez regula los honorarios en JUS en la sentencia, y se cobran al valor vigente en ese momento. En una causa larga, pactar o regular solo un monto fijo en pesos dejaría al profesional por debajo del trabajo real.

El **adelanto de gastos** sigue siendo distinto de los honorarios: cubre licencias, almacenamiento y otros costos operativos durante el trámite. En una pericia de este tamaño, pedirlo al inicio es lo que hace viable el trabajo. Los honorarios remuneran el dictamen; el adelanto financia las herramientas.

---

## 6. Apariencia de legalidad, sesgo y responsabilidad

La fiscalía sostiene que las 53 personas “no podían desconocer” que no estaban usando la transferencia oficial de millas. El sistema, sin embargo, les mostró una operación que **parecía** cerrada: millas acreditadas y pasajes emitidos. Un sistema puede devolver un resultado de aspecto lícito y, detrás, esconder una manipulación. Alcanza con que la pantalla confirme la compra mientras el precio real fue alterado en el pedido al servidor. La interfaz no detecta el dolo; muestra el efecto.

Eso no es lo mismo que el **sesgo o la discriminación algorítmica** del apunte. Ese principio (“ser justo y no discriminar”) apunta a sistemas que tratan peor a ciertos grupos o amplían desigualdades, aunque el proceso “parezca” neutro. Acá no hay un modelo que clasifique personas de forma injusta: hay una estafa que usa la confianza del sistema en los parámetros del cliente. El parecido es otro: **lo que el sistema muestra como válido no alcanza para decir que la decisión fue lícita o justa.** Hay que mirar cómo se produjo el resultado, no solo la pantalla final.

El responsable final no es el código. El código no tiene intención: es el instrumento. La responsabilidad penal de la manipulación es de **quien la ejecutó a sabiendas**, en este caso el programador al que la investigación señala como principal beneficiario. Quienes compraron esas millas pueden tener su propia responsabilidad si, como dice la fiscalía, no podían ignorar que la vía no era la oficial. La empresa puede tener un reproche distinto, de diseño inseguro (no validar el precio en el servidor), pero ese defecto no convierte al programa en autor de la estafa ni borra la decisión de quien explotó la falla.
