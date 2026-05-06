# Bitácora de GestiCat — Ideas, mejoras y conceptos aprendidos

Este documento recoge las decisiones de diseño, mejoras aplicadas, ideas
futuras y conceptos nuevos aprendidos durante el desarrollo del proyecto.
Sirve como referencia personal para no perder el hilo entre sesiones.

---

## Conceptos aprendidos

### Enum
Clase de Python que permite definir un conjunto de valores constantes con
nombre. Se importa con `from enum import Enum`. Útil para representar opciones
cerradas como estados, sexos o tipos, evitando el uso de strings o números
"mágicos" que pueden causar errores. Cada valor del enum tiene un nombre y un
valor asociado (`Sexo.HEMBRA = "H"`).
Documentación oficial: https://docs.python.org/3/library/enum.html

### Conversión de enums a SQLite y viceversa

SQLite no tiene tipo ENUM. Para guardar un enum de Python hay que
convertirlo a texto o número. Al recuperarlo, hay que convertirlo
de vuelta al enum.

Hay dos formas según cómo esté definido el enum:

**Por valor** — cuando el valor ya es un string corto y estable:


**Por nombre** — cuando el valor es largo o podría cambiar:


La diferencia entre paréntesis y corchetes:
- `Sexo("M")` busca el miembro cuyo `.value` es `"M"`
- `EstadoGato["COL"]` busca el miembro cuyo `.name` es `"COL"`

Usar `.name` es más seguro para enums cuyos valores pueden cambiar,
porque el nombre del miembro en el código es más estable que su
descripción textual.

### Fail fast
Principio de diseño que dice que un sistema debe detectar y reportar errores
lo antes posible, en lugar de continuar ejecutándose con datos inválidos y
fallar más tarde en un punto inesperado. En GestiCat se aplica en los setters
del dominio: si alguien intenta crear un `Gato` con un ID inválido, el error
se lanza inmediatamente en el setter, no cuando se intenta usar el gato más
adelante. Esto hace los errores más fáciles de localizar y corregir. Es la
razón por la que las validaciones viven en el dominio y no en la presentación.

### Type hinting
Sistema de Python para indicar de forma opcional el tipo esperado de los
parámetros y el valor de retorno de una función o método. No es obligatorio
ni lo comprueba Python en tiempo de ejecución, pero mejora la legibilidad
del código y permite que los editores como VSCode detecten errores antes de
ejecutar. Ejemplo en GestiCat: `def tramitar_anexo(self, nuevo_estado: EstadoColonia)`
indica que `nuevo_estado` debe ser una instancia de `EstadoColonia`.
Documentación oficial: https://docs.python.org/3/library/typing.html

### ABC (Abstract Base Class)
Mecanismo de Python para definir clases abstractas que no pueden instanciarse
directamente. Se importa con `from abc import ABC`. Al heredar de `ABC`, Python
impide crear instancias de esa clase — solo se pueden instanciar sus subclases.
Usado en GestiCat en `Responsable` para impedir su instanciación directa y
obligar a usar `PersonaFisica` o `Protectora`.

### @abstractmethod
Decorador que va justo encima de un método dentro de una clase `ABC`. Marca
ese método como obligatorio — cualquier subclase debe implementarlo antes de
poder instanciarse. Sin `@abstractmethod`, Python no avisa si una subclase
olvida implementar un método hasta que se intenta llamarlo en tiempo de
ejecución. Con `@abstractmethod`, el error aparece en el momento de crear el
objeto. Se importa con `from abc import ABC, abstractmethod`. Usado en
`RepositorioGatos` para garantizar que cualquier implementación concreta
implemente `insertar`, `actualizar`, `listar`, `obtener` y `quitar`.
Nota: pendiente de aplicar cuando el profesor lo explique en clase.

### Instancia
Objeto concreto creado a partir de una clase. La clase es el molde (define
estructura y comportamiento), la instancia es el objeto real en memoria con
sus propios datos. `Gato("001", "Miguelito", ...)` crea una instancia de `Gato`.

