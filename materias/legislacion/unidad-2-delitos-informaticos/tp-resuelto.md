# TRABAJO PRÁCTICO – DELITOS INFORMÁTICOS
## Análisis de la Ley N° 26.388

**Materia:** Legislación  
**Unidad 2:** Delitos Informáticos  
**Alumno:** Nicolás Viruel

---

## PARTE 1 – Análisis de la Ley N° 26.388

### 1. ¿Cuál es el objetivo principal de la Ley N° 26.388?

La Ley 26.388 (de 2008) incorpora los **delitos informáticos al Código Penal argentino**. Básicamente busca regular conductas delictivas que se cometen usando sistemas informáticos, redes o datos digitales, y establecer las penas correspondientes.

Para nosotros como técnicos en programación, es importante porque marca qué acciones sobre sistemas o datos pueden tener consecuencias penales, no solo laborales o civiles.

---

### 2. ¿Qué tipos de delitos informáticos están tipificados en esta ley? (mínimo cinco)

Algunos de los delitos que incorpora o modifica:

1. **Acceso indebido a sistemas o datos** (Art. 153 bis CP): entrar sin autorización a un sistema o dato restringido.
2. **Violación de comunicaciones electrónicas** (Art. 153 CP): acceder o interceptar comunicaciones ajenas.
3. **Fraude informático** (Art. 173 inc. 16 CP): defraudar usando manipulación informática del sistema.
4. **Daño informático** (Arts. 183 y 184 CP): alterar, destruir o inutilizar datos, programas o sistemas.
5. **Acceso a bancos de datos personales** (Art. 157 bis CP): acceder, revelar o insertar datos falsos en archivos de datos personales.

---

### 3. ¿Qué sanciones establece la ley para quienes cometen delitos informáticos?

No hay una sola pena para todos los casos; depende del delito cometido. Por ejemplo:

- Acceso indebido (Art. 153 bis): de 15 días a 6 meses de prisión (hasta 1 año si afecta organismos estatales o entidades financieras).
- Fraude informático (Art. 173 inc. 16): se rige por las penas de estafa, que varían según el monto.
- Daño informático (Art. 183): de 15 días a 1 año de prisión.

También pueden aplicarse multas e inhabilitación para ejercer cargos públicos en algunos casos.

---

### 4. ¿Qué acciones se consideran delitos en relación con el acceso no autorizado a sistemas informáticos?

El **Art. 153 bis** sanciona acceder a sabiendas, sin autorización o excediendo la que se tiene, a un sistema o dato informático de acceso restringido.

En la práctica, esto incluye cosas como:

- Entrar a un servidor, red o base de datos sin permiso.
- Usar usuario y contraseña de otra persona.
- Aprovechar permisos para acceder a datos que no te corresponden.

Si el sistema afectado pertenece al sector financiero o es de un organismo público, la pena es más grave.

---

### 5. ¿Cómo define la ley el concepto de "delito informático"?

La ley **no da una definición única** del término. Lo que hace es tipificar conductas concretas en el Código Penal donde intervienen sistemas informáticos, ya sea como **medio** para cometer el delito (por ejemplo, hackear para robar) o como **objeto** del ataque (dañar datos o sistemas).

En resumen, delito informático es cualquier conducta penal tipificada que involucra tecnología de la información.

---

### 6. Caso hipotético: un hacker accede a una base de datos sin autorización

Si un hacker entra sin permiso a una base de datos, los artículos que podrían aplicarse son:

- **Art. 153 bis:** acceso indebido al sistema/dato informático.
- **Art. 157 bis:** si la base tiene datos personales (nombres, DNI, etc.).
- **Art. 183:** si altera o destruye información.
- **Art. 173 inc. 16:** si usa esos datos para obtener un beneficio económico.

Lo más directo sería el **153 bis**, y el **157 bis** si hay datos personales involucrados.

---

## PARTE 2 – Caso práctico: "Inversiones S.A."

Esteban, empleado de Inversiones S.A., entró al sistema con la cuenta de Iván y transfirió $1.000.000 a una cuenta en el extranjero a nombre de un familiar. Planeó todo desde sus dispositivos personales, pero hizo la transferencia desde la empresa (desde la IP de Iván).

