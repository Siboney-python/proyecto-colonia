# Guía de rutas Flask — GestiCat (gestión de colonias felinas)

## El dominio en una línea

**GestiCat** es una aplicación de gestión de colonias felinas urbanas con tres entidades
principales: `Gato` (animal individual con estado y esterilización), `Colonia` (agrupación
de gatos con estado administrativo — `SOLICITADA`, `ACTIVA`, `PENDIENTE`, `BAJA`) y
`Responsable` (persona física `PersonaFisica` o asociación `Protectora`). Solo existe una
colonia por aplicación, por lo que las rutas de colonia no llevan identificador.

---

## Inventario completo del menú

La interfaz de consola (`presentation/menu.py`) expone **9 operaciones + salida**:

| Opción | Función en menu.py | Método de servicio |
|---|---|---|
| 1 | `registrar_gato()` | `servicio.registrar_gato(...)` |
| 2 | `quitar_gato()` | `servicio.quitar_gato(id_gato)` |
| 3 | `actualizar_estado_gato()` | `servicio.actualizar_estado_gato(id_gato, nuevo_estado)` |
| 4 | `actualizar_esterilizacion_gato()` | `servicio.actualizar_esterilizacion_gato(id_gato, True, clinica)` |
| 5 | `listar_sin_esterilizar()` | `servicio.listar_sin_esterilizar()` |
| 6 | `asignar_responsable()` | `servicio.asignar_responsable(responsable)` |
| 7 | `tramitar_anexo()` | `servicio.tramitar_anexo(nuevo_estado)` |
| 8 | `mostrar_reporte_censo()` | `servicio.reporte_censo()` |
| 9 | `mostrar_reporte_colonia()` | `servicio.reporte_colonia()` |
| 0 | — | Salir |

---

## Rutas sugeridas (toda la API)

Los parámetros de creación y modificación se pasan como segmentos de URL.

### Gatos

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/gatos` | `listar_gatos()` | Lista todos los gatos (**añadir al servicio**) |
| `/gatos/sin-esterilizar` | `servicio.listar_sin_esterilizar()` | Lista gatos activos no esterilizados |
| `/gatos/nuevo/<id_gato>/<nombre>/<color>/<sexo>/<estado>/<clinica>/<esterilizado>` | `servicio.registrar_gato(...)` | Registra un gato nuevo; `esterilizado` llega como cadena `"True"` o `"False"` desde la URL — conviértelo con `esterilizado_bool = (esterilizado == "True")` antes de pasarlo al servicio |
| `/gatos/<id_gato>` | `obtener_gato(id_gato)` | Detalle de un gato; 404 si no existe (**añadir al servicio**) |
| `/gatos/<id_gato>/eliminar` | `servicio.quitar_gato(id_gato)` | Borra el registro de un gato |
| `/gatos/<id_gato>/estado/<nuevo_estado>` | `servicio.actualizar_estado_gato(id_gato, nuevo_estado)` | Actualiza el estado del gato |
| `/gatos/<id_gato>/esterilizar/<clinica>` | `servicio.actualizar_esterilizacion_gato(id_gato, True, clinica)` | Marca el gato como esterilizado |

> **Orden de definición en Flask:** registrar `/gatos/sin-esterilizar` y `/gatos/nuevo/...` **antes** de `/gatos/<id_gato>`
> para que Flask no interprete los segmentos fijos como valores de `id_gato`.

### Colonia

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/colonia` | `servicio.reporte_colonia()` | Reporte general de la colonia |
| `/colonia/censo` | `servicio.reporte_censo()` | Reporte de censo (estadísticas) |
| `/colonia/responsable/<tipo>/<nombre>/<telefono>/<email>/<identificacion>/<campo_extra>` | `servicio.asignar_responsable(responsable)` | Asigna nuevo responsable (`tipo`: `persona` o `protectora`) |
| `/colonia/estado/<nuevo_estado>` | `servicio.tramitar_anexo(nuevo_estado)` | Tramita anexo (cambio de estado) |

### Ejemplo: cómo quedaría `app.py` con dos rutas ya hechas

El siguiente fragmento muestra la estructura mínima de `app.py` con dos rutas implementadas
para que puedas tomar el patrón y aplicarlo al resto:

