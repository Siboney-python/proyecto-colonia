# Descripción y alcance

## Descripción funcional

GestiCat es una aplicación de consola para gestionar el censo y seguimiento
de una colonia felina urbana. Permite registrar gatos con sus datos básicos
(identificador, nombre, color, sexo, estado y esterilización), gestionar el
responsable de la colonia, controlar el estado administrativo mediante anexos
municipales y obtener reportes de población.

El sistema dispone de dos interfaces de usuario independientes que comparten
el mismo dominio y la misma base de datos SQLite:
- **Menú de consola** (`presentation/menu.py`) — interfaz interactiva por terminal.
- **API web con Flask** (`presentation/app.py`) — interfaz HTTP accesible desde
  el navegador.

## Objetivos de la fase actual

- Añadir Flask como segunda capa de presentación sin modificar el dominio.
- Exponer todas las operaciones del menú de consola como routes HTTP.
- Añadir observabilidad global: manejadores de error 404 y 500, ruta `/ayuda`
  con introspección de routes, y logging de peticiones en `gesticat.log`.

## Alcance

### Incluye
- Entidades y reglas del dominio (`domain/gato.py`, `domain/colonia.py`,
  `domain/responsable.py`).
- Contrato del repositorio (`domain/repositorio_gatos.py`).
- Implementación SQLite del repositorio (`infrastructure/repositorio_gatos_sqlite.py`).
- Implementación en memoria del repositorio y datos de ejemplo
  (`infrastructure/repositorio_gatos_memoria.py`, `infrastructure/datos_iniciales.py`).
- Excepciones de dominio para persistencia (`infrastructure/errores.py`).
- Servicio de aplicación (`application/servicio_colonia.py`).
- Menú de consola (`presentation/menu.py`).
- Interfaz web con Flask (`presentation/app.py`).
- Pruebas unitarias con `unittest` (`tests/`).

### No incluye
- Gestión de múltiples colonias o múltiples responsables simultáneos.
- Módulo de adopciones ni seguimiento veterinario detallado.
- Autenticación ni control de acceso.

## Supuestos y límites

- Un único responsable por colonia (persona física o protectora).
- El identificador de cada gato es exactamente 3 dígitos numéricos (ej. `001`).
- Los estados del gato y de la colonia son cerrados y se definen mediante enums.
- La esterilización es irreversible una vez aplicada.
- Las fechas se manejan en formato `dd/mm/aaaa` o como objetos `date` de Python.
- Los datos persisten entre ejecuciones mediante SQLite (`gesticat.db`).