### Persistencia
Guardar datos de forma que sobrevivan al cerrar el programa. Un diccionario
en memoria no es persistente. Un archivo JSON, SQLite o una API sí lo son.
En GestiCat, llamar a `actualizar()` en el repositorio es el paso que hace
que un cambio sea persistente, aunque en `RepositorioGatosMemoria` no marque
diferencia práctica.

### Documentación inline
Documentación que vive dentro de los propios archivos `.py`, entrelazada con
el código. Incluye docstrings de módulo, clase y método, y comentarios. Se
distingue de la documentación externa (archivos `.md` en `docs/`).

### Hardcodeado
Valor escrito fijo directamente en el código en lugar de venir de una variable
o entrada del usuario. No siempre es malo — a veces es una decisión de diseño
intencionada que merece un comentario explicando el por qué. Ejemplo en
GestiCat: `servicio.actualizar_esterilizacion_gato(id_gato, True, clinica)` —
el `True` es hardcodeado porque el dominio impide revertir una esterilización.

### Invariantes
Condiciones que siempre deben cumplirse para que una entidad del dominio sea
válida, antes y después de cualquier operación. Si una invariante se rompe,
el sistema está en un estado inconsistente. Ejemplos en GestiCat: "un gato
esterilizado siempre tiene clínica asignada", "el precio siempre es mayor
que 0", "no puede haber dos gatos con el mismo ID en la colonia". Las
invariantes se protegen en los setters del dominio lanzando excepciones si
se intentan violar.

### Top-down vs Bottom-up
Dos enfoques para construir un proyecto. Top-down empieza por la interfaz de
usuario (menú con `pass`) para definir casos de uso antes de implementar.
Bottom-up empieza por el dominio, construyendo sobre una base sólida de reglas
de negocio. Ambos son válidos — bottom-up encaja mejor cuando las reglas de
negocio son conocidas y complejas desde el principio, como en GestiCat.

### FUTURE_IMPROVEMENTS.md — por qué existe este documento
Durante el desarrollo es habitual dejar comentarios `# TODO` en el código
para marcar ideas pendientes. El problema es que en una entrega o revisión
esos comentarios ensucian el código y dan la impresión de trabajo inacabado.

`docs/FUTURE_IMPROVEMENTS.md` es el lugar donde esas ideas viven de forma
ordenada y visible, fuera del código. Sirve para tres cosas:
- Mantener el código limpio, sin TODOs dispersos.
- No perder ninguna idea de mejora entre sesiones.
- Comunicar al lector (o al profesor) que esas decisiones son intencionadas,
  no olvidos.

La regla es simple: cuando un `# TODO` no se va a implementar en la fase
actual, se mueve a este documento con su contexto y se elimina del código.

### README.md raíz vs docs/README.md

En un proyecto bien documentado conviven dos archivos README con propósitos
distintos:

- **`README.md` raíz**: carta de presentación del proyecto. Lo primero que
  ve cualquier persona que llega al repositorio. Explica qué es el proyecto,
  cómo instalarlo y cómo ejecutarlo. Está pensado para cualquier audiencia.

- **`docs/README.md`**: índice de la documentación técnica. Solo lo lee
  quien quiere profundizar en el diseño, las reglas de negocio o la
  arquitectura. Está pensado para quien ya está dentro del proyecto.

La regla: el README raíz es para entrar, el README de docs es para
profundizar.

### strftime — formatear fechas como texto
Método del objeto `date` (y `datetime`) de Python que convierte una fecha
en un string con el formato que le indiques.
Se usa en los tests cuando necesitas comparar una fecha (`date`) con un
string, porque Python no puede comparar directamente tipos distintos.
Sin `strftime`, `assertEqual(gato.fecha_registro, "10/01/2024")` fallaría
aunque la fecha sea correcta.
Documentación oficial: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

### setUp — preparador de tests en unittest

Método especial de `unittest.TestCase` que se ejecuta automáticamente
antes de cada test. No empieza por `test_` pero `unittest` lo reconoce
por su nombre exacto.

Se usa para preparar el estado necesario antes de cada test: crear objetos,
inicializar datos, configurar dependencias. Evita repetir el código de
preparación en cada método de test.

