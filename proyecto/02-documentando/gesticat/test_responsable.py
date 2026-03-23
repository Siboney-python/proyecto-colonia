"""Pruebas manuales de validación para Responsable, PersonaFisica y Protectora."""

from domain.responsable import PersonaFisica, Protectora

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

print("Nombre vacío")
try:
    PersonaFisica("", "612345678", "ana@email.com", "12345678A", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)

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

print("Email inválido")
try:
    PersonaFisica("Ana García", "612345678", "correo_sin_arroba", "12345678A", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)

print("Identificación vacía")
try:
    PersonaFisica("Ana García", "612345678", "ana@email.com", "", "15/06/1985")
except ValueError as e:
    print("Error esperado:", e)

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

print("Número de registro vacío en Protectora")
try:
    Protectora("Asociación Felina", "912345678", "info@asociacion.com",
               "A12345678", "")
except ValueError as e:
    print("Error esperado:", e)