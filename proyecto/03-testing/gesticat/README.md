# GestiCat LPGC

Sistema de gestión y censo de colonias felinas urbanas de Las Palmas de Gran Canaria.

## Quickstart

Desde la carpeta que contiene el paquete gesticat/:

```bash
python3 -m gesticat.presentation.menu
```

## Propósito del proyecto

- Digitalizar la gestión de una colonia de gatos callejeros del municipio.
- Facilitar el registro, seguimiento y control del censo de gatos de la colonia.
- Gestionar el estado administrativo de la colonia ante el ayuntamiento.
- Permitir la incorporación de mejoras futuras (base de datos, interfaz móvil,
  múltiples colonias) sin romper el núcleo del sistema.

## Requisitos

- Python 3.10+.
- No requiere dependencias externas.
- Compatible con Linux, macOS y Windows.

## Estructura del proyecto

```
02-documentando/
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
    docs/
    test_*.py
```

- `presentation/menu.py`: interfaz de consola que solo pide datos y muestra resultados.
- `application/servicio_colonia.py`: coordina los casos de uso sobre la `Colonia`
  sin exponer la lógica interna.
- `domain/`: alberga las entidades (`Gato`, `Colonia`, `Responsable`), las
  validaciones y el contrato `RepositorioGatos`.
- `infrastructure/`: contiene los datos iniciales y el repositorio en memoria
  (`RepositorioGatosMemoria`).
- `test_*.py`: pruebas manuales que validan cada componente por separado.

## Documentación

Consulta la documentación detallada del proyecto en `docs/`
(índice en [docs/README.md](docs/README.md)).

## Tests

Desde la carpeta `02-documentando/`:

```bash
python3 -m gesticat.test_gato
python3 -m gesticat.test_responsable
python3 -m gesticat.test_colonia
python3 -m gesticat.test_repo_memoria
python3 -m gesticat.test_contrato
python3 -m gesticat.test_servicio
```