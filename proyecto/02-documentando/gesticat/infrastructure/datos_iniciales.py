"""
Infraestructura/datos_iniciales: Datos de ejemplo para el proyecto GestiCat.

Este módulo carga una colonia con un responsable y varios gatos de ejemplo
para poder probar el sistema manualmente al arrancar la aplicación.
"""

from gesticat.domain.gato import Gato, Sexo, EstadoGato
from gesticat.domain.colonia import Colonia
from gesticat.domain.responsable import PersonaFisica
from gesticat.infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria


def cargar_datos_iniciales():
    """Crea y devuelve una colonia de ejemplo lista para usar.

    Construye una colonia con responsable, repositorio en memoria y cinco gatos
    de muestra que representan distintos estados y situaciones reales de la colonia.
    Se usa al arrancar la aplicación para poder probarla sin introducir datos manualmente.

    Devuelve una instancia de Colonia lista para pasar a ServicioColonia.
    """

    # -- REPOSITORIO --
    # Repositorio en memoria: los datos no persisten al cerrar la aplicación.
    repositorio = RepositorioGatosMemoria()

    # -- RESPONSABLE --
    responsable = PersonaFisica(
        nombre="Siboney Apellido",
        telefono="612345678",
        email="siboney_apellido@email.com",
        identificacion="12345678A",
        fecha_nacimiento="10/10/1986"
    )

    # -- COLONIA --
    colonia = Colonia("Colonia Sur", responsable, repositorio)

    # -- GATOS --
    # Gatos de ejemplo con distintos estados: en colonia, en acogida, fallecido.
    # Las fechas de registro son históricas (anteriores al sistema),
    # por eso se pasan explícitamente en lugar de usar la fecha de hoy.
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