# Diseño de la Base de Datos - GestiCat LPGC
---

## Mapeo Entidades → Tablas

| Clase de Dominio | Tabla SQL | Propósito |
|---|---|---|
| `Responsable` | `responsables` | Almacena tanto personas físicas como protectoras. Una única tabla con columna discriminadora. |
| `PersonaFisica` | `responsables` | Tabla `responsables` — `tipo = 'PERSONA_FISICA'. |
| `Protectora` | `responsables` | Tabla `responsables` — `tipo` = 'PROTECTORA'. |
| `Colonia` | `colonias` | Almacena las colonias registradas en el sistema. |
| `Gato` | `gatos`| Almacena cada gato con sus datos. |

La jerarquía `Responsable`/`PersonaFisica`/`Protectora` se mapea a una única
tabla con columna discriminadora `tipo`. Los atributos específicos de cada
subclase (`fecha_nacimiento`, `numero_registro`) aceptan NULL cuando no aplican.


## Descripción de tablas

### Tabla `responsables` 

**Propósito:** Almacena tanto personas físicas como protectoras. Una única tabla con columna discriminadora.

| Columna | Tipo | Restricciones | Notas |
|---|---|---|---|
| `identificacion` | TEXT | PRIMARY KEY | Clave primaria (DNI o CIF en MAYÚSCULAS) |
| `nombre` | TEXT | NOT NULL | Nombre |
| `telefono` | TEXT | NOT NULL | 9 dígitos |
| `email` | TEXT | NOT NULL | Email válido |
| `tipo` | TEXT | NOT NULL | Discriminador: 'PERSONA_FISICA' o 'PROTECTORA' |
| `fecha_nacimiento` | TEXT |  | Solo para PersonaFisica (NULL en otras) |
| `numero_registro` | TEXT |  | Solo para Protectora (NULL en otras) |

**Ejemplo de datos:**
```
identificacion | nombre           | telefono  | email                      | tipo           | fecha_nacimiento | numero_registro
---------------|------------------|-----------|----------------------------|----------------|-----------------|----------------
12345678A      | Siboney Apellido  | 612345678 | siboney_apellido@email.com | PERSONA_FISICA | 1986-10-10      | NULL
A12345678      | Asociación Felina | 928765432 | info@asociacion.com        | PROTECTORA     | NULL            | REG-001
```


### Tabla `colonias`

**Propósito:** Almacena las colonias registradas en el sistema.

| Columna | Tipo | Restricciones | Notas |
|---|---|---|---|
| `nombre` | TEXT | PRIMARY KEY | Clave primaria (ej: "Colonia Sur") |
| `responsable_identificacion` | TEXT | FOREIGN KEY → `responsables(identificacion)`, NOT NULL | Identificación del responsable asignado a la colonia. |
| `estado` | TEXT | NOT NULL | SOLICITADA, ACTIVA, PENDIENTE, BAJA |
| `ultima_actualizacion` | TEXT | NOT NULL | Fecha ISO |

**Ejemplo de datos:**
```
nombre       | responsable_identificacion | estado     | ultima_actualizacion
-------------|---------------------------|------------|---------------------
Colonia Sur  | 12345678A                 | SOLICITADA | 2026-05-06
```


### Tabla `gatos`

**Propósito:** Almacena cada gato con sus datos.

| Columna | Tipo | Restricciones | Notas |
|---|---|---|---|
| `id_gato` | TEXT | PRIMARY KEY | Clave primaria (3 dígitos) |
| `colonia_nombre` | TEXT | FOREIGN KEY →  `colonias(nombre)`, NOT NULL | Identificación de la colonia en la que se encuentra el gato. |
| `nombre` | TEXT | NOT NULL | Nombre del gato |
| `color` | TEXT | NOT NULL | Color del pelaje |
| `sexo` | TEXT | NOT NULL | H, M, ? |
| `estado` | TEXT | NOT NULL | COL, ACOG, ADOP, FALL, DESA |
| `clinica_veterinaria` | TEXT | NULL | Nombre de la clínica (NULL si no tiene) |
| `esterilizado` | INTEGER | NOT NULL | 1 o 0 |
| `fecha_registro` | TEXT | NOT NULL | Fecha ISO de registro |

**Ejemplo de datos:**
```
id_gato | colonia_nombre | nombre    | color  | sexo | estado | clinica_veterinaria | esterilizado | fecha_registro
--------|----------------|-----------|--------|------|--------|---------------------|--------------|---------------
001     | Colonia Sur    | Miguelito | Gris   | M    | COL    | Clínica Sur         | 1            | 2024-01-10
002     | Colonia Sur    | Kiwi      | Blanca | H    | ACOG   | Clínica Sur         | 1            | 2024-02-15
003     | Colonia Sur    | GordiLuis | Pardo  | M    | FALL   | Clínica Norte       | 1            | 2024-03-20
004     | Colonia Sur    | Sombra    | Negro  | H    | COL    | NULL                | 0            | 2024-04-05
005     | Colonia Sur    | Nieve     | Blanco | ?    | COL    | NULL                | 0            | 2024-06-01
```


## Relaciones entre tablas

```
┌─────────────────────────────────┐
│         responsables (1)        │
│  ┌─────────────────────────┐    │
│  │ ★ identificacion (PK)   │    │
│  │   nombre                │    │
│  │   telefono              │    │
│  │   email                 │    │
│  │   tipo                  │    │
│  │   fecha_nacimiento      │    │
│  │   numero_registro       │    │
│  └─────────────────────────┘    │
└─────────────────────────────────┘
          │ 1
          │
          ▼ N
┌─────────────────────────────────┐
│           colonias              │
│  ┌─────────────────────────┐    │
│  │ ★ nombre (PK)           │    │
│  │ ◆ responsable_id (FK)   │    │
│  │   estado                │    │
│  │   ultima_actualizacion  │    │
│  └─────────────────────────┘    │
└─────────────────────────────────┘
          │ 1
          │
          ▼ N
┌─────────────────────────────────┐
│             gatos               │
│  ┌─────────────────────────┐    │
│  │ ★ id_gato (PK)          │    │
│  │ ◆ colonia_nombre (FK)   │    │
│  │   nombre                │    │
│  │   color                 │    │
│  │   sexo                  │    │
│  │   estado                │    │
│  │   clinica_veterinaria   │    │
│  │   esterilizado          │    │
│  │   fecha_registro        │    │
│  └─────────────────────────┘    │
└─────────────────────────────────┘
```

**Tipo de relación:** Uno a n (1:N)
- **responsables → colonias** (1:N): un responsable puede tener muchas colonias.
- **colonias → gatos** (1:N): una colonia contiene muchos gatos.


## Orden de creación y ejecución

Las tablas deben crearse en este orden por las dependencias de claves foráneas:

1. `responsables` — no depende de ninguna otra tabla
2. `colonias` — depende de `responsables`
3. `gatos` — depende de `colonias`

Para crear la base de datos con las tablas y datos iniciales, ejecuta desde
la carpeta que contiene el paquete `gesticat/`:

    python3 -m gesticat.crear_bd
