# TP1 – Elicitación de requerimientos

**Materia:** Metodología de Sistemas II  
**Unidad 5:** Habilidades blandas + IA  
**Caso:** tienda online Sabores de Cuyo  
**Alumno:** Nicolás Viruel

Hice el relevamiento yo, como analista del caso. Sabores de Cuyo vende vinos, aceite, dulces, frutos secos y conservas, y quiere una tienda para todo el país. Abajo dejo a quién incluiría, qué le preguntaría al dueño y qué saqué de la documentación y de dos tiendas que entré a mirar.

---

## Parte 1. Stakeholders

| Categoría | Stakeholder | Rol en el sistema | Interés / necesidad |
|-----------|-------------|-------------------|---------------------|
| Usuario directo | Cliente | Busca, compra y sigue el envío | Comprar sin depender de un mensaje y saber si hay stock |
| Usuario directo | Dueño | Carga productos y mira los pedidos | No perder ventas porque tardó en contestar |
| Usuario indirecto | Depósito | Arma el paquete y la etiqueta | Saber qué salió y si hay que usar caja de vino |
| Usuario indirecto | Mercado Pago | Cobra el pedido | Que no se prepare nada sin pago confirmado |
| Usuario indirecto | Correo (Andreani u otro) | Lleva el paquete | Datos de destino y etiqueta bien hechos |
| Consejero | Contador | Factura | No cargar cada venta a mano |
| Referente interno | Quien publica en redes | Sube fotos y el código de bienvenida | Que la oferta que publicó coincida con la tienda |

Al correo, a Mercado Pago y al contador no los pondría en una entrevista larga, pero si no los tengo en cuenta el sistema se queda corto.

---

## Parte 2. Acta de entrevista con el dueño

La entrevista es simulada. Me imaginé un negocio chico que todavía vende por WhatsApp.

**1. ¿Cómo vende hoy y qué problemas tiene?**

Ferias en Mendoza, Instagram y sobre todo WhatsApp. Las fotos están sueltas y el stock lo mira en una planilla. No le faltan consultas: le faltan respuestas a tiempo. A veces confirma un vino que ya se vendió.

**2. ¿Cuántos pedidos y por dónde?**

Unos 40 pedidos pagos por mes. Casi todos por WhatsApp; el resto, feria o Instagram. No separa CABA del interior hasta que tiene que despachar. Calcula que se le cae cerca de un tercio de las consultas por la demora.

**3. Qué necesita (marqué más de cinco)**

- Catálogo con fotos
- Carrito
- Pagos online
- Seguimiento del envío
- Stock
- Promociones
- Otra: avisar al depósito qué embalar (caja especial si hay vino) y poder facturar el pedido

**4. Pagos y envíos**

Tarjeta y transferencia, por Mercado Pago. A todo el país: 3 a 5 días en CABA y 5 a 7 en el interior. Envío gratis desde $25.000, como ya dice su política. Contra reembolso no lo pondría en la primera versión: la cobranza se le complica.

**5. De qué lo tiene que avisar el sistema**

Pedido pago, pago rechazado, stock bajo (vinos y aceites primero) y pedido listo para despachar. Un resumen del día le serviría para no vivir en el WhatsApp.

---

## Parte 3. Dos tiendas que miré

Entré como si fuera a comprar, en octubre de 2026.

| Aspecto | Familia Luján Conesa | Made in Mendoza |
|---------|----------------------|-----------------|
| Qué destaca | Finca en Palmira, vinos y aceites propios, embalaje de botellas, Andreani, envío gratis desde $70.000, cuotas y descuento por transferencia | Más variedad (alfajores, dulces, vinos, aceites), combos, stock a la vista, descuento por transferencia, regalos y mayorista |
| Compra | Corta: producto, carrito, pago. La historia de la finca da confianza | También corta. El cartel de "últimas unidades" apura |
| Qué no me convence | El envío gratis queda alto para una compra chica. No tienen dulces ni conservas, que Sabores de Cuyo sí vende | Mezcla marcas de otros. Si el stock no está al día, el aviso de urgencia juega en contra |
| Qué me llevo | Decir en el pedido que el vino viaja en caja especial | Mostrar stock antes de que pregunten, y el descuento de la primera compra bien visible |

