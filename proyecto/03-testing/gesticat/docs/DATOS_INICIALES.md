# Datos iniciales

Al arrancar la aplicación se cargan automáticamente una colonia, un
responsable y cinco gatos de ejemplo definidos en
`infrastructure/datos_iniciales.py`. Esto permite probar el sistema
sin necesidad de introducir datos manualmente.

## Colonia

| Campo                | Valor                  |
|----------------------|------------------------|
| Nombre               | Colonia Sur            |
| Estado               | SOLICITADA             |
| Última actualización | Fecha de hoy           |

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

| ID  | Nombre    | Color  | Sexo       | Estado     | Clínica       | Esterilizado | Fecha registro |
|-----|-----------|--------|------------|------------|---------------|--------------|----------------|
| 001 | Miguelito | Gris   | MACHO      | COL        | Clínica Sur   | Sí           | 10/01/2024     |
| 002 | Kiwi      | Blanca | HEMBRA     | ACOG       | Clínica Sur   | Sí           | 15/02/2024     |
| 003 | GordiLuis | Pardo  | MACHO      | FALL       | Clínica Norte | Sí           | 20/03/2024     |
| 004 | Sombra    | Negro  | HEMBRA     | COL        | —             | No           | 05/04/2024     |
| 005 | Nieve     | Blanco | DESCONOCIDO| COL        | —             | No           | 01/06/2024     |

Los gatos 001 y 002 están activos y esterilizados. Los gatos 004 y 005
están activos y pendientes de esterilizar. El gato 003 está fallecido
y no se contabiliza en el censo ni en el listado de sin esterilizar.

Las fechas de registro son históricas — anteriores al sistema — por eso
se pasan explícitamente en lugar de usar la fecha de hoy.

## Modificar los datos iniciales

Para cambiar los datos de ejemplo, editar
`infrastructure/datos_iniciales.py`:

- **Cambiar el responsable**: modificar los datos de `PersonaFisica`
  o sustituirla por una instancia de `Protectora`.
- **Cambiar el nombre de la colonia**: modificar el primer parámetro
  de `Colonia(...)`.
- **Añadir o quitar gatos**: añadir o eliminar entradas de la lista
  `gatos`, respetando el formato de `Gato(...)`.
- **Cambiar datos de un gato**: modificar los parámetros correspondientes
  en su línea de la lista.