**Clave:** se ejecuta antes de *cada* test, no una sola vez. Esto garantiza
que cada test empieza desde un estado limpio e independiente del resto.
Sin `setUp`, un test que modifique el estado podría afectar a los siguientes.

Documentación oficial: https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp

### Aislamiento en tests unitarios

En tests unitarios, cada test debe controlar exactamente su estado y no
depender de datos externos. Hay dos enfoques para construir el estado
inicial en `setUp`:

- Tests **unitarios** → **Construir desde cero**: crear todos los objetos necesarios directamente
  en `setUp`. Los tests son completamente independientes — si cambia
  `datos_iniciales.py`, los tests no se ven afectados.

- Tests de **integración** → **Usar datos iniciales**: delegar la construcción a una función de
  `datos_iniciales.py`. El `setUp` es más limpio pero los tests dependen
  de datos externos — si alguien modifica los datos iniciales, los tests
  pueden fallar sin que el código haya cambiado.


### Conversión silenciosa vs prohibición explícita en setters
Dos formas de manejar datos con formato incorrecto en los setters del dominio:
- **Conversión silenciosa**: el setter corrige el dato automáticamente.
  Apropiado cuando es una normalización de formato intencionada y esperada
  (mayúsculas, eliminar guiones...).
- **Prohibición explícita**: el setter lanza un error y obliga a corregirlo.
  Apropiado cuando el dato mal formado es probablemente un error del usuario.

La regla es: si es una normalización conocida → conversión silenciosa.
Si es un posible error → prohibición explícita con mensaje claro.
La misma regla debe aplicarse de forma consistente en todo el dominio.

**Importante:** los espacios laterales solo se comprueban en campos de
texto libre donde se escribe directamente. En campos con formato
estructurado (fechas, emails) el propio parser detecta el error de formato
y no es necesaria una comprobación adicional de espacios.

### Coverage

Herramienta de Python que mide qué líneas del código se ejecutan al correr
los tests. El resultado se expresa como porcentaje. Útil para detectar
partes del código sin tests, pero un 100% de cobertura no garantiza calidad
— un test puede ejecutar una línea sin verificar nada útil.

Documentación oficial: https://coverage.readthedocs.io

##SQLite y bd
### PRAGMA

Mecanismo propio de SQLite (no es SQL estándar) para leer o cambiar
configuraciones del motor en tiempo de ejecución. Sintaxis:

```sql
PRAGMA nombre = valor;   -- cambiar configuración
PRAGMA nombre;           -- leer valor actual
```

En proyectos normales solo necesitas uno:

```sql
PRAGMA foreign_keys = ON;
```

SQLite tiene las claves foráneas **desactivadas por defecto**. Sin este PRAGMA,
puedes insertar un gato con una `colonia_nombre` que no existe y SQLite lo
acepta sin error. Con él activado, esa inserción falla como debe fallar.

Hay que activarlo en **cada conexión** — no persiste entre sesiones.

Documentación oficial: https://www.sqlite.org/pragma.html


### cursor.rowcount — filas afectadas por la última operación

Después de ejecutar un `UPDATE` o `DELETE`, SQLite no lanza error si
no encuentra ninguna fila — simplemente no hace nada.

`cursor.rowcount` indica cuántas filas afectó la última operación:
- `1` → encontró y modificó la fila
- `0` → no encontró ninguna fila


### Excepciones de dominio vs excepciones técnicas

Cuando un repositorio falla (duplicado, no encontrado, error de base de datos),
puede lanzar dos tipos de excepciones:

- **Excepciones técnicas**: las que lanza el motor directamente.
  `sqlite3.IntegrityError`, `psycopg2.IntegrityError`, `KeyError`...
  Son específicas del motor o tecnología que estás usando.

- **Excepciones de dominio**: las que define tu aplicación con significado
  de negocio. `GatoYaExisteError`, `GatoNoEncontradoError`...
  No saben nada del motor — solo describen qué salió mal en términos
  del problema que resuelve el sistema.

