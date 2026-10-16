TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA




                        PROGRAMACIÓN IV
              Trabajo Práctico - CRUD Categorías + CRUD Productos


OBJETIVO GENERAL
Desarrollar una aplicación Full Stack conectando un frontend React + TypeScript con
un backend FastAPI. El estudiante implementará el CRUD completo de Categorías
desde la interfaz de usuario, integrando el backend mediante fetch nativo. Los CRUDs
de Producto y ProductoCategoria serán construidos en el backend y demostrados
mediante un archivo REST Client.


MARCO TEÓRICO
             Concepto                               Aplicación en el proyecto

                             Biblioteca para construir interfaces de usuario mediante componentes
 React
                             reutilizables.
                             Superset tipado de JavaScript para detectar errores en compilación y
 TypeScript
                             mejorar la legibilidad.
                             Herramienta de build moderna que inicializa proyectos React con
 Vite
                             TypeScript, reemplazando Create React App.
                             Framework Python de alto rendimiento para construir APIs REST.
 FastAPI                     Permite definir endpoints, validar datos con Pydantic y exponer
                             documentación automática en /docs.
                             Librería de validación de datos usada por FastAPI para definir modelos
 Pydantic
                             (schemas) con tipado estricto.
                             API del navegador para realizar peticiones HTTP. Se usa con
 fetch nativo
                             async/await para consumir la API REST desde el frontend.
                             Hook de React para manejar estado local en un componente funcional
 useState
                             (ej: lista de categorías, estado del modal).
                             Hook de React para ejecutar efectos secundarios (ej: fetch al montar el
 useEffect
                             componente para cargar datos).
                             Construcción de TypeScript que define la forma de un objeto (ej:
 Interface
                             Categoria, Producto).
                             Framework de CSS utilitario. Estilos aplicados directamente en el JSX
 Tailwind CSS
                             mediante clases predefinidas.
                             Mecanismo que permite al frontend (localhost:5173) comunicarse con
 CORS
                             el backend (localhost:8000) en dominios distintos.




                                                                                           1
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA




CASO PRÁCTICO
Parte A — Backend con Fast Api


Tomando como base el trabajo práctico de la unidad 6:


a) Crear y activar un entorno virtual Python, crea archivo de dependencias e instalar
las dependencias:


  python -m venv .venv
  source .venv/bin/activate   # macOS/Linux
  .venv\Scripts\activate     # Windows
  pip install -r requirements.txt

b) Definir los models y schemas del modulo Catálogo de Productos restantes.
(SVG adjunto a este pdf)


c) Al módulo “Catálogo de productos” agregar campos faltantes (Auditoría)
d) Crear un CRUD siguiendo la arquitectura Models-Schemas-Service-Router



Endpoint Necesarios:

Categorías
 Método      Endpoint           Body              Response                   Query Params
 GET         /categorias/       —                 CategoriaPaginatedRespon   offset, limit,
                                                  se                         nombre,
                                                                             incluir_inactivos
 POST        /categorias/       CategoriaCreate   CategoriaRead (201)        —
 GET         /categorias/{id}   —                 CategoriaRead              —
 PUT         /categorias/{id}   CategoriaUpdate   CategoriaRead              —
 DELETE      /categorias/{id}   —                 204 No Content             —


Productos
 Método      Endpoint           Body              Response                   Query Params
 GET         /productos/        —                 ProductoPaginatedRespons   offset, limit,
                                                  e                          nombre,
                                                                             incluir_inactivos
 POST        /productos/        ProductoCreate    ProductoRead (201)         —


                                                                                                 2
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

 GET          /productos/{id}      —                    ProductoRead                 —
 PUT          /productos/{id}      ProductoUpdate       ProductoRead                 —
 DELETE       /productos/{id}      —                    204 No Content               —


Relaciones N:M (solo consulta)
No existen endpoints POST/DELETE para gestionar relaciones. Las asociaciones se
crean/actualizan ÚNICAMENTE al crear o editar el producto.

 Método                            Endpoint                           Descripción
 GET                               /productos/{id}/categorias         Categorías de un producto
 GET                               /productos/{id}/ingredientes       Ingredientes de un producto
 GET                               /categorias/{id}/productos         Productos de una categoría


