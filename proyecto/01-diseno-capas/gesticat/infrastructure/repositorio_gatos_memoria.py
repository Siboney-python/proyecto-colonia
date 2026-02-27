# infrastructure/repositorio_gatos_memoria.py

from domain.repositorio_gatos import RepositorioGatos


class RepositorioGatosMemoria(RepositorioGatos):
    """Implementación en memoria del repositorio de gatos."""

    def __init__(self):
        """Inicializa el almacén vacío."""
        self._gatos = {}

    def guardar(self, gato):
        """Guarda o sobreescribe un gato por su id."""
        self._gatos[gato.id_gato] = gato

    def obtener(self, id_gato):
        """Devuelve el gato con ese id o None si no existe."""
        return self._gatos.get(id_gato)

    def listar(self):
        """Devuelve una lista con todos los gatos."""
        return list(self._gatos.values())

    def quitar(self, id_gato):
        """Quitar el gato con ese id si existe."""
        if id_gato not in self._gatos:
            raise ValueError(f"No existe ningún gato con id {id_gato}.")
        del self._gatos[id_gato]