"""Pruebas manuales de validación para Colonia."""

from domain.colonia import Colonia, EstadoColonia
from domain.gato import Gato, Sexo, EstadoGato
from domain.responsable import PersonaFisica
from infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria

responsable = PersonaFisica("Ana García", "612345678", "ana@email.com",
                             "12345678A", "15/06/1985")
repo = RepositorioGatosMemoria()

print("Caso válido")
colonia_ok = Colonia("Colonia Sur", responsable, repo)
print("Creada:", colonia_ok.nombre, colonia_ok.estado.value)

print("Estado inicial es SOLICITADA")
print("Estado:", colonia_ok.estado == EstadoColonia.SOLICITADA)

print("Nombre vacío")
try:
    Colonia("", responsable, repo)
except ValueError as e:
    print("Error esperado:", e)

print("Responsable inválido")
try:
    Colonia("Colonia Sur", "no es un responsable", repo)
except TypeError as e:
    print("Error esperado:", e)

print("Agregar gato")
gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
            None, False, "10/01/2024")
colonia_ok.agregar_gato(gato)
print("Gatos:", colonia_ok.reporte_colonia()["total_gatos"])

print("Agregar gato duplicado")
try:
    colonia_ok.agregar_gato(gato)
except ValueError as e:
    print("Error esperado:", e)

print("Buscar gato por id")
encontrado = colonia_ok.buscar_por_id("001")
print("Encontrado:", encontrado.nombre)

print("Buscar gato inexistente")
print("Resultado:", colonia_ok.buscar_por_id("999"))

print("Tramitar anexo a ACTIVA")
colonia_ok.tramitar_anexo(EstadoColonia.ACTIVA)
print("Estado:", colonia_ok.estado.value)

print("Tramitar anexo a SOLICITADA")
try:
    colonia_ok.tramitar_anexo(EstadoColonia.SOLICITADA)
except ValueError as e:
    print("Error esperado:", e)

print("Reporte censo")
print("Censo:", colonia_ok.reporte_censo())

print("Reporte colonia")
print("Colonia:", colonia_ok.reporte_colonia())