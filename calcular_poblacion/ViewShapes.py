import random

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize, QFileInfo
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QAction, QToolBar, QStatusBar, QTableWidget, QTableWidgetItem, \
    QWidget, QAbstractItemView
from qgis._core import QgsVectorLayerSimpleLabeling, QgsPalLayerSettings, QgsTextFormat, \
    QgsPointXY, QgsGeometry, QgsRandomColorRamp, QgsFillSymbol, QgsExpression, QgsRuleBasedRenderer, QgsRendererCategory
from qgis._gui import QgsRubberBand, QgsMapToolIdentifyFeature, \
    QgsMapToolEmitPoint, QgsVertexMarker
from qgis.core import QgsApplication, QgsVectorLayer, QgsProject
from qgis.gui import QgsMapCanvas, QgsMapToolZoom, QgsMapToolPan
import geopandas as gpd

# initialize the QGIS application
QgsApplication.setPrefixPath(r'C:\OSGeo4W64\apps\qgis', True)
qgs = QgsApplication([], True)
qgs.initQgis()


class ViewSgapesGeneral(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor")
        uic.loadUi('shapefile_viewer.ui', self)
        self.canvas = QgsMapCanvas()
        self.canvas.enableAntiAliasing(True)

        # Agregar el Map canvas a la ventana principal, dentro del marco
        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.canvas)

        # TABLA
        layerTable = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada_Suma.shp'
        layerInfoTable = QFileInfo(layerTable)
        layerProviderTable = "ogr"
        self.layerT = QgsVectorLayer(layerTable, layerInfoTable.fileName(), layerProviderTable)

        self.table_layout = QVBoxLayout(self.frame3)
        self._table_widget = QTableWidget(self)
        self._table_widget.setColumnCount(3)
        self.table_layout.addWidget(self._table_widget)

        self.layout.addLayout(self.table_layout)
        self._table_widget.setRowCount(self.layerT.featureCount())
        self._table_widget.setColumnCount(len(self.layerT.fields()))

        # Agregar los nombres de los campos a la tabla
        headers = [field.name() for field in self.layerT.fields()]
        self._table_widget.setHorizontalHeaderLabels(headers)
        # Ajustar automáticamente el ancho de las columnas
        self._table_widget.setAutoFillBackground(False)
        self.frame2.setStyleSheet("background-color: #f0f0f0;")
        self._table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        features = self.layerT.getFeatures()
        row = 0
        for feature in features:
            attributes = feature.attributes()
            for col, attribute in enumerate(attributes):
                item = QTableWidgetItem(str(attribute))
                self._table_widget.setItem(row, col, item)
            row += 1

        layerPath = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poligonos_de_ejemplo.shp'
        layerInfo = QFileInfo(layerPath)
        layerProvider = "ogr"

        layerPath2 = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada.shp'
        layerInfo2 = QFileInfo(layerPath)
        layerProvider2 = "ogr"

        self.layers = []
        self.layer1 = QgsVectorLayer(layerPath, layerInfo.fileName(), layerProvider)
        self.layer2 = QgsVectorLayer(layerPath2, layerInfo2.fileName(), layerProvider2)

        QgsProject.instance().addMapLayer(self.layer1)
        QgsProject.instance().addMapLayer(self.layerT)

        root = QgsProject.instance().layerTreeRoot()
        self.layer1_node = root.addLayer(self.layer1)
        self.layer2_node = root.addLayer(self.layer2)

        symbol = self.layer2.renderer().symbol().symbolLayer(0)
        fill_color = QColor(255, 255, 255)
        symbol.setFillColor(fill_color)
        # Obtener el color actual del símbolo
        color = symbol.color()

        # Establecer la opacidad del color en 0.5 (50%)
        color.setAlpha(128)  # 128 = 0.5 * 255 (el valor alfa debe ser un entero entre 0 y 255)

        # Establecer el color actualizado en el símbolo
        symbol.setColor(color)
        self.layer2.triggerRepaint()

        self.canvas.setExtent(self.layer1.extent())

        self.canvas.setLayers([self.layer2_node.layer(), self.layer1_node.layer()])
        self.canvas.refresh()

        toolbar = QToolBar("Visor de ShapeFiles")
        toolbar.setIconSize(QSize(42, 42))
        self.addToolBar(toolbar)

        # Crear las herramientas (tools) para el mapa
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False)  # false = Acercar
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True)  # true = Alejar
        self.select_tool = QgsMapToolEmitPoint(self.canvas)
        self.select_tool.canvasPressEvent = self.canvasPressEvent
        self.select_tool.canvasMoveEvent = self.canvasMoveEvent

        button_action = QAction(QIcon("../resources/icon/hand-point-090.png"), "Desplazar Mapa", self)
        button_action.setStatusTip("Desplazar Mapa")
        button_action.setCheckable(True)
        button_action.triggered.connect(self.pan)
        toolbar.addAction(button_action)

        actionZoomIn = QAction(QIcon('../resources/icon/magnifier-zoom-in'), "Zoom In", self.frame)
        actionZoomIn.setStatusTip("Zoom In")
        actionZoomIn.setCheckable(True)
        actionZoomIn.triggered.connect(self.zoomIn)
        toolbar.addAction(actionZoomIn)

        button_action3 = QAction(QIcon('../resources/icon/magnifier-zoom-out.png'), "Zoom Out", self)
        button_action3.setStatusTip("Zoom Out")
        button_action3.triggered.connect(self.zoomOut)
        toolbar.addAction(button_action3)

        actionMapSelection = QAction(QIcon('../resources/icon/information.png'), "Identificar Objetos espaciales", self)
        actionMapSelection.setStatusTip("Objetos Espaciales")
        actionMapSelection.setCheckable(True)
        actionMapSelection.triggered.connect(self.select)
        toolbar.addAction(actionMapSelection)

        actionSaveFile = QAction(QIcon('../resources/icon/report-excel.png'), "Guardar en csv", self)
        actionSaveFile.setStatusTip("Guardar en csv")
        actionSaveFile.setCheckable(True)
        actionSaveFile.triggered.connect(self.saveFile)
        toolbar.addAction(actionSaveFile)

        self.setStatusBar(QStatusBar(self))
        self.show()

    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)

    def zoomFull(self):
        self.canvas.zoomToFullExtent()

    def show_attributes(self):
        self.canvas.setMapTool(self.toolIdentify)

    def saveFile(self):
        gdf = gpd.read_file(r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada.shp')
        df = gdf.drop("geometry", axis=1)

        df.to_csv(r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada.csv', index=False)

    def select(self):
        self.canvas.setMapTool(self.select_tool)

    def canvasPressEvent(self, event):
        point, _ = self.snapper.snapToBackgroundLayers(event.pos())
        self.center = QgsPointXY(point)
        self.marker.setCenter(self.center)
        self.marker.show()

    def canvasMoveEvent(self, event):
        point, _ = self.snapper.snapToBackgroundLayers(event.pos())
        self.radius = self.center.distance(QgsPointXY(point))
        geom = QgsGeometry.fromPointXY(self.center).buffer(self.radius, 10)
        self.canvas.scene().removeItem(self.marker)
        self.marker = QgsVertexMarker(self.canvas)
        self.marker.setCenter(self.center)
        self.marker.setIconSize(2 * self.radius)
        self.marker.setPenWidth(3)
        self.marker.setColor(QColor(255, 0, 0))
        self.marker.setIconType(QgsVertexMarker.ICON_BOX)
        self.canvas.scene().addItem(self.marker)
        self.canvas.scene().addMapLayer(geom.asWktGeometry(), QgsProject.instance())

    def deactivate(self):
        self.canvas.scene().removeItem(self.marker)
        self.center = None
        self.radius = 0

    def get_random_color(self, field):
        random.seed(field)
        return QColor.fromRgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class SectoZoneWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de Shapefiles")
        uic.loadUi('shapefile_viewer.ui', self)
        self.canvas = QgsMapCanvas()
        self.canvas.enableAntiAliasing(True)

        # Agregar el Map canvas a la ventana principal, dentro del marco
        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.canvas)

        layerPath = r'C:\Users\RI\Documents\QGIS\GISSAT\GISSAT\Shapes\Poblacion_Calculada_Zona_Sector_Suma.shp'
        layerInfo = QFileInfo(layerPath)
        layerProvider = "ogr"

        self.layers = []
        layer = QgsVectorLayer(layerPath, layerInfo.fileName(), layerProvider)

        QgsProject.instance().addMapLayer(layer)

        textFormat = QgsTextFormat()
        textFormat.setColor(QColor(253, 45, 0))

        textFormat.setFont(QFont("Arial", 2))
        textFormat.setSize(12)

        label_settings = QgsPalLayerSettings()

        label_settings.fieldName = "Poblacion"
        label_settings.setFormat(textFormat)
        labeling = QgsVectorLayerSimpleLabeling(label_settings)

        layer.setLabeling(labeling)
        layer.setLabelsEnabled(True)

        self.canvas.setExtent(layer.extent())

        self.canvas.setLayers([layer])
        self.canvas.refresh()

        toolbar = QToolBar("Visor de ShapeFiles")
        toolbar.setIconSize(QSize(42, 42))
        self.addToolBar(toolbar)

        # Crear las herramientas (tools) para el mapa
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False)  # false = Acercar
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True)  # true = Alejar
        self.identity = QgsMapToolIdentifyFeature(self.canvas)
        self.identity.setLayer(layer)

        button_action = QAction(QIcon("../resources/icon/hand-point-090.png"), "Desplazar Mapa", self)
        button_action.setStatusTip("Desplazar Mapa")
        button_action.triggered.connect(self.pan)
        toolbar.addAction(button_action)

        actionZoomIn = QAction(QIcon('../resources/icon/magnifier-zoom-in'), "Zoom In", self.frame)
        actionZoomIn.setStatusTip("Zoom In")
        actionZoomIn.triggered.connect(self.zoomIn)
        toolbar.addAction(actionZoomIn)

        actionZoomOut = QAction(QIcon('../resources/icon/magnifier-zoom-out.png'), "Zoom Out", self)
        actionZoomOut.setStatusTip("Zoom Out")
        actionZoomOut.triggered.connect(self.zoomOut)
        toolbar.addAction(actionZoomOut)

        actionMapSelection = QAction(QIcon('../resources/icon/information.png'), "Identificar Objetos espaciales", self)
        actionMapSelection.setStatusTip("Objetos Espaciales")
        actionMapSelection.triggered.connect(self.showAttributes)
        toolbar.addAction(actionMapSelection)

        actionSaveFile = QAction(QIcon('../resources/icon/report-excel.png'), "Guardar en csv", self)
        actionSaveFile.setStatusTip("Guardar en csv")
        actionSaveFile.triggered.connect(self.saveFile)
        toolbar.addAction(actionSaveFile)

        self.setStatusBar(QStatusBar(self))
        self.show()

    def zoomIn(self, s):
        print("click", s)
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self, s):
        print("click", s)
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self, s):
        print("click", s)
        self.canvas.setMapTool(self.toolPan)

    def zoomFull(self):
        self.canvas.zoomToFullExtent()

    def showAttributes(self, feature):
        self.canvas.scene().removeItem(self.band)
        self.band = QgsRubberBand(self.canvas, True)
        self.setToGeometry(feature.geometry(), None)
        self.band.show()
        self.label.setText("ID: {} Poblacion: {}".format(feature.id, feature['Poblacion']))
        print("click")

    def saveFile(self):
        print("click")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_window = ViewSgapesGeneral()
    main_window.show()
    app.exec_()
