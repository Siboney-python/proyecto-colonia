# Contrato de repositorio

Define el acuerdo entre el dominio y cualquier implementación de
almacenamiento de gatos. Cualquier repositorio concreto debe respetar
este contrato para que el resto del sistema funcione sin cambios.

## Contrato RepositorioGatos (domain)

Definido en `domain/repositorio_gatos.py`. Establece las operaciones
mínimas que cualquier implementación debe proporcionar:

### `insertar(gato)`
- **Recibe**: una instancia de `Gato`.
- **Efecto**: almacena el gato en el repositorio.
- **Error**: `GatoYaExisteError` si ya existe un gato con el mismo ID.

### `actualizar(gato)`
- **Recibe**: una instancia de `Gato` ya existente.
- **Efecto**: sobreescribe el gato con ese ID en el repositorio.
- **Error**: `GatoNoEncontradoError` si no existe un gato con ese ID.
- **Nota**: necesario para que repositorios con persistencia real
  (SQLite, JSON, API...) reflejen los cambios. En memoria no es
  estrictamente necesario porque Python trabaja con referencias,
  pero se llama igualmente para mantener consistencia.

### `obtener(id_gato)`
- **Recibe**: el ID del gato (string de 3 dígitos).
- **Devuelve**: la instancia de `Gato` si existe, `None` si no existe.
- **Error**: no lanza error si el ID no existe — devuelve `None`.

### `listar()`
- **Recibe**: nada.
- **Devuelve**: lista con todas las instancias de `Gato` del repositorio.
  Lista vacía si no hay gatos.

### `quitar(id_gato)`
- **Recibe**: el ID del gato (string de 3 dígitos).
- **Efecto**: elimina el gato con ese ID del repositorio.
- **Error**: `GatoNoEncontradoError` si no existe un gato con ese ID.

---

## Implementaciones disponibles

- `RepositorioGatosMemoria` (`infrastructure/repositorio_gatos_memoria.py`):
  almacena en un diccionario en memoria. Solo para tests rápidos y desarrollo.
- `RepositorioGatosSQLite` (`infrastructure/repositorio_gatos_sqlite.py`):
  persiste en `gesticat.db`. Implementación de producción.
  
## Cómo elegir la implementación

Desde `infrastructure/datos_iniciales.py`:

- `crear_servicio()` — usa `RepositorioGatosMemoria`. Para desarrollo y demos.
- `crear_servicio_sqlite()` — usa `RepositorioGatosSQLite`. Para producción.

En `presentation/menu.py` se elige cuál usar:
```python
servicio = crear_servicio_sqlite()  # producción
# servicio = crear_servicio()       # desarrollo
```

---
## Excepciones de dominio (`infrastructure/errores.py`)

- `ErrorRepositorio`: base de todas las excepciones del repositorio.
- `GatoYaExisteError`: id duplicado al guardar un gato.
- `GatoNoEncontradoError`: id no encontrado al obtener un gato.
- `ErrorPersistencia`: error inesperado del motor de base de datos.
- `ColoniaYaExisteError`: id duplicado al guardar una colonia (aún no disponible).
- `ColoniaNoEncontradoError`: id no encontrado al obtener una colonia.
- `ResponsableYaExisteError`: id duplicado al guardar una responsable (aún no disponible)..
- `ResponsableNoEncontradoError`: id no encontrado al obtener un responsable.


## Tests

- `tests/test_repositorio_sqlite.py`: cubre `insertar`, `obtener`, `actualizar`,
  `listar`, `quitar` y excepciones del repositorio SQLite.

```bash
python3 -m unittest gesticat.tests.test_repositorio_sqlite
```
  
