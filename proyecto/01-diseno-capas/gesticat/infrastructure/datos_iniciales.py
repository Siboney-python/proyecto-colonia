"""
Infraestructura/datos_iniciales: Datos de ejemplo para el proyecto GestiCat.

Este módulo carga una colonia con un responsable y varios gatos de ejemplo
para poder probar el sistema manualmente al arrancar la aplicación.
"""

from datetime import date
from domain.gato import Gato, Sexo, EstadoGato
from domain.colonia import Colonia
from domain.responsable import PersonaFisica
from infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria


def cargar_datos_iniciales():
    """Crea y devuelve una colonia con datos de ejemplo."""

    # -- REPOSITORIO --
    repositorio = RepositorioGatosMemoria()

    # -- RESPONSABLE --
    responsable = PersonaFisica(
        nombre="Siboney Pérez",
        telefono="612345678",
        email="siboney_perez@email.com",
        identificacion="12345678A",
        fecha_nacimiento="10/10/1986"
    )

    # -- COLONIA --
    colonia = Colonia("Colonia Sur", responsable, repositorio)

    # -- GATOS --
    gatos = [
        Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
             "Clínica Sur", True, "10/01/2024"),
        Gato("002", "Kiwi", "Blanca", Sexo.HEMBRA, EstadoGato.ACOG,
          "Clínica Sur", True, "15/02/2024"),
        Gato("003", "GordiLuis", "Pardo", Sexo.MACHO, EstadoGato.FALL,
             "Clínica Norte", True, "20/03/2024"),
        Gato("004", "Sombra", "Negro", Sexo.HEMBRA, EstadoGato.COL,
             None, False, "05/04/2024"),
        Gato("005", "Nieve", "Blanco", Sexo.DESCONOCIDO, EstadoGato.COL,
             None, False, "01/06/2024"),
    ]

    for gato in gatos:
        colonia.agregar_gato(gato)

    return colonia