El repositorio captura las excepciones técnicas y las convierte en excepciones
de dominio. Las capas superiores (aplicación y presentación) solo ven las de
dominio y nunca importan `sqlite3` ni ningún otro motor.

Beneficio: si mañana se cambia de SQLite a PostgreSQL por ejemplo, solo cambia el repositorio.
El servicio, el menú y los tests siguen funcionando sin tocarlos.

### Decisión: gesticat.db en el repositorio

En proyectos reales, los ficheros de base de datos no deben subirse al
repositorio porque se regeneran automáticamente, cambian con el uso y
pueden contener datos sensibles.

En GestiCat lo mantengo en el repositorio para que pueda verse sin necesidad de ejecutar.

En un proyecto real se añadiría al `.gitignore`.


### Parser / Parsear
Leer un dato en bruto y convertirlo a una estructura que el programa
puede usar.
Si el formato no es el esperado, el parser falla y lanza un error.
Por eso en campos con formato estructurado (fechas, emails) no hace falta
comprobar espacios laterales por separado — el parser ya los detecta.

Ejemplos cotidianos: `int("42")` convierte un string a entero.
El navegador parsea HTML y lo convierte en la página visible.

### Buena práctica — longitud máxima de línea
PEP 8 recomienda máximo 79 caracteres por línea de código y 72 para docstrings
y comentarios. Muchos proyectos modernos usan 88 (límite de `black`,
formateador automático). El editor puede mostrar una guía visual configurando
la regla en VSCode o PyCharm.
Referencia: https://peps.python.org/pep-0008/#maximum-line-length

### Buena práctica — orden de imports
PEP 8 indica que todos los imports deben ir al principio del archivo, justo
después del docstring del módulo. Nunca en medio del código.
Referencia: https://peps.python.org/pep-0008/#imports

### Buena práctica — carpeta de ejecución
En Python es más correcto ejecutar desde la carpeta que contiene el paquete
(`02-documentando/`) que desde dentro del paquete (`gesticat/`). Esto permite
usar imports absolutos (`from gesticat.domain.gato import Gato`), es compatible
con herramientas como `pytest`, `coverage` y frameworks como Flask. Actualmente
el proyecto usa imports relativos y obliga a ejecutar desde dentro de `gesticat/`.
El refactor a imports absolutos está pendiente para la fase 03.

### Comando Unix: touch
Crea un archivo vacío si no existe, o actualiza la fecha de modificación si
ya existe. Se usa mucho en proyectos Python para crear los archivos
`__init__.py` vacíos que convierten una carpeta en un paquete.
Ejemplo: `touch gesticat/domain/__init__.py`. Disponible en Linux y macOS.

---

## Decisiones de diseño

### fecha_registro opcional en Gato
`fecha_registro` acepta `None` y usa `date.today()` como valor por defecto,
para facilitar el uso diario sin introducir fecha y las migraciones desde
registros en papel sin perder fechas históricas.

### Validación de fecha futura en fecha_registro y fecha_nacimiento
Técnicamente redundante con la validación de mayoría de edad (en
`fecha_nacimiento`) y con la validación de fecha futura (en `fecha_registro`),
pero se mantienen ambas por claridad del mensaje de error. Una fecha futura
daría un mensaje confuso de "menor de edad" sin la validación explícita.

### guardar() → insertar() + actualizar()
Separar en dos operaciones distintas hace el contrato más explícito y prepara
el proyecto para persistencia real. En memoria, modificar un objeto directamente
ya actualiza el diccionario porque Python trabaja con referencias. Pero en
SQLite, JSON o una API, habría que llamar explícitamente a una operación de
escritura. Al introducir `actualizar()` desde ahora, cualquier repositorio
futuro funcionará sin cambiar `Colonia` ni `ServicioColonia`.

### Responsable como ABC
`Responsable` convertida en clase abstracta con `ABC` para impedir su
instanciación directa. Al heredar de `ABC`, Python lanza `TypeError` si
alguien intenta instanciarla. Sin `ABC`, la restricción era solo documental.

