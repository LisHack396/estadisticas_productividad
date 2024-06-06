import unittest

class GraficarTest(unittest.TestCase):
    def setUp(self):
        print("Preparando el contexto")
        self.data = {"labels": ["A", "B", "C"], "values": [34, 56, 12]}
    
    def test(self):
        print("Ejecutando pruebas de evaluacion de datos para graficar")
        self.assertTrue(all(isinstance(label, (str)) for label in self.data['labels']))
        self.assertTrue(all(isinstance(value, (int, float)) for value in self.data['values']))
    
    def tearDown(self):
        print("Deconstruyendo el contexto")
        del self.data