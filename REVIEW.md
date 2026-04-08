# Revisión del proyecto — Siboney

**Fuente de verdad:** `proyecto/02-documentando/gesticat/`
**Fases detectadas:** 01 (capas), 02 (documentación)

---

## REVISIÓN FASE 02 - 2026-04-08 — Nota: 8/10

### Resuelto desde la revisión anterior

- Creado `presentation/menu.py` con menú completo y todas las opciones funcionales.
- Añadido `infrastructure/datos_iniciales.py` con colonia, responsable y cinco gatos de ejemplo.
- `README.md` ampliado con quick-start, árbol de carpetas, requisitos y enlace a `docs/`.
- Corregida la inconsistencia del contrato: `quitar()` ya está declarado en `domain/repositorio_gatos.py`.
- Implementada la validación de mayoría de edad en el setter `fecha_nacimiento` de `PersonaFisica`.
- Renombrado el parámetro `id` del setter de `id_gato` — ya no usa la palabra reservada de Python.

### Cumple

- Todos los módulos Python tienen docstring de módulo como **primer statement del fichero** (antes de los imports), cumpliendo PEP 257.
- Todas las clases y métodos públicos tienen docstrings descriptivos, con `:param`, `:return` y `:raises` donde corresponde.
- Las reglas de negocio están comentadas en el dominio con el "por qué" de cada decisión (p. ej. la no reversión de esterilización, el cálculo de 3 meses, el uso de `hasattr` para evitar fallos en `__init__`).
- Comentarios orientados al "por qué", sin comentarios evidentes que solo repiten el código.
- `CHANGELOG.md` bien estructurado con versiones `0.1.0` y `0.2.0`, secciones Added/Changed/Fixed y nota de breaking changes.
- Carpeta `docs/` completa con los diez documentos requeridos, todos con contenido coherente.
- `docs/CONTRATO_REPOSITORIO.md` describe exactamente los cinco métodos (`insertar`, `actualizar`, `obtener`, `listar`, `quitar`) que existen en el código, con las mismas garantías documentadas.
- `docs/REGLAS_DE_NEGOCIO.md` refleja fielmente todas las validaciones implementadas en el dominio.
- `docs/DATOS_INICIALES.md` coincide exactamente con los cinco gatos precargados en `infrastructure/datos_iniciales.py`.
- `docs/CASOS_DE_USO.md` lista exactamente las nueve opciones del menú con sus entradas, efectos y errores posibles.
- `docs/MODELO_DE_DOMINIO.md` describe todos los atributos de las entidades, todos los cuales existen en el código.
- Nomenclatura PEP8 consistente en todo el proyecto: `snake_case` para funciones/métodos/variables, `PascalCase` para clases, nombres del vocabulario del dominio.
- Diseño de capas sólido: la presentación no instancia entidades de dominio directamente (solo `PersonaFisica` y `Protectora` en `asignar_responsable`, que es un caso límite aceptable), no hay `print()` fuera de `presentation/`.
- Herencia real y justificada: `PersonaFisica` y `Protectora` añaden atributos y comportamiento distintos (`fecha_nacimiento`/`numero_registro`, `__str__` diferente). `RepositorioGatosMemoria` implementa todas las operaciones del contrato.
- `RepositorioGatos` usa `raise NotImplementedError` con mensaje en todos los métodos — patrón correcto para el contrato del dominio.
- Tests manuales por componente cubriendo todos los módulos; los nombres de fichero descritos en `docs/TESTS_Y_PASOS.md` coinciden exactamente con los que existen en el repositorio.

### Errores y aspectos a mejorar

- **[DISEÑO] `presentation/menu.py:9-12` — La presentación importa clases del dominio directamente.** `menu.py` importa `EstadoColonia`, `EstadoGato`, `Sexo`, `PersonaFisica` y `Protectora` desde `domain/`. La regla de capas exige que `presentation/` solo hable con `application/` (y con `infrastructure/` exclusivamente para `cargar_datos_iniciales`). Convertir cadenas de texto en enums del dominio (`EstadoGato[estado_input]`, `Sexo.HEMBRA`, etc.) es una decisión de dominio que no debería tomarse en la presentación.
  - *Cómo resolverlo:* El servicio puede aceptar cadenas y encargarse de convertirlas a enums internamente, o el servicio puede exponer métodos auxiliares como `estados_gato_disponibles()` que devuelvan diccionarios `{clave: descripción}`. Así la presentación solo pasa strings y no necesita importar los enums.

- **[DISEÑO] `presentation/menu.py:139-145` — La presentación instancia entidades de dominio (`PersonaFisica`, `Protectora`).** `asignar_responsable()` construye directamente objetos de dominio en la capa de presentación. La presentación debería pasar los datos crudos al servicio, y el servicio crear la entidad correcta.
  - *Cómo resolverlo:* Añadir métodos al servicio como `asignar_responsable_fisica(nombre, telefono, email, identificacion, fecha_nacimiento)` y `asignar_responsable_protectora(...)`, o un único método que reciba el tipo como string. La presentación solo recopila datos y llama al servicio.

