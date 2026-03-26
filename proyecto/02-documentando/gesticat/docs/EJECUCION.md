# Ejecución

## Requisitos

- Python 3.10+.
- No requiere dependencias externas (solo librería estándar).
- Compatible con Linux, macOS y Windows.

## Clonar el repositorio

```bash
git clone git@github-python:Siboney-python/proyecto-colonia.git
cd proyecto-colonia/proyecto/02-documentando/gesticat
```

## Ejecutar el menú

Desde la carpeta `gesticat/`:

```bash
cd proyecto/02-documentando/gesticat
python3 -m presentation.menu
```

## Ejecutar los tests

Desde la misma carpeta `gesticat/`:

```bash
python3 -m test_gato
python3 -m test_responsable
python3 -m test_colonia
python3 -m test_repo_memoria
python3 -m test_contrato
python3 -m test_servicio
```

## Flujo rápido de ejemplo

Al arrancar la aplicación se cargan automáticamente cinco gatos de ejemplo
y una colonia con responsable asignado. Puedes probar el sistema sin
introducir datos manualmente:

```
Opción 9 → Reporte de colonia   (ver el estado inicial)
Opción 8 → Reporte de censo     (ver población activa)
Opción 5 → Listar sin esterilizar
```

## Flujo completo de ejemplo

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