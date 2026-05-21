# Arquitectura por capas

El proyecto sigue una arquitectura por capas que separa las responsabilidades
del sistema en cuatro niveles bien definidos. El objetivo es mantener el código
cohesionado, con acoplamiento bajo y fácil de extender sin romper el núcleo
del negocio.

## Capas y responsabilidades

### Domain
Núcleo del sistema. Contiene las entidades, las validaciones y las reglas de
negocio. No depende de ninguna otra capa — es la única capa que puede existir
de forma completamente independiente.

- No sabe cómo se almacenan los datos.
- No sabe cómo se muestra la información al usuario.
- No sabe qué casos de uso orquesta el servicio.

### Infrastructure
Contiene las implementaciones concretas de almacenamiento y los datos de
ejemplo. Depende del dominio para conocer las entidades que maneja, pero
el dominio no sabe que existe.

- Implementa el contrato definido en el dominio.
- Se puede sustituir por otra implementación (JSON, SQLite, API...)
  sin tocar el dominio ni el servicio.

### Application
Orquesta los casos de uso del sistema. Coordina las operaciones entre la
presentación y el dominio sin contener lógica de negocio — esa responsabilidad
pertenece exclusivamente al dominio.

- Recibe peticiones de la presentación.
- Delega la lógica en el dominio.
- Usa el repositorio a través del contrato definido en el dominio.

### Presentation
Interfaz de consola. Solo pide datos al usuario y muestra resultados.
No contiene validaciones de negocio ni lógica de dominio.

- Recoge inputs del usuario.
- Llama al servicio de aplicación.
- Muestra los resultados o errores al usuario.

## Dependencias permitidas

```
presentation  →  application  →  domain
infrastructure               →  domain
```

- `presentation` solo habla con `application` — nunca accede al dominio
  directamente ni a la infraestructura.
- `application` solo habla con `domain` — orquesta sin implementar reglas.
- `infrastructure` solo habla con `domain` — implementa sus contratos.
- `domain` no depende de nadie — es el núcleo protegido del sistema.

Esta estructura garantiza que cambiar la interfaz (consola → web), el
almacenamiento (memoria → SQLite) o los casos de uso no afecta al dominio.

## Mapa de archivos

```
gesticat/
  domain/
    gato.py                     → entidad Gato, enums Sexo y EstadoGato
    responsable.py              → entidades Responsable, PersonaFisica y Protectora
    colonia.py                  → entidad Colonia y enum EstadoColonia
    repositorio_gatos.py        → contrato RepositorioGatos
  infrastructure/
    repositorio_gatos_memoria.py → implementación en memoria del contrato
    datos_iniciales.py           → datos de ejemplo para arrancar la aplicación
  application/
    servicio_colonia.py          → casos de uso de ServicioColonia
  presentation/
    menu.py                      → interfaz de consola
  test_*.py                      → pruebas manuales por componente
```