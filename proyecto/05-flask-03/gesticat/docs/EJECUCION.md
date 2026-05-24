# Ejecución

## Requisitos

- Python 3.10+.
- Dependencias en `requirements.txt` (incluye `coverage` y `flask`).
- Compatible con Linux, macOS y Windows.

## Clonar el repositorio

```bash
git clone git@github.com:Siboney-python/proyecto-colonia.git
cd proyecto-colonia/proyecto/05-flask-03
```

## Preparación del entorno

Desde la carpeta `05-flask-03/`:

```bash
python3 -m venv .venv
```

Activar el entorno virtual:

```bash
# Linux y macOS
source .venv/bin/activate

# Windows GitBash
source .venv/Scripts/activate

# Windows PowerShell
source .venv/Scripts/Activate.ps1
```

Instalar dependencias:

```bash
pip install -r gesticat/requirements.txt 
```

## Crear base de datos

Desde la carpeta `05-flask-03/`:

```bash
python3 -m gesticat.crear_bd
```

## Ejecutar la interfaz web (Flask)

Desde la carpeta `05-flask-03/`:

```bash
python3 -m gesticat.presentation.app
```

Abre `http://localhost:5000` en el navegador.

### Rutas de ayuda y observabilidad

- `/ayuda` — lista todas las rutas registradas. Se actualiza automáticamente
  al añadir o quitar routes sin tocar su código.
- `gesticat.log` — fichero de log que se crea automáticamente al arrancar
  la app. Registra cada petición con timestamp, método y ruta. No se
  versiona en git (`*.log` está en `.gitignore`).

### Verificación de coexistencia menu↔web

Ambas interfaces pueden ejecutarse simultáneamente sobre la misma base de
datos SQLite. Un alta hecha desde la web aparece inmediatamente en el menú
de consola y viceversa:

```bash
# Terminal 1 — interfaz web
python3 -m gesticat.presentation.app

# Terminal 2 — menú de consola
python3 -m gesticat.presentation.menu
```

### Plantillas Jinja2

Las vistas de lectura usan plantillas HTML ubicadas en
`presentation/templates/`. La plantilla base `base.html` define la
cabecera y navegación comunes. Si añades una plantilla nueva debe
extender de `base.html` con `{% extends "base.html" %}` para mantener
la cabecera en todas las páginas.

## Ejecutar el menú

Desde la carpeta `05-flask-03/`:

```bash
python3 -m gesticat.presentation.menu
```

## Ejecutar los tests

Desde la carpeta `05-flask-03/`:

```bash
python3 -m unittest
```

## Cobertura

```bash
coverage run -m unittest
coverage report
coverage html
```

El reporte HTML se consulta en `htmlcov/index.html`.

## Flujo rápido de ejemplo con menu.py

Al arrancar la aplicación se conecta a la base de datos `gesticat.db` con
cinco gatos de ejemplo y una colonia con responsable asignado. Si aún no
has ejecutado `crear_bd.py`, hazlo primero.

```
Opción 9 → Reporte de colonia   (ver el estado inicial)
Opción 8 → Reporte de censo     (ver población activa)
Opción 5 → Listar sin esterilizar
```

## Flujo completo de ejemplo con menu.py

1. Opción 9: Ver el reporte de colonia — estado, responsable y total de gatos.
2. Opción 1: Registrar un gato nuevo (ej. ID=006, nombre=Canela, color=Naranja,
   sexo=H, estado=COL, sin clínica, no esterilizado, Enter para fecha de hoy).
3. Opción 5: Comprobar que aparece en la lista de no esterilizados.
4. Opción 4: Marcar el gato 006 como esterilizado (indicar clínica).
5. Opción 5: Comprobar que ya no aparece en la lista.
6. Opción 3: Actualizar el estado del gato 006 a ACOG (en acogida).
7. Opción 8: Ver el reporte de censo actualizado.
8. Opción 2: Borrar el registro del gato 006.
9. Opción 7: Tramitar anexo → ACTIVA.
10. Opción 0: Salir.

## Errores comunes

- `❌ El ID debe ser exactamente 3 dígitos` — el ID introducido no tiene
  exactamente 3 dígitos numéricos.
- `❌ No existe ningún gato con id XXX` — se intenta operar con un ID
  que no existe en la colonia.
- `❌ Un gato esterilizado debe tener clínica veterinaria asignada` — se
  intenta marcar como esterilizado sin indicar clínica.
- `❌ Un gato esterilizado no puede pasar a no esterilizado` — la
  esterilización es irreversible.
- `❌ No se puede volver al estado SOLICITADA` — el estado inicial de la
  colonia no puede recuperarse una vez tramitado un anexo.
  

