"""Prueba manual del contrato RepositorioGatos.

Verifica que la clase base lanza NotImplementedError en todos sus métodos.
Esto garantiza que cualquier implementación concreta (como RepositorioGatosMemoria o
futuros repositorios con persistencia real) que olvide implementar algún método 
recibirá un error claro en lugar de un comportamiento silencioso inesperado.
"""

from domain.repositorio_gatos import RepositorioGatos

repo = RepositorioGatos()

print("insertar lanza NotImplementedError")
try:
    repo.insertar(None)
except NotImplementedError as e:
    print("Error esperado:", e)

print("actualizar lanza NotImplementedError")
try:
    repo.actualizar(None)
except NotImplementedError as e:
    print("Error esperado:", e)

print("obtener lanza NotImplementedError")
try:
    repo.obtener("001")
except NotImplementedError as e:
    print("Error esperado:", e)

print("listar lanza NotImplementedError")
try:
    repo.listar()
except NotImplementedError as e:
    print("Error esperado:", e)

print("quitar lanza NotImplementedError")
try:
    repo.quitar("001")
except NotImplementedError as e:
    print("Error esperado:", e)