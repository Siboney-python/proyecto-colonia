"""
Infraestructura/datos_iniciales: Datos de ejemplo para el proyecto GestiCat.

Este módulo proporciona funciones para crear una colonia de ejemplo con
responsable y gatos precargados, y un servicio listo para usar. Se utiliza
tanto para arrancar la aplicación manualmente como para pruebas y demos.
"""

from gesticat.domain.colonia import Colonia
from gesticat.domain.responsable import PersonaFisica
from gesticat.infrastructure.repositorio_gatos_sqlite import RepositorioGatosSQLite


def crear_colonia_con_datos():
    """Crea y devuelve una colonia lista para usar con el repositorio SQLite.

    Construye la colonia con su responsable y conecta el repositorio SQLite donde
    ya están cargados los gatos iniciales. Los datos de los gatos vienen de la 
    base de datos creada por crear_bd.py.


    Devuelve una instancia de Colonia lista para pasar a ServicioColonia.
    """
    repositorio = RepositorioGatosSQLite()

    responsable = PersonaFisica(
        nombre="Siboney Apellido",
        telefono="612345678",
        email="siboney_apellido@email.com",
        identificacion="12345678A",
        fecha_nacimiento="10/10/1986"
    )

    colonia = Colonia("Colonia Sur", responsable, repositorio)

    return colonia


def crear_servicio():
    """Crea y devuelve un ServicioColonia listo para usar.

    Construye el grafo completo de objetos — repositorio, colonia con datos
    de ejemplo y servicio — y lo devuelve listo para usar desde el menú
    o desde pruebas de integración.

    Devuelve una instancia de ServicioColonia lista para usar.
    """
    from gesticat.application.servicio_colonia import ServicioColonia
    colonia = crear_colonia_con_datos()
    return ServicioColonia(colonia)