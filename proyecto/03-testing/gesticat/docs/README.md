# Documentación de GestiCat LPGC — Fase 02

Índice de la documentación técnica del proyecto. Se recomienda leer
los documentos en el orden indicado para una comprensión progresiva
del sistema.

## Orden de lectura recomendado

1. [DESCRIPCION_Y_ALCANCE.md](DESCRIPCION_Y_ALCANCE.md) — Qué hace el sistema y qué límites tiene.
2. [EJECUCION.md](EJECUCION.md) — Cómo arrancar la aplicación y ejecutar los tests.
3. [ARQUITECTURA_POR_CAPAS.md](ARQUITECTURA_POR_CAPAS.md) — Cómo está organizado el código.
4. [CASOS_DE_USO.md](CASOS_DE_USO.md) — Qué puede hacer el usuario, opción por opción.
5. [MODELO_DE_DOMINIO.md](MODELO_DE_DOMINIO.md) — Entidades, invariantes y colaboraciones.
6. [REGLAS_DE_NEGOCIO.md](REGLAS_DE_NEGOCIO.md) — Condiciones y restricciones del dominio.
7. [CONTRATO_REPOSITORIO.md](CONTRATO_REPOSITORIO.md) — Contrato de almacenamiento y cómo sustituirlo.
8. [DATOS_INICIALES.md](DATOS_INICIALES.md) — Datos de ejemplo cargados al arrancar.
9. [TESTS_Y_PASOS.md](TESTS_Y_PASOS.md) — Cómo ejecutar los tests y qué valida cada uno.
10. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Errores comunes y cómo resolverlos.

## Notas

- Si se amplía el proyecto (persistencia real, interfaz web o móvil,
  múltiples colonias), actualizar primero `DESCRIPCION_Y_ALCANCE.md`
  y `REGLAS_DE_NEGOCIO.md`.
