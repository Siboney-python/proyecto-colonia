"""
Dominio/repositorio_gatos: Contrato del repositorio de gatos de GestiCat.

Define las operaciones mínimas que cualquier implementación de almacenamiento
de gatos debe cumplir. Cualquier repositorio concreto debe heredar de esta
clase e implementar todos sus métodos.
"""


class RepositorioGatos:
    """Define la interfaz mínima que requiere el dominio para gestionar gatos."""

    def guardar(self, gato):
        """Guarda un gato en el repositorio."""
        raise NotImplementedError("guardar no implementado.")

    def obtener(self, id_gato):
        """Recupera un gato por su id. Devuelve None si no existe."""
        raise NotImplementedError("obtener no implementado.")

    def listar(self):
        """Devuelve una lista con todos los gatos del repositorio."""
        raise NotImplementedError("listar no implementado.")

    def quitar(self, id_gato):
        """Elimina un gato por su id del repositorio."""
        raise NotImplementedError("quitar no implementado.")