Ingredientes
 Método       Endpoint               Body                  Response                          Query
                                                                                             Params
 GET          /ingredientes/         —                     IngredientePaginatedRespons       offset, limit
                                                           e
 POST         /ingredientes/         IngredienteCreate     IngredienteRead (201)             —
 GET          /ingredientes/{id}     —                     IngredienteRead                   —
 PUT          /ingredientes/{id}     IngredienteUpdate     IngredienteRead                   —
 DELETE       /ingredientes/{id}     —                     204 No Content                    —


Unidades de Medida (Catálogo — solo lectura)
 Método                  Endpoint                   Body                   Response
 GET                     /unidades-medida/          —                      UnidadMedidaListRespons
                                                                           e
 GET                     /unidades-medida/{id}      —                      UnidadMedidaRead




Health
 Método                             Endpoint                          Response
 GET                                /health/                          200 OK
 GET                                /health/db                        200 OK




Query Parameters (comunes)
 Parámetro                Tipo                      Default                    Descripción
 offset                   int                       0                          Desplazamiento para
                                                                               paginación

                                                                                                             3
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

 limit                      int              10                   Cantidad de resultados
                                                                  por página
 nombre                     string           —                    Filtro por nombre
                                                                  (búsqueda parcial)
 incluir_inactivos          bool             false                Incluir registros
                                                                  eliminados (soft delete)




Seed Data — Unidades de Medida
 ID                        Nombre            Símbolo              Tipo
 1                         kilogramo         kg                   masa
 2                         gramo             g                    masa
 3                         litro             L                    volumen
 4                         mililitro         mL                   volumen
 5                         pieza             u                    unidad
 6                         docena            doc                  unidad
 7                         metro cuadrado    m²                   area



Notas:
      ●​ Recuerda agregar CORS para poder consumir tu API desde su frontend
      ●​ No debes de borrar nada de la Base de Datos, debes utilizar borrado lógico (En
         todos los modelos).

 Recuerda que: ​
 Las tablas Catalog se cargan a partir de un archivo seed.py. No deben de
 tener operaciones de escritura (POST/PUT/PATCH) solo deben ser operaciones
 de lectura (GET)


e) Los endpoints deberán de tener la optimización aprendida en la unidad y respuestas
estandarizadas

f) Ejecutar el servidor:


  python -m fastapi dev main.py




📘 Parte B — Frontend con React + TypeScript (MEJORADO)
g) Páginas (Routing)

La aplicación debe estar organizada en páginas separadas.




                                                                                             4
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA




Crear en src/pages/:

   ●​ CategoriasPage.tsx
   ●​ ProductsPage.tsx

CategoriasPage

Debe contener:

   ●​ Toda la lógica de categorías:
         ○​ useQuery
         ○​ useMutation
         ○​ manejo del modal
   ●​ Renderiza:
         ○​ CategoriaList
         ○​ CategoriaModal
         ○​ botón “Nueva categoría”

ProductsPage

   ●​ Estructura similar a CategoriasPage
   ●​ Preparada para trabajar con productos
   ●​ Puede reutilizar lógica (recomendado)
   ●​ Debe tener:
         ○​ listado
         ○​ formulario (modal o página)

h) Navegación

Implementar rutas usando React Router.

Instalar:

pnpm add react-router-dom




                                              5
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA




Configuración básica

Definir rutas:

      ●​ /categorias → CategoriasPage
      ●​ /productos → ProductsPage

Navbar

Actualizar Navbar.tsx para incluir navegación:

      ●​ Link a Categorías
      ●​ Link a Productos

i) App.tsx (cambio clave)

Ahora App ya no tiene lógica de negocio.

Solo debe encargarse de:

      ●​ Definir rutas
      ●​ Renderizar el Navbar
      ●​ Mostrar las páginas

Comportamiento esperado (actualizado)

      ●​ La app inicia en /categorias
      ●​ Se puede navegar a /productos
      ●​ Cada página maneja su propia lógica
      ●​ No hay lógica mezclada en App (orden profesional)


