"""Tests unitarios para la entidad Responsable."""

import unittest
from datetime import date
from gesticat.domain.responsable import PersonaFisica, Protectora

class TestResponsable(unittest.TestCase):

    # -- CASOS VÁLIDOS --

    def test_crear_personafisica_valido(self):
        persona_ok = PersonaFisica("Ana García", "612345678", "ana@email.com",
                            "12345678A", "15/06/1985")
        self.assertEqual(persona_ok.nombre, "Ana García")
        self.assertEqual(persona_ok.telefono, "612345678")
        self.assertEqual(persona_ok.email, "ana@email.com")
        self.assertEqual(persona_ok.identificacion, "12345678A")
        self.assertEqual(persona_ok.fecha_nacimiento.strftime("%d/%m/%Y"), "15/06/1985")

    def test_crear_protectora_valido(self):
        protectora_ok = Protectora("Asociación Felina", "912345678", "info@asociacion.com",
                            "A12345678", "REG-001")
        self.assertEqual(protectora_ok.nombre, "Asociación Felina")
        self.assertEqual(protectora_ok.telefono, "912345678")
        self.assertEqual(protectora_ok.email, "info@asociacion.com")
        self.assertEqual(protectora_ok.identificacion, "A12345678")
        self.assertEqual(protectora_ok.numero_registro, "REG-001")


    # -- NOMBRE --

    def test_nombre_vacio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("", "612345678", "ana@email.com", "12345678A", "15/06/1985")

    def test_nombre_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("   ", "612345678", "ana@email.com", "12345678A", "15/06/1985")

    def test_nombre_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica(" Ana García", "612345678", "ana@email.com", "12345678A", "15/06/1985")


    # -- TELÉFONO --

    def test_telefono_corto_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "12345", "ana@email.com", "12345678A", "15/06/1985")

    def test_telefono_letras_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "ABCDEFGHI", "ana@email.com", "12345678A", "15/06/1985")

    def test_telefono_largo_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "6123456789", "ana@email.com", "12345678A", "15/06/1985")

    def test_telefono_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", " 612345678", "ana@email.com", "12345678A", "15/06/1985")


    # -- EMAIL --

    def test_email_sin_arroba_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", "correo_sin_arroba", "12345678A", "15/06/1985")

    def test_email_sin_dominio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", "correo@", "12345678A", "15/06/1985")

    def test_email_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", " ana@email.com", "12345678A", "15/06/1985")


    # -- IDENTIFICACIÓN --

    def test_identificacion_vacia_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", "ana@email.com", "", "15/06/1985")

    def test_identificacion_normaliza_a_mayusculas(self):
        persona = PersonaFisica("Ana García", "612345678", "ana@email.com",
                                "12345678a", "15/06/1985")
        self.assertEqual(persona.identificacion, "12345678A")

    def test_identificacion_protectora_normaliza_a_mayusculas(self):
        protectora = Protectora("Asociación Felina", "912345678", "info@asociacion.com",
                            "a12345678", "REG-001")
        self.assertEqual(protectora.identificacion, "A12345678")

    def test_identificacion_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", "ana@email.com", " 12345678A", "15/06/1985")


    # -- FECHA DE NACIMIENTO --

    def test_fecha_nacimiento_futura_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", "ana@email.com", "12345678A", "01/01/2099")

    def test_fecha_nacimiento_menor_de_edad_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", "ana@email.com", "12345678A", "01/01/2015")

    def test_fecha_nacimiento_formato_incorrecto_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            PersonaFisica("Ana García", "612345678", "ana@email.com", "12345678A", "1985-06-15")


    # -- NUMERO REGISTRO --

    def test_numero_registro_vacio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Protectora("Asociación Felina", "912345678", "info@asociacion.com",
                       "A12345678", "")

    def test_numero_registro_normaliza_a_mayusculas(self):
        protectora = Protectora("Asociación Felina", "912345678", "info@asociacion.com",
                                "A12345678", "reg-001")
        self.assertEqual(protectora.numero_registro, "REG-001")

    def test_numero_registro_espacios_laterales_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Protectora("Asociación Felina", "912345678", "info@asociacion.com",
                    "A12345678", "   ")


    # -- __str__ --

    def test_str_personafisica(self):
        persona = PersonaFisica("Ana García", "612345678", "ana@email.com",
                                "12345678A", "15/06/1985")
        self.assertEqual(str(persona), "Ana García - DNI: 12345678A")

    def test_str_protectora(self):
        protectora = Protectora("Asociación Felina", "912345678", "info@asociacion.com",
                                "A12345678", "REG-001")
        self.assertEqual(str(protectora), "Asociación Felina - CIF: A12345678 - Reg: REG-001")


if __name__ == "__main__":
    unittest.main()