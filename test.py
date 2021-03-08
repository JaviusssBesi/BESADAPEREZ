import unittest
import clients, conexion, var
from PyQt5 import QtSql

class MyTestCase(unittest.TestCase):

    def test_codigo(self):
        codigo = 2
        val = False
        msg = 'Código incorrecto'

        if codigo > 0:
            val = True

        self.assertTrue(val, msg)

if __name__ == '__main__':
    unittest.main()
