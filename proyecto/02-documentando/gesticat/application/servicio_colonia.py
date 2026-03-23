"""
Aplicación/servicio_colonia: Casos de uso del proyecto GestiCat.

Este módulo coordina las operaciones entre la presentación y el dominio.
No contiene lógica de negocio — esa responsabilidad es del dominio.
"""

from domain.colonia import Colonia, EstadoColonia
from domain.gato import Gato, EstadoGato, Sexo
from domain.responsable import Responsable


class ServicioColonia:
    """Coordina los casos de uso de la aplicación GestiCat."""

    def __init__(self, colonia: Colonia):
        """Inicializa el servicio con una colonia."""
        self._colonia = colonia

    # -- GATOS --

    def registrar_gato(self, id_gato, nombre, color, sexo, estado,
                       clinica_veterinaria, esterilizado, fecha_registro):
        """Crea un gato y lo añade a la colonia."""
        gato = Gato(id_gato, nombre, color, sexo, estado,
                    clinica_veterinaria, esterilizado, fecha_registro)
        self._colonia.agregar_gato(gato)

    def quitar_gato(self, id_gato):
        """Elimina un gato de la colonia por su id."""
        self._colonia.quitar_gato(id_gato)

    def actualizar_estado_gato(self, id_gato, nuevo_estado: EstadoGato):
        """Actualiza el estado de un gato existente."""
        gato = self._colonia.buscar_por_id(id_gato)
        if gato is None:
            raise ValueError(f"No existe ningún gato con id {id_gato}.")
        gato.estado = nuevo_estado

    def actualizar_esterilizacion_gato(self, id_gato, esterilizado: bool,
                                        clinica_veterinaria=None):
        """Actualiza el estado de esterilización de un gato."""
        gato = self._colonia.buscar_por_id(id_gato)
        if gato is None:
            raise ValueError(f"No existe ningún gato con id {id_gato}.")
        # Si se esteriliza, actualizamos también la clínica si se proporciona.
        if clinica_veterinaria and not gato.clinica_veterinaria:
            gato.clinica_veterinaria = clinica_veterinaria
        gato.esterilizado = esterilizado

    def listar_sin_esterilizar(self):
        """Devuelve la lista de gatos activos no esterilizados."""
        return self._colonia.listar_sin_esterilizar()

    # -- COLONIA --

    def asignar_responsable(self, responsable: Responsable):
        """Asigna un nuevo responsable a la colonia."""
        self._colonia.responsable = responsable

    def tramitar_anexo(self, nuevo_estado: EstadoColonia):
        """Tramita un cambio de estado administrativo de la colonia."""
        self._colonia.tramitar_anexo(nuevo_estado)

    # -- REPORTES --

    def reporte_censo(self):
        """Devuelve las estadísticas de población de la colonia."""
        return self._colonia.reporte_censo()

    def reporte_colonia(self):
        """Devuelve la información general de la colonia."""
        return self._colonia.reporte_colonia()