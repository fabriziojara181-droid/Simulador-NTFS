import unittest
from src.Disco import Disco


class TestDisco(unittest.TestCase):

    def test_crear_disco_con_capacidad(self):
        disco = Disco(10)

        self.assertEqual(disco.capacidad_total, 10)

    def test_disco_inicia_con_todos_los_bloques_libres(self):
        disco = Disco(5)

        self.assertEqual(disco.bloques_disponibles(), 5)


if __name__ == "__main__":
    unittest.main()