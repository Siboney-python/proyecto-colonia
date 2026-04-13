"""Tests unitarios para la entidad Colonia."""

import unittest
from datetime import date

from gesticat.domain.colonia import Colonia, EstadoColonia
from gesticat.domain.gato import Gato, Sexo, EstadoGato
from gesticat.domain.responsable import PersonaFisica
from gesticat.infrastructure.repositorio_gatos_memoria import RepositorioGatosMemoria


class TestColonia(unittest.TestCase):

    def setUp(self):
        self.responsable = PersonaFisica("Ana García", "612345678", "ana@email.com",
                                         "12345678A", "15/06/1985")
        self.repo = RepositorioGatosMemoria()
        self.colonia = Colonia("Colonia Sur", self.responsable, self.repo)


    # -- PROPIEDADES DE LA COLONIA--

    def test_crear_colonia_valida(self):
        self.assertEqual(self.colonia.nombre, "Colonia Sur")
        self.assertEqual(self.colonia.responsable, self.responsable)
        self.assertEqual(self.colonia.estado, EstadoColonia.SOLICITADA)

    def test_nombre_vacio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Colonia("", self.responsable, self.repo)

    def test_nombre_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Colonia("   ", self.responsable, self.repo)

    def test_nombre_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Colonia(" Colonia Sur", self.responsable, self.repo)

    def test_responsable_invalido_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            Colonia("Colonia Sur", "no es un responsable", self.repo)

    def test_estado_inicial_es_solicitada(self):
        self.assertEqual(self.colonia.estado, EstadoColonia.SOLICITADA)


    # -- GESTIÓN DE GATOS --

    def test_agregar_gato(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    None, False, "10/01/2024")
        self.colonia.agregar_gato(gato)
        encontrado = self.colonia.buscar_por_id("001")
        self.assertEqual(encontrado.id_gato, "001")
        self.assertEqual(encontrado.nombre, "Miguelito")
        self.assertEqual(encontrado.color, "Gris")
        self.assertEqual(encontrado.sexo, Sexo.MACHO)
        self.assertEqual(encontrado.estado, EstadoGato.COL)
        self.assertEqual(encontrado.esterilizado, False)

    def test_agregar_gato_duplicado_lanza_valueerror(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    None, False, "10/01/2024")
        self.colonia.agregar_gato(gato)
        with self.assertRaises(ValueError):
            self.colonia.agregar_gato(gato)

    def test_agregar_objeto_no_gato_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            self.colonia.agregar_gato("no es un gato")

    def test_actualizar_gato(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    None, False, "10/01/2024")
        self.colonia.agregar_gato(gato)
        gato.estado = EstadoGato.ACOG
        self.colonia.actualizar_gato(gato)
        self.assertEqual(self.colonia.buscar_por_id("001").estado, EstadoGato.ACOG)

    def test_quitar_gato(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    None, False, "10/01/2024")
        self.colonia.agregar_gato(gato)
        self.colonia.quitar_gato("001")
        self.assertIsNone(self.colonia.buscar_por_id("001"))

    def test_buscar_por_id_inexistente_devuelve_none(self):
        self.assertIsNone(self.colonia.buscar_por_id("999"))

    def test_buscar_por_nombre(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    None, False, "10/01/2024")
        self.colonia.agregar_gato(gato)
        resultados = self.colonia.buscar_por_nombre("Miguelito")
        self.assertEqual(len(resultados), 1)

    def test_buscar_por_nombre_inexistente_devuelve_lista_vacia(self):
        resultados = self.colonia.buscar_por_nombre("Fantasma")
        self.assertEqual(resultados, [])


    # -- ESTADO ADMINISTRATIVO --

    def test_tramitar_anexo_cambia_estado_valido(self):
        self.colonia.tramitar_anexo(EstadoColonia.ACTIVA)
        self.assertEqual(self.colonia.estado, EstadoColonia.ACTIVA)

    def test_tramitar_anexo_a_solicitada_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            self.colonia.tramitar_anexo(EstadoColonia.SOLICITADA)

    def test_tramitar_anexo_tipo_invalido_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            self.colonia.tramitar_anexo("ACTIVA")

    def test_necesita_actualizacion_recien_creada(self):
        self.assertFalse(self.colonia.necesita_actualizacion())

    def test_ultima_actualizacion_es_fecha_de_hoy(self):
        self.assertEqual(self.colonia.ultima_actualizacion, date.today())


    # -- REPORTES --

    def test_reporte_censo_colonia_vacia(self):
        reporte = self.colonia.reporte_censo()
        self.assertEqual(reporte["total"], 0)
        self.assertEqual(reporte["machos"], 0)
        self.assertEqual(reporte["hembras"], 0)
        self.assertEqual(reporte["esterilizados"], 0)
        self.assertEqual(reporte["no_esterilizados"], 0)

    def test_reporte_censo_con_gatos(self):
        self.colonia.agregar_gato(Gato("001", "Miguelito", "Gris", Sexo.MACHO,
                                    EstadoGato.COL, "Clínica Sur", True, "10/01/2024"))
        self.colonia.agregar_gato(Gato("002", "Luna", "Blanca", Sexo.HEMBRA,
                                    EstadoGato.COL, None, False, "10/01/2024"))
        self.colonia.agregar_gato(Gato("003", "Sombra", "Negro", Sexo.DESCONOCIDO,
                                    EstadoGato.FALL, None, False, "10/01/2024"))
        reporte = self.colonia.reporte_censo()
        self.assertEqual(reporte["total"], 2)
        self.assertEqual(reporte["machos"], 1)
        self.assertEqual(reporte["hembras"], 1)
        self.assertEqual(reporte["esterilizados"], 1)
        self.assertEqual(reporte["no_esterilizados"], 1)

    def test_reporte_colonia(self):
        reporte = self.colonia.reporte_colonia()
        self.assertEqual(reporte["nombre"], "Colonia Sur")
        self.assertEqual(reporte["estado"], EstadoColonia.SOLICITADA.value)
        self.assertFalse(reporte["necesita_actualizacion"])
        self.assertEqual(reporte["total_gatos"], 0)


    # -- LISTAR SIN ESTERILIZAR --

    def test_listar_sin_esterilizar(self):
        self.colonia.agregar_gato(Gato("001", "Miguelito", "Gris", Sexo.MACHO,
                                    EstadoGato.COL, "Clínica Sur", True, "10/01/2024"))
        self.colonia.agregar_gato(Gato("002", "Luna", "Blanca", Sexo.HEMBRA,
                                    EstadoGato.COL, None, False, "10/01/2024"))
        sin_esterilizar = self.colonia.listar_sin_esterilizar()
        self.assertEqual(len(sin_esterilizar), 1)
        self.assertEqual(sin_esterilizar[0].id_gato, "002")

    def test_listar_sin_esterilizar_excluye_inactivos(self):
        self.colonia.agregar_gato(Gato("001", "Miguelito", "Gris", Sexo.MACHO,
                                    EstadoGato.FALL, None, False, "10/01/2024"))
        sin_esterilizar = self.colonia.listar_sin_esterilizar()
        self.assertEqual(len(sin_esterilizar), 0)


    # -- REPOSITORIO EN MEMORIA --

    def test_repositorio_insertar_duplicado_lanza_valueerror(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    None, False, "10/01/2024")
        self.repo.insertar(gato)
        with self.assertRaises(ValueError):
            self.repo.insertar(gato)

    def test_repositorio_actualizar_inexistente_lanza_valueerror(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    None, False, "10/01/2024")
        with self.assertRaises(ValueError):
            self.repo.actualizar(gato)

    def test_repositorio_quitar_inexistente_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            self.repo.quitar("999")

if __name__ == "__main__":
    unittest.main()