### RepositorioGatos sin ABC
`RepositorioGatos` mantiene `raise NotImplementedError` en lugar de `ABC` y
`@abstractmethod` para seguir el estilo del profesor y no adelantar conceptos
que aún no se han dado en clase. Se revisará cuando se trabaje con bases de
datos SQL.

### Orden de capas en documentación
En el alcance y el mapa de archivos se ordena de dentro hacia afuera:
domain → infrastructure → application → presentation → tests. Refleja la
arquitectura del proyecto y las dependencias entre capas.



---

## Mejoras futuras

### Gestión de múltiples colonias
Añadir `RepositorioColonias` y `ServicioColonias` para gestionar múltiples
colonias. La entidad `Colonia` ya está diseñada para ello sin necesidad de
cambios. El menú necesitaría adaptarse para listar las colonias disponibles
y permitir seleccionar con cuál trabajar antes de operar.

### Gestión de responsables
`RepositorioResponsables` con su contrato e implementación (mismo patrón que
`RepositorioGatos`). Operaciones: crear responsable nuevo, buscar responsable
existente por identificación, asignar a una colonia. En SQL esto se modelaría
con una tabla `responsables` y una clave foránea en la tabla `colonias`.

### Repositorios alternativos
`RepositorioGatosMemoria` podría sustituirse por `RepositorioGatosJSON`,
`RepositorioGatosSQLite` o similar para persistencia real. Al respetar el
contrato de `RepositorioGatos`, el resto del proyecto no necesitaría ningún
cambio. Solo se modificaría `datos_iniciales.py` para instanciar el nuevo
repositorio.

### UX en menu.py
Actualmente cualquier input inválido aborta la función y vuelve al menú
principal. Lo correcto en producción sería usar bucles `while` con `try/except`
por cada campo para permitir reintentar solo el campo incorrecto sin perder
los datos ya introducidos. El profesor indica que esto se implementará de
forma natural cuando se migre a una interfaz web con Flask, donde la
validación de formularios funciona de forma distinta.

### MarcaEsterilizacion
Enum pendiente de implementar para registrar la marca física de esterilización
en las orejas del gato (sin marca, oreja izquierda, oreja derecha). Está
comentado en `gato.py` como `TODO`.

### Registrar fecha en cambios de estado
Registrar la fecha cuando el estado de un gato pase a `ADOP`, `FALL` o `DESA`.
Está marcado como `TODO` en el enum `EstadoGato`.

### Desglose de esterilizados por sexo en reporte_censo
Añadir al reporte de censo el desglose de gatos esterilizados por sexo.
Está marcado como `TODO` en `reporte_censo()` de `Colonia`.


---

## Arquitectura por capas — para qué sirve cada capa

- **Domain (dominio)** — es el cerebro del sistema. Contiene las reglas del
  negocio: qué es un gato, qué condiciones debe cumplir, qué está permitido
  y qué no. Es la capa más importante y no depende de nadie.
- **Infrastructure (infraestructura)** — es el almacén. Se encarga de guardar
  y recuperar los datos. Ahora mismo los guarda en memoria (se pierden al
  cerrar), pero podría cambiarse por una base de datos sin tocar nada más.
- **Application (aplicación)** — es el coordinador. Recibe las peticiones del
  menú, las organiza y delega el trabajo en el dominio. No toma decisiones de
  negocio, solo orquesta. Si mañana hay una interfaz web, usaría el mismo
  coordinador.
- **Presentation (presentación)** — es la ventana al usuario. Muestra el menú,
  recoge lo que escribe el usuario y muestra los resultados. No sabe nada de
  cómo funciona el sistema por dentro — solo habla con el coordinador.

---

### Conventional Commits

Convención para escribir mensajes de commit descriptivos y consistentes.
Cada commit empieza con un prefijo que indica el tipo de cambio:

- `feat:` — nueva funcionalidad
- `fix:` — corrección de un bug
- `refactor:` — cambio de código que no añade funcionalidad ni corrige bug
- `docs:` — cambios en documentación
- `test:` — añadir o modificar tests
- `chore:` — tareas de mantenimiento (dependencias, configuración...)

Referencia: https://www.conventionalcommits.org
