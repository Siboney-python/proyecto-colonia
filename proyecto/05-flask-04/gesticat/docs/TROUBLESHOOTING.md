# Troubleshooting

Recoge los errores más comunes al ejecutar GestiCat, su causa y cómo
resolverlos. Separados en tres bloques: errores técnicos al arrancar el
proyecto, errores de uso durante la ejecución del menú y errores HTTP
de la interfaz web.

## Errores técnicos

### `ModuleNotFoundError: No module named 'gesticat'`
- **Causa**: se está ejecutando desde una carpeta incorrecta. Los imports
  usan rutas absolutas relativas al paquete `gesticat/`.
- **Solución**: ejecutar siempre desde la carpeta que contiene `gesticat/`
  (ej. `05-flask-03/`):
```bash
  cd proyecto/05-flask-03
  python3 -m gesticat.presentation.app
  python3 -m gesticat.presentation.menu
```

### `ModuleNotFoundError: No module named 'flask'`
- **Causa**: Flask no está instalado en el entorno virtual activo.
- **Solución**: activar el entorno virtual e instalar dependencias:
```bash
  source .venv/bin/activate
  pip install -r gesticat/requirements.txt
```

### `SyntaxError` o `IndentationError`
- **Causa**: error de sintaxis en algún archivo `.py` modificado.
- **Solución**: revisar el archivo indicado en el mensaje de error,
  prestando atención a la línea señalada.

### `jinja2.exceptions.TemplateNotFound`
- **Causa**: Flask no encuentra la plantilla indicada en `render_template`.
  Puede ser un error de nombre o que la carpeta `templates/` no está en
  el lugar correcto.
- **Solución**: verificar que la plantilla existe en
  `gesticat/presentation/templates/` y que el nombre coincide exactamente
  con el indicado en `render_template`.

### `werkzeug.routing.exceptions.BuildError: Could not build url for endpoint`
- **Causa**: `url_for` en una plantilla o route referencia una función
  que no existe o tiene un nombre distinto.
- **Solución**: verificar que el nombre en `url_for('nombre')` coincide
  exactamente con el nombre de la función del route en `app.py`.

---

## Errores de uso — menú de consola

### `❌ El ID debe ser exactamente 3 dígitos`
- **Causa**: el ID introducido no tiene exactamente 3 dígitos numéricos.
- **Solución**: introducir un ID con exactamente 3 dígitos (ej. `001`, `042`).

### `❌ No existe ningún gato con id XXX`
- **Causa**: se intenta operar con un ID que no existe en la colonia.
- **Solución**: consultar el reporte de censo (opción 8) para ver los
  IDs disponibles, o registrar el gato primero (opción 1).

### `❌ Ya existe un gato con id XXX`
- **Causa**: se intenta registrar un gato con un ID ya usado.
- **Solución**: usar un ID diferente o consultar el censo para ver
  cuáles están disponibles.

### `❌ Un gato esterilizado debe tener clínica veterinaria asignada`
- **Causa**: se intenta marcar un gato como esterilizado sin indicar
  la clínica donde se realizó la intervención.
- **Solución**: introducir el nombre de la clínica al marcar la
  esterilización (opción 4).

### `❌ Un gato esterilizado no puede pasar a no esterilizado`
- **Causa**: se intenta revertir la esterilización de un gato.
- **Solución**: la esterilización es irreversible por diseño.

### `❌ No se puede volver al estado SOLICITADA`
- **Causa**: se intenta tramitar un anexo con el estado `SOLICITADA`.
- **Solución**: elegir entre los estados disponibles: `ACTIVA`,
  `PENDIENTE` o `BAJA`.

### `❌ El responsable debe ser mayor de edad`
- **Causa**: la fecha de nacimiento corresponde a una persona menor de 18 años.
- **Solución**: verificar que la fecha de nacimiento es correcta.

### `❌ El email no tiene un formato válido`
- **Causa**: el email introducido no tiene el formato `texto@texto.dominio`.
- **Solución**: introducir un email con formato válido (ej. `nombre@gmail.com`).

### `❌ El teléfono debe tener exactamente 9 dígitos`
- **Causa**: el teléfono introducido no tiene exactamente 9 dígitos numéricos.
- **Solución**: introducir el teléfono sin espacios ni guiones (ej. `612345678`).

### `❌ La fecha debe tener formato dd/mm/aaaa`
- **Causa**: la fecha introducida no sigue el formato esperado.
- **Solución**: introducir la fecha con el formato correcto (ej. `15/06/1985`).

### `❌ La fecha de registro no puede ser futura`
- **Causa**: la fecha de registro introducida es posterior a hoy.
- **Solución**: introducir una fecha anterior o igual a hoy, o dejar
  vacío para usar la fecha de hoy automáticamente.

---

## Errores HTTP — interfaz web

### `404 Not Found`
- **Causa**: la URL solicitada no existe en GestiCat.
- **Solución**: revisar la URL o volver al inicio desde el enlace de
  la página de error.

### `409 Conflict`
- **Causa**: se intenta registrar un gato con un ID que ya existe.
- **Solución**: usar un ID diferente o consultar `/gatos` para ver
  los IDs disponibles.

### `400 Bad Request`
- **Causa**: algún parámetro de la URL no es válido — estado, sexo
  o tipo de responsable fuera de los valores permitidos.
- **Solución**: revisar los valores válidos en `/ayuda` y corregir
  la URL.

### `500 Internal Server Error`
- **Causa**: error inesperado en el servidor.
- **Solución**: revisar el fichero `gesticat.log` para ver el detalle
  del error.