HISTORIAS DE USUARIO
Las siguientes historias de usuario describen, desde la perspectiva del actor que opera el
sistema, el comportamiento esperado de la aplicacion. Cada historia sigue el formato "Como...
quiero... para..." y se acompania de sus criterios de aceptacion, que constituyen la condicion
verificable de que la historia fue implementada correctamente.

 ID           Historia de usuario y criterios de aceptacion      Canal de verificacion




                                                                                                 6
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

HU-01      Listar categorias                                  Frontend (React)

           Como administrador del catalogo, quiero ver al
           ingresar a la aplicacion la lista de todas las
           categorias existentes, para tener una vision
           inmediata de como esta organizado el
           inventario.

           Criterios de aceptacion:

           • Al montar CategoriasPage se ejecuta
           useQuery con GET /categorias, que responde
           200 con la lista.

           • Cada categoria se muestra con nombre y
           descripcion en la pagina.

           • Si no existen categorias, se muestra un estado
           vacio comprensible.

           • Si la peticion falla, se informa el error al
           usuario con el formato {"detail": "..."}.

HU-02      Crear una categoria                                Frontend (React)

           Como administrador del catalogo, quiero crear
           una nueva categoria mediante un formulario en
           un modal, para incorporar al inventario una
           clasificacion que todavia no existe.

           Criterios de aceptacion:

           • Un boton "Nueva categoria" abre el modal con
           el formulario de alta vacio.

           • El formulario valida nombre obligatorio con
           min_length=1 y rechaza solo espacios.

           • Al guardar se envia POST /categorias, que
           responde 201 con la categoria creada, o 409 si
           ya existe el nombre (RN-02).

           • Tras una respuesta exitosa, la nueva categoria
           aparece en la lista sin recargar la pagina y el
           modal se cierra.




                                                                                 7
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

HU-03      Editar una categoria                                Frontend (React)

           Como administrador del catalogo, quiero editar
           una categoria existente desde el mismo modal,
           para corregir o actualizar su informacion.

           Criterios de aceptacion:

           • El boton Editar de la tarjeta abre el modal con
           los campos precargados con los datos actuales
           de la categoria.

           • Al guardar se envia PUT /categorias/{id}
           (reemplazo total), que responde 200 con la
           categoria actualizada, 404 si el id no existe, o
           409 si hay duplicado de nombre.

           • Tras la respuesta exitosa, la tarjeta
           correspondiente refleja los nuevos valores y el
           modal se cierra.

           • El modal distingue claramente entre modo alta
           y modo edicion.

HU-04      Eliminar una categoria                              Frontend (React)

           Como administrador del catalogo, quiero
           eliminar una categoria que ya no se utiliza, para
           mantener el inventario limpio y libre de
           clasificaciones obsoletas.

           Criterios de aceptacion:

           • El boton Eliminar dispara DELETE
           /categorias/{id}, que responde 204 sin cuerpo,
           404 si no existe, o 409 si la categoria tiene
           productos asociados (RN-05).

           • Tras la respuesta exitosa, la categoria
           desaparece de la lista de forma inmediata.

           • Se solicita confirmacion antes de eliminar para
           evitar borrados accidentales.




                                                                                  8
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

HU-05      Navegar entre paginas con React Router               Frontend (React)

           Como administrador del catalogo, quiero
           navegar entre las secciones de Categorias y
           Productos sin recargar la pagina, para trabajar
           de forma fluida.

           Criterios de aceptacion:

           • El Navbar contiene enlaces a /categorias y
           /productos usando <Link> de React Router.

           • La navegacion entre rutas no recarga el
           navegador; solo cambia el contenido de la
           pagina.

           • App.tsx no contiene logica de negocio: solo
           define rutas y renderiza el Navbar.

           • Cada pagina maneja su propia logica con
           hooks (useState, useEffect).

