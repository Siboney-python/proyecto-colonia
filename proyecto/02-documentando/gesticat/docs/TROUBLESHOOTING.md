# Troubleshooting

Recoge los errores más comunes al ejecutar GestiCat, su causa y cómo
resolverlos. Separados en dos bloques: errores técnicos al arrancar el
proyecto y errores de uso durante la ejecución del menú.

## Errores técnicos

### `ModuleNotFoundError: No module named 'application'`
- **Causa**: se está ejecutando el menú desde una carpeta incorrecta.
  Los imports del proyecto usan rutas relativas al paquete `gesticat/`.
- **Solución**: ejecutar siempre desde dentro de la carpeta `gesticat/`:
  ```bash
  cd proyecto/02-documentando/gesticat
  python3 -m presentation.menu
  ```

### `ModuleNotFoundError: No module named 'domain'`
- **Causa**: mismo problema de carpeta incorrecta al ejecutar un test.
- **Solución**: ejecutar los tests también desde dentro de `gesticat/`:
  ```bash
  cd proyecto/02-documentando/gesticat
  python3 -m test_gato
  ```

### `SyntaxError` o `IndentationError`
- **Causa**: error de sintaxis en algún archivo `.py` modificado.
- **Solución**: revisar el archivo indicado en el mensaje de error,
  prestando atención a la línea señalada.

---

## Errores de uso

### `❌ El ID debe ser exactamente 3 dígitos`
- **Causa**: el ID introducido no tiene exactamente 3 dígitos numéricos.
- **Solución**: introducir un ID con exactamente 3 dígitos (ej. `001`, `042`).

### `❌ No existe ningún gato con id XXX`
- **Causa**: se intenta operar con un ID que no existe en la colonia.
- **Solución**: consultar el reporte de censo (opción 8) para ver los
  IDs disponibles, o registrar el gato primero (opción 1).

### `❌ Ya existe un gato con id XXX`
- **Causa**: se intenta registrar un gato con un ID ya usado.
- **Solución**: usar un ID diferente o consultar el censo para ver
  cuáles están disponibles.

### `❌ Un gato esterilizado debe tener clínica veterinaria asignada`
- **Causa**: se intenta marcar un gato como esterilizado sin indicar
  la clínica donde se realizó la intervención.
- **Solución**: introducir el nombre de la clínica al marcar la
  esterilización (opción 4).

### `❌ Un gato esterilizado no puede pasar a no esterilizado`
- **Causa**: se intenta revertir la esterilización de un gato.
- **Solución**: la esterilización es irreversible por diseño — una vez
  marcado como esterilizado no puede deshacerse.

### `❌ No se puede volver al estado SOLICITADA`
- **Causa**: se intenta tramitar un anexo con el estado `SOLICITADA`,
  que es el estado inicial y no puede recuperarse.
- **Solución**: elegir entre los estados disponibles: `ACTIVA`,
  `PENDIENTE` o `BAJA`.

### `❌ El responsable debe ser mayor de edad`
- **Causa**: la fecha de nacimiento introducida corresponde a una
  persona menor de 18 años.
- **Solución**: verificar que la fecha de nacimiento es correcta.

### `❌ El email no tiene un formato válido`
- **Causa**: el email introducido no tiene el formato `texto@texto.dominio`.
- **Solución**: introducir un email con formato válido
  (ej. `nombre@gmail.com`).

### `❌ El teléfono debe tener exactamente 9 dígitos`
- **Causa**: el teléfono introducido no tiene exactamente 9 dígitos
  numéricos.
- **Solución**: introducir el teléfono sin espacios ni guiones
  (ej. `612345678`).

### `❌ La fecha debe tener formato dd/mm/aaaa`
- **Causa**: la fecha introducida no sigue el formato esperado.
- **Solución**: introducir la fecha con el formato correcto
  (ej. `15/06/1985`).

### `❌ La fecha de registro no puede ser futura`
- **Causa**: la fecha de registro introducida es posterior a hoy.
- **Solución**: introducir una fecha anterior o igual a hoy, o dejar
  vacío para usar la fecha de hoy automáticamente.
