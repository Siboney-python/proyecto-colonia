"""Pruebas manuales de validación para RepositorioGatosMemoria."""

from domain.gato import Gato, Sexo, EstadoGato
from infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria

repo = RepositorioGatosMemoria()

print("Caso válido - guardar y obtener")
gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
            None, False, "10/01/2024")
repo.guardar(gato)
print("Obtenido:", repo.obtener("001").nombre)

print("Obtener inexistente")
print("Resultado:", repo.obtener("999"))

print("Listar")
repo.guardar(Gato("002", "Kiwi", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                  None, False, "15/02/2024"))
print("Total:", len(repo.listar()))

print("Borrar registro")
repo.quitar("001")
print("Tras borrar registro del gato:", repo.obtener("001"))

print("Borrar registro inexistente")
try:
    repo.quitar("999")
except ValueError as e:
    print("Error esperado:", e)