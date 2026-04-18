"""Excepciones de dominio para el repositorio de persistencia."""


class ErrorRepositorio(Exception):
    """Excepción base para errores de persistencia."""
    pass


class ProductoYaExisteError(ErrorRepositorio):
    """Se lanza al insertar un producto con código duplicado."""
    pass


class ProductoNoEncontradoError(ErrorRepositorio):
    """Se lanza al buscar un producto que no existe."""
    pass


class ErrorPersistencia(ErrorRepositorio):
    """Se lanza ante fallos inesperados del motor de base de datos."""
    pass