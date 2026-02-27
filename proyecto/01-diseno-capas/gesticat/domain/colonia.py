"""
Dominio/colonia: Entidad Colonia del proyecto GestiCat.

Reglas de negocio:
- El estado inicial siempre es SOLICITADA.
- Una colonia debe tener siempre un responsable asignado.
- Las colonias deben actualizarse cada 3 meses.
- No puede haber dos gatos con el mismo id en la misma colonia.
"""

from enum import Enum
from datetime import date

from domain.gato import Gato, Sexo
from domain.responsable import Responsable, PersonaFisica, Protectora

# -- ENUMS --

class EstadoColonia(Enum):
    """Estado administrativo de la colonia en el programa municipal."""
    SOLICITADA = "Solicitada (Anexo I)"
    ACTIVA = "Activa"
    PENDIENTE = "Pendiente actualización (Anexo II)"
    BAJA = "Baja (Anexo III)"


# -- CLASE PRINCIPAL --

class Colonia:
    """Representa una colonia felina con sus gatos y su responsable."""

    def __init__(self, nombre, responsable):
        """Inicializa la colonia. El estado inicial siempre es SOLICITADA."""
        self.nombre = nombre
        self.responsable = responsable
        self._estado = EstadoColonia.SOLICITADA  # Regla: estado inicial fijo.
        self._ultima_actualizacion = date.today()
        self._gatos = {}

    # -- PROPIEDADES --

    @property
    def nombre(self):
        """Nombre de la colonia."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        texto = (valor or "").strip()
        if not texto:
            raise ValueError("El nombre de la colonia no puede estar vacío.")
        self._nombre = texto

    @property
    def responsable(self):
        """Responsable de la colonia (Persona o Protectora)."""
        return self._responsable

    @responsable.setter
    def responsable(self, valor):
        if not isinstance(valor, Responsable):
            raise TypeError("El responsable debe ser una instancia de PersonaFisica o Protectora.")
        self._responsable = valor

    @property
    def estado(self):
        """Estado administrativo de la colonia."""
        return self._estado

    @property
    def ultima_actualizacion(self):
        """Fecha de la última actualización de la colonia."""
        return self._ultima_actualizacion

    # -- TRAMITAR ANEXO --

    def tramitar_anexo(self, nuevo_estado: EstadoColonia):
        """Cambia el estado administrativo de la colonia."""
        if not isinstance(nuevo_estado, EstadoColonia):
            raise TypeError("El estado debe ser una opción de EstadoColonia.")
        # No puede volver a SOLICITADA una vez creada.
        if nuevo_estado == EstadoColonia.SOLICITADA:
            raise ValueError("No se puede volver al estado SOLICITADA.")
        self._estado = nuevo_estado
        self._ultima_actualizacion = date.today()

    # -- CONTROL DE ACTUALIZACIÓN --

    def necesita_actualizacion(self):
        """Devuelve True si han pasado más de 3 meses desde la última actualización."""
        hoy = date.today()
        mes = hoy.month - 3
        anio = hoy.year
        if mes <= 0:
            mes += 12
            anio -= 1
        limite = hoy.replace(year=anio, month=mes)
        return self._ultima_actualizacion < limite

    # -- GESTIÓN DE GATOS --

    def agregar_gato(self, gato: Gato):
        """Agrega un gato a la colonia."""
        if not isinstance(gato, Gato):
            raise ValueError("Solo se permiten objetos Gato.")
        if gato.id_gato in self._gatos:
            raise ValueError(f"Ya existe un gato con id {gato.id_gato}.")
        self._gatos[gato.id_gato] = gato

    def eliminar_gato(self, id_gato: str):
        """Elimina un gato de la colonia por su id."""
        if id_gato not in self._gatos:
            raise ValueError(f"No existe ningún gato con id {id_gato}.")
        del self._gatos[id_gato]

    def buscar_por_id(self, id_gato: str):
        """Devuelve el gato con ese id o None si no existe."""
        return self._gatos.get(id_gato)

    def buscar_por_nombre(self, nombre: str):
        """Devuelve una lista de gatos cuyo nombre coincida (sin distinguir mayúsculas)."""
        nombre = nombre.strip().lower()
        return [g for g in self._gatos.values() if g.nombre.lower() == nombre]

    def listar_sin_esterilizar(self):
        """Devuelve una lista de gatos que no están esterilizados."""
        return [g for g in self._gatos.values() if not g.esterilizado]


    # -- REPORTES --

    def reporte_censo(self):
        """Devuelve estadísticas de población de la colonia."""
        gatos = list(self._gatos.values())
        total = len(gatos)
        machos = sum(1 for g in gatos if g.sexo == Sexo.MACHO)
        hembras = sum(1 for g in gatos if g.sexo == Sexo.HEMBRA)
        desconocidos = sum(1 for g in gatos if g.sexo == Sexo.DESCONOCIDO)
        esterilizados = sum(1 for g in gatos if g.esterilizado)
        no_esterilizados = total - esterilizados
        # TODO: Añadir desglose de esterilizados por sexo.
        return {
            "total": total,
            "machos": machos,
            "hembras": hembras,
            "desconocidos": desconocidos,
            "esterilizados": esterilizados,
            "no_esterilizados": no_esterilizados,
        }

    def reporte_colonia(self):
        """Devuelve la información general de la colonia."""
        return {
            "nombre": self._nombre,
            "responsable": str(self._responsable),
            "estado": self._estado.value,
            "ultima_actualizacion": self._ultima_actualizacion.strftime("%d/%m/%Y"),
            "necesita_actualizacion": self.necesita_actualizacion(),
            "total_gatos": len(self._gatos),
        }