- **[BUG] `presentation/menu.py:76-78` — `registrar_gato` no captura excepciones propias: una entrada inválida propaga la excepción al bucle principal sin mostrar el campo que falló.** Si el usuario introduce un nombre vacío (`nombre = ""`) o un color con espacios laterales, el `ValueError` lanzado por los setters de `Gato` es capturado por el `try/except` del bucle principal en `main()`, pero el mensaje de error aparece sin contexto (el usuario ya no ve qué campo fue) y el gato no se registra. Esto es el comportamiento esperado, pero hay un caso especial: si `esterilizado=True` y `clinica=None`, la excepción se lanza correctamente. Sin embargo, la función no hace `.strip()` en `nombre` ni en `color` antes de pasar al servicio, por lo que una entrada de solo espacios (`"   "`) llegará al setter y será rechazada por `texto != texto.strip()` con un mensaje confuso ("no puede tener espacios laterales") cuando la intención del usuario era dejarla vacía.
  - *Cómo resolverlo:* Aplicar `.strip()` a `nombre` y `color` antes de pasarlos al servicio, igual que se hace con `id_gato`. También se puede añadir un `try/except ValueError` local en la función para mostrar el error y pedir de nuevo ese campo sin volver al menú.

- **[BUG] `presentation/menu.py:84-86` — `quitar_gato` no envuelve la llamada en `try/except`.** El `try/except ValueError` que captura los errores está en `main()`, lo que significa que sí queda cubierto. Sin embargo, el ID se pasa directamente sin limpiar con `.strip()` y sin validar que tenga 3 dígitos. Si el usuario introduce `" 001"` (con espacio), `quitar_gato` llamará a `self._repo.quitar(" 001")` que buscará una clave que no existe y lanzará `ValueError: No existe ningún gato con id  001` con el espacio incluido en el mensaje, lo que puede confundir al usuario.
  - *Cómo resolverlo:* Aplicar `.strip()` al `id_gato` en `quitar_gato`, igual que se hace en `registrar_gato`.

- **[BUG] `presentation/menu.py:92` — `actualizar_estado_gato` pasa el ID sin `.strip()`.** Mismo problema que en `quitar_gato`: un ID con espacio no encontrará el gato y el mensaje de error incluirá el espacio, confundiendo al usuario.
  - *Cómo resolverlo:* Aplicar `.strip()` al resultado de `input("ID del gato: ")`.

- **[BUG] `presentation/menu.py:106` — `actualizar_esterilizacion_gato` pasa el ID sin `.strip()`.** Mismo problema que en los dos puntos anteriores.
  - *Cómo resolverlo:* Aplicar `.strip()` al resultado de `input("ID del gato: ")`.

- **[DISEÑO] `presentation/menu.py:12` — Importación de `cargar_datos_iniciales` desde `infrastructure/` en la presentación.** `menu.py` importa directamente desde `infrastructure.datos_iniciales`. La presentación no debería conocer la capa de infraestructura. La construcción del grafo de objetos (repositorio + colonia + servicio) debería hacerse fuera de la presentación, idealmente en un punto de entrada separado o en el propio `main()` con la inicialización delegada al servicio o a un módulo de bootstrap.
  - *Cómo resolverlo:* Mover la lógica de inicialización a una función de `application/` o crear un módulo `__main__.py` en la raíz del paquete que construya el grafo y llame a `menu.main()`. Así `presentation/` solo necesita importar de `application/`.

- **[IMPORTANTE] `domain/repositorio_gatos.py` — El contrato no hereda de `ABC` y sus métodos no están decorados con `@abstractmethod`.** Los métodos lanzan `NotImplementedError`, lo que es funcional, pero Python permite instanciar `RepositorioGatos` directamente sin forzar la implementación de todos los métodos. Con `ABC` y `@abstractmethod`, Python impide crear una instancia de la clase concreta si falta algún método, dando un error claro en tiempo de creación.
  - *Cómo resolverlo:* Añadir `from abc import ABC, abstractmethod` e incluir `@abstractmethod` en cada método del contrato, igual que se hace con `Responsable`. Esto convierte el contrato en una interfaz real.

- **[SUGERENCIA] `domain/colonia.py:192` — `reporte_colonia` accede a atributos privados directamente (`self._nombre`, `self._responsable`, `self._estado`, `self._ultima_actualizacion`).** Dentro de la misma clase esto es técnicamente correcto, pero es más coherente usar las propiedades definidas (`self.nombre`, `self.responsable`, `self.estado`, `self.ultima_actualizacion`) para que si alguna propiedad añade lógica en el futuro, `reporte_colonia` la use automáticamente.
  - *Cómo resolverlo:* Sustituir los accesos `self._atributo` por `self.atributo` (usando las propiedades) dentro de `reporte_colonia`.

