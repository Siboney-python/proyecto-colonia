"""
Dominio/colonia: Entidad Colonia del proyecto GestiCat.

Este módulo define la colonia felina como entidad central del programa,
agrupando los gatos bajo un responsable y gestionando su estado administrativo.

Reglas de negocio:
- El estado inicial siempre es SOLICITADA.
- Una colonia debe tener siempre un responsable asignado.
- Las colonias deben actualizarse cada 3 meses.
- No puede haber dos gatos con el mismo id.
- El censo solo cuenta gatos activos en la colonia.
"""

from enum import Enum
from datetime import date

from gesticat.domain.gato import Gato, Sexo, EstadoGato
from gesticat.domain.responsable import Responsable


# -- ENUMS --

class EstadoColonia(Enum):
    """Estado administrativo de la colonia en el programa municipal."""
    SOLICITADA = "Solicitada (Anexo I)"
    ACTIVA = "Activa"
    PENDIENTE = "Pendiente actualización (Anexo II)"
    BAJA = "Baja (Anexo III)"


# -- CONSTANTES --

# Estados que se consideran activos: gatos presentes en colonia o en acogida.
_ESTADOS_ACTIVOS = {EstadoGato.COL, EstadoGato.ACOG}


# -- CLASE PRINCIPAL --

class Colonia:
    """Representa una colonia felina con sus gatos y su responsable."""

    def __init__(self, nombre, responsable, repositorio):
        """Inicializa la colonia. El estado inicial siempre es SOLICITADA."""
        self.nombre = nombre
        self.responsable = responsable
        self._estado = EstadoColonia.SOLICITADA  # Regla: estado inicial fijo, no modificable desde fuera.
        self._ultima_actualizacion = date.today()
        self._repo = repositorio


    # -- PROPIEDADES --

    @property
    def nombre(self):
        """Nombre de la colonia."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Exige que el nombre no esté vacío ni tenga espacios laterales."""
        texto = valor or ""
        if texto != texto.strip():
            raise ValueError("El nombre de la colonia no puede tener espacios laterales.")
        if not texto.strip():
            raise ValueError("El nombre de la colonia no puede estar vacío.")
        self._nombre = texto

    @property
    def responsable(self):
        """Responsable de la colonia (PersonaFisica o Protectora)."""
        return self._responsable

    @responsable.setter
    def responsable(self, valor):
        """Exige que el responsable sea una instancia de Responsable o sus subclases."""
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
        """Cambia el estado administrativo de la colonia y registra la fecha.

        No permite volver al estado SOLICITADA una vez creada la colonia.
        """
        if not isinstance(nuevo_estado, EstadoColonia):
            raise TypeError("El estado debe ser una opción de EstadoColonia.")
        # El estado SOLICITADA es solo el estado inicial — no puede recuperarse.
        if nuevo_estado == EstadoColonia.SOLICITADA:
            raise ValueError("No se puede volver al estado SOLICITADA.")
        self._estado = nuevo_estado
        self._ultima_actualizacion = date.today()


    # -- CONTROL DE ACTUALIZACIÓN --

    def necesita_actualizacion(self):
        """Devuelve True si han pasado más de 3 meses desde la última actualización.

        Para calcular la fecha límite restamos 3 meses al día de hoy.
        Si el mes resultante es 0 o negativo, ajustamos retrocediendo un año
        y sumando 12 al mes para mantener una fecha válida.
        """
        hoy = date.today()
        mes = hoy.month - 3
        anio = hoy.year
        # Si al restar 3 meses el mes queda en 0 o negativo, retrocedemos un año.
        if mes <= 0:
            mes += 12
            anio -= 1
        limite = hoy.replace(year=anio, month=mes)
        return self._ultima_actualizacion < limite


    # -- GESTIÓN DE GATOS --

    def agregar_gato(self, gato: Gato):
        """Agrega un gato nuevo a la colonia.

        Lanza TypeError si el objeto no es un Gato.
        Lanza ValueError si ya existe un gato con el mismo id.
        """
        if not isinstance(gato, Gato):
            raise TypeError("Solo se permiten objetos Gato.")
        if self._repo.obtener(gato.id_gato) is not None:
            raise ValueError(f"Ya existe un gato con id {gato.id_gato}.")
        self._repo.insertar(gato)

    def actualizar_gato(self, gato: Gato):
        """Persiste los cambios de un gato ya existente en el repositorio.

        Necesario para repositorios con persistencia real (JSON, SQLite, API...)
        donde modificar el objeto en memoria no es suficiente para guardar el cambio.
        """
        self._repo.actualizar(gato)

    def quitar_gato(self, id_gato: str):
        """Quita un gato de la colonia por su id."""
        self._repo.quitar(id_gato)

    def buscar_por_id(self, id_gato: str):
        """Devuelve el gato con ese id o None si no existe."""
        return self._repo.obtener(id_gato)

    def buscar_por_nombre(self, nombre: str):
        """Devuelve una lista de gatos cuyo nombre coincida (sin distinguir mayúsculas)."""
        nombre_buscado = nombre.strip().lower()
        return [g for g in self._repo.listar() if g.nombre.lower() == nombre_buscado]


    # -- MÉTODOS PRIVADOS DE APOYO --

    def _gatos_activos(self):
        """Devuelve la lista de gatos con estado activo (en colonia o en acogida)."""
        return [g for g in self._repo.listar() if g.estado in _ESTADOS_ACTIVOS]

    def listar_sin_esterilizar(self):
        """Devuelve los gatos activos que no están esterilizados."""
        return [g for g in self._gatos_activos() if not g.esterilizado]


    # -- REPORTES --

    def reporte_censo(self):
        """Devuelve estadísticas de población activa de la colonia."""
        gatos = self._gatos_activos()
        total = len(gatos)
        machos = sum(1 for g in gatos if g.sexo == Sexo.MACHO)
        hembras = sum(1 for g in gatos if g.sexo == Sexo.HEMBRA)
        desconocidos = sum(1 for g in gatos if g.sexo == Sexo.DESCONOCIDO)
        esterilizados = sum(1 for g in gatos if g.esterilizado)
        no_esterilizados = total - esterilizados
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
            "total_gatos": len(self._gatos_activos()),
        }
