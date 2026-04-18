# GestiCat LPGC

Sistema de gestión y censo de colonias felinas urbanas de Las Palmas de Gran Canaria.

## Propósito del proyecto

- Digitalizar la gestión de una colonia de gatos callejeros del municipio.
- Facilitar el registro, seguimiento y control del censo de gatos de la colonia.
- Gestionar el estado administrativo de la colonia ante el ayuntamiento.
- Permitir la incorporación de mejoras futuras (base de datos, interfaz móvil,
  múltiples colonias) sin romper el núcleo del sistema.

## Estado de la fase
Esta carpeta corresponde a la fase `03-testing`.

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
python3 -m gesticat.presentation.menu
```

## Uso (menú de consola)

Ejecuta desde la carpeta `03-testing/`:

```bash
python3 -m gesticat.presentation.menu
```

El menú permite: registrar y borrar gatos, actualizar estado y esterilización,
listar gatos sin esterilizar, asignar responsable, tramitar anexos municipales
y consultar reportes de censo y colonia.

## Tests

Desde la carpeta `03-testing/`:

```bash
python3 -m unittest
```

Para ejecutar un archivo concreto:

```bash
python3 -m unittest gesticat.tests.test_gato
python3 -m unittest gesticat.tests.test_responsable
python3 -m unittest gesticat.tests.test_colonia
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
03-testing/
  gesticat/
    domain/
      gato.py
      responsable.py
      colonia.py
      repositorio_gatos.py
    infrastructure/
      repositorio_gatos_memoria.py
      datos_iniciales.py
    application/
      servicio_colonia.py
    presentation/
      menu.py
    tests/
      test_gato.py
      test_responsable.py
      test_colonia.py
    docs/
    requirements.txt
```

- `presentation/menu.py`: interfaz de consola que solo pide datos y muestra resultados.
- `application/servicio_colonia.py`: coordina los casos de uso sobre la `Colonia`
  sin exponer la lógica interna.
- `domain/`: alberga las entidades (`Gato`, `Colonia`, `Responsable`), las
  validaciones y el contrato `RepositorioGatos`.
- `infrastructure/`: contiene los datos iniciales y el repositorio en memoria
  (`RepositorioGatosMemoria`).
- `tests/`: pruebas unitarias con `unittest`.

## Documentación

Consulta la documentación detallada del proyecto en `docs/`
(índice en [docs/README.md](docs/README.md)).

## Changelog
Historial de cambios en `CHANGELOG.md`.