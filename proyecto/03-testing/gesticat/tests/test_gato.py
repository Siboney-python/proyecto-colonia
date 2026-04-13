"""Tests unitarios para la entidad Gato."""

import unittest
from datetime import date
from gesticat.domain.gato import Gato, Sexo, EstadoGato


class TestGato(unittest.TestCase):

    # -- CASO VÁLIDO --
    
    def test_crear_gato_valido(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    "Clínica Sur", True, "10/01/2024")
        self.assertEqual(gato.id_gato, "001")
        self.assertEqual(gato.nombre, "Miguelito")
        self.assertEqual(gato.color, "Gris")
        self.assertEqual(gato.sexo, Sexo.MACHO)
        self.assertEqual(gato.estado, EstadoGato.COL)
        self.assertEqual(gato.clinica_veterinaria, "Clínica Sur")
        self.assertEqual(gato.esterilizado, True)
        self.assertEqual(gato.fecha_registro.strftime("%d/%m/%Y"), "10/01/2024")


    # -- ID --

    def test_id_invalido_corto_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("01", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")

    def test_id_invalido_letras_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("ABC", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")
            
    def test_id_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("   ", "Luna", "Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")
            
    def test_id_invalido_largo_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("0001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")
            

    # -- NOMBRE Y COLOR --
            
    def test_nombre_vacio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "", "Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")

    def test_nombre_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", " Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")
            
    def test_nombre_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "   ", "Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")

    def test_color_vacio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")        

    def test_color_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", " Gris", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")

    def test_color_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "   ", Sexo.MACHO, EstadoGato.COL,
                None, False, "10/01/2024")
            

    # -- SEXO Y ESTADO --

    def test_sexo_invalido_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            Gato("002", "Luna", "Blanca", "MACHO", EstadoGato.COL,
                None, False, "10/01/2024")

    def test_estado_invalido_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, "COL",
                None, False, "10/01/2024")
            

    # -- CLINICA VETERINARIA Y ESTERILIZACIÓN --

    def test_clinica_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                "   ", False, "10/01/2024")

    def test_clinica_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                " Clínica Sur", False, "10/01/2024")
            
    def test_esterilizado_no_bool_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                None, "si", "10/01/2024")

    def test_esterilizado_sin_clinica_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                None, True, "10/01/2024")

    def test_revertir_esterilizacion_lanza_valueerror(self):
        gato = Gato("001", "Miguelito", "Gris", Sexo.MACHO, EstadoGato.COL,
                    "Clínica Sur", True, "10/01/2024")
        with self.assertRaises(ValueError):
            gato.esterilizado = False


    # -- FECHA DE REGISTRO --

    def test_fecha_futura_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                None, False, "01/01/2099")

    def test_fecha_formato_incorrecto_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                None, False, "2024-01-10")

    def test_fecha_none_usa_fecha_de_hoy(self):
        gato = Gato("003", "Canela", "Naranja", Sexo.HEMBRA, EstadoGato.COL,
                    None, False)
        self.assertEqual(gato.fecha_registro, date.today())

    def test_fecha_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                None, False, "   ")

    def test_fecha_registro_tipo_invalido_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            Gato("002", "Luna", "Blanca", Sexo.HEMBRA, EstadoGato.COL,
                None, False, 20240110)

if __name__ == "__main__":
    unittest.main()