"""
Infraestructura/datos_iniciales: Datos de ejemplo para el proyecto GestiCat.

Este módulo proporciona funciones para crear una colonia de ejemplo con
responsable y gatos precargados, y un servicio listo para usar. Se utiliza
tanto para arrancar la aplicación manualmente como para pruebas y demos.
"""

from gesticat.domain.colonia import Colonia
from gesticat.domain.responsable import PersonaFisica
from gesticat.application.servicio_colonia import ServicioColonia

# -- REPOSITORIO EN MEMORIA --

def crear_colonia_con_datos():
    """Crea y devuelve una colonia de ejemplo lista para usar.

    Construye una colonia con responsable, repositorio en memoria y cinco gatos
    de muestra que representan distintos estados y situaciones reales de la colonia.
    Las fechas de registro son históricas y se pasan explícitamente para
    preservarlas en lugar de usar la fecha de hoy.

    Devuelve una instancia de Colonia lista para pasar a ServicioColonia.
    """
    from gesticat.domain.gato import Gato, Sexo, EstadoGato
    from gesticat.infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria

    repositorio = RepositorioGatosMemoria()

    responsable = PersonaFisica(
        nombre="Siboney Apellido",
        telefono="612345678",
        email="siboney_apellido@email.com",
        identificacion="12345678A",
        fecha_nacimiento="10/10/1986"
    )

    colonia = Colonia("Colonia Sur", responsable, repositorio)

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


def crear_servicio():
    """Crea y devuelve un ServicioColonia con repositorio en memoria listo para usar.
    """
    colonia = crear_colonia_con_datos()
    return ServicioColonia(colonia)

# -- REPOSITORIO EN SQLITE --

def crear_servicio_sqlite(ruta_bd="gesticat.db"):
    """Crea y devuelve un ServicioColonia con persistencia en SQLite."""
    from gesticat.infrastructure.repositorio_gatos_sqlite import RepositorioGatosSQLite
    repositorio = RepositorioGatosSQLite(ruta_bd)
    responsable = PersonaFisica(
        nombre="Siboney Apellido",
        telefono="612345678",
        email="siboney_apellido@email.com",
        identificacion="12345678A",
        fecha_nacimiento="10/10/1986"
    )
    colonia = Colonia("Colonia Sur", responsable, repositorio)
    return ServicioColonia(colonia)
