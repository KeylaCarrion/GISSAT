from PyQt5.QtCore import pyqtSignal


class controllerTanques:
    datos = pyqtSignal()

    def __init__(self, modelo):
        super().__init__()
        self.modelo = modelo

    def insertTanques_excel(self, file_path):
        self.modelo.insertTanque_excel(file_path)


    def obtenerTanques(self):
        return self.modelo.obtenerTanques()

    def cerrar_conexion(self):
        self.modelo.cerrar_conexion()
