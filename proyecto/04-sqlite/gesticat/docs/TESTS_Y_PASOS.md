# Tests y pasos

Describe cómo ejecutar las pruebas del proyecto y qué valida
cada una.

## Cómo ejecutar los tests

Desde la carpeta que contiene el paquete `gesticat/` (en este caso `03-testing/`):

```bash
python3 -m unittest
```

Para ejecutar un archivo concreto:

```bash
python3 -m unittest gesticat.tests.test_gato
python3 -m unittest gesticat.tests.test_responsable
python3 -m unittest gesticat.tests.test_colonia
```

## Qué valida cada test

### `tests/test_gato.py`
Valida la entidad `Gato`:
- Creación válida con todos sus atributos.
- Validaciones de ID (corto, largo, letras, espacios).
- Validaciones de nombre y color (vacío, espacios laterales).
- Validaciones de sexo y estado (tipo incorrecto).
- Validación de clínica veterinaria (solo espacios , espacios laterales)
- Reglas de esterilización (sin clínica, reversión prohibida, tipo incorrecto).
- Validaciones de fecha de registro (futura, formato incorrecto, None usa hoy, tipo incorrecto).

### `tests/test_responsable.py`
Valida las entidades `PersonaFisica` y `Protectora`:
- Creación válida de ambos tipos.
- Validaciones de nombre, teléfono, email e identificación.
- Normalización a mayúsculas en identificación y número de registro.
- Prohibición de espacios laterales en todos los campos de texto.
- Validaciones de fecha de nacimiento (futura, menor de edad, formato incorrecto, tipo incorrecto).
- Validaciones de número de registro de `Protectora`.
- Representación legible (`__str__`) de ambas subclases.

### `tests/test_colonia.py`
Valida la entidad `Colonia` y el repositorio en memoria:
- Creación válida con nombre, responsable y estado inicial.
- Validaciones de nombre (vacío, espacios).
- Validaciones de responsable (tipo incorrecto).
- Gestión de gatos: agregar, actualizar, quitar, buscar por ID y por nombre.
- Estado administrativo: tramitar anexo, bloqueo de vuelta a SOLICITADA.
- Control de actualización: colonia recién creada no necesita actualización.
- Reportes: censo vacío, censo con gatos, reporte de colonia.
- Listado de gatos sin esterilizar, incluyendo exclusión de inactivos.
- Repositorio en memoria: inserción duplicada, actualización y borrado inexistentes.

## Cobertura

Desde la carpeta que contiene el paquete `gesticat/` (en este caso `03-testing/`):

```bash
coverage run -m unittest
```

Ver reporte en consola:

```bash
coverage report
```

Ver reporte detallado en el navegador:

```bash
coverage html
```

El reporte HTML se genera en `htmlcov/index.html`.
