# Changelog

Todos los cambios relevantes del proyecto, organizados por versión y fase.

---

## [0.3.0] - 2026-04-18 (Fase 03: testing)

Versión disponible en `proyecto/03-testing/`

### Added
- Paquete de pruebas `tests/` con `test_gato.py`, `test_responsable.py`
  y `test_colonia.py` usando `unittest`.
- `requirements.txt` con `coverage` como dependencia.
- `.gitignore` para excluir `.venv/`, `htmlcov/` y `.coverage`.
- `docs/FUTURE_IMPROVEMENTS.md` con ideas de desarrollo pendientes. (También añadido en la fase 02)

### Changed
- `docs/TESTS_Y_PASOS.md` actualizado con los nuevos comandos de unittest
  y coverage.
- `docs/EJECUCION.md` actualizado con pasos de preparación del entorno
  virtual e instalación de dependencias.
- `README.md` actualizado con estructura y comandos actuales.
- `infrastructure/datos_iniciales.py` refactorizado: `cargar_datos_iniciales()`
  renombrado a `crear_colonia_con_datos()` y añadida `crear_servicio()`.

### Fixed
- Setters de `nombre`, `telefono`, `email` e `identificacion` en
  `responsable.py` corregidos para prohibir espacios laterales
  explícitamente en lugar de eliminarlos silenciosamente.
- Setter de `nombre` en `colonia.py` corregido por el mismo motivo.
- `RepositorioGatos` convertido a `ABC` con `@abstractmethod`.

### Removed
- Tests por pasos en la raiz del paquete (`test_*.py`) reemplazados por la estructura de pruebas en `tests/`.


## [0.2.1] - 2026-04-08 (Fase 02: correcciones)

Versión disponible en `proyecto/02-documentando/`

### Fixed
- Corregida URL del repositorio en `docs/EJECUCION.md` —
  `github-python` sustituido por `github.com`.
- Corregido directorio de ejecución en `README.md`, `docs/EJECUCION.md`
  y `docs/TESTS_Y_PASOS.md` — hay que ejecutar desde la carpeta que
  contiene `gesticat/`, no desde dentro de ella.

### Refactor
- Imports relativos (`from domain.gato import Gato`) convertidos a imports
  absolutos (`from gesticat.domain.gato import Gato`) en todos los módulos
  del proyecto. Permite ejecutar desde la carpeta padre y es compatible con
  herramientas externas como `pytest` y `coverage`.

---

## [0.2.0] - 2026-04-01 (Fase 02: documentación)

Versión disponible en `proyecto/02-documentando/`

### Added
- Documentación completa en `docs/`: descripción y alcance, ejecución,
  arquitectura por capas, casos de uso, reglas de negocio, modelo de dominio,
  contrato de repositorio, datos iniciales, tests y pasos, y troubleshooting.
- `CHANGELOG.md` para registrar la evolución del proyecto por fases.
- `docs/README.md` como índice de la documentación de la fase.

### Changed
- Mejorados docstrings en todos los módulos, clases y métodos siguiendo
  las buenas prácticas de documentación en Python (PEP 257).
- Comentarios del código reorientados al "por qué" de las decisiones
  de diseño en lugar de describir lo obvio.
- `fecha_registro` en `Gato` pasa a ser opcional — si no se indica,
  usa la fecha de hoy. Facilita migraciones desde registros en papel.
- `README.md` ampliado con quickstart, requisitos, árbol de carpetas
  y enlace a la documentación.
- Corregido comando de ejecución — debe lanzarse desde dentro de `gesticat/`.

### Refactor
- `guardar()` eliminado del contrato `RepositorioGatos` y de
  `RepositorioGatosMemoria`. Sustituido por `insertar()` y `actualizar()`
  para separar explícitamente la creación de la actualización.
- `Colonia` añade `actualizar_gato()` para persistir cambios correctamente
  en cualquier tipo de repositorio.
- `ServicioColonia` llama a `actualizar_gato()` tras modificar estado
  o esterilización de un gato.

### Compatibility / Breaking changes
- **Breaking**: `RepositorioGatos` ya no tiene `guardar()`. Cualquier
  implementación concreta debe implementar `insertar()` y `actualizar()`
  en su lugar.
- Los tests `test_repo_memoria.py` y `test_contrato.py` actualizados
  para reflejar el nuevo contrato.

---

## [0.1.0] - 2026-03-03 (Fase 01: diseño por capas)

Versión disponible en `proyecto/01-diseno-capas/`

### Added
- Aplicación base de GestiCat por capas:
  - Menú de consola en `presentation/`.
  - Servicio de casos de uso en `application/`.
  - Entidades y reglas de negocio en `domain/` (`Gato`, `Colonia`,
    `Responsable` con herencia `PersonaFisica` y `Protectora`).
  - Repositorio en memoria y datos iniciales en `infrastructure/`.
- Contrato `RepositorioGatos` con `guardar()`, `obtener()`,
  `listar()` y `quitar()`.
- Tests manuales por componente (`test_*.py`).
- `README.md` con propósito, estructura y comandos de ejecución.
