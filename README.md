# Proyecto GestiCat — Módulo 5100 Programación Orientada a Objetos

Proyecto del Curso de Especialización en Desarrollo de Aplicaciones en Lenguaje Python.

El objetivo es construir una aplicación real aplicando los principios de
Programación Orientada a Objetos (POO) vistos en clase: encapsulamiento,
herencia, separación de responsabilidades y arquitectura por capas.

El proyecto elegido es **GestiCat LPGC** — un sistema de gestión y censo de
colonias felinas urbanas de Las Palmas de Gran Canaria. Es un proyecto de idea
propia, inspirado en la gestión real de colonias felinas del municipio, con el
objetivo de convertirse en una herramienta útil para las personas voluntarias
que las gestionan.

## Instrucciones para ejecutar el proyecto

### TODAS LAS FASES

Clonar el repositorio:

```bash
git clone git@github.com:Siboney-python/proyecto-colonia.git
```

Acceder a la carpeta de la fase y ejecutar desde la carpeta que contiene `gesticat/` (en fase 01 desde gesticat/`):

```bash
# Fase 01
cd proyecto-colonia/proyecto/01-diseno-capas/gesticat
python3 -m presentation.menu
```

```
# Fase 02
cd proyecto-colonia/proyecto/02-documentando
python3 -m gesticat.presentation.menu
```

```
# Fase 03
cd proyecto-colonia/proyecto/03-testing
python3 -m gesticat.presentation.menu

python3 -m unittest

coverage run -m unittest
coverage report
```

```
# Fase 04
cd proyecto-colonia/proyecto/04-sqlite
python3 -m gesticat.crear_bd
python3 -m gesticat.presentation.menu
```

```
# Fase 05
cd proyecto-colonia/proyecto/05-flask-01
python3 -m gesticat.crear_bd
python3 -m gesticat.presentation.app

# Abre `http://localhost:5000` en el navegador.
```

## Fases del proyecto

### Fase 01 — Diseño por capas
Organizar la aplicación en cuatro capas (presentación, aplicación, dominio e
infraestructura), aplicar los principios de POO y crear un menú de consola funcional.

### Fase 02 — Documentación
Mejorar la documentación inline del código (docstrings y comentarios) y crear
la documentación externa del proyecto en `docs/`.

### Fase 03 — Testing
Reorganizar y ampliar los tests usando `unittest` y medir la cobertura con `coverage`.

### Fase 04 - Persistencia con SQLite
Añadir persistencia real con SQLite: diseño del esquema de base de datos,
script de inicialización, repositorio SQLite, excepciones de dominio
y tests específicos para el repositorio.

### Fase 05 — Interfaz web con Flask (parte 1)
Añadir Flask como segunda capa de presentación. Todas las operaciones del
menú de consola expuestas como routes de una API web. El menú de consola
sigue funcionando sin cambios.

### Fase 05 — Interfaz web con Flask (parte 2)
Añadir observabilidad global a la interfaz web: manejadores de error 404 y 500
con HTML personalizado, ruta `/ayuda` con introspección de routes, y logging
de peticiones en fichero `gesticat.log`.

### Fase 05 — Plantillas Jinja2 (parte 3)
Introducir plantillas Jinja2 para sacar el HTML inline de `app.py`: plantilla
base con cabecera y navegación, plantillas hijas para cada vista de lectura,
y plantilla común para errores 404 y 500.

### Fase 05 — Formularios HTML y método POST (parte 4)
Convertir las operaciones de escritura en formularios HTML con método POST.
Validación con re-render conservando los datos tecleados, patrón
Post/Redirect/Get tras éxito, y confirmación antes de eliminar.
Ninguna acción de escritura queda accesible por GET.

---

## Checklists por fases

<details>
<summary>Fase 01 — Diseño por capas ✅</summary>

- [x] Crear cuenta en Github.
- [x] Crear repositorio para alojar el proyecto.
- [x] Compartir repositorio con el usuario del profesor (ichigar).
- [x] Instalar y configurar GIT en ordenador de clase y en ordenador de casa.
- [x] Crear claves SSH en ordenador de casa y en ordenador de clase. Añadir claves públicas a las cuentas de GitHub.
- [x] Clonar repositorio en clase y en casa.
- [x] Probar a hacer cambios en clase y en casa y aprender a mantener actualizados los cambios realizados (clase/casa/repositorio).
- [x] Crear subcarpeta `proyecto/` en el repositorio.
- [x] Incluir `README.md` con las instrucciones para instalar y ejecutar el proyecto.
- [x] Crear en `proyecto/` la subcarpeta `01-diseno-capas/` e incluir en la misma el código para dicha fase.
- [x] Los apartados de la interfaz que aparecen en el menú principal funcionan correctamente.
- [x] El proyecto está organizado en capas.
- [x] La estructura de archivos y carpetas sigue las pautas de módulos, paquetes y subpaquetes vistas en clase.
- [x] Se han aplicado los principios de POO vistos en clase.
- [x] Los nombres de ficheros, clases y variables son significativos y siguen los principios de la recomendación PEP 8.

</details>

<details>
<summary>Fase 02 — Documentación ✅</summary>

- [x] Copiado en subcarpeta `02-documentando/` el contenido de `01-diseno-capas/`.
- [x] Renombrar todos los identificadores de módulos, clases, métodos y variables que no cumplan con los criterios de los apuntes.
- [x] Añadir docstring a los módulos, clases y métodos públicos del proyecto.
- [x] Comentar las reglas de negocio de las clases del dominio.
- [x] Comentar los bloques de código que no expresen claramente para qué se usan.
- [x] Eliminar comentarios evidentes.
- [x] `README.md`
- [x] `CHANGELOG.md`
- [x] `docs/README.md`
- [x] `docs/DESCRIPCION_Y_ALCANCE.md`
- [x] `docs/EJECUCION.md`
- [x] `docs/ARQUITECTURA_POR_CAPAS.md`
- [x] `docs/CASOS_DE_USO.md`
- [x] `docs/REGLAS_DE_NEGOCIO.md`
- [x] `docs/MODELO_DE_DOMINIO.md`
- [x] `docs/CONTRATO_REPOSITORIO.md`
- [x] `docs/DATOS_INICIALES.md`
- [x] `docs/TESTS_Y_PASOS.md`
- [x] `docs/TROUBLESHOOTING.md`

</details>

<details>
<summary>Fase 03 — Testing ✅</summary>

- [x] Copiar en `03-testing/` el estado base de `02-documentando/`.
- [x] Reorganizar las pruebas en la subcarpeta `tests/`.
- [x] Crear y mantener tests para, al menos, dos clases del dominio.
- [x] Verificar que todos los tests pasan con `python3 -m unittest`.
- [x] Añadir `coverage` como dependencia en `requirements.txt`.
- [x] Ejecutar cobertura con `coverage run -m unittest` y revisar reporte con `coverage report`.
- [x] Documentar la ejecución de tests y coverage en `docs/TESTS_Y_PASOS.md`.
- [x] Actualizar `docs/EJECUCION.md` con pasos completos desde clonado hasta ejecución.
- [x] Revisar y corregir documentos desactualizados de `docs/` para reflejar la fase 03.
- [x] Registrar los cambios de fase en `CHANGELOG.md` (versión `0.3.0`).
- [x] Actualizar `README.md` para reflejar estructura y comandos actuales.

</details>

<details>
  <summary>Fase 04 - Persistencia con SQLite ✅</summary>

### Diseño e implementación del esquema de base de datos

- [x] Copiar en `04-sqlite` el estado base de `03-testing` (o crear rama específica para la fase 04).
- [x] Diseñar las tablas SQL mapeando cada entidad de dominio a tablas con sus columnas, tipos y restricciones (`PRIMARY KEY`, `NOT NULL`, `FOREIGN KEY`).
- [x] Usar nombres de columnas en snake_case.

### Script de inicialización de base de datos

- [x] Crear script que cree el esquema de la BD e inserte datos iniciales de prueba
  - [x] Debe poder ejecutarse varias veces sin error
  - [x] Crea todas las tablas respetando dependencias de claves foráneas
  - [x] Inserta datos iniciales para probar la aplicación

### Excepciones de dominio para persistencia

- [x] (*opcional*) Crear fichero de excepciones (`infrastructure/errores.py`) con las excepciones que el repositorio SQLite lanza al usuario
  - [x] Clase base para todas las excepciones de persistencia
  - [x] Excepciones por cada tipo de error que puede ocurrir (duplicado, no encontrado, etc.)

### Implementación del repositorio SQLite

- [x] Crear clase(s) de repositorio que implementen persistencia en SQLite (realizando las mismas operaciones que el repositorio en memoria: guardar, obtener, actualizar, eliminar, etc.)
- [x] Usar consultas SQL parametrizadas (parámetros `?`) para prevenir inyección SQL
- [x] Capturar excepciones SQLite (`sqlite3.IntegrityError`, `sqlite3.OperationalError`, etc.) y transformarlas en excepciones de dominio
- [x] Activar `PRAGMA foreign_keys = ON` al conectar para garantizar integridad referencial
- [x] **El flujo principal de la aplicación (menú) debe usar SOLO el repositorio SQLite para persistencia** (no usar en memoria)

### Repositorio en memoria (referencia, no en uso)

- [x] (**opcional**) Mantener el código del repositorio en memoria como referencia de implementación y contrato
- [x] (**opcional**) Modificar `infrastructure/repositorio_memoria.py` para lanzar las **mismas excepciones de dominio** que el repositorio SQLite (útil para tests sin persistencia)

### Integración con SQLite en la capa de presentación

- [x] Modificar la capa de presentación para cargar datos iniciales desde la BD en lugar de desde memoria (al iniciar la aplicación)
- [x] Capturar excepciones de dominio, no excepciones de `sqlite3`
- [ ] (*opcional*) Mostrar mensajes amigables al usuario cuando ocurran errores de persistencia
- [x] No hacer imports de `sqlite3` directamente en la presentación.

### Actualización de los tests

- [x] *(opcional)* Actualizar tests existentes para esperar excepciones de dominio en lugar de excepciones genéricas de Python
- [x] Verificar que `python -m unittest` pasa con todos los tests en verde
- [x] *(opcional)* Crear tests específicos para el repositorio SQLite

### Documentación

- [x] Actualizar `CHANGELOG.md` (versión `0.4.0`) con los cambios principales
- [x] Actualizar `README.md` con instrucciones de cómo ejecutar el script de inicialización
- [x] Documentar el diseño de la BD en `docs/DISEÑO_BD.md`:
- [ ] (*opcional*) Documentar el contrato de excepciones en `docs/CONTRATO_EXCEPCIONES.md`:

### Verificación final

- [X] La aplicación funciona igual desde el punto de vista del usuario (mismo menú, mismas operaciones)
- [x] Los datos persisten entre ejecuciones (cierra y reabre la app, verifica que los datos están)
- [x] Los tests pasan todos sin cambios de lógica de dominio

</details>

<details>
  <summary>Fase 05 - Flask como nueva capa de presentación (parte 1) ✅</summary>

### Preparación

- [x] Carpeta `05-flask-01/` creada con el contenido de `04-sqlite/` como base.
- [x] `requirements.txt` incluye `flask`.

### Aplicación Flask

- [x] `presentation/app.py` ejecutable con `python -m gesticat.presentation.app`.
- [x] Route `/` con mensaje de bienvenida y enlaces a las rutas principales.
- [x] Routes de lectura: `/gatos`, `/gatos/<id_gato>`, `/gatos/sin-esterilizar`, `/colonia`, `/colonia/censo`.
- [x] Routes de escritura: registrar, eliminar, cambiar estado, esterilizar, tramitar anexo, asignar responsable.
- [x] Parámetros tipados con converters (`<int:id>`, `<float:precio>`…) donde aplica.
- [x] Routes que modifican datos redirigen con `redirect(url_for(...))`.

### Gestión de errores

- [x] Excepciones de dominio capturadas con código HTTP apropiado (404, 409, 400).

### Integridad de capas

- [x] `presentation/menu.py` sigue funcionando sin cambios.

### Documentación

- [x] `CHANGELOG.md` con entrada nueva (`0.5.0`).
- [x] `README.md` y `docs/EJECUCION.md` actualizados.
- [x] `docs/ARQUITECTURA_POR_CAPAS.md` actualizado con `app.py`.

</details>

<details>
  <summary>Fase 05 - Observabilidad: manejadores de error, introspección y logging (parte 2) ✅</summary>

### Preparación

- [x] Carpeta `05-flask-02/` creada con el contenido de `05-flask-01/` como base.

### Manejadores globales de error

- [x] `@app.errorhandler(404)` registrado y devuelve HTML personalizado al visitar una URL inexistente.
- [x] `@app.errorhandler(500)` registrado y devuelve HTML personalizado. Probado provocando una excepción no controlada.

### Introspección

- [x] Ruta `/ayuda` que itera `app.url_map.iter_rules()`, filtra `static` y muestra todas las rutas registradas. Al añadir o quitar rutas, `/ayuda` refleja el cambio sin tocar su código.

### Logging

- [x] `logging.basicConfig(...)` configurado al inicio de `app.py` con nombre de fichero `gesticat.log`.
- [x] Hook `@app.before_request` registra cada petición con método y ruta.
- [x] El fichero `.log` aparece en disco al hacer peticiones, con timestamp y una línea por petición.
- [x] `.gitignore` incluye `*.log` y el fichero de log no se versiona.

### Integridad de capas y coexistencia

- [x] Coexistencia menu↔web verificada: un alta hecha desde la web aparece en el menú y viceversa.
- [x] `presentation/menu.py` sigue funcionando sin cambios.

### Documentación

- [x] `CHANGELOG.md` con entrada nueva `0.6.0`.
- [x] `README.md` y `docs/EJECUCION.md` actualizados (mencionan `/ayuda`, el fichero `.log` y cómo reconfigurar el logging).

</details>

<details>
  <summary>Fase 05 — Plantillas Jinja2 (parte 3) ✅</summary>

### Preparación
- [x] Carpeta `05-flask-03/` creada con el contenido de `05-flask-02/` como base.
- [x] Borrar el `.venv` copiado y crear uno nuevo con `python3 -m venv .venv` e `pip install -r gesticat/requirements.txt`.

### Plantillas
- [x] Plantilla base `base.html` con la estructura común y bloques.
- [x] Plantillas hijas para las vistas de lectura, extendiendo de `base.html`.
- [x] Sintaxis Jinja2 aplicada: inyección de valores, iteración, condicionales y filtros.
- [x] Conversión tupla → diccionario en el route cuando el servicio devuelva tuplas.
- [x] `url_for` en plantillas para los enlaces (no hardcodear URLs).
- [x] Plantilla común `error.html` reutilizada por `@app.errorhandler(404)` y `@app.errorhandler(500)`.

### Routes
- [x] Se han generado plantillas para todas las rutas que muestran información del proyecto.
- [x] Los routes de lectura usan `render_template` en lugar de devolver texto o HTML inline.

### Verificación visual
- [x] La cabecera con navegación es visible en todas las páginas, incluidas las de error 404 y 500.

### Integridad de capas
- [x] `domain/` e `infrastructure/` sin cambios. `application/` solo añade métodos de delegación pura si hace falta.
- [x] `presentation/menu.py` sigue funcionando sin cambios.

### Documentación
- [x] `CHANGELOG.md` con entrada nueva `0.7.0`.
- [x] `README.md` y `docs/EJECUCION.md` actualizados (mencionan `presentation/templates/` y el patrón de herencia con `base.html`).

</details>

<details open>
  <summary>Fase 05 — Formularios HTML y método POST (parte 4) [ ]</summary>

### Preparación
- [x] Carpeta `05-flask-04/` creada con el contenido de `05-flask-03/` como base.
- [ ] Borrar el `.venv` copiado y crear uno nuevo con `python3 -m venv .venv` e `pip install -r gesticat/requirements.txt`.

### Formularios
- [ ] Cada operación de escritura tiene su plantilla HTML en `presentation/templates/`, extendiendo de `base.html`.
- [ ] Cada `<form>` tiene `method="post"` y `action="{{ url_for(...) }}"`.
- [ ] Los campos conservan los datos tecleados al volver tras un error.
- [ ] Mensaje de error visible en el formulario cuando el dominio lanza una excepción.

### Routes
- [ ] Las routes de escritura aceptan `methods=['GET', 'POST']` (o solo `['POST']` si no necesitan pantalla previa).
- [ ] Rama `GET` renderiza el formulario vacío (o con datos actuales si es edición).
- [ ] Rama `POST` procesa los datos y llama al servicio del dominio.
- [ ] Tras POST con éxito: `redirect(url_for(...))` a una ruta de lectura — patrón Post/Redirect/Get.
- [ ] Tras POST con error: re-render del formulario con código HTTP coherente (400, 404, 409).

### Eliminaciones
- [ ] `GET /gatos/<id_gato>/eliminar` muestra pantalla de confirmación con datos del gato.
- [ ] `POST /gatos/<id_gato>/eliminar` ejecuta la baja y redirige a `/gatos`.

### Verificación
- [ ] Ninguna URL accesible por GET modifica estado del dominio.
- [ ] Las rutas viejas de escritura con parámetros en URL (de `ut4e1`) han desaparecido o devuelven 404.

### Integridad de capas
- [ ] `domain/` e `infrastructure/` sin cambios.
- [ ] `application/` solo con métodos de delegación pura si hace falta.
- [ ] `presentation/menu.py` sigue funcionando sin cambios.

### Documentación
- [ ] `CHANGELOG.md` con entrada nueva `0.8.0`.
- [ ] `README.md` y `docs/EJECUCION.md` actualizados con lista de rutas y verbos HTTP.

</details>
---

## Aspectos a tener en cuenta durante el desarrollo

- Hacer `pull` antes de empezar a trabajar para sincronizar cambios del repositorio remoto.
- Hacer commits periódicos cada vez que se complete una tarea.
- Hacer `push` después de cada commit.
- Añadir al repositorio en subcarpeta las actividades completadas en clase.

---
*Proyecto desarrollado por Siboney Pérez Martínez — IES El Rincón, 2025-2026.*