Para Sabores de Cuyo yo priorizaría catálogo variado, stock visible y el envío gratis en $25.000, que ya está en su política. El depósito tiene que recibir el pedido armado, no un mensaje.

---

## Parte 4. Requisitos que saqué de los documentos

| Requisito | De dónde | Tipo | Prioridad |
|-----------|----------|------|-----------|
| Envío gratis arriba de $25.000 | Política comercial | Funcional | Alta |
| Mostrar 3-5 días en CABA y 5-7 en el interior | Política comercial | Funcional | Alta |
| Devolución a los 7 días si el producto está defectuoso | Política comercial | Funcional | Media |
| 10 % con el código BIENVENIDA en la primera compra | Política comercial | Funcional | Media |
| Fotos del producto | Mail de un cliente | Funcional | Alta |
| Stock visible, sin tener que preguntar | Mail de un cliente | Funcional | Alta |
| Pago con tarjeta | Mail de un cliente | Funcional | Alta |
| Aviso de productos nuevos y ofertas | Mail de un cliente | Funcional | Media |
| Listado de lo vendido para embalar | Nota de logística | Funcional | Alta |
| Los vinos marcados para caja especial | Nota de logística | Funcional | Alta |
| Etiqueta y número de seguimiento | Nota de logística | Funcional | Alta |
| El carrito recalcula solo si el envío pasó a gratis | Política comercial | No funcional | Media |

La devolución y las ofertas las dejaría para después. Primero tiene que poder vender y despachar.

---

## Parte 5. Perfiles

**María Fernández, 35, CABA.** Compra seguido por el celular. Quiere encontrar un vino o un dulce, ver foto y stock, y pagar en pocos pasos. Lo que la haría irse es escribir por WhatsApp y que le digan que no hay stock.

**Roberto Sánchez, 58, Córdoba.** No quiere un sitio cargado. Le da desconfianza cargar la tarjeta y no saber cuánto tarda el envío al interior. Necesita el plazo antes de pagar, pocos pasos, y un teléfono o un mail si algo sale mal. El código BIENVENIDA tiene que estar explicado.

---

## Parte 6. Verificación

**Cliente**

1. Buscar, ver foto y stock, armar el carrito, usar BIENVENIDA, pagar y seguir el envío. Si llegó mal, pedir la devolución.
2. Consulta precio, stock, plazo de su zona y si el envío es gratis.
3. Quiere aviso de pago, de despacho con seguimiento y, si se anotó, de ofertas.

**Administrador**

1. Publicar producto con foto y stock, marcar la caja de vino, ver pedidos pagos y bajar la lista para el depósito.
2. Mira los pedidos del día y qué está por quedarse sin stock.
3. Lo tienen que avisar: pedido pago, pago rechazado y stock bajo.

---

## Parte 7. Casos de uso

| ID | Caso de uso | Actor | Qué hace |
|----|-------------|-------|----------|
| CU-01 | Buscar productos | Cliente | Por nombre o por tipo |
| CU-02 | Ver foto y stock | Cliente | Antes de comprar |
| CU-03 | Armar el carrito | Cliente | Ve el total, el plazo y si el envío es gratis |
| CU-04 | Usar BIENVENIDA | Cliente | 10 % solo la primera vez |
| CU-05 | Pagar | Cliente | Tarjeta o transferencia |
| CU-06 | Seguir el envío | Cliente | Con el número cuando despachan |
| CU-07 | Preparar y etiquetar | Depósito | Lista, caja especial si hay vino, etiqueta |
| CU-08 | Avisar stock bajo | Sistema al dueño | Cuando un producto llega al mínimo |

Con eso alcanza para una primera versión: catálogo, carrito con la regla de envío, pago y el aviso al depósito.
