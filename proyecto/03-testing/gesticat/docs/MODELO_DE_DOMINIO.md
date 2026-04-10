# Modelo de dominio

Describe las entidades principales del sistema, las condiciones que siempre
deben cumplirse (invariantes) y cómo se relacionan entre sí (colaboraciones).

## Entidades

### Gato
Representa un gato individual dentro de la colonia felina.

- `id_gato`: identificador único de 3 dígitos numéricos (ej. `001`).
- `nombre`: nombre del gato, no vacío.
- `color`: color o patrón del pelaje, no vacío.
- `sexo`: valor del enum `Sexo` (HEMBRA, MACHO, DESCONOCIDO).
- `estado`: valor del enum `EstadoGato` (COL, ACOG, ADOP, FALL, DESA).
- `clinica_veterinaria`: clínica donde se esterilizó. Puede ser `None`
  si el gato no está esterilizado.
- `esterilizado`: booleano. Irreversible una vez marcado como `True`.
- `fecha_registro`: fecha de alta en el sistema. Si no se indica,
  se usa la fecha de hoy.

### Responsable (clase base abstracta)
Agrupa los datos de contacto comunes a cualquier responsable de una colonia.
No se instancia directamente — se usa a través de sus subclases.

- `nombre`: nombre del responsable, no vacío.
- `telefono`: exactamente 9 dígitos numéricos.
- `email`: formato válido (texto@texto.dominio).
- `identificacion`: DNI, NIF o CIF, normalizado a mayúsculas.

#### PersonaFisica
Responsable individual (voluntaria). Hereda de `Responsable`.

- `fecha_nacimiento`: debe ser mayor de edad (18 años cumplidos)
  y no puede ser futura.

#### Protectora
Responsable jurídico (asociación). Hereda de `Responsable`.

- `numero_registro`: número de registro oficial, normalizado a mayúsculas.

### Colonia
Entidad central del sistema. Agrupa los gatos bajo un responsable
y gestiona el estado administrativo ante el ayuntamiento.

- `nombre`: nombre de la colonia, no vacío.
- `responsable`: instancia de `PersonaFisica` o `Protectora`.
- `estado`: valor del enum `EstadoColonia` (SOLICITADA, ACTIVA,
  PENDIENTE, BAJA). El estado inicial siempre es SOLICITADA.
- `ultima_actualizacion`: fecha del último cambio de estado o
  tramitación de anexo.

### RepositorioGatos
Contrato que define las operaciones mínimas de almacenamiento.
No es una entidad del dominio en sí, pero vive en él para que
el dominio pueda definir cómo quiere que se gestionen los gatos
sin depender de una implementación concreta.

---

## Invariantes

### Gato
- El ID es exactamente 3 dígitos numéricos y único en la colonia.
- El nombre y el color no pueden estar vacíos ni tener espacios laterales.
- El sexo y el estado deben ser valores válidos de sus enums.
- Un gato esterilizado siempre tiene clínica veterinaria asignada.
- La esterilización es irreversible — no puede pasar de `True` a `False`.
- La fecha de registro no puede ser futura.

### Responsable
- El teléfono tiene exactamente 9 dígitos numéricos.
- El email tiene formato válido.
- La identificación no puede estar vacía.
- Una persona física debe ser mayor de edad (18 años cumplidos).

### Colonia
- Siempre tiene un responsable asignado.
- El estado inicial es siempre SOLICITADA y no puede recuperarse
  una vez tramitado un anexo.
- No puede haber dos gatos con el mismo ID en el repositorio.
- El censo solo cuenta gatos con estado activo (COL o ACOG).

---

## Colaboraciones

- `Colonia` delega el almacenamiento de gatos en `RepositorioGatos`
  a través de su contrato — no sabe ni le importa cómo se implementa.
- `ServicioColonia` orquesta los casos de uso y delega la lógica
  de negocio en `Colonia` y sus entidades.
- `RepositorioGatosMemoria` implementa el contrato `RepositorioGatos`
  en memoria — puede sustituirse por otra implementación sin cambiar
  el dominio ni el servicio.
