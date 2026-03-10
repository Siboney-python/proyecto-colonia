# domain/repositorio_gatos.py

class RepositorioGatos:
    """
    Contrato para el repositorio de gatos.
    
    Define las operaciones mínimas que cualquier implementación
    de almacenamiento de gatos debe cumplir.
    """

    def guardar(self, gato):
        """Guarda un gato en el repositorio."""
        raise NotImplementedError("guardar no implementado.")

    def obtener(self, id_gato):
        """Recupera un gato por su id. Devuelve None si no existe."""
        raise NotImplementedError("obtener no implementado.")

    def listar(self):
        """Devuelve una lista con todos los gatos."""
        raise NotImplementedError("listar no implementado.")

    def quitar(self, id_gato):
        """Quita un gato por su id."""
        raise NotImplementedError("quitar no implementado.")