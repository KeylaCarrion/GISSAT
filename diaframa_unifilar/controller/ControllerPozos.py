from PyQt5.QtCore import pyqtSignal


class controllerPozos:
    datos = pyqtSignal()

    def __init__(self, modelo):
        super().__init__()
        self.modelo = modelo

    def insertPozos_excel(self, file_path):
        self.modelo.insertPozos_excel(file_path)


    def obtnerPozos(self):
        return self.modelo.obtenerPozos()

    def cerrar_conexion(self):
        self.modelo.cerrar_conexion()
