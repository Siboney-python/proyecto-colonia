"""Pruebas manuales de validación para RepositorioGatosMemoria."""

from gesticat.domain.gato import Gato, Sexo, EstadoGato
from gesticat.infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria

repo = RepositorioGatosMemoria()

print("Caso válido - insertar y obtener")
gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
            None, False, "10/01/2024")
repo.insertar(gato)
print("Obtenido:", repo.obtener("001").nombre)

print("Insertar duplicado")
try:
    repo.insertar(gato)
except ValueError as e:
    print("Error esperado:", e)

print("Obtener inexistente")
print("Resultado:", repo.obtener("999"))

print("Listar")
repo.insertar(Gato("002", "Kiwi", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                   None, False, "15/02/2024"))
print("Total:", len(repo.listar()))

print("Actualizar gato existente")
gato.estado = EstadoGato.ACOG
repo.actualizar(gato)
print("Estado actualizado:", repo.obtener("001").estado.value)

print("Actualizar gato inexistente")
gato_inexistente = Gato("999", "Fantasma", "Negro", Sexo.DESCONOCIDO, EstadoGato.COL,
                         None, False, "10/01/2024")
try:
    repo.actualizar(gato_inexistente)
except ValueError as e:
    print("Error esperado:", e)

print("Borrar registro")
repo.quitar("001")
print("Tras borrar registro del gato:", repo.obtener("001"))

print("Borrar registro inexistente")
try:
    repo.quitar("999")
except ValueError as e:
    print("Error esperado:", e)