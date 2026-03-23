"""Prueba manual del contrato RepositorioGatos."""

from domain.repositorio_gatos import RepositorioGatos

repo = RepositorioGatos()

print("guardar lanza NotImplementedError")
try:
    repo.guardar(None)
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