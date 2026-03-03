# Revisión del proyecto — Siboney

**Fuente de verdad:** `proyecto/01-diseno-capas/gesticat/`
**Fases detectadas:** 01 (capas)

## REVISIÓN FASE 01 - 2026-03-03 — Nota: 4/10

### Cumple

- Repositorio creado y compartido con el profesor.
- Subcarpeta `proyecto/` en el repositorio con la carpeta de fase `01-diseno-capas/`.
- El proyecto está organizado en las cuatro capas: `domain/`, `application/`, `infrastructure/`, `presentation/`.
- Estructura de ficheros correcta: paquetes con `__init__.py`, módulos bien separados.
- POO aplicado con solidez: clases `Gato`, `Colonia`, `Responsable` (con herencia `PersonaFisica` y `Protectora`), encapsulamiento mediante `@property` y setters con validaciones robustas, uso correcto de `Enum` para estados y sexos.
- Contrato de repositorio definido en `domain/repositorio_gatos.py` e implementado en `infrastructure/repositorio_gatos_memoria.py`.
- Servicio de aplicación `ServicioColonia` que coordina casos de uso sin mezclar lógica de negocio.
- Reglas de negocio comentadas en los módulos del dominio.
- Nombres de ficheros, clases y variables significativos y conformes a PEP8.

### Errores y aspectos a mejorar

- **[IMPORTANTE] No hay menú ni punto de entrada — el programa no se puede ejecutar.** La carpeta `presentation/` existe pero está vacía. No hay `main.py` ni módulo de menú. El programa no funciona como aplicación.
  - *Cómo resolverlo:* Crea, al menos,  `presentation/menu.py` con un bucle de menú que llame a `ServicioColonia` (registrar gato, ver censo, tramitar anexo, etc.).

- **[IMPORTANTE] `README.md` sin instrucciones de instalación ni ejecución.** El fichero tiene solo 2 líneas genéricas. Quien clone el repositorio no sabe cómo ejecutar el proyecto.
  - *Cómo resolverlo:* Amplía el `README.md` con descripción del proyecto, versión de Python requerida y los comandos para clonar e iniciar la aplicación.

- **[IMPORTANTE] No hay datos iniciales.** No existe ningún fichero que cargue datos de ejemplo al arrancar. Sin menú ni datos iniciales, no hay forma de probar el sistema manualmente.
  - *Cómo resolverlo:* Añade un módulo en `infrastructure/` (por ejemplo `datos_iniciales.py`) que cree una colonia con algunos gatos de ejemplo y un responsable, y úsalo al arrancar la aplicación desde `main.py`.

- **[DISEÑO] `domain/repositorio_gatos.py` declara un TODO para añadir `quitar(id_gato)` al contrato, pero `infrastructure/repositorio_gatos_memoria.py` ya lo implementa.** 

- **[SUGERENCIA] `domain/gato.py:68` — el parámetro del setter `id_gato` se llama `id`.** `id` es una palabra reservada de Python; no deberías usarlo como nombre de parámetro.
  - *Cómo resolverlo:* Renómbralo a `valor` o `id_gato` para ser consistente con el resto de setters.

- **[SUGERENCIA] `domain/responsable.py` — `PersonaFisica` tiene un TODO pendiente para validar mayoría de edad.** No es un error ahora mismo, pero es una regla de negocio declarada y no aplicada.
  - *Cómo resolverlo:* Implementa la validación en el setter correspondiente o anótalo como limitación conocida en un comentario más explícito.


