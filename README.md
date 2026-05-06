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

### Fase 01 y 02

Clonar el repositorio:

```bash
git clone git@github.com:Siboney-python/proyecto-colonia.git
```

Acceder a la carpeta de la fase y ejecutar desde la carpeta que contiene `gesticat/` (en fase 01 desde gesticat/`):

```bash
# Fase 01
cd proyecto-colonia/proyecto/01-diseno-capas/gesticat
python3 -m presentation.menu

# Fase 02
cd proyecto-colonia/proyecto/02-documentando
python3 -m gesticat.presentation.menu

# Fase 03
cd proyecto-colonia/proyecto/03-testing
python3 -m gesticat.presentation.menu

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
<summary>Fase 03 — Testing ⬜</summary>

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

<details open>
  <summary>Fase 04 - persistencia con SQLite</summary>

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
- [ ] *(opcional)* Crear tests específicos para el repositorio SQLite

### Documentación

- [ ] Actualizar `CHANGELOG.md` (versión `0.4.0`) con los cambios principales
- [ ] Actualizar `README.md` con instrucciones de cómo ejecutar el script de inicialización
- [ ] Documentar el diseño de la BD en `docs/DISEÑO_BD.md`:
- [ ] (*opcional*) Documentar el contrato de excepciones en `docs/CONTRATO_EXCEPCIONES.md`:

### Verificación final

- [ ] La aplicación funciona igual desde el punto de vista del usuario (mismo menú, mismas operaciones)
- [ ] Los datos persisten entre ejecuciones (cierra y reabre la app, verifica que los datos están)
- [ ] Los tests pasan todos sin cambios de lógica de dominio

</details>

---

## Aspectos a tener en cuenta durante el desarrollo

- Hacer `pull` antes de empezar a trabajar para sincronizar cambios del repositorio remoto.
- Hacer commits periódicos cada vez que se complete una tarea.
- Hacer `push` después de cada commit.
- Añadir al repositorio en subcarpeta las actividades completadas en clase.

---
*Proyecto desarrollado por Siboney Pérez Martínez — IES El Rincón, 2025-2026.*
