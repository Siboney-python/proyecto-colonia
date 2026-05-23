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

## Gestión de múltiples colonias, responsables y autenticación

- **Origen**: `infrastructure/datos_iniciales.py`, `application/servicio_colonia.py`,
  `presentation/app.py`, `domain/responsable.py`
- **Idea**: ampliar el sistema para gestionar múltiples colonias con sus
  responsables, y convertir estos en usuarios autenticados de la interfaz web.
  Las operaciones de lectura serían públicas, pero las de escritura requerirían
  estar autenticado. Cada responsable solo podría gestionar su propia colonia.
- **Lo que implicaría**:
  - Crear `RepositorioResponsables` con su contrato e implementación SQLite
    — mismo patrón que `RepositorioGatos`.
  - Crear `RepositorioColonias` con su contrato e implementación SQLite
    para gestionar múltiples colonias.
  - Ampliar `ServicioColonia` o crear un `ServicioGestion` que permita
    listar, crear y seleccionar colonias.
  - Adaptar el menú para que el usuario elija con qué colonia trabajar
    antes de operar.
  - Añadir campos `usuario` y `contraseña` (hasheada) a la entidad
    `Responsable` o crear una entidad `Usuario` separada vinculada al
    responsable.
  - Implementar el flujo de login/logout en `app.py` con sesiones Flask.
  - Proteger los routes de escritura con un decorador que compruebe
    si hay sesión activa.
  - Filtrar los datos por colonia según el responsable autenticado —
    un responsable no podría ver ni modificar la colonia de otro.
  - Adaptar el esquema SQLite para almacenar las credenciales y las
    relaciones entre usuarios, responsables y colonias.
- **Por qué no está implementado**: el alcance actual es una sola colonia.
  La arquitectura por capas y el esquema SQLite están diseñados para
  facilitar esta ampliación. Requiere además el módulo de autenticación
  de Flask (flask-login o sesiones nativas), previsto para fases posteriores.

