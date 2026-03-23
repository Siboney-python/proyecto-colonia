"""Pruebas manuales de validación para la entidad Gato.

Cubre los casos válidos e inválidos de cada campo, las reglas de negocio 
sobre esterilización y las validaciones de fecha de registro.
"""

from datetime import date
from domain.gato import Gato, Sexo, EstadoGato


# -- CASO VÁLIDO --

print("Caso válido")
gato_ok = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
               "Clínica Sur", True, "10/01/2024")
print("Creado:", gato_ok.id_gato, gato_ok.nombre, gato_ok.color,
      gato_ok.sexo.value, gato_ok.estado.value, gato_ok.esterilizado)


# -- ID --

print("ID inválido (menos de 3 dígitos)")
try:
    Gato("01", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
         None, False, "10/01/2024")
except ValueError as e:
    print("Error esperado:", e)

print("ID inválido (letras)")
try:
    Gato("ABC", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
         None, False, "10/01/2024")
except ValueError as e:
    print("Error esperado:", e)


# -- NOMBRE Y COLOR --

print("Nombre vacío")
try:
    Gato("002", "", "Gris", Sexo.MACHO, EstadoGato.COL,
         None, False, "10/01/2024")
except ValueError as e:
    print("Error esperado:", e)

print("Color vacío")
try:
    Gato("002", "Luna", "", Sexo.MACHO, EstadoGato.COL,
         None, False, "10/01/2024")
except ValueError as e:
    print("Error esperado:", e)


# -- SEXO Y ESTADO --

print("Sexo inválido")
try:
    Gato("002", "Luna", "Blanca", "MACHO", EstadoGato.COL,
         None, False, "10/01/2024")
except TypeError as e:
    print("Error esperado:", e)

print("Estado inválido")
try:
    Gato("002", "Luna", "Blanca", Sexo.HEMBRA, "COL",
         None, False, "10/01/2024")
except TypeError as e:
    print("Error esperado:", e)


# -- ESTERILIZACIÓN --

print("Esterilizado sin clínica")
try:
    Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
         None, True, "10/01/2024")
except ValueError as e:
    print("Error esperado:", e)

print("Revertir esterilización")
try:
    gato_ok.esterilizado = False
except ValueError as e:
    print("Error esperado:", e)


# -- FECHA DE REGISTRO --

print("Fecha futura")
try:
    Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
         None, False, "01/01/2099")
except ValueError as e:
    print("Error esperado:", e)

print("Fecha formato incorrecto")
try:
    Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
         None, False, "2024-01-10")
except ValueError as e:
    print("Error esperado:", e)

print("Fecha opcional (None usa fecha de hoy)")
gato_sin_fecha = Gato("003", "Canela", "Naranja", Sexo.HEMBRA, EstadoGato.COL,
                      None, False)
print("Fecha asignada:", gato_sin_fecha.fecha_registro == date.today())