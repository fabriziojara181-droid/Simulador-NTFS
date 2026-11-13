import unittest
from src.Disco import Disco


class TestDisco(unittest.TestCase):

    def test_crear_disco_con_capacidad(self):
        disco = Disco(10)

        self.assertEqual(disco.capacidad_total, 10)

    def test_disco_inicia_con_todos_los_bloques_libres(self):
        disco = Disco(5)

        self.assertEqual(disco.bloques_disponibles(), 5)


    def test_reservar_bloques_reduce_espacio_disponible(self):
        disco = Disco(8)

        disco.reservar_bloques(3)

        self.assertEqual(disco.bloques_disponibles(), 5)


    def test_no_permite_reservar_mas_bloques_de_los_disponibles(self):
        disco = Disco(5)

        with self.assertRaises(ValueError):
            disco.reservar_bloques(8)

        self.assertEqual(disco.bloques_disponibles(), 5)


    def test_reservar_bloques_devuelve_las_posiciones_asignadas(self):
        disco = Disco(6)

        bloques = disco.reservar_bloques(3)

        self.assertEqual(bloques, [0, 1, 2])
        self.assertEqual(disco.bloques_disponibles(), 3)


    def test_no_reserva_bloques_que_ya_estan_ocupados(self):
        disco = Disco(6)

        primera_reserva = disco.reservar_bloques(2)
        segunda_reserva = disco.reservar_bloques(2)

        self.assertEqual(primera_reserva, [0, 1])
        self.assertEqual(segunda_reserva, [2, 3])
        self.assertEqual(disco.bloques_disponibles(), 2)

if __name__ == "__main__":
    unittest.main()