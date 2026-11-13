
import unittest
from src.SistemaArchivos import SistemaArchivos


class TestSistemaArchivos(unittest.TestCase):

    def test_crear_archivo(self):
        sistema = SistemaArchivos(10)

        archivo = sistema.crear_archivo("foto.jpg", 3)

        self.assertEqual(archivo.tamano, 3)
        self.assertEqual(sistema.disco.bloques_disponibles(), 7)

    def test_no_permite_archivos_duplicados(self):
        sistema = SistemaArchivos(10)
        sistema.crear_archivo("foto.jpg", 3)

        with self.assertRaises(ValueError):
            sistema.crear_archivo("foto.jpg", 2)

    def test_eliminar_archivo_libera_espacio(self):
        sistema = SistemaArchivos(10)
        sistema.crear_archivo("foto.jpg", 4)

        sistema.eliminar_archivo("foto.jpg")

        self.assertEqual(sistema.disco.bloques_disponibles(), 10)
        self.assertEqual(len(sistema.listar_archivos()), 0)

    def test_modificar_tamano_de_archivo(self):
        sistema = SistemaArchivos(10)
        sistema.crear_archivo("foto.jpg", 3)

        sistema.modificar_tamano("foto.jpg", 5)

        self.assertEqual(sistema.buscar_archivo("foto.jpg").tamano, 5)
        self.assertEqual(sistema.disco.bloques_disponibles(), 5)

    def test_no_crea_archivo_sin_espacio(self):
        sistema = SistemaArchivos(5)

        with self.assertRaises(ValueError):
            sistema.crear_archivo("grande.txt", 8)

        self.assertEqual(sistema.disco.bloques_disponibles(), 5)

    def test_calcula_metricas(self):
        sistema = SistemaArchivos(10)
        sistema.crear_archivo("foto.jpg", 4)

        metricas = sistema.obtener_metricas()

        self.assertEqual(metricas["ocupados"], 4)
        self.assertEqual(metricas["libres"], 6)
        self.assertEqual(metricas["porcentaje"], 40)

    def test_reutiliza_bloques_liberados(self):
        sistema = SistemaArchivos(8)
        sistema.crear_archivo("primero.txt", 3)
        sistema.crear_archivo("segundo.txt", 2)
        sistema.eliminar_archivo("primero.txt")

        nuevo = sistema.crear_archivo("tercero.txt", 3)

        self.assertEqual(nuevo.bloques, [0, 1, 2])
        self.assertEqual(sistema.disco.bloques_disponibles(), 3)

    def test_registra_extensiones_fragmentadas(self):
        sistema = SistemaArchivos(8)
        sistema.crear_archivo("primero.txt", 2)
        sistema.crear_archivo("segundo.txt", 2)
        sistema.eliminar_archivo("primero.txt")

        archivo = sistema.crear_archivo("tercero.txt", 4)

        self.assertEqual(archivo.extensiones, [(0, 2), (4, 2)])

    def test_no_modifica_archivo_si_falta_espacio(self):
        sistema = SistemaArchivos(5)
        sistema.crear_archivo("foto.jpg", 3)

        with self.assertRaises(ValueError):
            sistema.modificar_tamano("foto.jpg", 8)

        self.assertEqual(sistema.buscar_archivo("foto.jpg").tamano, 3)
        self.assertEqual(sistema.disco.bloques_disponibles(), 2)


if __name__ == "__main__":
    unittest.main()
