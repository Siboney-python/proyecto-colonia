# Mejoras futuras

Recoge las ideas de desarrollo pendientes que han sido eliminadas del código
como comentarios `# TODO` para mantener el código limpio. Cada entrada indica
qué archivo las originó y qué habría que implementar.

---

## Registrar fecha en cambios de estado de Gato

- **Origen**: `domain/gato.py` — enum `EstadoGato`
- **Idea**: cuando el estado de un gato pase a `ADOP`, `FALL` o `DESA`,
  registrar automáticamente la fecha en que se produjo el cambio.
- **Por qué no está implementado**: requiere añadir un atributo `fecha_cambio_estado`
  a `Gato` y modificar el setter de `estado` para asignarlo condicionalmente.
  Se dejó fuera del alcance de las fases iniciales para mantener la entidad simple.

---

## Desglose de esterilizados por sexo en reporte_censo

- **Origen**: `domain/colonia.py` — método `reporte_censo()`
- **Idea**: añadir al reporte de censo el desglose de gatos esterilizados
  separado por sexo (machos esterilizados, hembras esterilizadas).
- **Por qué no está implementado**: el reporte actual ya cubre los casos
  de uso prioritarios. El desglose por sexo es útil pero no urgente.

---

## Mejora de UX en el manejo de errores del menú

- **Origen**: `presentation/menu.py`
- **Idea**: cuando el usuario introduce un dato inválido en una opción del menú,
  actualmente se aborta toda la función y se vuelve al menú principal. Lo ideal
  sería usar bucles `while` con `try/except` por cada campo para permitir
  reintentar solo el campo incorrecto sin perder los datos ya introducidos.
- **Por qué no está implementado**: esta mejora tiene más sentido cuando el
  proyecto migre a una interfaz web (Flask), donde la validación de formularios
  funciona de forma distinta y este patrón queda obsoleto.

---

## Gestión de múltiples colonias y responsables

- **Origen**: `infrastructure/datos_iniciales.py`, `application/servicio_colonia.py`
- **Idea**: el sistema actualmente gestiona una única colonia con un único
  responsable. Para dar soporte a múltiples colonias habría que:
  - Crear `RepositorioColoniasSQLite` e implementar su contrato.
  - Crear `RepositorioResponsablesSQLite` e implementar su contrato.
  - Ampliar `ServicioColonia` o crear un `ServicioGestion` que permita
    listar, crear y seleccionar colonias.
  - Adaptar el menú para que el usuario elija con qué colonia trabajar
    antes de operar.
  - La base de datos ya está preparada para ello: las tablas `colonias`
    y `responsables` con sus claves foráneas soportan múltiples registros
    desde el diseño actual.
- **Por qué no está implementado**: el alcance actual del proyecto es
  una sola colonia. La arquitectura por capas y el esquema SQLite están
  diseñados para facilitar esta ampliación en el futuro.