HU-06      CRUD de Productos desde REST Client​                 Backend (REST Client)
            Como administrador del catálogo, quiero listar,
           crear, actualizar y eliminar productos desde el
           backend, para gestionar la oferta del inventario.​
            Criterios de aceptación:​
            • GET /productos devuelve la colección
           completa de productos.​
            • POST /productos crea un producto validado
           con Pydantic (201). El body debe incluir
           categoria_ids (lista con al menos 1 ID).
           Opcionalmente puede incluir ingredientes. Si
           falta categoria_ids o está vacío, rechaza con
           422.​
            • PUT /productos/{id} actualiza los datos (200) o
           devuelve 404. Si se envían categoria_ids o
           ingredientes, se reemplazan completamente las
           relaciones existentes.​
            • DELETE /productos/{id} elimina el producto y
           en cascada sus asociaciones (204) o 404.​
            • Todas las operaciones se demuestran con
           archivos .http.




                                                                                        9
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

 HU-07       Consultar relación N:M Producto-Categoría y        Backend (REST Client)
             Producto-Ingrediente​
              Como administrador del catálogo, quiero
             consultar las categorías e ingredientes
             asociados a un producto y los productos de una
             categoría, para conocer la organización del
             inventario.​
              Criterios de aceptación:​
              • GET /productos/{id}/categorias devuelve las
             categorías del producto.​
              • GET /productos/{id}/ingredientes devuelve los
             ingredientes del producto.​
              • GET /categorias/{id}/productos devuelve los
             productos de una categoría.​
              • Las relaciones N:M se gestionan
             ÚNICAMENTE al crear o actualizar un producto
             (POST /productos y PUT /productos/{id}). NO
             existen endpoints específicos para
             asociar/desasociar por separado.​
              • Consultar contra entidad inexistente devuelve
             404.




REGLAS DE NEGOCIO
Las reglas de negocio definen las restricciones que el sistema debe hacer cumplir para
mantener la integridad de los datos. Son responsabilidad del backend (capa de validacion con
Pydantic y logica de los servicios) y complementan las historias de usuario: una historia
describe que quiere lograr el usuario, mientras que una regla de negocio establece que esta
permitido y que debe rechazarse.

 ID         Regla de negocio                                    Entidad / Verificacion

 RN-01      El nombre de una categoria es obligatorio           Categoria / 422
            (min_length=1) y no puede quedar vacio ni
            contener solo espacios.

 RN-02      El nombre de una categoria es unico: no pueden      Categoria / 409 Conflict
            existir dos categorias con el mismo nombre
            (comparacion sin distincion de mayusculas y
            espacios externos).

 RN-03      La descripcion de una categoria es opcional; se     Categoria / 201 o 200
            declara con valor por defecto (descripcion: str =
            "") y se almacena como cadena vacia si se omite.

 RN-04      No se puede actualizar ni eliminar una categoria    Categoria / 404 Not Found
            cuyo id no exista.

 RN-05      Una categoria con productos asociados no puede      Categoria / 409 Conflict
            eliminarse hasta desasociar esos productos o
            eliminarlos.




                                                                                            10
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

RN-06     El nombre de un producto es obligatorio               Producto / 422
          (min_length=1) y no puede quedar vacio ni
          contener solo espacios. No es unico: pueden
          coexistir productos con el mismo nombre.

RN-07     El precio_base de un producto debe ser >= 0           Producto / 422
          (Field(ge=0)); no se aceptan precios negativos.

RN-08     El campo disponible es booleano; se declara con       Producto / 201
          valor por defecto True.

RN-09     El campo imagenes_url es una lista de cadenas;        Producto / 422
          puede estar vacia.

RN-10     No se puede consultar, actualizar ni eliminar un      Producto / 404 Not Found
          producto cuyo id no exista.

RN-11     Al crear o actualizar un producto, todas las          Relacion / 404
          categorías incluidas en categoria_ids deben
          existir previamente. Si alguna no existe, la
          operación se rechaza con 404.

RN-12     Si se envían categoria_ids en un PUT                  Relacion / 409 Conflict
          /productos/{id}, se reemplazan TODAS las
          asociaciones existentes del producto. No es
          necesario desasociar manualmente.

RN-13     Un producto puede asociarse a varias categorias       Relacion / verificable con
          y una categoria puede agrupar varios productos        GET inversos
          (cardinalidad N:M).

RN-14     Al eliminar un producto, se eliminan                  Relacion / consistencia tras
          automaticamente todas sus asociaciones con            DELETE
          categorias (borrado en cascada).

