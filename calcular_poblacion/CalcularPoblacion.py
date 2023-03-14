import subprocess
import sys
import pickle
from osgeo import ogr
import geopandas as gpd

from PyQt5 import QtWidgets, uic
from qgis._core import QgsProcessingFeedback, QgsProcessing, QgsVectorLayer, QgsProject, QgsApplication, QgsExpression
from calcular_poblacion.ViewShapes import ViewSgapesGeneral, SectoZoneWindow

QgsApplication.setPrefixPath(r'C:\OSGeo4W64\apps\qgis-ltr', True)
qgs = QgsApplication([], True)
qgs.initQgis()
sys.path.append(r'C:\OSGeo4W64\apps\qgis-ltr\python\plugins')


class CalculaPoblacion(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('calcular_poblacion.ui', self)
        self.show()
        # Nombres a los Radio Button
        self.rbPI.setText(" Población Actual (INEGI)")
        self.rbPA.setText(" Población de Proyecto")
        self.rbZona.setText(" Zonas de influencia Actual")
        self.rbSector.setText(" Sectores de Proyecto")
        self.rbAll.setText(" Todas las Zonas o sectores")
        self.rbPZona.setText(" Elegir Zona/Sector")

        # Conectar botones a las funciones
        self.rbPZona.toggled.connect(self.fillSectorZone)
        self.btnCalculate.clicked.connect(self.calculate)

        # Condiciones

    def calculate(self):
        if self.rbPI.isChecked() and self.rbZona.isChecked() and self.rbAll.isChecked():
            resultado_layer = subprocess.call(["python", "algorithm_population.py"])
            if resultado_layer == 0:
                self.view_canvas = ViewSgapesGeneral()
                self.view_canvas.show()
            else:
                print("error---------")
        if self.rbPI.isChecked and self.rbZona.isChecked() and self.rbPZona.isChecked():
            input_data = self.porZonas()

            print("P", input_data)
            resultado_zona_Sector = subprocess.call(["python", "algorithm_population_Zone_Sector.py", input_data])

            if resultado_zona_Sector == 0:
                self.view_sector_canvas = SectoZoneWindow()
                self.view_sector_canvas.show()
            else:
                s = self.porZonas()
                print(s)
                print("Capa ya creada")

    def porZonas(self):
        seleccion = self.cbZonas.currentText()
        print("El elemento seleccionado es:", seleccion)

        return seleccion

    def fillSectorZone(self):
        if self.rbPZona.isChecked():
            zonas_Sectores = gpd.read_file(r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poligonos_de_ejemplo.shp')
            valores = zonas_Sectores['nombre'].unique()

            self.cbZonas.addItems(valores)
        else:
            self.cbZonas.setEnabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_window = CalculaPoblacion()
    main_window.show()
    app.exec_()
