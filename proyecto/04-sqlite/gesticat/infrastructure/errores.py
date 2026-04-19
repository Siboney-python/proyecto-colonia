"""
Infraestructura/errores: Excepciones de dominio para la capa de persistencia de GestiCat.

Este módulo define excepciones con significado de negocio que cualquier implementación
de repositorio debe lanzar en lugar de excepciones técnicas del motor de persistencia
(sqlite3.IntegrityError, psycopg2.IntegrityError, etc.), para que las capas superiores
(aplicación y presentación) no dependan del motor concreto que se esté usando.

Organización:
- ErrorRepositorio: clase base para todas las excepciones de este módulo.
- Excepciones específicas por entidad (Gato, Colonia, Responsable) y tipo de error
  (ya existe, no encontrado).
- ErrorPersistencia: para errores inesperados del motor de base de datos.
"""


class ErrorRepositorio(Exception):
    """Clase base para todas las excepciones del repositorio."""
    pass

class GatoYaExisteError(ErrorRepositorio):
    """Se lanza cuando se intenta insertar un gato con id duplicado."""
    pass

class GatoNoEncontradoError(ErrorRepositorio):
    """Se lanza cuando se intenta recuperar un gato inexistente."""
    pass

class ErrorPersistencia(ErrorRepositorio):
    """Se lanza para errores inesperados de la base de datos."""
    pass

class ColoniaYaExisteError(ErrorRepositorio):
    """Se lanza cuando se intenta insertar una colonia con nombre duplicado."""
    pass

class ColoniaNoEncontradaError(ErrorRepositorio):
    """Se lanza cuando se intenta recuperar una colonia inexistente."""
    pass

class ResponsableYaExisteError(ErrorRepositorio):
    """Se lanza cuando se intenta insertar un responsable con identificacion duplicada."""
    pass

class ResponsableNoEncontradoError(ErrorRepositorio):
    """Se lanza cuando se intenta recuperar un responsable inexistente."""
    pass