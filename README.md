# GestiCat LPGC

Sistema de gestión y censo de colonias felinas urbanas de Las Palmas de Gran Canaria.

## Propósito del proyecto
- Digitalizar la gestión de una colonia de gatos callejeros del municipio.
- Mostrar cómo crear una aplicación ordenada manteniendo cohesión, encapsulación y acoplamiento bajo.
- Permitir experimentar con un menú de consola que delega toda la lógica en servicios y en el dominio.
- Facilitar la incorporación de mejoras (base de datos, interfaz web, módulo de adopciones, múltiples colonias) sin romper el núcleo del negocio.

## Estructura por capas
- `presentation/menu.py`: interfaz de consola que solo pide datos y muestra resultados.
- `application/servicio_colonia.py`: coordina los casos de uso sobre la `Colonia` sin exponer la lógica interna.
- `domain/`: alberga las entidades (`Gato`, `Colonia`, `Responsable`), las validaciones y el contrato `RepositorioGatos`.
- `infrastructure/`: contiene los datos iniciales y el repositorio en memoria (`RepositorioGatosMemoria`).
- `test_*.py`: pruebas manuales que validan cada componente por separado.

## Requisitos y ejecución
1. Instala Python 3.10+ y ejecuta desde la carpeta `gesticat/`:
```bash
   python3 -m presentation.menu
```
2. Para comprobar los componentes por separado:
```bash
   python3 -m test_gato
   python3 -m test_responsable
   python3 -m test_colonia
   python3 -m test_repo_memoria
   python3 -m test_servicio
   python3 -m test_contrato
```
