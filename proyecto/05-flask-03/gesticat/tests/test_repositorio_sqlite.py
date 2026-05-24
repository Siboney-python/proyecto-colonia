"""
Test/test_repositorio_sqlite: Pruebas unitarias para RepositorioGatosSQLite.
"""

import sqlite3
import unittest
from pathlib import Path
from datetime import date

from gesticat.domain.gato import Gato, Sexo, EstadoGato
from gesticat.infrastructure.repositorio_gatos_sqlite import RepositorioGatosSQLite
from gesticat.infrastructure.errores import (
    GatoYaExisteError,
    GatoNoEncontradoError,
)

class TestRepositorioSQLite(unittest.TestCase):
    """Pruebas unitarias para RepositorioGatosSQLite."""

    BD_TEST = Path("test_gesticat.db")

    def setUp(self):
        self.BD_TEST.unlink(missing_ok=True)

        conn = sqlite3.connect(self.BD_TEST)
        cursor = conn.cursor()
        
        cursor.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS responsables (
            identificacion TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            tipo TEXT NOT NULL,
            fecha_nacimiento TEXT,
            numero_registro TEXT
        );

        CREATE TABLE IF NOT EXISTS colonias (
            nombre TEXT PRIMARY KEY,
            responsable_identificacion TEXT NOT NULL,
            estado TEXT NOT NULL,
            ultima_actualizacion TEXT NOT NULL,
            FOREIGN KEY (responsable_identificacion) REFERENCES responsables(identificacion)
        );

        CREATE TABLE IF NOT EXISTS gatos (
            id_gato TEXT PRIMARY KEY,
            colonia_nombre TEXT NOT NULL,
            nombre TEXT NOT NULL,
            color TEXT NOT NULL,
            sexo TEXT NOT NULL,
            estado TEXT NOT NULL,
            clinica_veterinaria TEXT,
            esterilizado INTEGER NOT NULL,
            fecha_registro TEXT NOT NULL,
            FOREIGN KEY (colonia_nombre) REFERENCES colonias(nombre)
        );
        """)

        # Responsable
        cursor.execute("""
            INSERT INTO responsables
            (identificacion, nombre, telefono, email, tipo, fecha_nacimiento, numero_registro)
            VALUES ('12345678A', 'Test Apellido', '612345678',
                    'test_apellido@email.com', 'PERSONA_FISICA', '1986-10-10', NULL)
        """)

        # Colonia
        cursor.execute("""
            INSERT INTO colonias
            (nombre, responsable_identificacion, estado, ultima_actualizacion)
            VALUES ('Colonia Test', '12345678A', 'SOLICITADA', date('now'))
        """)
        conn.commit()
        conn.close()
        self.repo = RepositorioGatosSQLite(self.BD_TEST, "Colonia Test")

    def tearDown(self):
        self.BD_TEST.unlink(missing_ok=True)

    # -- insertar() ---
    def test_insertar_persiste_el_gato(self):
        self.repo.insertar(Gato("001", "Mimi", "Gris", Sexo.MACHO, EstadoGato.COL, None, False, "01/01/2024"))
        gato = self.repo.obtener("001")
        self.assertEqual(gato.nombre, "Mimi")
        self.assertEqual(gato.color, "Gris")
        self.assertEqual(gato.sexo, Sexo.MACHO)
        self.assertEqual(gato.estado, EstadoGato.COL)
        self.assertEqual(gato.clinica_veterinaria, None)
        self.assertFalse(gato.esterilizado)
        self.assertEqual(gato.fecha_registro, date(2024, 1, 1))

    def test_insertar_persiste_clinica_veterinaria(self):
        self.repo.insertar(Gato("001", "Mimi", "Gris", Sexo.MACHO, EstadoGato.COL, "Clínica Sur", True, "01/01/2024"))
        gato = self.repo.obtener("001")
        self.assertEqual(gato.clinica_veterinaria, "Clínica Sur")
        self.assertTrue(gato.esterilizado)

    def test_insertar_gato_duplicado_lanza_error(self):
        self.repo.insertar(Gato("001", "Mimi", "Gris", Sexo.MACHO, EstadoGato.COL, None, False, "01/01/2024"))
        with self.assertRaises(GatoYaExisteError):
            self.repo.insertar(Gato("001", "Duplicado", "Blanca", Sexo.HEMBRA, EstadoGato.COL, None, False, "01/01/2024"))

    # -- obtener() --
    def test_obtener_gato_no_existe_devuelve_none(self):
        gato = self.repo.obtener("999")
        self.assertIsNone(gato)

    # -- listar() -- 
    def test_listar_devuelve_todos_los_gatos(self):
        self.repo.insertar(Gato("001", "Mimi", "Gris", Sexo.MACHO, EstadoGato.COL, None, False, "01/01/2024"))
        self.repo.insertar(Gato("002", "Kiwinchi", "Blanca", Sexo.HEMBRA, EstadoGato.COL, None, False, "01/01/2024"))
        gatos = self.repo.listar()
        self.assertEqual(len(gatos), 2)

    def test_listar_vacio_devuelve_lista_vacia(self):
        gatos = self.repo.listar()
        self.assertEqual(gatos, [])

    # -- actualizar() --
    def test_actualizar_persiste_los_cambios(self):
        self.repo.insertar(Gato("001", "Mimi", "Gris", Sexo.MACHO, EstadoGato.COL, None, False, "01/01/2024"))
        gato = self.repo.obtener("001")
        gato.estado = EstadoGato.ACOG
        self.repo.actualizar(gato)
        actualizado = self.repo.obtener("001")
        self.assertEqual(actualizado.estado, EstadoGato.ACOG)

    def test_actualizar_gato_inexistente_lanza_excepcion(self):
        with self.assertRaises(GatoNoEncontradoError):
            self.repo.actualizar(Gato("999", "Inexistente", "Gris", Sexo.MACHO, EstadoGato.COL, None, False, "01/01/2024"))

    # -- quitar() --
    def test_quitar_gato_inexistente_lanza_excepcion(self):
        with self.assertRaises(GatoNoEncontradoError):
            self.repo.quitar("999")
    
    def test_quitar_elimina_el_gato(self):
        self.repo.insertar(Gato("001", "Mimi", "Gris", Sexo.MACHO, EstadoGato.COL, None, False, "01/01/2024"))
        self.repo.quitar("001")
        self.assertIsNone(self.repo.obtener("001"))

    # -- mensaje de excepción --
    def test_excepcion_incluye_el_id(self):
        with self.assertRaises(GatoNoEncontradoError) as ctx:
            self.repo.quitar("999")
        self.assertIn("999", str(ctx.exception))       


if __name__ == "__main__":
    unittest.main()