- **[SUGERENCIA] `domain/gato.py:31` y `domain/gato.py:34-39` — TODOs de código pendiente visibles en la entrega.** Hay un `# TODO` dentro del enum `EstadoGato` y un bloque comentado de `MarcaEsterilizacion`. Son notas de desarrollo que no deberían aparecer en una entrega de documentación.
  - *Cómo resolverlo:* Eliminar los TODOs y el bloque comentado, o moverlos a `docs/` como trabajo futuro planificado.

- **[SUGERENCIA] `presentation/menu.py:38-40` — TODO de mejora de UX visible en la entrega.** El comentario sobre aplicar `try/except` por campo es una nota de desarrollo, no un comentario de diseño.
  - *Cómo resolverlo:* Eliminar el TODO o moverlo a `docs/DESCRIPCION_Y_ALCANCE.md` como limitación conocida.

- **[SUGERENCIA] `docs/EJECUCION.md` — No incluye los pasos de creación y activación del entorno virtual.** El documento asume que el usuario ya tiene el entorno configurado. Para una documentación completa de fase 02 debería describir cómo crear un entorno virtual, aunque no haya dependencias externas.
  - *Cómo resolverlo:* Añadir una sección con `python3 -m venv .venv` y `source .venv/bin/activate` (o equivalente en Windows), aunque luego se indique que no hay paquetes que instalar.

- **[SUGERENCIA] `README.md:54` — Los tests se describen como "pruebas manuales" con `python3 -m test_gato`.** El término es correcto para esta fase, pero el `README.md` principal no menciona que estos ficheros de test están sueltos en la raíz (no en `tests/`), lo que puede confundir a quien espere la estructura estándar de fase 03.
  - *Cómo resolverlo:* Añadir una nota breve indicando que los tests de esta fase son scripts independientes y que en fase 03 se reorganizarán en una carpeta `tests/` con `unittest`.

---

## REVISIÓN FASE 01 - 2026-03-03 — Nota: 4/10

### Cumple

- Repositorio creado y compartido con el profesor.
- Subcarpeta `proyecto/` en el repositorio con la carpeta de fase `01-diseno-capas/`.
- El proyecto está organizado en las cuatro capas: `domain/`, `application/`, `infrastructure/`, `presentation/`.
- Estructura de ficheros correcta: paquetes con `__init__.py`, módulos bien separados.
- POO aplicado con solidez: clases `Gato`, `Colonia`, `Responsable` (con herencia `PersonaFisica` y `Protectora`), encapsulamiento mediante `@property` y setters con validaciones robustas, uso correcto de `Enum` para estados y sexos.
- Contrato de repositorio definido en `domain/repositorio_gatos.py` e implementado en `infrastructure/repositorio_gatos_memoria.py`.
- Servicio de aplicación `ServicioColonia` que coordina casos de uso sin mezclar lógica de negocio.
- Reglas de negocio comentadas en los módulos del dominio.
- Nombres de ficheros, clases y variables significativos y conformes a PEP8.

### Errores y aspectos a mejorar

- **[IMPORTANTE] No hay menú ni punto de entrada — el programa no se puede ejecutar.** La carpeta `presentation/` existe pero está vacía. No hay `main.py` ni módulo de menú. El programa no funciona como aplicación.
  - *Cómo resolverlo:* Crea, al menos,  `presentation/menu.py` con un bucle de menú que llame a `ServicioColonia` (registrar gato, ver censo, tramitar anexo, etc.).

- **[IMPORTANTE] `README.md` sin instrucciones de instalación ni ejecución.** El fichero tiene solo 2 líneas genéricas. Quien clone el repositorio no sabe cómo ejecutar el proyecto.
  - *Cómo resolverlo:* Amplía el `README.md` con descripción del proyecto, versión de Python requerida y los comandos para clonar e iniciar la aplicación.

- **[IMPORTANTE] No hay datos iniciales.** No existe ningún fichero que cargue datos de ejemplo al arrancar. Sin menú ni datos iniciales, no hay forma de probar el sistema manualmente.
  - *Cómo resolverlo:* Añade un módulo en `infrastructure/` (por ejemplo `datos_iniciales.py`) que cree una colonia con algunos gatos de ejemplo y un responsable, y úsalo al arrancar la aplicación desde `main.py`.

- **[DISEÑO] `domain/repositorio_gatos.py` declara un TODO para añadir `quitar(id_gato)` al contrato, pero `infrastructure/repositorio_gatos_memoria.py` ya lo implementa.** 

- **[SUGERENCIA] `domain/gato.py:68` — el parámetro del setter `id_gato` se llama `id`.** `id` es una palabra reservada de Python; no deberías usarlo como nombre de parámetro.
  - *Cómo resolverlo:* Renómbralo a `valor` o `id_gato` para ser consistente con el resto de setters.

- **[SUGERENCIA] `domain/responsable.py` — `PersonaFisica` tiene un TODO pendiente para validar mayoría de edad.** No es un error ahora mismo, pero es una regla de negocio declarada y no aplicada.
  - *Cómo resolverlo:* Implementa la validación en el setter correspondiente o anótalo como limitación conocida en un comentario más explícito.
