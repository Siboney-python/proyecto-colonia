"""
Infraestructura/repositorio_gatos_sqlite: Implementación SQLite del repositorio de gatos.

Implementa el contrato RepositorioGatos usando SQLite para persistencia real.
Los datos sobreviven entre ejecuciones del programa, a diferencia del repositorio
en memoria. Traduce las excepciones técnicas de sqlite3 en excepciones de dominio
para que las capas superiores no dependan del motor de base de datos.
"""

import sqlite3
from datetime import date

from gesticat.domain.gato import Gato, Sexo, EstadoGato
from gesticat.domain.repositorio_gatos import RepositorioGatos
from gesticat.infrastructure.errores import (
    GatoNoEncontradoError, GatoYaExisteError, ErrorPersistencia)


class RepositorioGatosSQLite(RepositorioGatos):
    """Repositorio de gatos utilizando SQLite para persistencia."""
    
    def __init__(self, ruta_bd="gesticat.db", colonia_nombre="Colonia Sur"):
        self._ruta_bd = ruta_bd
        self._colonia_nombre = colonia_nombre

    def _conectar(self):
        """Crea una conexión con integridad referencial activada."""
        conn = sqlite3.connect(self._ruta_bd)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def insertar(self, gato: Gato):
        """Inserta un nuevo gato a la base de datos."""
        conn = self._conectar()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO gatos (
                   id_gato, colonia_nombre, nombre, color, sexo, estado,       clinica_veterinaria, esterilizado, fecha_registro)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                    gato.id_gato,
                    self._colonia_nombre,
                    gato.nombre,
                    gato.color,
                    gato.sexo.value,    # enum -> str
                    gato.estado.name,  # enum -> str
                    gato.clinica_veterinaria,
                    1 if gato.esterilizado else 0,  # bool -> int
                    gato.fecha_registro.isoformat()
                ))
        except sqlite3.IntegrityError as e:
            raise GatoYaExisteError(
                f"Ya existe un gato con id '{gato.id_gato}'"
            ) from e
        except sqlite3.OperationalError as e:
            raise ErrorPersistencia(f"Error al insertar el gato: {e}") from e
        finally:
            conn.close()


    def obtener(self, id_gato):
        """Recupera un gato por su id. Devuelve None si no existe."""
        conn = self._conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id_gato, nombre, color, sexo, estado,
                          clinica_veterinaria, esterilizado, fecha_registro
                   FROM gatos WHERE id_gato = ?""",
                (id_gato,),
            )
            fila = cursor.fetchone()
            if fila is None:
                return None  # Respeta el contrato actual del repo en memoria
            return self._fila_a_gato(fila)
        except sqlite3.OperationalError as e:
            raise ErrorPersistencia(f"Error al obtener el gato: {e}") from e
        finally:
            conn.close()


    def _fila_a_gato(self, fila):
        """Convierte una fila de la BD en un objeto Gato."""
        (id_gato, nombre, color, sexo_str, estado_str,
         clinica, esterilizado, fecha_str) = fila
        return Gato(
            id_gato=id_gato,
            nombre=nombre,
            color=color,
            sexo=Sexo(sexo_str),            # "M" -> Sexo.MACHO
            estado=EstadoGato[estado_str],  # "COL" -> EstadoGato.COL
            clinica_veterinaria=clinica,
            esterilizado=bool(esterilizado),
            fecha_registro=date.fromisoformat(fecha_str),
        )

    def actualizar(self, gato):
        """Actualiza un gato existente en la base de datos."""
        conn = self._conectar()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    """UPDATE gatos SET nombre = ?, color = ?, sexo = ?, estado = ?, clinica_veterinaria = ?, esterilizado = ?, fecha_registro = ?
                    WHERE id_gato = ?""", (
                    gato.nombre,
                    gato.color,
                    gato.sexo.value,    # enum -> str
                    gato.estado.name,  # enum -> str
                    gato.clinica_veterinaria,
                    1 if gato.esterilizado else 0,  # bool -> int
                    gato.fecha_registro.isoformat(),
                    gato.id_gato
                ))
                if cursor.rowcount == 0:
                    raise GatoNoEncontradoError(
                        f"No existe ningún gato con id '{gato.id_gato}' para actualizar."
                    )
        except sqlite3.OperationalError as e:
            raise ErrorPersistencia(f"Error al actualizar el gato: {e}") from e
        finally:
            conn.close()

    def listar(self):
        """Devuelve una lista de todos los gatos en la base de datos."""
        conn = self._conectar()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id_gato, nombre, color, sexo, estado,
                            clinica_veterinaria, esterilizado, fecha_registro
                    FROM gatos WHERE colonia_nombre = ?""",
                    (self._colonia_nombre,),
                )
                filas = cursor.fetchall()
                return [self._fila_a_gato(fila) for fila in filas]
        except sqlite3.OperationalError as e:
            raise ErrorPersistencia(f"Error al listar los gatos: {e}") from e
        finally:
            conn.close()

    def quitar(self, id_gato):
        """Elimina un gato de la base de datos."""
        conn = self._conectar()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    """DELETE FROM gatos WHERE id_gato = ?""",
                    (id_gato,),
                )
                if cursor.rowcount == 0:
                    raise GatoNoEncontradoError(
                        f"No existe ningún gato con id '{id_gato}' para eliminar."
                    )
        except sqlite3.OperationalError as e:
            raise ErrorPersistencia(f"Error al eliminar el gato: {e}") from e
        finally:
            conn.close()