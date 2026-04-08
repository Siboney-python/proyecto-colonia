"""
Aplicación/servicio_colonia: Casos de uso del proyecto GestiCat.

Este módulo coordina las operaciones entre la presentación y el dominio,
orquestando los casos de uso sin contener lógica de negocio — esa
responsabilidad pertenece exclusivamente al dominio.
"""

from gesticat.domain.colonia import Colonia, EstadoColonia
from gesticat.domain.gato import Gato, EstadoGato, Sexo
from gesticat.domain.responsable import Responsable


class ServicioColonia:
    """Coordina los casos de uso de la aplicación GestiCat."""

    def __init__(self, colonia: Colonia):
        """Inicializa el servicio con una colonia."""
        self._colonia = colonia

    # -- GATOS --

    def registrar_gato(self, id_gato, nombre, color, sexo, estado,
                       clinica_veterinaria, esterilizado, fecha_registro=None):
        """Crea un gato y lo añade a la colonia.

        Si no se indica fecha_registro, se usa la fecha de hoy.
        Pasar una fecha explícita permite registrar gatos con fechas históricas
        en migraciones desde registros en papel.
        """
        gato = Gato(id_gato, nombre, color, sexo, estado,
                    clinica_veterinaria, esterilizado, fecha_registro)
        self._colonia.agregar_gato(gato)

    def quitar_gato(self, id_gato):
        """Elimina un gato de la colonia por su id."""
        self._colonia.quitar_gato(id_gato)

    def actualizar_estado_gato(self, id_gato, nuevo_estado: EstadoGato):
        """Actualiza el estado de un gato existente y lo persiste en el repositorio."""
        gato = self._colonia.buscar_por_id(id_gato)
        if gato is None:
            raise ValueError(f"No existe ningún gato con id {id_gato}.")
        gato.estado = nuevo_estado
        # Llamamos a actualizar() para que repositorios con persistencia real
        # reflejen el cambio. En memoria no es estrictamente necesario porque
        # trabajamos con referencias, pero es correcto y consistente hacerlo.
        self._colonia.actualizar_gato(gato)

    def actualizar_esterilizacion_gato(self, id_gato, esterilizado: bool,
                                        clinica_veterinaria=None):
        """Marca un gato como esterilizado y lo persiste en el repositorio.

        En la práctica siempre se llama con esterilizado=True — el dominio
        impide revertir una esterilización una vez aplicada.
        Si se indica clinica_veterinaria y el gato no tenía una asignada, se actualiza.
        """
        gato = self._colonia.buscar_por_id(id_gato)
        if gato is None:
            raise ValueError(f"No existe ningún gato con id {id_gato}.")
        if clinica_veterinaria and not gato.clinica_veterinaria:
            gato.clinica_veterinaria = clinica_veterinaria
        gato.esterilizado = esterilizado
        self._colonia.actualizar_gato(gato)

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