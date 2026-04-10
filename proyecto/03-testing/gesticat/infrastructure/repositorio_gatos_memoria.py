"""
Infraestructura/repositorio_gatos_memoria: Implementación en memoria del repositorio de gatos.

Almacena los gatos en un diccionario mientras la aplicación está en ejecución.
Los datos no persisten al cerrar el programa.
"""

from gesticat.domain.repositorio_gatos import RepositorioGatos


class RepositorioGatosMemoria(RepositorioGatos):
    """
    Implementación en memoria del repositorio de gatos.

    Usa un diccionario interno con el id del gato como clave.
    Los datos solo existen mientras la aplicación está en ejecución —
    no hay persistencia real. Útil para desarrollo, pruebas y demos.
    """

    def __init__(self):
        """Inicializa el almacén vacío."""
        self._gatos = {}

    def insertar(self, gato):
        """Inserta un gato nuevo. Lanza ValueError si el id ya existe.

        La comprobación de duplicados se hace aquí como segunda línea de defensa,
        aunque Colonia.agregar_gato() ya lo comprueba antes de llamar a insertar().
        """
        if gato.id_gato in self._gatos:
            raise ValueError(f"Ya existe un gato con id {gato.id_gato}.")
        self._gatos[gato.id_gato] = gato

    def actualizar(self, gato):
        """Actualiza un gato existente. Lanza ValueError si el id no existe.

        Se usa para reflejar cambios en el repositorio cuando no se trabaja
        con referencias directas al objeto, como ocurriría en persistencia real.
        """
        if gato.id_gato not in self._gatos:
            raise ValueError(f"No existe ningún gato con id {gato.id_gato}.")
        self._gatos[gato.id_gato] = gato

    def obtener(self, id_gato):
        """Devuelve el gato con ese id o None si no existe."""
        return self._gatos.get(id_gato)

    def listar(self):
        """Devuelve una lista con todos los gatos."""
        return list(self._gatos.values())

    def quitar(self, id_gato):
        """Elimina el gato con ese id. Lanza ValueError si no existe."""
        if id_gato not in self._gatos:
            raise ValueError(f"No existe ningún gato con id {id_gato}.")
        del self._gatos[id_gato]
