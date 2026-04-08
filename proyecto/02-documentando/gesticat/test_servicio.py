"""Pruebas manuales de validación para ServicioColonia.

Cubre los casos de uso principales del servicio: registro y gestión de gatos,
esterilización, asignación de responsable, tramitación de anexos y reportes.
"""

from datetime import date

from gesticat.domain.colonia import Colonia, EstadoColonia
from gesticat.domain.gato import Sexo, EstadoGato
from gesticat.domain.responsable import PersonaFisica, Protectora
from gesticat.infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria
from gesticat.application.servicio_colonia import ServicioColonia

responsable = PersonaFisica("Ana García", "612345678", "ana@email.com",
                             "12345678A", "15/06/1985")
repo = RepositorioGatosMemoria()
colonia = Colonia("Colonia Sur", responsable, repo)
servicio = ServicioColonia(colonia)


# -- REGISTRO DE GATOS --

print("Registrar gato con fecha explícita")
servicio.registrar_gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                         None, False, "10/01/2024")
print("Registrado:", colonia.buscar_por_id("001").nombre)

print("Registrar gato sin fecha (usa fecha de hoy)")
servicio.registrar_gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                         None, False)
print("Fecha de hoy:", colonia.buscar_por_id("002").fecha_registro == date.today())

print("Registrar gato duplicado")
try:
    servicio.registrar_gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                             None, False, "10/01/2024")
except ValueError as e:
    print("Error esperado:", e)


# -- ACTUALIZAR ESTADO --

print("Actualizar estado gato")
servicio.actualizar_estado_gato("001", EstadoGato.ACOG)
print("Estado:", colonia.buscar_por_id("001").estado.value)

print("Actualizar estado gato inexistente")
try:
    servicio.actualizar_estado_gato("999", EstadoGato.ACOG)
except ValueError as e:
    print("Error esperado:", e)


# -- ESTERILIZACIÓN --

print("Marcar gato como esterilizado")
servicio.actualizar_esterilizacion_gato("001", True, "Clínica Sur")
print("Esterilizado:", colonia.buscar_por_id("001").esterilizado)

print("Revertir esterilización")
try:
    servicio.actualizar_esterilizacion_gato("001", False)
except ValueError as e:
    print("Error esperado:", e)

print("Listar sin esterilizar")
sin_esterilizar = servicio.listar_sin_esterilizar()
print("Sin esterilizar:", len(sin_esterilizar))


# -- COLONIA --

print("Asignar responsable")
nueva_protectora = Protectora("Asociación Felina", "912345678",
                               "info@asociacion.com", "A12345678", "REG-001")
servicio.asignar_responsable(nueva_protectora)
print("Nuevo responsable:", colonia.responsable.nombre)

print("Tramitar anexo")
servicio.tramitar_anexo(EstadoColonia.ACTIVA)
print("Estado colonia:", colonia.estado.value)


# -- REPORTES --

print("Reporte censo")
print("Censo:", servicio.reporte_censo())

print("Reporte colonia")
print("Colonia:", servicio.reporte_colonia())