# Casos de uso

Describe las operaciones disponibles en el menú de GestiCat. Para cada caso
se especifica entrada, precondiciones, salida, efectos y errores posibles.

## Opciones del menú

```
--- Gatos ---
1. Registrar gato
2. Borrar registro del gato
3. Actualizar estado del gato
4. Marcar gato como esterilizado
5. Listar gatos sin esterilizar
--- Colonia ---
6. Asignar responsable
7. Tramitar anexo
--- Reportes ---
8. Reporte de censo
9. Reporte de colonia
--- ---
0. Salir
```

---

## 1. Registrar gato

- **Entrada**: ID (3 dígitos), nombre, color, sexo (H/M/?), estado
  (COL/ACOG/ADOP/FALL/DESA), clínica veterinaria (opcional), esterilizado
  (s/n), fecha de registro (dd/mm/aaaa, opcional — usa hoy si se deja vacío).
- **Precondiciones**: el ID no debe existir ya en la colonia.
- **Salida**: confirmación de registro.
- **Efectos**: el gato queda registrado en el repositorio de la colonia.
- **Errores**:
  - `ValueError`: ID duplicado, fecha futura, formato de fecha incorrecto.
  - `TypeError`: sexo o estado con valor fuera del enum.

## 2. Borrar registro del gato

- **Entrada**: ID del gato.
- **Precondiciones**: el ID debe existir en la colonia.
- **Salida**: confirmación de borrado.
- **Efectos**: el gato es eliminado del repositorio.
- **Errores**:
  - `ValueError`: ID inexistente.

## 3. Actualizar estado del gato

- **Entrada**: ID del gato, nuevo estado (COL/ACOG/ADOP/FALL/DESA).
- **Precondiciones**: el ID debe existir en la colonia.
- **Salida**: confirmación de actualización.
- **Efectos**: el estado del gato queda actualizado y persistido en el repositorio.
- **Errores**:
  - `ValueError`: ID inexistente.
  - `TypeError`: estado con valor fuera del enum.

## 4. Marcar gato como esterilizado

- **Entrada**: ID del gato, clínica veterinaria (opcional si ya tiene una asignada).
- **Precondiciones**: el ID debe existir en la colonia. El gato no debe estar
  ya esterilizado (la esterilización es irreversible).
- **Salida**: confirmación de actualización.
- **Efectos**: el gato queda marcado como esterilizado y se actualiza la
  clínica si se indica una nueva.
- **Errores**:
  - `ValueError`: ID inexistente, intento de revertir esterilización,
    esterilizar sin clínica asignada.

## 5. Listar gatos sin esterilizar

- **Entrada**: ninguna.
- **Salida**: listado de gatos activos (en colonia o en acogida) que no
  están esterilizados, con ID, nombre, sexo y estado.
- **Efectos**: ninguno.
- **Errores**: ninguno. Si todos están esterilizados, muestra un mensaje
  informativo.

## 6. Asignar responsable

- **Entrada**: tipo (1=Persona física, 2=Protectora), nombre, teléfono (9
  dígitos), email, identificación (DNI/NIF/CIF). Para persona física:
  fecha de nacimiento. Para protectora: número de registro.
- **Precondiciones**: ninguna — sustituye al responsable actual.
- **Salida**: confirmación de asignación.
- **Efectos**: la colonia queda con el nuevo responsable asignado.
- **Errores**:
  - `ValueError`: teléfono inválido, email sin formato válido,
    identificación vacía, fecha futura, menor de edad.
  - `TypeError`: tipo de responsable no válido.

## 7. Tramitar anexo

- **Entrada**: nuevo estado administrativo (ACTIVA/PENDIENTE/BAJA).
- **Precondiciones**: no se puede volver al estado SOLICITADA.
- **Salida**: confirmación de tramitación.
- **Efectos**: el estado de la colonia queda actualizado y se registra
  la fecha de la última actualización.
- **Errores**:
  - `ValueError`: intento de volver al estado SOLICITADA.
  - `TypeError`: estado con valor fuera del enum.

## 8. Reporte de censo

- **Entrada**: ninguna.
- **Salida**: estadísticas de población activa — total, machos, hembras,
  desconocidos, esterilizados y no esterilizados.
- **Efectos**: ninguno.
- **Errores**: ninguno.

## 9. Reporte de colonia

- **Entrada**: ninguna.
- **Salida**: información general de la colonia — nombre, responsable,
  estado administrativo, fecha de última actualización, si necesita
  revisión y total de gatos activos.
- **Efectos**: ninguno.
- **Errores**: ninguno.

## 0. Salir

- **Entrada**: ninguna.
- **Salida**: mensaje de despedida.
- **Efectos**: termina la ejecución del programa.
- **Errores**: ninguno.