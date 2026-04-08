# Tests y pasos

Describe cómo ejecutar las pruebas manuales del proyecto y qué valida
cada una. Estas pruebas permiten comprobar que cada componente funciona
correctamente de forma independiente.

## Cómo ejecutar los tests

Desde la carpeta que contiene el paquete `gesticat/`:

```bash
python3 -m gesticat.test_gato
python3 -m gesticat.test_responsable
python3 -m gesticat.test_colonia
python3 -m gesticat.test_repo_memoria
python3 -m gesticat.test_contrato
python3 -m gesticat.test_servicio
```

## Qué valida cada test

### `test_gato.py`
Valida la entidad `Gato`:
- Creación de un gato válido con todos sus datos.
- Rechazo de ID inválido (menos de 3 dígitos, letras).
- Rechazo de nombre y color vacíos.
- Rechazo de sexo y estado con valores fuera del enum.
- Reglas de esterilización: sin clínica y reversión prohibida.
- Validaciones de fecha: futura, formato incorrecto y uso de fecha de hoy
  cuando no se indica ninguna.

### `test_responsable.py`
Valida las entidades `PersonaFisica` y `Protectora`:
- Creación válida de ambos tipos de responsable.
- Rechazo de nombre vacío, teléfono inválido y email sin formato válido.
- Rechazo de identificación vacía y normalización a mayúsculas.
- Rechazo de fecha de nacimiento futura y de menores de edad.
- Rechazo de número de registro vacío en `Protectora`.
- Representación legible (`__str__`) de ambas subclases.

### `test_colonia.py`
Valida la entidad `Colonia`:
- Creación válida con nombre y responsable correctos.
- Estado inicial siempre `SOLICITADA`.
- Rechazo de nombre vacío y responsable con tipo incorrecto.
- Agregar gato, detectar duplicados y rechazar objetos que no sean `Gato`.
- Actualizar gato existente y verificar que el cambio persiste.
- Quitar gato y comprobar que ya no existe.
- Búsqueda por ID (existente e inexistente) y por nombre.
- Tramitación de anexo y bloqueo de vuelta a `SOLICITADA`.
- Control de actualización en colonia recién creada.
- Generación de reporte de censo y reporte de colonia.

### `test_repo_memoria.py`
Valida `RepositorioGatosMemoria`:
- Insertar un gato y recuperarlo por ID.
- Rechazo de inserción duplicada.
- `obtener()` devuelve `None` para ID inexistente.
- Listar todos los gatos del repositorio.
- Actualizar un gato existente y verificar el cambio.
- Rechazo de actualización de gato inexistente.
- Quitar un gato y comprobar que ya no existe.
- Rechazo de quitar un gato inexistente.

### `test_contrato.py`
Valida el contrato `RepositorioGatos`:
- Todos los métodos del contrato (`insertar`, `actualizar`, `obtener`,
  `listar`, `quitar`) lanzan `NotImplementedError` en la clase base,
  garantizando que cualquier implementación concreta debe implementarlos.

### `test_servicio.py`
Valida `ServicioColonia` a través de sus casos de uso:
- Registrar gato con fecha explícita y sin fecha (usa hoy).
- Rechazo de registro de gato duplicado.
- Actualizar estado de gato existente e inexistente.
- Marcar gato como esterilizado y bloqueo de reversión.
- Listar gatos sin esterilizar.
- Asignar nuevo responsable a la colonia.
- Tramitar cambio de estado administrativo.
- Generación de reporte de censo y reporte de colonia.

## Qué test ejecutar según qué modifiques

| Si modificas...                               | Ejecuta...                                   |
|-----------------------------------------------|----------------------------------------------|
| `domain/gato.py`                              | `test_gato`, `test_colonia`, `test_servicio` |
| `domain/responsable.py`                       | `test_responsable`, `test_servicio`          |
| `domain/colonia.py`                           | `test_colonia`, `test_servicio`              |
| `domain/repositorio_gatos.py`                 | `test_contrato`, `test_repo_memoria`         |
| `infrastructure/repositorio_gatos_memoria.py` | `test_repo_memoria`, `test_servicio`         |
| `application/servicio_colonia.py`             | `test_servicio`                              |
| `infrastructure/datos_iniciales.py`           | Ejecutar el menú y comprobar manualmente     |
