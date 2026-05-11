# GestiCat LPGC

Sistema de gestión y censo de colonias felinas urbanas de Las Palmas de Gran Canaria.

## Propósito del proyecto

- Digitalizar la gestión de una colonia de gatos callejeros del municipio.
- Facilitar el registro, seguimiento y control del censo de gatos de la colonia.
- Gestionar el estado administrativo de la colonia ante el ayuntamiento.
- Permitir la incorporación de mejoras futuras (base de datos, interfaz móvil,
  múltiples colonias) sin romper el núcleo del sistema.

## Estado de la fase
Esta carpeta corresponde a la fase `04-sqlite/`.

## Requisitos

- Python 3.10+.
- Dependencias en `gesticat/requirements.txt`.
- Compatible con Linux, macOS y Windows.

## Quickstart

Desde la carpeta que contiene el paquete `gesticat/`:

```bash
python3 -m venv .venv

source .venv/bin/activate # Linux y macOS
source .venv/Scripts/activate # Windows GitBash
source .venv/Scripts/Activate.ps1 # Windows PowerShell

pip install -r gesticat/requirements.txt

python3 -m gesticat.crear_bd
python3 -m gesticat.presentation.menu
```

## Base de datos
La aplicación usa SQLite para persistencia. El fichero `gesticat.db` se crea
ejecutando el script de inicialización:

```bash
python3 -m gesticat.crear_bd
```

Esto crea las tablas (`responsables`, `colonias`, `gatos`) e inserta los datos
iniciales. Si la BD ya existe, la elimina y la recrea desde cero.

## Uso (menú de consola)

Ejecuta desde la carpeta `04-sqlite/`:

```bash
python3 -m gesticat.presentation.menu
```

El menú permite: registrar y borrar gatos, actualizar estado y esterilización,
listar gatos sin esterilizar, asignar responsable, tramitar anexos municipales
y consultar reportes de censo y colonia.

## Tests

Desde la carpeta `04-sqlite/`:

```bash
python3 -m unittest
```

Para ejecutar un archivo concreto:

```bash
python3 -m unittest gesticat.tests.test_gato
python3 -m unittest gesticat.tests.test_responsable
python3 -m unittest gesticat.tests.test_colonia
python3 -m unittest gesticat.tests.test_repositorio_sqlite
```

## Cobertura

```bash
coverage run -m unittest
coverage report
coverage html
```

El reporte HTML queda en `htmlcov/index.html`.

## Estructura del proyecto

```
04-sqlite/
  gesticat/
    domain/
      gato.py
      responsable.py
      colonia.py
      repositorio_gatos.py
    infrastructure/
      repositorio_gatos_memoria.py
      repositorio_gatos_sqlite.py
      datos_iniciales.py
      errores.py
    application/
      servicio_colonia.py
    presentation/
      menu.py
    tests/
      test_gato.py
      test_responsable.py
      test_colonia.py
      test_repositorio_sqlite.py
    docs/
	  ARQUITECTURA_POR_CAPAS.md
      CASOS_DE_USO.md
      CONTRATO_REPOSITORIO.md
      DATOS_INICIALES.md
      DESCRIPCION_Y_ALCANCE.md
      DISEÑO_BD.md
      EJECUCION.md
      FUTURE_IMPROVEMENTS.md
      MODELO_DE_DOMINIO.md
      README.md
      REGLAS_DE_NEGOCIO.md
      TESTS_Y_PASOS.md
      TROUBLESHOOTING.md
    requirements.txt
    crear_bd.py
    gesticat.db    
```

- `infrastructure/repositorio_gatos_sqlite.py`: repositorio con persistencia real
  en SQLite. Usado por el flujo principal de la aplicación.
- `infrastructure/repositorio_gatos_memoria.py`: repositorio en memoria para
  desarrollo, demos y tests de dominio.
- `infrastructure/errores.py`: excepciones de dominio para la capa de persistencia.
- `infrastructure/crear_bd.py`: script para crear el esquema e insertar datos iniciales.
- `tests/`: pruebas unitarias con `unittest`, incluyendo tests específicos para
  el repositorio SQLite.

## Documentación

Consulta la documentación detallada del proyecto en
[gesticat/docs/README.md](gesticat/docs/README.md).

## Changelog
Historial de cambios en `CHANGELOG.md`.