### A) Preguntas del caso

#### 1. ¿Qué tipo de delito informático se ha cometido en este caso?

Principalmente dos:

- **Acceso indebido (Art. 153 bis):** entró al sistema sin autorización usando credenciales ajenas.
- **Fraude informático (Art. 173 inc. 16):** usó el sistema para transferir plata que no le correspondía.

Como Inversiones S.A. es del sector financiero, la pena del acceso indebido puede ser más alta.

#### 2. ¿Dónde se ha cometido el delito?

Esteban planificó desde sus dispositivos personales, pero la transferencia se hizo **dentro de la empresa**, desde la IP de Iván. El perjuicio económico también tiene efectos en el extranjero por la cuenta destino.

Jurídicamente, el hecho se entiende cometido en **Argentina**, en la sede de Inversiones S.A., donde se produjo el acceso y la transferencia.

#### 3. ¿Quiénes son las víctimas en este caso?

- **Inversiones S.A.:** perdió $1.000.000 y sufrió una violación de su sistema.
- **Iván:** le usaron la identidad digital sin permiso; puede quedar involucrado en la investigación sin ser culpable.
- **Clientes de la empresa:** podrían verse afectados indirectamente si el dinero era de terceros.

#### 4. ¿Quiénes son los autores del delito?

- **Esteban** es el autor: planeó todo, accedió al sistema y ejecutó la transferencia.
- **Iván no es autor**; en todo caso es víctima de la suplantación de credenciales.
- El **familiar** del extranjero podría ser partícipe si sabía que el dinero era producto de un delito.

---

## PARTE 3 – Tipos de PHISHING

### Vishing (Voice Phishing)

**Ejemplo:** Te llaman haciéndose pasar por el banco y te dicen que hubo un movimiento raro en tu cuenta. Te piden el DNI y la clave del home banking para "bloquearla". Si caés, les das acceso a tu cuenta.

Es phishing pero por **llamada telefónica** en lugar de mail.

### Quishing (QR Phishing)

**Ejemplo:** En un estacionamiento alguien pega un **QR falso** encima del original. Lo escaneás pensando que vas a pagar el estacionamiento, pero te manda a una web trucha que imita la del banco y te pide usuario y contraseña.

Usa **códigos QR maliciosos** para engañar.

### Spear Phishing (Phishing dirigido)

**Ejemplo:** Un empleado de contabilidad recibe un mail que parece de su jefe, con el logo de la empresa y datos reales del trabajo: *"Transferí $500.000 urgente a esta cuenta"*. No es un mail masivo; está armado específicamente para esa persona.

Es un ataque **personalizado** contra alguien en particular, usando info real de la organización.

---

## PARTE 4 – Tecnologías de protección

### Autenticación Multifactor (MFA)

Consiste en pedir **más de un dato** para verificar quién sos. Por ejemplo: contraseña + código que te llega al celular o a una app como Google Authenticator.

Los factores suelen ser algo que sabés (contraseña), algo que tenés (el celular) o algo que sos (huella).

En el caso de Inversiones S.A., si hubiera MFA activo, Esteban no hubiera podido entrar solo con la contraseña de Iván: le faltaba el segundo factor.

### Autenticación Biométrica

Usa características físicas propias para identificarte: **huella dactilar**, reconocimiento facial, iris, etc. El sistema compara tu dato biométrico con uno guardado y, si coincide, te deja entrar.

En una empresa financiera, combinar biometría con contraseña hace mucho más difícil que alguien use credenciales robadas, porque necesitaría también la huella o el rostro del titular.

Un punto a tener en cuenta: si filtran tus datos biométricos, no podés cambiarlos como una contraseña. Por eso deben protegerse bien (Ley 25.326 de datos personales).

---

## Referencias

- Ley N° 26.388 – Delitos Informáticos.
- Código Penal de la Nación – Arts. 153, 153 bis, 157 bis, 173 inc. 16, 183, 184.
- Material Unidad 2 – Delitos Informáticos (Moodle UTN TUP).
