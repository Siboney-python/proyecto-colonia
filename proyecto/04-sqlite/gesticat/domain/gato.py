"""
Dominio/gato: Entidad Gato del proyecto GestiCat.

Este módulo define los gatos individuales del programa de gestión de colonias felinas.

Reglas de negocio:
- No puede estar esterilizado sin clínica veterinaria asignada.
- No puede revertirse la esterilización una vez aplicada.
"""

from enum import Enum
from datetime import date


# -- ENUMS --

class Sexo(Enum):
    """Sexo biológico del gato."""
    HEMBRA = "H"
    MACHO = "M"
    DESCONOCIDO = "?"


class EstadoGato(Enum):
    """Estado actual del gato en el programa."""
    COL = "En colonia"
    ACOG = "En acogida"
    ADOP = "Adoptado"
    FALL = "Fallecido"
    DESA = "Desaparecido"
    

# -- CLASE PRINCIPAL --

class Gato:
    """Representa un gato individual dentro del programa de colonias felinas."""

    def __init__(self, id_gato, nombre, color,
                 sexo: Sexo, estado: EstadoGato,
                 clinica_veterinaria,
                 esterilizado,
                 fecha_registro=None):
        """Inicializa un nuevo gato con todos sus datos.

        Si no se indica fecha_registro, se usa la fecha de hoy. Esto permite
        tanto el uso diario (sin indicar fecha) como migraciones desde registros
        en papel, pasando la fecha histórica explícitamente.
        """
        self.id_gato = id_gato
        self.nombre = nombre
        self.color = color
        self.sexo = sexo
        self.estado = estado
        self.clinica_veterinaria = clinica_veterinaria
        self.esterilizado = esterilizado
        self.fecha_registro = fecha_registro


    # -- PROPIEDADES --

    @property
    def id_gato(self):
        """Identificador único del gato. Debe ser exactamente 3 dígitos."""
        return self._id_gato

    @id_gato.setter
    def id_gato(self, valor):
        """Exige exactamente 3 dígitos numéricos."""
        dato = (valor or "").strip().upper()
        if len(dato) != 3 or not dato.isdigit():
            raise ValueError("El ID debe ser exactamente 3 dígitos numéricos.")
        self._id_gato = dato

    @property
    def nombre(self):
        """Nombre del gato."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Exige que el nombre no esté vacío ni tenga espacios laterales."""
        texto = valor or ""
        if not texto.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if texto != texto.strip():
            raise ValueError("El nombre no puede tener espacios laterales.")
        self._nombre = texto

    @property
    def color(self):
        """Color o patrón del pelaje del gato."""
        return self._color

    @color.setter
    def color(self, valor):
        """Exige que el color no esté vacío ni tenga espacios laterales."""
        texto = valor or ""
        if not texto.strip():
            raise ValueError("El color no puede estar vacío.")
        if texto != texto.strip():
            raise ValueError("El color no puede tener espacios laterales.")
        self._color = texto

    @property
    def sexo(self):
        """Sexo biológico del gato."""
        return self._sexo

    @sexo.setter
    def sexo(self, dato):
        """Exige que el valor sea una opción válida del enum Sexo."""
        if not isinstance(dato, Sexo):
            raise TypeError("El sexo debe ser una opción de la clase Sexo.")
        self._sexo = dato

    @property
    def estado(self):
        """Estado actual del gato en el programa."""
        return self._estado

    @estado.setter
    def estado(self, dato):
        """Exige que el valor sea una opción válida del enum EstadoGato."""
        if not isinstance(dato, EstadoGato):
            raise TypeError("El estado debe ser una opción de la clase EstadoGato.")
        self._estado = dato

    @property
    def clinica_veterinaria(self):
        """Clínica donde se realizó la esterilización. Puede ser None."""
        return self._clinica_veterinaria

    @clinica_veterinaria.setter
    def clinica_veterinaria(self, valor):
        """Acepta None o un nombre no vacío sin espacios laterales."""
        if valor is None:
            self._clinica_veterinaria = None
            return
        texto = valor.strip()
        if not texto:
            raise ValueError("La clínica veterinaria no puede estar vacía.")
        if valor != texto:
            raise ValueError("La clínica veterinaria no puede tener espacios laterales.")
        self._clinica_veterinaria = texto

    @property
    def esterilizado(self):
        """Indica si el gato está esterilizado."""
        return self._esterilizado

    @esterilizado.setter
    def esterilizado(self, valor):
        """Aplica las reglas de negocio sobre la esterilización.

        Reglas:
        - No se puede revertir: un gato esterilizado no puede pasar a no esterilizado.
        - Requiere clínica: si se marca como esterilizado, debe tener clínica asignada.
        """
        if not isinstance(valor, bool):
            raise TypeError("Esterilizado debe ser True o False.")
        # Comprobamos si ya existe el atributo para evitar fallar en la primera asignación (__init__).
        if hasattr(self, '_esterilizado') and self._esterilizado and not valor:
            raise ValueError("Un gato esterilizado no puede pasar a no esterilizado.")
        if valor and not self._clinica_veterinaria:
            raise ValueError("Un gato esterilizado debe tener clínica veterinaria asignada.")
        self._esterilizado = valor

    @property
    def fecha_registro(self):
        """Fecha de alta del gato en el sistema."""
        return self._fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor):
        """Acepta string dd/mm/aaaa, un objeto date o None (usa fecha de hoy).

        El valor por defecto None permite el uso diario sin indicar fecha,
        y pasar una fecha explícita facilita migraciones desde registros en papel.
        """
        # Si no se indica fecha, se usa hoy. Útil para el uso diario.
        if valor is None:
            self._fecha_registro = date.today()
            return
        if isinstance(valor, str):
            try:
                partes = valor.split("/")
                valor = date(int(partes[2]), int(partes[1]), int(partes[0]))
            except (ValueError, IndexError):
                raise ValueError("La fecha debe tener formato dd/mm/aaaa.")
        if not isinstance(valor, date):
            raise TypeError("La fecha de registro debe ser un objeto date.")
        if valor > date.today():
            raise ValueError("La fecha de registro no puede ser futura.")
        self._fecha_registro = valor