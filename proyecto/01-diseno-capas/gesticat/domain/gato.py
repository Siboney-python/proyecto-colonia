"""
Dominio/gato: Entidad Gato del proyecto GestiCat.

Este módulo define los gatos individuales del programa de gestión de colonias felinas.

Reglas de negocio:
- No puede estar esterilizado sin clínica veterinaria asignada.
- No puede tener fecha de esterilización si no está esterilizado.
- No puede tener marca de esterilización si no está esterilizado.
"""

from enum import Enum
from datetime import date

# -- ENUMS: Con los Enum defino las opciones cerradas. --

class Sexo(Enum):
    """Sexo del gato."""    
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
    # TODO: Registrar fecha cuando el estado pase a ADOP, FALL o DESA.

# TODO: 
# class MarcaEsterilizacion(Enum):
#    """Marca física de esterilización en las orejas."""
#    SIN_MARCA = "Sin marcar"
#    IZQUIERDA = "Oreja izquierda"
#    DERECHA = "Oreja derecha"

# -- CLASE PRINCIPAL --

class Gato:
    """Representa un gato individual dentro del programa de colonias felinas."""

    def __init__(self, id_gato, nombre, color,
                 sexo: Sexo, estado: EstadoGato, 
                 clinica_veterinaria,  
                 esterilizado, 
                 #marca_esterilizacion,
                 fecha_registro):
        """Inicializa un nuevo gato."""
        self.id_gato = id_gato
        self.nombre = nombre
        self.color = color
        self.sexo = sexo
        self.estado = estado
        self.clinica_veterinaria = clinica_veterinaria
        self.esterilizado = esterilizado
        self.fecha_registro = fecha_registro
        
    # -- PROPIEDADES (GETTERS) --

    @property
    def id_gato(self):
        """Identificador único del gato."""
        return self._id_gato
    
    @id_gato.setter
    def id_gato(self, valor):
        """Valida que el código sean 3 cifras."""
        dato = (valor or "").strip().upper()
        if len(dato) != 3:
            raise ValueError("Codigo invalido.")
        if not dato.isdigit():
            raise ValueError("Codigo invalido.")
        self._id_gato = dato
    
    @property
    def nombre(self):
        """Nombre del gato."""
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        """Valida nombre no vacio y sin espacios laterales."""
        texto = valor or ""
        if not texto.strip():
            raise ValueError("El nombre no puede estar vacio.")
        if texto != texto.strip():
            raise ValueError("El nombre no puede tener espacios laterales.")
        self._nombre = texto
    
    @property
    def color(self):
        """Color o patrón del gato."""
        return self._color
    
    @color.setter
    def color(self, valor):
        """Valida color no vacio y sin espacios laterales."""
        texto = valor or ""
        if not texto.strip():
            raise ValueError("El color no puede estar vacio.")
        if texto != texto.strip():
            raise ValueError("El color no puede tener espacios laterales.")
        self._color = texto

    @property
    def sexo(self):
        """Sexo biológico del gato."""
        return self._sexo
    
    @sexo.setter
    def sexo(self, dato):
        if not isinstance(dato, Sexo):
            raise TypeError(f"El sexo debe ser una opción de la clase Sexo") 
        self._sexo = dato

    @property
    def estado(self):
        """Estado actual del gato."""
        return self._estado
    
    @estado.setter
    def estado(self, dato):
        if not isinstance(dato, EstadoGato):
            raise TypeError(f"El estado debe ser una opción de la clase EstadoGato") 
        self._estado = dato
    
    @property
    def clinica_veterinaria(self):
        """Clínica donde se esterilizó."""
        return self._clinica_veterinaria
    
    @clinica_veterinaria.setter
    def clinica_veterinaria(self, valor):
        """Valida clinica_veterinaria no vacio y sin espacios laterales."""
        if valor is None:
            self._clinica_veterinaria = None
            return
        texto = valor.strip()
        if not texto:
            raise ValueError("Clinica_veterinaria no puede estar vacio.")
        if valor != texto:
            raise ValueError("Clinica_veterinaria no puede tener espacios laterales.")
        self._clinica_veterinaria = texto
    
    @property
    def esterilizado(self):
        """Si el gato está esterilizado."""
        return self._esterilizado

    @esterilizado.setter
    def esterilizado(self, valor):
        """Valida que sea booleano y que cumpla las reglas de negocio."""
        if not isinstance(valor, bool):
            raise TypeError("Esterilizado debe ser True o False.")
        # Regla: si está esterilizado, debe tener clínica asignada.
        if valor and not self._clinica_veterinaria:
            raise ValueError("Un gato esterilizado debe tener clínica veterinaria asignada.")
        self._esterilizado = valor

    @property
    def fecha_registro(self):
        """Fecha de alta en el sistema."""
        return self._fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor):
        """Valida formato, que sea un objeto date y no futuro."""
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