RN-15     El id de cada entidad lo asigna el backend de         Todas / id de solo lectura
          forma autoincremental (entero, desde 1); el
          cliente nunca lo envia al crear.

RN-16     Los datos se mantienen en memoria durante la          Todas / comportamiento
          ejecucion del servidor; al reiniciar, el catalogo     esperado
          vuelve a su estado inicial.

RN-17     Toda solicitud con datos invalidos, entidad           Todas / 404, 409 o 422
          inexistente o conflicto de estado no modifica el
          catalogo y devuelve el error correspondiente.

RN-18     La aplicacion gestiona la navegacion del lado del     Frontend / comportamiento
          cliente con React Router; el servidor no interviene   esperado
          en el enrutamiento interno.

RN-19     Al crear un producto, categoria_ids es obligatorio    Producto / 422
          y debe contener al menos un ID de categoría
          (Field(min_length=1)). Si se omite o está vacío, la
          operación se rechaza con 422.




                                                                                               11
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

 RN-20      Los ingredientes de un producto son opcionales         Producto / 201
            tanto al crear como al actualizar. Si no se envían,
            el producto se crea sin ingredientes asociados.

 RN-21      Si se envían ingredientes en PUT /productos/{id},      Producto / 200
            se reemplazan TODOS los ingredientes
            existentes del producto por los nuevos.

 RN-22      No existen endpoints POST/DELETE específicos           Relación / —
            para gestionar relaciones N:M. Las asociaciones
            se gestionan exclusivamente a través de POST
            /productos y PUT /productos/{id}.




CONCLUSIONES ESPERADAS
Al finalizar el trabajo práctico, el estudiante debe demostrar:


         ● Integración Full Stack: El frontend React consume la API FastAPI
            mediante fetch nativo. El CRUD de Categorías funciona de extremo a
            extremo.
         ● Modal con useState: El formulario de alta y edición está dentro de un
           modal controlado con estado booleano.
         ● Hooks aplicados correctamente: useState y useEffect utilizados en
           App.tsx. Los demás componentes son funcionales puros sin hooks.
         ● Tipado TypeScript: Interfaces Categoria y Producto definidas. Props
           tipados en todos los componentes .tsx.
         ● Backend REST documentado: Endpoints de Producto y
           ProductoCategoria funcionando y demostrados en el archivo .http.
         ● CORS configurado: El backend permite peticiones desde el origen del
           frontend.




RÚBRICA DE EVALUACIÓN
 Criterio                      Descripción                                          Puntos

 CRUD Categorías –             Listar, crear, editar y eliminar categorías            30
 Frontend                      desde React usando fetch nativo y
                               useState/useEffect.

 Modal funcional               Modal que se abre para crear y editar                  15
                               categorías, controlado con useState. Se
                               cierra al guardar o cancelar.

 CRUD Categorías –             Endpoints FastAPI GET /categorias, POST,               20
 Backend                       PUT/{id}, DELETE/{id} con Pydantic y
                               persistencia en lista/DB.


                                                                                             12
TECNICATURA UNIVERSITARIA
EN PROGRAMACIÓN
A DISTANCIA

 CRUD Productos y            Endpoints de Productos y                   15
 relación – REST Client      ProductoCategoria demostrados con REST
                             Client (.http). No requiere UI.

 Tipado TypeScript           Interfaces Categoria y Producto tipadas.   10
                             Props tipados en todos los componentes.

 Estructura y buenas         Carpetas components/ y types/. Tailwind    10
 prácticas                   CSS aplicado. Sin errores de TS en
                             consola.


Modalidad de Entrega
       • ​ Eliminar la carpeta node_modules y venv antes de comprimir
       • ​ Proyecto Frontend comprimido en un archivo .zip
       • ​ Proyecto Backend comprimido en un archivo .zip


RECURSOS ADICIONALES
📚   Documentación oficial:

       ● React: https://react.dev/
       ● TypeScript: https://www.typescriptlang.org/docs/
       ● Tailwind CSS: https://tailwindcss.com/docs/
       ● Vite: https://vitejs.dev/
       ● FastAPI: https://fastapi.tiangolo.com/




                                                                             13