```python
from flask import Flask
from gesticat.infrastructure.datos_iniciales import crear_colonia_con_datos
from gesticat.application.servicio_colonia import ServicioColonia

app = Flask(__name__)

colonia = crear_colonia_con_datos()
servicio = ServicioColonia(colonia)


@app.route("/")
def bienvenida():
    return (
        "Bienvenido a GestiCat\n"
        "  /gatos            → lista todos los gatos de la colonia\n"
        "  /gatos/<id_gato>  → detalle de un gato por ID\n"
        "  /colonia          → reporte general de la colonia\n"
    )


@app.route("/gatos")
def listar_gatos():
    gatos = servicio.listar_gatos()
    if not gatos:
        return "No hay gatos registrados."
    return "\n".join(str(g) for g in gatos)


if __name__ == "__main__":
    app.run(debug=True)
```

**Lo que hace cada parte:**

- El objeto `colonia` y el `servicio` se crean **una sola vez** fuera de las vistas, al arrancar la
  aplicación. Así todas las rutas comparten el mismo estado en memoria.
- Cada función de vista llama al método del servicio correspondiente y devuelve texto plano.
- Para rutas con excepciones puedes devolver una tupla `(mensaje, código)`:
  `return "No encontrado", 404` o `return "Ya existe", 409`.

---

## Métodos a añadir al servicio

Para que la API sea navegable (listar y obtener gatos individuales) hacen falta
dos métodos que el menú de consola no necesitaba porque operaba sobre flujo lineal.

### `obtener_gato(id_gato)` — ruta `/gatos/<id_gato>`

```python
def obtener_gato(self, id_gato):
    return self._colonia.buscar_por_id(id_gato)
```

### `listar_gatos()` — ruta `/gatos`

```python
def listar_gatos(self):
    return self._colonia._repo.listar()
```

> **Opción recomendada:** añadir `listar_gatos()` a `Colonia` que delegue en `self._repo.listar()`, y llamar `self._colonia.listar_gatos()` desde el servicio. Así no se accede a `_repo` (atributo protegido) desde fuera de la clase.

---

## Puntos de atención

### Instancia única del servicio

El objeto `colonia` y el `servicio` se crean **una sola vez al nivel de módulo** (fuera de
cualquier función de vista), igual que en el lab A2. Todas las rutas del fichero comparten
la misma instancia y, por tanto, el mismo estado en memoria.

### Orden de las rutas en Flask

Flask compara las URLs en el orden en que están registradas. Hay que definir las rutas con
segmentos fijos **antes** de las rutas con parámetros variables:

```
/gatos/sin-esterilizar   ← primero (segmento fijo "sin-esterilizar")
/gatos/nuevo/<id>/...    ← primero (segmento fijo "nuevo")
/gatos/<id_gato>         ← después (captura cualquier valor)
```

Si se registra `/gatos/<id_gato>` antes, Flask interpretará `sin-esterilizar` y `nuevo`
como valores de `id_gato` y nunca llegará a las rutas correctas.

### Mostrar gatos y enumerados como texto

`Gato`, `Colonia` y `Responsable` no se convierten automáticamente a texto. Usa `str(g)`
si el dominio tiene `__str__`, o construye la cadena accediendo a sus atributos:

```python
linea = f"[{g.id_gato}] {g.nombre} — Estado: {g.estado.name} — Esterilizado: {g.esterilizado}"
```

Los valores de `EstadoGato`, `Sexo` y `EstadoColonia` son objetos Python (enumerados).
Usa `.name` para obtener la clave (`"COL"`) o `.value` para la descripción (`"En colonia"`).

### Errores del dominio y códigos HTTP

El dominio puede lanzar excepciones propias (`GatoNoEncontradoError`, `GatoYaExisteError`,
etc.) y también `ValueError` para validaciones. Captúralas en cada route y devuelve una
tupla con el mensaje y el código HTTP apropiado:

```python
try:
    servicio.quitar_gato(id_gato)
except GatoNoEncontradoError as e:
    return str(e), 404
except ValueError as e:
    return str(e), 400
return "Gato eliminado."
```

### Valores válidos para los segmentos de URL

Al probar las rutas en el navegador, los segmentos deben coincidir exactamente con los
valores del enumerado:

- **Estado del gato**: `COL`, `ACOG`, `ADOP`, `FALL`, `DESA`
- **Sexo**: `H`, `M`, `?`
- **Estado de la colonia**: `ACTIVA`, `PENDIENTE`, `BAJA` (no se puede volver a `SOLICITADA`)
- **Tipo de responsable**: `persona` (PersonaFisica) o `protectora` (Protectora)

---

## Códigos de estado HTTP sugeridos

| Situación | Código |
|-----------|--------|
| Lectura correcta | `200 OK` |
| Creación correcta | `201 Created` |
| Recurso no encontrado | `404 Not Found` |
| Conflicto (ya existe) | `409 Conflict` |
| Validación fallida / transición no permitida | `400 Bad Request` |
