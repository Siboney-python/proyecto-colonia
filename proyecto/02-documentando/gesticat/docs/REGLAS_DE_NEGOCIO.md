# Reglas de negocio

Recoge todas las reglas implementadas en el dominio que definen cómo se
comporta el sistema. Están organizadas por entidad y reflejan las condiciones
reales de gestión de una colonia felina urbana.

## Reglas de Gato

### Identificador
- Debe tener exactamente 3 dígitos numéricos (ej. `001`).
- Se normaliza eliminando espacios laterales y convirtiendo a mayúsculas.
- Es único dentro de la colonia — no puede haber dos gatos con el mismo ID.

### Nombre y color
- No pueden estar vacíos.
- No pueden tener espacios laterales.

### Sexo y estado
- Deben ser valores válidos de sus respectivos enums (`Sexo` y `EstadoGato`).
- No se aceptan cadenas de texto ni ningún otro tipo.

### Esterilización
- Solo acepta valores booleanos (`True` o `False`).
- Es irreversible: un gato marcado como esterilizado no puede volver a
  no esterilizado.
- Un gato no puede marcarse como esterilizado sin tener una clínica
  veterinaria asignada.

### Clínica veterinaria
- Puede ser `None` si el gato no está esterilizado.
- Si se indica, no puede estar vacía ni tener espacios laterales.

### Fecha de registro
- No puede ser una fecha futura.
- Acepta formato `dd/mm/aaaa` o un objeto `date` de Python.
- Si no se indica, se usa la fecha de hoy — permite el uso diario sin
  introducir fecha y facilita migraciones desde registros en papel con
  fechas históricas.

---

## Reglas de Responsable

### Datos de contacto (comunes a PersonaFisica y Protectora)
- El nombre no puede estar vacío.
- El teléfono debe tener exactamente 9 dígitos numéricos.
- El email debe tener formato válido (texto@texto.dominio).
- La identificación (DNI/NIF/CIF) no puede estar vacía y se normaliza
  a mayúsculas.

### PersonaFisica
- Debe ser mayor de edad: 18 años cumplidos en la fecha actual.
- La fecha de nacimiento no puede ser futura.
- Acepta formato `dd/mm/aaaa` o un objeto `date` de Python.

### Protectora
- El número de registro no puede estar vacío y se normaliza a mayúsculas.

---

## Reglas de Colonia

### Nombre
- No puede estar vacío ni tener espacios laterales.

### Responsable
- Debe ser una instancia de `PersonaFisica` o `Protectora`.
- La colonia siempre tiene un responsable asignado.

### Estado administrativo
- El estado inicial siempre es `SOLICITADA` — se asigna automáticamente
  al crear la colonia.
- No se puede volver al estado `SOLICITADA` una vez tramitado un anexo.
- Cada cambio de estado registra la fecha de la última actualización.
- Si han pasado más de 3 meses desde la última actualización, la colonia
  se considera pendiente de revisión.

### Gestión de gatos
- No puede haber dos gatos con el mismo ID en la colonia.
- El censo solo cuenta gatos con estado activo: `COL` (en colonia)
  o `ACOG` (en acogida).
- Los gatos con estado `ADOP`, `FALL` o `DESA` no se contabilizan
  en el censo ni aparecen en el listado de sin esterilizar.

---

## Reglas del repositorio

- `insertar()` falla si ya existe un gato con el mismo ID.
- `actualizar()` falla si no existe un gato con ese ID.
- `quitar()` falla si no existe un gato con ese ID.
- `obtener()` devuelve `None` si el ID no existe — no lanza error.
