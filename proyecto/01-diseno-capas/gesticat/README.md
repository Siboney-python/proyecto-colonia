# GestiCat LPGC

Sistema de gestión y censo de colonias felinas urbanas de Las Palmas de Gran Canaria.

## Propósito del proyecto

- Digitalizar la gestión de una colonia de gatos callejeros del municipio.
- Facilitar el registro, seguimiento y control del censo de gatos de la colonia.
- Gestionar el estado administrativo de la colonia ante el ayuntamiento.
- Permitir la incorporación de mejoras futuras (base de datos, interfaz móvil,
  múltiples colonias) sin romper el núcleo del sistema.

## Estructura por capas

- `presentation/menu.py`: interfaz de consola que solo pide datos y muestra resultados.
- `application/servicio_colonia.py`: coordina los casos de uso sobre la `Colonia`
  sin exponer la lógica interna.
- `domain/`: alberga las entidades (`Gato`, `Colonia`, `Responsable`), las
  validaciones y el contrato `RepositorioGatos`.
- `infrastructure/`: contiene los datos iniciales y el repositorio en memoria
  (`RepositorioGatosMemoria`).
- `test_*.py`: pruebas manuales que validan cada componente por separado.

## Requisitos y ejecución

Instala Python 3.10+ y ejecuta desde la carpeta `gesticat/`:

```bash
python3 -m presentation.menu
```

Para comprobar los componentes por separado:

```bash
python3 -m test_gato
python3 -m test_responsable
python3 -m test_colonia
python3 -m test_repo_memoria
python3 -m test_contrato
python3 -m test_servicio
```
