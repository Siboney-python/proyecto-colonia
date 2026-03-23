"""Pruebas manuales de validación para PersonaFisica y Protectora.

Cubre los casos válidos e inválidos de cada campo, la normalización
de identificación a mayúsculas y la representación legible de cada subclase.
"""

from domain.responsable import PersonaFisica, Protectora


# -- CASOS VÁLIDOS --

print("Caso válido PersonaFisica")
persona_ok = PersonaFisica("Ana García", "612345678", "ana@email.com",
                            "12345678A", "15/06/1985")
print("Creado:", persona_ok.nombre, persona_ok.telefono,
      persona_ok.email, persona_ok.identificacion)

print("Caso válido Protectora")
protectora_ok = Protectora("Asociación Felina", "912345678", "info@asociacion.com",
                            "A12345678", "REG-001")
print("Creado:", protectora_ok.nombre, protectora_ok.telefono,
      protectora_ok.email, protectora_ok.numero_registro)


# -- NOMBRE --

print("Nombre vacío")
try:
    PersonaFisica("", "612345678", "ana@email.com", "12345678A", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)


# -- TELÉFONO --

print("Teléfono inválido (menos de 9 dígitos)")
try:
    PersonaFisica("Ana García", "12345", "ana@email.com", "12345678A", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)

print("Teléfono inválido (letras)")
try:
    PersonaFisica("Ana García", "ABCDEFGHI", "ana@email.com", "12345678A", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)


# -- EMAIL --

print("Email inválido")
try:
    PersonaFisica("Ana García", "612345678", "correo_sin_arroba", "12345678A", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)


# -- IDENTIFICACIÓN --

print("Identificación vacía")
try:
    PersonaFisica("Ana García", "612345678", "ana@email.com", "", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)

print("Identificación normalizada a mayúsculas")
persona_minus = PersonaFisica("Ana García", "612345678", "ana@email.com",
                               "12345678a", "15/06/1985")
print("Normalizada:", persona_minus.identificacion == "12345678A")


# -- FECHA DE NACIMIENTO --

print("Fecha de nacimiento futura")
try:
    PersonaFisica("Ana García", "612345678", "ana@email.com", "12345678A", "01/01/2099")
except ValueError as e:
    print("Error esperado:", e)

print("Menor de edad")
try:
    PersonaFisica("Ana García", "612345678", "ana@email.com", "12345678A", "01/01/2015")
except ValueError as e:
    print("Error esperado:", e)


# -- PROTECTORA --

print("Número de registro vacío en Protectora")
try:
    Protectora("Asociación Felina", "912345678", "info@asociacion.com",
               "A12345678", "")
except ValueError as e:
    print("Error esperado:", e)


# -- REPRESENTACIÓN __str__ --

print("__str__ PersonaFisica")
print("Resultado:", str(persona_ok))

print("__str__ Protectora")
print("Resultado:", str(protectora_ok))