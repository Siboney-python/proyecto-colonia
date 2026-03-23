"""
Dominio/responsable: Entidades Responsable del proyecto GestiCat.

Este módulo define los responsables de las colonias felinas, que pueden ser
personas físicas (voluntarios) o protectoras (asociaciones).

Reglas de negocio:
- Todo responsable debe tener nombre, teléfono, email e identificación.
- El email debe tener formato válido.
- El teléfono debe tener exactamente 9 dígitos.
- Las personas físicas deben ser mayores de 18 años.
"""

from abc import ABC
from datetime import date
import re


# -- CLASE PADRE --

class Responsable(ABC):
    """
    Clase base abstracta para PersonaFisica y Protectora.

    Agrupa los datos de contacto comunes a cualquier responsable de una colonia.
    Al heredar de ABC, Python impide instanciarla directamente — usar sus subclases.

    Nota: no define __str__ porque cada subclase muestra datos distintos
    (DNI para personas físicas, CIF y número de registro para protectoras).
    """

    def __init__(self, nombre, telefono, email, identificacion):
        """Inicializa los datos comunes de cualquier responsable."""
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.identificacion = identificacion


    # -- PROPIEDADES --

    @property
    def nombre(self):
        """Nombre del responsable."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Elimina espacios laterales y exige que el nombre no quede vacío."""
        texto = (valor or "").strip()
        if not texto:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = texto

    @property
    def telefono(self):
        """Teléfono de contacto."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        """Exige exactamente 9 dígitos numéricos."""
        dato = (valor or "").strip()
        if not dato.isdigit() or len(dato) != 9:
            raise ValueError("El teléfono debe tener exactamente 9 dígitos.")
        self._telefono = dato

    @property
    def email(self):
        """Correo electrónico de contacto."""
        return self._email

    @email.setter
    def email(self, valor):
        """Valida el formato del email con una expresión regular básica."""
        dato = (valor or "").strip()
        # Comprobación mínima de formato: texto@texto.dominio
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", dato):
            raise ValueError("El email no tiene un formato válido.")
        self._email = dato

    @property
    def identificacion(self):
        """DNI, NIF u otro identificador del responsable."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        """Elimina espacios laterales, normaliza a mayúsculas y exige que no quede vacío."""
        dato = (valor or "").strip().upper()
        if not dato:
            raise ValueError("La identificación no puede estar vacía.")
        self._identificacion = dato


# -- SUBCLASES --

class PersonaFisica(Responsable):
    """
    Responsable individual (voluntaria).

    Representa a una persona física que actúa como responsable de colonias.
    Debe ser mayor de edad (18 años).
    """

    def __init__(self, nombre, telefono, email, identificacion, fecha_nacimiento):
        """Inicializa una persona física con sus datos personales."""
        super().__init__(nombre, telefono, email, identificacion)
        self.fecha_nacimiento = fecha_nacimiento

    @property
    def fecha_nacimiento(self):
        """Fecha de nacimiento de la persona."""
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, valor):
        """Acepta string dd/mm/aaaa o un objeto date.

        Reglas:
        - No puede ser una fecha futura.
        - La persona debe ser mayor de edad (18 años cumplidos).
        """
        if isinstance(valor, str):
            try:
                partes = valor.split("/")
                valor = date(int(partes[2]), int(partes[1]), int(partes[0]))
            except (ValueError, IndexError):
                raise ValueError("La fecha debe tener formato dd/mm/aaaa.")
        if not isinstance(valor, date):
            raise TypeError("La fecha debe ser un objeto date o string dd/mm/aaaa.")
        if valor > date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura.")
        # Calculamos la fecha límite restando 18 años al día de hoy.
        hoy = date.today()
        edad_minima = hoy.replace(year=hoy.year - 18)
        if valor > edad_minima:
            raise ValueError("El responsable debe ser mayor de edad.")
        self._fecha_nacimiento = valor

    def __str__(self):
        """Representación legible de la persona física."""
        return f"{self._nombre} - DNI: {self._identificacion}"


class Protectora(Responsable):
    """
    Responsable jurídico (asociación/protectora).

    Representa a una entidad legal que actúa como responsable de colonias felinas.
    """

    def __init__(self, nombre, telefono, email, identificacion, numero_registro):
        """Inicializa una protectora con su número de registro."""
        super().__init__(nombre, telefono, email, identificacion)
        self.numero_registro = numero_registro

    @property
    def numero_registro(self):
        """Número de registro oficial de la asociación."""
        return self._numero_registro

    @numero_registro.setter
    def numero_registro(self, valor):
        """Elimina espacios laterales, normaliza a mayúsculas y exige que no quede vacío."""
        dato = (valor or "").strip().upper()
        if not dato:
            raise ValueError("El número de registro no puede estar vacío.")
        self._numero_registro = dato

    def __str__(self):
        """Representación legible de la protectora."""
        return f"{self._nombre} - CIF: {self._identificacion} - Reg: {self._numero_registro}"