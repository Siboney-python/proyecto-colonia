"""Pruebas manuales de validación para ServicioColonia."""

from domain.colonia import Colonia, EstadoColonia
from domain.gato import Sexo, EstadoGato
from domain.responsable import PersonaFisica, Protectora
from infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria
from application.servicio_colonia import ServicioColonia

responsable = PersonaFisica("Ana García", "612345678", "ana@email.com",
                             "12345678A", "15/06/1985")
repo = RepositorioGatosMemoria()
colonia = Colonia("Colonia Sur", responsable, repo)
servicio = ServicioColonia(colonia)

print("Registrar gato")
servicio.registrar_gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                         None, False, "10/01/2024")
print("Registrado:", colonia.buscar_por_id("001").nombre)

print("Registrar gato duplicado")
try:
    servicio.registrar_gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                             None, False, "10/01/2024")
except ValueError as e:
    print("Error esperado:", e)

print("Actualizar estado gato")
servicio.actualizar_estado_gato("001", EstadoGato.ACOG)
print("Estado:", colonia.buscar_por_id("001").estado.value)

print("Actualizar estado gato inexistente")
try:
    servicio.actualizar_estado_gato("999", EstadoGato.ACOG)
except ValueError as e:
    print("Error esperado:", e)

print("Marcar gato como esterilizado")
servicio.actualizar_esterilizacion_gato("001", True, "Clínica Sur")
print("Esterilizado:", colonia.buscar_por_id("001").esterilizado)

print("Revertir esterilización")
try:
    servicio.actualizar_esterilizacion_gato("001", False)
except ValueError as e:
    print("Error esperado:", e)

print("Listar sin esterilizar")
servicio.registrar_gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                         None, False, "15/02/2024")
sin_esterilizar = servicio.listar_sin_esterilizar()
print("Sin esterilizar:", len(sin_esterilizar))

print("Asignar responsable")
nueva_protectora = Protectora("Asociación Felina", "912345678",
                               "info@asociacion.com", "A12345678", "REG-001")
servicio.asignar_responsable(nueva_protectora)
print("Nuevo responsable:", colonia.responsable.nombre)

print("Tramitar anexo")
servicio.tramitar_anexo(EstadoColonia.ACTIVA)
print("Estado colonia:", colonia.estado.value)

print("Reporte censo")
print("Censo:", servicio.reporte_censo())

print("Reporte colonia")
print("Colonia:", servicio.reporte_colonia())