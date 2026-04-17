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
- **Error**: `ValueError` si ya existe un gato con el mismo ID.

### `actualizar(gato)`
- **Recibe**: una instancia de `Gato` ya existente.
- **Efecto**: sobreescribe el gato con ese ID en el repositorio.
- **Error**: `ValueError` si no existe un gato con ese ID.
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
- **Error**: `ValueError` si no existe un gato con ese ID.

---

## Implementación actual: RepositorioGatosMemoria

Definida en `infrastructure/repositorio_gatos_memoria.py`. Implementa
el contrato usando un diccionario interno con el ID del gato como clave.

- Los datos solo existen mientras la aplicación está en ejecución.
- No hay persistencia real — al cerrar el programa los datos se pierden.
- Útil para desarrollo, pruebas y demos.

---

## Cómo sustituir por otra implementación

Para añadir persistencia real (base de datos, archivo JSON, API remota...):

1. Crear una nueva clase que herede de `RepositorioGatos`:
   ```python
   from domain.repositorio_gatos import RepositorioGatos

   class RepositorioGatosSQLite(RepositorioGatos):
       def insertar(self, gato): ...
       def actualizar(self, gato): ...
       def obtener(self, id_gato): ...
       def listar(self): ...
       def quitar(self, id_gato): ...
   ```

2. Implementar los cinco métodos del contrato respetando las mismas
   garantías: qué devuelve cada uno y qué errores lanza.

3. Sustituir en `infrastructure/datos_iniciales.py` la línea:
   ```python
   repositorio = RepositorioGatosMemoria()
   ```
   por:
   ```python
   repositorio = RepositorioGatosSQLite()
   ```

El resto del sistema — `Colonia`, `ServicioColonia` y `menu.py` —
no necesita ningún cambio.
