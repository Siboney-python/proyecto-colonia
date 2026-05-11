# Descripción y alcance

## Descripción funcional

GestiCat es una aplicación de consola para gestionar el censo y seguimiento
de una colonia felina urbana. Permite registrar gatos con sus datos básicos
(identificador, nombre, color, sexo, estado y esterilización), gestionar el
responsable de la colonia, controlar el estado administrativo mediante anexos
municipales y obtener reportes de población.

El sistema está pensado para ser usado por la persona responsable de la colonia,
que puede registrar altas y bajas de gatos, marcar esterilizaciones, tramitar
cambios de estado ante el ayuntamiento y consultar el censo actualizado en
cualquier momento.

## Objetivos de la fase 04

- Añadir persistencia real con SQLite mediante `RepositorioGatosSQLite`.
- Crear el script de inicialización de la base de datos (`crear_bd.py`).
- Definir excepciones de dominio para la capa de persistencia (`errores.py`).
- Mantener el repositorio en memoria como alternativa para desarrollo y tests.
- Documentar el diseño de la base de datos en `docs/DISEÑO_BD.md`.

## Alcance

### Incluye
- Entidades y reglas del dominio (`domain/gato.py`, `domain/colonia.py`,
  `domain/responsable.py`).
- Contrato del repositorio (`domain/repositorio_gatos.py`).
- Implementación en memoria del repositorio y datos de ejemplo
  (`infrastructure/repositorio_gatos_memoria.py`, `infrastructure/datos_iniciales.py`).
- Servicio de aplicación (`application/servicio_colonia.py`).
- Menú de consola (`presentation/menu.py`).
- Pruebas manuales por componente (`test_*.py`).

### No incluye
- Interfaz gráfica o web.
- Gestión de múltiples colonias o múltiples responsables simultáneos.
- Módulo de adopciones ni seguimiento veterinario detallado.
- Autenticación ni control de acceso.

## Supuestos y límites

- Un único responsable por colonia (persona física o protectora).
- El identificador de cada gato es exactamente 3 dígitos numéricos (ej. `001`).
- Los estados del gato y de la colonia son cerrados y se definen mediante enums.
- La esterilización es irreversible una vez aplicada.
- Las fechas se manejan en formato `dd/mm/aaaa` o como objetos `date` de Python.
- Los datos persisten entre ejecuciones mediante SQLite (`gesticat.db`).
