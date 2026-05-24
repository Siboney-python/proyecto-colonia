# Datos iniciales

Al arrancar la aplicación se conecta a la base de datos `gesticat.db`,
que contiene una colonia, un responsable y cinco gatos de ejemplo creados
por `infrastructure/crear_bd.py`. Esto permite probar el sistema sin
necesidad de introducir datos manualmente.

## Colonia

| Campo                | Valor                  |
|----------------------|------------------------|
| Nombre               | Colonia Sur            |
| Estado               | SOLICITADA             |
| Última actualización | Fecha de creación      |

## Responsable

| Campo              | Valor                          |
|--------------------|--------------------------------|
| Tipo               | PersonaFisica                  |
| Nombre             | Siboney Apellido               |
| Teléfono           | 612345678                      |
| Email              | siboney_apellido@email.com     |
| Identificación     | 12345678A                      |
| Fecha nacimiento   | 10/10/1986                     |

## Gatos precargados

| ID  | Nombre    | Color  | Sexo        | Estado | Clínica       | Esterilizado | Fecha registro |
|-----|-----------|--------|-------------|--------|---------------|--------------|----------------|
| 001 | Miguelito | Gris   | MACHO       | COL    | Clínica Sur   | Sí           | 10/01/2024     |
| 002 | Kiwi      | Blanca | HEMBRA      | ACOG   | Clínica Sur   | Sí           | 15/02/2024     |
| 003 | GordiLuis | Pardo  | MACHO       | FALL   | Clínica Norte | Sí           | 20/03/2024     |
| 004 | Sombra    | Negro  | HEMBRA      | COL    | —             | No           | 05/04/2024     |
| 005 | Nieve     | Blanco | DESCONOCIDO | COL    | —             | No           | 01/06/2024     |

Los gatos 001 y 002 están activos y esterilizados. Los gatos 004 y 005
están activos y pendientes de esterilizar. El gato 003 está fallecido
y no se contabiliza en el censo ni en el listado de sin esterilizar.

## Modificar los datos iniciales

Para cambiar los datos de ejemplo, editar `infrastructure/crear_bd.py`
y volver a ejecutar el script:

```bash
python3 -m gesticat.crear_bd
```

**Atención:** esto elimina la base de datos existente y la recrea desde
cero. Se perderán todos los datos introducidos durante el uso.

- **Cambiar el responsable**: modificar los datos del `INSERT INTO responsables`.
- **Cambiar el nombre de la colonia**: modificar el `INSERT INTO colonias`.
- **Añadir o quitar gatos**: añadir o eliminar entradas de `gatos_iniciales`.
